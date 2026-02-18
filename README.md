# shukatsu-manager

就活の「会社」「面接」「振り返り」を管理するDjangoアプリです。

## 主な機能
- 面接一覧 / 面接詳細
- 面接ごとの振り返り追加（質問 / 回答 / 改善点）
- ダッシュボード（直近面接 / 最近の振り返り）

## 技術スタック
- Python / Django
- SQLite（開発用）

## セットアップ（ローカル）
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```bash
...
