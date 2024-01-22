import pandas as pd
import os

app_to_soft_hard = {
    'ツール類': 'soft', 'ライフ': 'soft', '写真・ビデオ': 'soft', 'その他／不明': 'soft',
    'ヘルスケア／フィットネス': 'soft', 'ショッピング': 'soft', 'ファイナンス': 'hard',
    'メディカル': 'hard', '旅行＆地域': 'soft', 'スポーツ': 'soft', 'ニュース': 'hard',
    'エンタテイメント': 'soft', 'ゲーム': 'soft', 'フード＆ドリンク': 'soft',
    '地図＆ナビ': 'soft', '仕事効率化': 'hard', 'ソーシャルネットワーキング': 'soft',
    'ミュージック': 'soft', '天気': 'soft', 'ビジネス': 'hard', 'ブック・コミック・辞書': 'soft',
    'システム': 'hard', '教育': 'hard'
}
tv_to_soft_hard = {
    'スポーツ': 'soft', '情報/ワイドショー': 'hard', 'ドキュメンタリー': 'hard', 'ニュース/報道': 'hard',
    'ドラマ': 'soft', 'バラエティー': 'soft', '音楽': 'soft', 'アニメ/特撮': 'soft',
    '趣味/教育': 'soft', '演劇/公演': 'soft', '福祉': 'hard', '映画': 'soft'
}

df_app = pd.read_csv('../../data/csv/add_days/APP_add_days.csv', dtype={'user': str})
df_tv = pd.read_csv('../../data/csv/add_days/TV_add_days.csv', dtype={'user': str})
print(df_app)
print(df_tv)

df_app['category'] = df_app['app_category'].map(app_to_soft_hard)
df_tv['category'] = df_tv['tv_category'].map(tv_to_soft_hard)
print(df_app['category'].value_counts(dropna=False))
print(df_tv['category'].value_counts(dropna=False))

df_app = df_app[['user', 'date', 'duration','category', 'days']]
df_tv = df_tv[['user', 'date', 'duration', 'category', 'days']]

output_dir = '../../data/csv/soft_and_hard/'
os.makedirs(output_dir, exist_ok=True)
df_app.to_csv(f'{output_dir}APP.csv', index=False)
df_tv.to_csv(f'{output_dir}TV.csv', index=False)