# iQuant3D-terminal

## インストール
zipファイルをダウンロードし、以下のコマンドを実行してください。
```
python setup.py install
```
解析ファイルを作成し、iQuant3D-terminalをインポートしてください。
```
from iquant3d_terminal import *
iq3t = iq3t('data','206Pb',20) #data folder, time_standard_element, washout_time
iq3t.run()
```
