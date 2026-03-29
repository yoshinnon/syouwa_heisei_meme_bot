# 昭和・平成ミームBot (Syouwa Heisei Meme Bot)

昭和から平成にかけて流行した懐かしいミームやフレーズを、X (旧Twitter) へ自動的にポストするPythonボットです。
GitHub Actionsを利用しており、完全にサーバーレスで運用可能な設計になっています。

## ⚠️ 現在の稼働状況について
現在、X APIの仕様変更（有料化・従量課金制への移行）に伴い、API残高をチャージしていないため、**本リポジトリの自動ポスト機能は一時停止しています。**

技術的な実装（PythonスクリプトおよびGitHub Actionsの設定）は完了しており、X Developer Consoleでの課金設定およびAPIキーの更新を行うことで、即座に再開可能な状態です。

## 概要
このプロジェクトは、エンジニアリングの学習と遊び心を兼ねて構築されました。ミームのデータはYAMLファイルで世代・ジャンルごとに構造化されており、プログラム本体を修正することなく投稿内容を柔軟に管理できる「データ駆動型」の設計を採用しています。

## 主な機能
- **自動ポスト機能**: GitHub Actionsのスケジュール実行（cron）による定期投稿。
- **時系列ローテーション**: 20時間周期（5グループ×4時間）で投稿グループを切り替え、毎日投稿時間帯がズレることでBotらしさを軽減するロジックを搭載。
- **データ管理**: 投稿内容は `yaml/memes.yml` に集約。
- **手動実行対応**: GitHub Actionsの `workflow_dispatch` により、ブラウザ上から即時テスト実行が可能。

## 技術スタック
- **Language**: Python 3.9+
- **Library**: [Tweepy](https://www.tweepy.org/) (X API v2), [PyYAML](https://pyyaml.org/)
- **Automation**: GitHub Actions
- **Data Format**: YAML

## ディレクトリ構成
```text
.
├── .github/workflows/
│   └── main.yml        # GitHub Actionsの設定（毎時0分実行）
├── python/
│   └── bot.py          # 投稿ロジック（JSTベースのグループ判定・API連携）
├── yaml/
│   └── memes.yml       # ミームデータ（5つのグループに構造化）
├── requirements.txt    # 依存ライブラリ（tweepy, PyYAML）
└── README.md           # 本ドキュメント
```

## セットアップ手順

### 1. X (Twitter) APIの準備
1. [X Developer Console](https://developer.x.com/)でプロジェクトとアプリを作成します。
2. **User authentication settings** で以下の設定を行います。
   - **App permissions**: `Read and Write` （※必須）
   - **Type of App**: `Web App, Automated App or Bot`
3. **Keys and Tokens** から以下の4つのキーを取得します。
   - `API Key` / `API Key Secret`
   - `Access Token` / `Access Token Secret (OAuth 1.0a)`

### 2. GitHub Secretsの設定
リポジトリの **Settings > Secrets and variables > Actions** に、以下の名前でSecretを登録します。

| Secret名 | 内容 |
| :--- | :--- |
| `X_API_KEY` | X API Key |
| `X_API_SECRET` | X API Key Secret |
| `X_ACCESS_TOKEN` | X Access Token (OAuth 1.0a) |
| `X_ACCESS_SECRET` | X Access Token Secret (OAuth 1.0a) |

### 3. ミームのカスタマイズ
`yaml/memes.yml` を編集することで、特定の時間帯に流れるフレーズをカスタマイズできます。

```yaml
groups:
  group1:
    name: "Showa_Bubble"
    items:
      - "しもしも〜？"
      - "おったまげー！"
```

## 運用・デバッグ

### 手動実行とログの確認
1. GitHubの **Actions** タブから `Heisei Meme Bot` を選択します。
2. **Run workflow** をクリックして実行します。
3. 実行されたジョブの **Run bot** ステップのログで、選択されたグループと投稿内容を確認できます。

### スケジュールの変更
現在は `.github/workflows/main.yml` にて毎時0分（`0 * * * *`）に実行される設定です。投稿頻度を下げたい場合は、cron設定を `0 */4 * * *`（4時間おき）等に修正してください。

## ライセンス
MIT License

