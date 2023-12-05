# tool_news_duration_user.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams
import japanize_matplotlib

data = pd.read_csv('./csv/APP_add_days.csv', dtype={'user': str})

# matplotlibのフォントを設定（日本語対応）
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']

# 不要な空白や非表示文字を削除する関数
def clean_app_name(app_name):
    app_name = app_name.strip()  # トリミング
    app_name = ''.join(char for char in app_name if char.isprintable())  # 非表示文字を削除
    return app_name

# 利用時間が0のユーザーも含めるため、全ユーザーのリストを作成
unique_users = data['user'].unique()

# カテゴリごとにデータをフィルタリングしてグラフ化する関数
def plot_category_usage_for_each_user(category_name):
    # 特定のカテゴリのデータをフィルタリング
    category_data = data[data['app_category'] == category_name]

    # userとapp_nameごとにdurationの合計を計算
    category_duration = category_data.groupby(['user', 'app_name'])['duration'].sum().reset_index()

    # 全ユーザーをループし、個別のグラフを作成
    for user in unique_users:
        user_data = category_duration[category_duration['user'] == user].copy()
        
        # ユーザーが使用したアプリがない場合、データフレームに追加
        if user not in user_data['user'].values:
            no_usage = pd.DataFrame({'user': [user], 'app_name': ['No Usage'], 'duration': [0]})
            user_data = pd.concat([user_data, no_usage], ignore_index=True)
        
        # アプリ名の文字数を適切な長さに制限
        user_data['app_name'] = user_data['app_name'].apply(lambda x: x if len(x) <= 12 else x[:12] + '...')

        # データをdurationで降順にソート
        user_data.sort_values('duration', ascending=False, inplace=True)

        # グラフをプロット
        plt.figure(figsize=(10, 6))
        bar_plot = sns.barplot(x='app_name', y='duration', data=user_data)

        # X軸のラベルを270度回転
        plt.xticks(rotation=270)

        plt.title(f'{user} - 「{category_name}」カテゴリのアプリ利用時間合計')
        plt.xlabel('アプリ名')
        plt.ylabel('合計利用時間（秒）')
        plt.tight_layout()  # レイアウトの調整
        plt.savefig(f'./img/tool_news/user/{user}_{category_name}_usage.png', dpi=300)
        plt.close()

# 'ツール類'カテゴリのグラフを生成
plot_category_usage_for_each_user('ツール類')

# 'ニュース'カテゴリのグラフを生成
plot_category_usage_for_each_user('ニュース')