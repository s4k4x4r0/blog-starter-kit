# 検証ノート

## 企画

eyecatchスキルに「グラデーション+ITサービスアイコン+タイトル」パターンを追加する。
既存のベース画像パターン（forest/cyber）に加え、アイコンのブランドカラーから自動でグラデーション背景を生成する方式。

## 方針

- **アイコン取得**: simple-icons (GitHub raw URL) からSVGを取得。3000+のITブランドアイコンにブランドカラー付き
- **グラデーション生成**: ブランドカラー1色からHSL色相回転で決定論的に2色を生成（LLM非依存）
  - warm_spread: +60°〜+140°回転（ピンク→黄色系、参考画像風）
  - analogous: ±30°（類似色）
  - complementary: ±90°（補色方向）
  - pastel: 彩度下げ+明度上げ
- **画像合成**: Pillow + cairosvg（既存make_eyecatch.pyと同じPillowベース）
- **テキスト**: NotoSansCJKjp-Bold、既存の日本語折り返しロジックを活用

## ログ

### 2026-03-16 PoC作成

- `poc/gradient_eyecatch.py` を作成
- simple-icons CDN (`cdn.simpleicons.org`) はプロキシで403ブロック → GitHub raw URL (`raw.githubusercontent.com`) に変更で解決
- Terraform/Docker/Kubernetes/Redisの4パターンを生成して確認
- warm_spread スタイルの色相回転パラメータを調整（+60°/+140°が参考画像に近い配色）
- 結果:
  - Terraform(紫): ピンク→黄色グラデ ✅ 参考画像に近い
  - Docker(青): ピンク→紫グラデ ✅ まとまりがある
  - Kubernetes(青): Dockerと似た配色（課題: 近い色相のブランドで差が出にくい）
  - Redis(赤): 黄色→緑グラデ ✅ アイコンが映える

## 未解決

- 近い色相のブランド（Docker/K8s等）でグラデーションが似てしまう問題
- 他のgradient-style（analogous, complementary, pastel）の実用性検証
- 本番化時に既存make_eyecatch.pyの禁則処理・行バランシングロジックの統合
- KNOWN_BRANDSのハードコード vs simple-iconsのJSONからの動的取得
