import pathlib
L='/home/claude/libs/node_modules/'
src=pathlib.Path('web/index.html').read_text()
def r(p): return pathlib.Path(L+p).read_text().replace('</script','<\\/script')
src=src.replace('/*__LEAFLET_CSS__*/',pathlib.Path(L+'leaflet/dist/leaflet.css').read_text())
src=src.replace('/*__LEAFLET_JS__*/',r('leaflet/dist/leaflet.js'))
src=src.replace('/*__THREE_JS__*/',r('three/build/three.min.js'))
src=src.replace('/*__ORBIT_JS__*/',r('three/examples/js/controls/OrbitControls.js'))
pathlib.Path('dist/index.html').write_text(src)
print(len(src)//1024,'KB')
