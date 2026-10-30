/*
  Smart Rajakaluve sensor node (ESP32 DevKit)
  Reads: JSN-SR04T ultrasonic (water level), turbidity, TDS, pH, DS18B20 temperature, battery
  Sends: JSON over Wi-Fi (HTTP POST) to the backend /api/readings, then deep-sleeps.
         For field use, replace sendWiFi() with a LoRa packet to a gateway that forwards the same JSON.

  Libraries (Arduino Library Manager): OneWire, DallasTemperature, ArduinoJson (v7)
  Board: "ESP32 Dev Module"

  Wiring (3.3 V logic! sensor outputs up to 5 V need a 10k/20k divider -> ADC pin):
    JSN-SR04T  TRIG -> GPIO25, ECHO -> GPIO26 (through divider), VCC 5 V
    Turbidity  AO   -> GPIO34 (through divider)
    pH board   PO   -> GPIO35 (through divider)
    TDS probe  AO   -> GPIO32 (board output is 0-2.3 V, no divider)
    DS18B20    DATA -> GPIO4 with 4.7k pull-up to 3.3 V
    Battery    18650 + -> 100k/100k divider -> GPIO33
*/
#include <WiFi.h>
#include <HTTPClient.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <ArduinoJson.h>

// ---------- Config: edit per node ----------
const char* WIFI_SSID = "your-wifi";
const char* WIFI_PASS = "your-password";
const char* API_URL   = "http://192.168.1.20:8000/api/readings";
const char* API_KEY   = "change-me";
const char* HW_ID     = "NODE-A";          // must match server/config.json hardware_map
const uint32_t SLEEP_SECONDS = 120;        // demo: 10; field: 120-300

// Calibration (do this with known samples before the demo)
const float DIVIDER_RATIO = 1.5f;          // 10k/20k divider: Vsensor = Vadc * 1.5
const float PH_NEUTRAL_V  = 2.50f;         // sensor volts in pH 7 buffer
const float PH_SLOPE      = -5.70f;        // pH per volt, from pH 4 and pH 7 buffers
const float TURB_CLEAR_V  = 4.20f;         // volts in clear water (for clamping)

// ---------- Pins ----------
#define PIN_TRIG 25
#define PIN_ECHO 26
#define PIN_TURB 34
#define PIN_PH   35
#define PIN_TDS  32
#define PIN_TEMP 4
#define PIN_BATT 33

OneWire oneWire(PIN_TEMP);
DallasTemperature tempSensor(&oneWire);
RTC_DATA_ATTR uint32_t bootCount = 0;

// median of N analog samples (rejects spikes from electrical noise)
float readVolts(int pin, int n = 15) {
  int v[25];
  n = min(n, 25);
  for (int i = 0; i < n; i++) { v[i] = analogReadMilliVolts(pin); delay(8); }
  for (int i = 1; i < n; i++) { int k = v[i], j = i - 1; while (j >= 0 && v[j] > k) { v[j + 1] = v[j]; j--; } v[j + 1] = k; }
  return v[n / 2] / 1000.0f;
}

// ultrasonic distance in cm, median of 7 pings; -1 if no echo
float readDistanceCm() {
  float d[7]; int ok = 0;
  for (int i = 0; i < 7; i++) {
    digitalWrite(PIN_TRIG, LOW); delayMicroseconds(4);
    digitalWrite(PIN_TRIG, HIGH); delayMicroseconds(20);
    digitalWrite(PIN_TRIG, LOW);
    unsigned long us = pulseIn(PIN_ECHO, HIGH, 30000UL);
    if (us > 0) d[ok++] = us * 0.0343f / 2.0f;
    delay(60);
  }
  if (!ok) return -1;
  for (int i = 1; i < ok; i++) { float k = d[i]; int j = i - 1; while (j >= 0 && d[j] > k) { d[j + 1] = d[j]; j--; } d[j + 1] = k; }
  return d[ok / 2];
}

float readTempC() {
  tempSensor.requestTemperatures();
  float t = tempSensor.getTempCByIndex(0);
  return (t < -50 || t > 80) ? 25.0f : t;   // fallback keeps TDS compensation sane
}

// Common analog turbidity module (e.g. DFRobot SEN0189) curve, valid ~2.5-4.2 V
float voltsToNTU(float v) {
  v = constrain(v, 2.5f, TURB_CLEAR_V);
  float ntu = -1120.4f * v * v + 5742.3f * v - 4352.9f;
  return constrain(ntu, 0.0f, 3000.0f);
}

// Gravity TDS meter formula with temperature compensation
float voltsToTDS(float v, float tempC) {
  float comp = 1.0f + 0.02f * (tempC - 25.0f);
  float cv = v / comp;
  float tds = (133.42f * cv * cv * cv - 255.86f * cv * cv + 857.39f * cv) * 0.5f;
  return max(0.0f, tds);
}

float voltsToPH(float v) { return constrain(7.0f + (v - PH_NEUTRAL_V) * PH_SLOPE, 0.0f, 14.0f); }

float batteryPercent() {
  float v = readVolts(PIN_BATT, 9) * 2.0f;               // 100k/100k divider
  return constrain((v - 3.3f) / (4.2f - 3.3f) * 100.0f, 0.0f, 100.0f);
}

bool sendWiFi(const String& body) {
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  for (int i = 0; i < 40 && WiFi.status() != WL_CONNECTED; i++) delay(250);
  if (WiFi.status() != WL_CONNECTED) return false;
  HTTPClient http;
  http.begin(API_URL);
  http.addHeader("Content-Type", "application/json");
  http.addHeader("X-API-Key", API_KEY);
  int code = http.POST(body);
  Serial.printf("POST %d %s\n", code, http.getString().c_str());
  http.end();
  return code == 200;
}

void setup() {
  Serial.begin(115200);
  bootCount++;
  pinMode(PIN_TRIG, OUTPUT);
  pinMode(PIN_ECHO, INPUT);
  analogReadResolution(12);
  analogSetAttenuation(ADC_11db);   // 0-3.3 V range
  tempSensor.begin();

  float tempC = readTempC();
  float dist  = readDistanceCm();
  float turbV = readVolts(PIN_TURB) * DIVIDER_RATIO;
  float phV   = readVolts(PIN_PH) * DIVIDER_RATIO;
  float tdsV  = readVolts(PIN_TDS);

  JsonDocument doc;
  doc["hw_id"] = HW_ID;
  if (dist > 0) doc["distance_cm"] = dist;          // server converts to level using mount height
  doc["turbidity_ntu"] = voltsToNTU(turbV);
  doc["tds_ppm"] = voltsToTDS(tdsV, tempC);
  doc["ph"] = voltsToPH(phV);
  doc["temp_c"] = tempC;
  doc["battery"] = batteryPercent();
  String body; serializeJson(doc, body);
  Serial.println(body);

  bool ok = sendWiFi(body);
  WiFi.disconnect(true);
  WiFi.mode(WIFI_OFF);

  // retry sooner after a failed send
  uint64_t sleepUs = (ok ? SLEEP_SECONDS : 30) * 1000000ULL;
  esp_sleep_enable_timer_wakeup(sleepUs);
  esp_deep_sleep_start();
}

void loop() {}
