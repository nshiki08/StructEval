# StructEval Dataset - 詳細分析レポート

## 📊 エグゼクティブサマリー

- **総サンプル数**: 2,035
- **Renderable (rendering=True)**: 1,085サンプル (53.3%)
- **Non-renderable (rendering=False)**: 950サンプル (46.7%)
- **総タスク種類**: 44種類
- **VQA質問総数**: 9,032問（Renderableのみ）
- **ユニークメトリクス**: 12,857種類

---

## 🎨 RENDERABLE DATA 詳細分析 (1,085サンプル)

### タスク別統計（25種類）

| ランク | タスク名 | サンプル数 | VQA平均 | メトリクス平均 | クエリ長平均 |
|--------|---------|-----------|---------|--------------|-------------|
| 1 | Convert Matplotlib to TikZ | 100 | 9.4 | 21.6 | 3,889 |
| 2 | Text to Angular | 50 | 7.2 | 12.1 | 1,438 |
| 3 | Text to Latex | 50 | 7.3 | 10.1 | 1,074 |
| 4 | Text to Markdown | 50 | 8.2 | 6.8 | 1,005 |
| 5 | Text to Matplotlib | 50 | 8.6 | 14.6 | 778 |
| 6 | Text to React | 50 | 8.9 | 16.5 | 1,025 |
| 7 | Text to SVG | 50 | 7.9 | 19.9 | 1,291 |
| 8 | Text to Tikz | 50 | 8.1 | 9.1 | 969 |
| 9 | Text to HTML | 50 | 6.9 | 11.9 | 882 |
| 10 | Text to Mermaid | 50 | 8.6 | 12.8 | 1,026 |
| 11 | Text to Typst | 50 | 8.3 | 6.5 | 1,274 |
| 12 | Text to Vega | 50 | 8.4 | 7.7 | 1,007 |
| 13 | Text to Vue | 50 | 6.4 | 9.2 | 1,175 |
| 14 | Convert Markdown to HTML | 50 | 8.8 | 19.8 | 4,054 |
| 15 | Text to Canvas | 50 | 7.9 | 9.6 | 1,118 |
| 16 | Convert React to HTML | 45 | 9.1 | 21.7 | 3,528 |
| 17 | Convert HTML to React | 45 | 9.3 | 21.8 | 3,969 |
| 18 | Convert Vue to HTML | 40 | 8.7 | 20.5 | 5,191 |
| 19 | Convert HTML to Vue | 40 | 8.9 | 21.8 | 3,984 |
| 20 | Convert Markdown to React | 30 | 9.1 | 26.0 | 4,222 |
| 21 | Convert HTML to Angular | 30 | 8.5 | 28.5 | 4,411 |
| 22 | Convert Markdown to Vue | 25 | 9.0 | 25.0 | 4,367 |
| 23 | Convert Vue to React | 15 | 8.8 | 19.3 | 4,468 |
| 24 | Convert Markdown to Angular | 10 | 8.5 | 28.3 | 4,585 |
| 25 | Convert React to Angular | 5 | 9.2 | 22.0 | 3,178 |

### VQA (Visual Question Answering) 分析

#### 全体統計
- **総質問数**: 9,032問
- **平均質問数/サンプル**: 8.3問
- **質問数の範囲**: 4〜12問

#### 質問タイプ分布（開始単語別）
| 開始単語 | 出現回数 | 割合 |
|---------|---------|------|
| What | 4,995 | 55.3% |
| How | 2,142 | 23.7% |
| Which | 627 | 6.9% |
| Is | 397 | 4.4% |
| Are | 356 | 3.9% |
| Does | 188 | 2.1% |
| Where | 169 | 1.9% |
| その他 | 158 | 1.8% |

**主要な質問パターン**:
- **What系**: 要素の識別、テキスト内容、構造の詳細
- **How系**: 数量、配置、スタイリング方法
- **Which/Is/Are系**: Yes/No質問、選択肢の確認

#### 回答タイプ分布
| 回答タイプ | 出現回数 | 割合 | 説明 |
|-----------|---------|------|------|
| Short phrase | 3,688 | 40.8% | 2〜5単語の短いフレーズ |
| Long answer | 2,463 | 27.3% | 6単語以上の詳細な回答 |
| Single word | 1,535 | 17.0% | 1単語での回答 |
| Numeric | 1,346 | 14.9% | 数値での回答 |

### 出力メトリクス分析

#### Renderable全体
- **総メトリクス数**: 16,848
- **ユニークメトリクス**: 7,255種類
- **平均/サンプル**: 15.5個
- **範囲**: 1〜66個

#### 頻出メトリクス Top 20
1. **Introduction** (168回) - セクションヘッダー
2. **Table of Contents** (95回) - 目次要素
3. **Description** (92回) - 説明文
4. **Value** (91回) - 値フィールド
5. **Overview** (84回) - 概要セクション
6. **Features** (84回) - 機能リスト
7. **green** (77回) - 色指定
8. **`<p>`** (73回) - HTMLタグ
9. **`<h1>`** (70回) - HTMLタグ
10. **`<hr>`** (68回) - HTMLタグ
11. **red** (68回) - 色指定
12. **Contact** (67回) - 連絡先セクション
13. **blue** (66回) - 色指定
14. **Contact Information** (66回)
15. **Home** (60回) - ナビゲーション項目
16. **Usage** (60回) - 使用方法セクション
17. **Dashboard Overview** (58回)
18. **Email** (53回)
19. **`<rect`** (53回) - SVG要素
20. **Status** (53回)

### Input/Output Type分布

#### Input Type（Renderable）
| Type | サンプル数 | 割合 |
|------|-----------|------|
| Text | 650 | 59.9% |
| Markdown | 115 | 10.6% |
| HTML | 115 | 10.6% |
| Matplotlib | 100 | 9.2% |
| Vue | 55 | 5.1% |
| React | 50 | 4.6% |

#### Output Type（Renderable）
| Type | サンプル数 | 割合 |
|------|-----------|------|
| HTML | 185 | 17.1% |
| React | 140 | 12.9% |
| Vue | 115 | 10.6% |
| TikZ | 100 | 9.2% |
| Angular | 95 | 8.8% |
| その他14種類 | 450 | 41.5% |

### タスク難易度指標

#### 複雑性の高いタスク（メトリクス数基準）
1. **Convert HTML to Angular**: 平均28.5メトリクス
2. **Convert Markdown to Angular**: 平均28.3メトリクス
3. **Convert Markdown to React**: 平均26.0メトリクス
4. **Convert Markdown to Vue**: 平均25.0メトリクス
5. **Convert HTML to Vue**: 平均21.8メトリクス

#### VQA質問数が多いタスク
1. **Convert Matplotlib to TikZ**: 平均9.4問
2. **Convert HTML to React**: 平均9.3問
3. **Convert React to Angular**: 平均9.2問
4. **Convert Markdown to React**: 平均9.1問
5. **Convert React to HTML**: 平均9.1問

---

## 📋 NON-RENDERABLE DATA 詳細分析 (950サンプル)

### タスク別統計（19種類）

**重要**: すべてのタスクが**正確に50サンプルずつ**の完全均等分布

| タスク名 | サンプル数 | メトリクス平均 | クエリ長平均 |
|---------|-----------|--------------|-------------|
| CSV to JSON | 50 | 16.4 | 810 |
| CSV to XML | 50 | 14.6 | 707 |
| CSV to YAML | 50 | 15.7 | 688 |
| JSON to CSV | 50 | 6.2 | 1,320 |
| JSON to XML | 50 | 7.4 | 631 |
| JSON to YAML | 50 | 20.3 | 960 |
| TOML to JSON | 50 | 17.5 | 713 |
| TOML to YAML | 50 | 19.3 | 755 |
| Text to CSV | 50 | 15.9 | 2,164 |
| Text to JSON | 50 | 15.9 | 2,465 |
| Text to TOML | 50 | 16.0 | 2,467 |
| Text to XML | 50 | 15.9 | 2,298 |
| Text to YAML | 50 | 15.9 | 2,477 |
| XML to CSV | 50 | 6.2 | 1,737 |
| XML to JSON | 50 | 5.4 | 776 |
| XML to YAML | 50 | 6.4 | 699 |
| YAML to CSV | 50 | 6.1 | 1,130 |
| YAML to JSON | 50 | 21.5 | 810 |
| YAML to XML | 50 | 5.9 | 460 |

### 出力メトリクス分析

#### Non-renderable全体
- **総メトリクス数**: 12,426
- **ユニークメトリクス**: 5,602種類
- **平均/サンプル**: 13.1個
- **範囲**: 3〜30個

#### 頻出メトリクス Top 20
1. **galaxy.name** (93回) - 銀河名フィールド
2. **planet.name** (84回) - 惑星名フィールド
3. **planet_name** (72回) - 惑星名（CSVスタイル）
4. **planet.atmosphere.pressure** (62回)
5. **planet.atmosphere.composition** (60回)
6. **museum.name** (57回) - 博物館名
7. **spaceship.name** (56回) - 宇宙船名
8. **museum.location.city** (55回)
9. **planet.discovery.year** (53回)
10. **csv::DiscoveryDate** (53回)
11. **museum.location.country** (51回)
12. **spaceship.crew.captain** (44回)
13. **system.star_name** (43回)
14. **spaceship.model** (43回)
15. **planet.moons** (40回)
16. **planet.discovery.method** (39回)
17. **spaceship.missions[0].destination** (39回)
18. **spaceship.missions[1].destination** (39回)
19. **planet.type** (38回)
20. **moons[0].diameter_km** (37回)

**データドメインの特徴**:
- **宇宙/SF系**: planet, galaxy, spaceship, moons など
- **文化施設**: museum, library など
- **構造化データ**: ネストされたオブジェクト、配列構造

### Input/Output Type分布

#### Input Type（Non-renderable）
| Type | サンプル数 | 割合 |
|------|-----------|------|
| Text | 250 | 26.3% |
| CSV | 150 | 15.8% |
| JSON | 150 | 15.8% |
| XML | 150 | 15.8% |
| YAML | 150 | 15.8% |
| TOML | 100 | 10.5% |

#### Output Type（Non-renderable）
| Type | サンプル数 | 割合 |
|------|-----------|------|
| JSON | 250 | 26.3% |
| YAML | 250 | 26.3% |
| CSV | 200 | 21.1% |
| XML | 200 | 21.1% |
| TOML | 50 | 5.3% |

### タスク複雑性分析

#### メトリクス数が多いタスク（構造が複雑）
1. **YAML to JSON**: 平均21.5メトリクス
2. **JSON to YAML**: 平均20.3メトリクス
3. **TOML to YAML**: 平均19.3メトリクス
4. **TOML to JSON**: 平均17.5メトリクス
5. **CSV to JSON**: 平均16.4メトリクス

#### メトリクス数が少ないタスク（構造がシンプル）
1. **XML to JSON**: 平均5.4メトリクス
2. **YAML to XML**: 平均5.9メトリクス
3. **YAML to CSV**: 平均6.1メトリクス
4. **JSON to CSV**: 平均6.2メトリクス
5. **XML to CSV**: 平均6.2メトリクス

---

## 🔍 タスクカテゴリ分析

### Renderableタスクの分類

#### 1. Text-to-Visual (650サンプル、59.9%)
テキスト記述から各種ビジュアルフォーマットを生成

**フロントエンドフレームワーク** (250サンプル):
- Text to React: 50
- Text to Vue: 50
- Text to Angular: 50
- Text to HTML: 50
- Text to Canvas: 50

**可視化/ダイアグラム** (300サンプル):
- Text to Matplotlib: 50
- Text to SVG: 50
- Text to Tikz: 50
- Text to TikZ (Matplotlibから): 100
- Text to Mermaid: 50

**ドキュメント** (100サンプル):
- Text to Latex: 50
- Text to Markdown: 50
- Text to Typst: 50
- Text to Vega: 50

#### 2. Framework Conversion (435サンプル、40.1%)
フレームワーク/フォーマット間の相互変換

**Markdownベース** (115サンプル):
- Markdown to HTML: 50
- Markdown to React: 30
- Markdown to Vue: 25
- Markdown to Angular: 10

**HTMLベース** (115サンプル):
- HTML to React: 45
- HTML to Vue: 40
- HTML to Angular: 30

**Reactベース** (50サンプル):
- React to HTML: 45
- React to Angular: 5

**Vueベース** (55サンプル):
- Vue to HTML: 40
- Vue to React: 15

**Matplotlibベース** (100サンプル):
- Matplotlib to TikZ: 100

### Non-renderableタスクの分類

#### 1. Text-to-Data (250サンプル、26.3%)
テキスト記述から構造化データを生成
- Text to JSON, CSV, XML, YAML, TOML

#### 2. Format Conversion (700サンプル、73.7%)
データフォーマット間の相互変換

**JSONハブ** (200サンプル):
- CSV/XML/YAML/TOML → JSON

**YAMLハブ** (200サンプル):
- CSV/JSON/XML/TOML → YAML

**CSVハブ** (150サンプル):
- JSON/XML/YAML → CSV

**XMLハブ** (150サンプル):
- CSV/JSON/YAML → XML

---

## 📈 クエリ長分析

### Renderable
| カテゴリ | 平均文字数 | 範囲 |
|---------|-----------|------|
| Text-to-Visual | 1,050 | 618〜1,749 |
| Conversion (短) | 3,650 | 1,831〜5,804 |
| Conversion (長) | 4,850 | 3,280〜10,043 |
| Matplotlib変換 | 3,889 | 1,488〜6,532 |

**最長クエリタスク**:
1. Convert Vue to HTML: 5,191文字
2. Markdown to Angular: 4,585文字
3. Vue to React: 4,468文字

**最短クエリタスク**:
1. Text to Matplotlib: 778文字
2. Text to HTML: 882文字
3. Text to Tikz: 969文字

### Non-renderable
| カテゴリ | 平均文字数 | 範囲 |
|---------|-----------|------|
| Text-to-Data | 2,374 | 1,687〜3,279 |
| Format変換 | 930 | 286〜2,079 |

---

## 💡 主要な洞察

### 1. データセット設計の特徴
- **Renderable**: タスクサイズが変動（5〜100サンプル）、多様な変換パターン
- **Non-renderable**: 完全均等分布（各50サンプル）、体系的なフォーマット変換

### 2. 評価の焦点
- **Renderable**: ビジュアル出力の正確性（VQA使用）、構造の一致（メトリクス）
- **Non-renderable**: データ構造の正確性（メトリクス）、フォーマット準拠

### 3. タスク難易度の指標
高難易度の特徴:
- VQA質問数が多い（9問以上）
- 出力メトリクス数が多い（20個以上）
- クエリ長が長い（4,000文字以上）
- フレームワーク間の複雑な変換

### 4. ドメイン特性
- **Renderable**: UI/UX、データビジュアライゼーション、ドキュメント
- **Non-renderable**: SF/宇宙テーマ、架空のエンティティ、構造化データ

### 5. VQAの質問設計
- **What系が過半数**: 具体的な要素の識別
- **How系が4分の1**: 数量、配置、実装方法
- **回答の多様性**: 40.8%が短いフレーズ、27.3%が詳細な回答

### 6. メトリクスの傾向
- **Renderable**: UI要素、色、HTMLタグ、セクション名
- **Non-renderable**: ネストされたフィールドパス、配列インデックス

---

## 📊 統計サマリー

| 指標 | Renderable | Non-renderable | 全体 |
|------|-----------|---------------|------|
| サンプル数 | 1,085 | 950 | 2,035 |
| タスク種類 | 25 | 19 | 44 |
| VQA質問総数 | 9,032 | 0 | 9,032 |
| 平均VQA/サンプル | 8.3 | N/A | N/A |
| 総メトリクス数 | 16,848 | 12,426 | 29,274 |
| ユニークメトリクス | 7,255 | 5,602 | 12,857 |
| 平均メトリクス/サンプル | 15.5 | 13.1 | 14.4 |
| 平均クエリ長 | 2,345文字 | 1,252文字 | 1,838文字 |

---

## 🎯 ユースケース

### Renderableデータの用途
1. **Webフレームワーク生成**: AI による UI コンポーネント生成の評価
2. **可視化変換**: データビジュアライゼーションフォーマット間の変換
3. **ドキュメント生成**: LaTeX、Markdown、Typstなどの文書生成

### Non-renderableデータの用途
1. **データフォーマット変換**: 異なるシリアライゼーション形式間の変換
2. **構造化データ抽出**: 自然言語からの構造化データ生成
3. **API/データ連携**: 異なるシステム間のデータ交換フォーマット変換

---

## 📝 データセット品質指標

### 長所
✅ タスクの多様性が高い（44種類）
✅ サンプルサイズが十分（2,035）
✅ VQAによる詳細な評価基準
✅ メトリクスによる客観的評価
✅ Non-renderableの完全均等分布

### 考慮点
⚠️ Renderableのタスク間サンプル数のばらつき（5〜100）
⚠️ 一部タスクのサンプル数が少ない（5サンプル）
⚠️ クエリ長の大きな変動（286〜10,043文字）

---

生成日時: 2025-12-30
分析スクリプト: `detailed_analysis.py`
