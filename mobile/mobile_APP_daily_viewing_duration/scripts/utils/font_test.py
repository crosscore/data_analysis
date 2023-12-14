import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


# インストールされているフォントのリストを取得
fonts = fm.findSystemFonts(fontpaths=None, fontext='ttf')
# フォントのリストを表示
for font in fonts:
    print(font)