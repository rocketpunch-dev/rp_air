# -*- mode: python -*-
#filename = rp_air_main.spec
import sys
# myLibPath = 'D:\\PyCharmProjects\\rp_air'  # Windows
# sys.path.append(myLibPath)
a = Analysis(['Input Main Python FullPath'],
             pathex=['Input Project Path'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
a.datas += [('ui/icon/icon_512.png', 'Input Icon FullPath(png)', 'DATA')]
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='RP_AIR_V1_32bit.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False , icon='Input Icon FullPath(ico)')