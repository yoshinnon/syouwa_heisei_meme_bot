import datetime
import yaml
import random
import os
import tweepy

# GitHub Secretsから認証情報を取得
X_API_KEY = os.getenv("X_API_KEY")
X_API_SECRET = os.getenv("X_API_SECRET")
X_ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
X_ACCESS_SECRET = os.getenv("X_ACCESS_SECRET")

# 1. API v2 クライアントの作成 (Freeプランはこっちが必須)
client = tweepy.Client(
    consumer_key=X_API_KEY,
    consumer_secret=X_API_SECRET,
    access_token=X_ACCESS_TOKEN,
    access_token_secret=X_ACCESS_SECRET
)

def get_current_group_key():
    # 日本時間を取得 (UTC+9)
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    now_jst = now_utc + datetime.timedelta(hours=9)
    
    # 【重要】累計時間を計算して20時間周期（5グループ×4時間）で回す
    # 2024/01/01等、固定の基準点からの経過時間を使うとより正確に毎日ズレます
    # 単純な hour // 4 だと毎日同じ時間にリセットされる可能性があるため
    total_hours = int(now_jst.timestamp() // 3600)
    group_index = (total_hours // 4) % 5 + 1
    
    return f"group{group_index}"

def post_meme():
    try:
        # 2. ファイルパスの解決 (bot.pyの場所を基準にyamlを探す)
        base_dir = os.path.dirname(__file__)
        yaml_path = os.path.join(base_dir, "..", "yaml", "memes.yml")
        
        with open(yaml_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        
        group_key = get_current_group_key()
        meme_list = data["groups"][group_key]["items"]
        content = random.choice(meme_list)
        
        # 3. 投稿処理 (API v2形式)
        client.create_tweet(text=content)
        
        print(f"Time(JST): {datetime.datetime.now() + datetime.timedelta(hours=9)}")
        print(f"Group: {group_key}, Post: {content}")

    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    post_meme()