# StructEval Dataset Analysis

## 概要

- **総サンプル数**: 2,035
- **Renderable (rendering=True)**: 1,085 (53.3%)
- **Non-renderable (rendering=False)**: 950 (46.7%)

---

## 📊 Renderable Data (rendering=True) - 1,085サンプル

### タスク内訳（25種類）

| タスク名 | サンプル数 | 割合 |
|---------|-----------|------|
| Convert Matplotlib to TikZ | 100 | 9.2% |
| Text to Angular | 50 | 4.6% |
| Text to Latex | 50 | 4.6% |
| Text to Markdown | 50 | 4.6% |
| Text to Matplotlib | 50 | 4.6% |
| Text to React | 50 | 4.6% |
| Text to SVG | 50 | 4.6% |
| Text to Tikz | 50 | 4.6% |
| Text to HTML | 50 | 4.6% |
| Text to Mermaid | 50 | 4.6% |
| Text to Typst | 50 | 4.6% |
| Text to Vega | 50 | 4.6% |
| Text to Vue | 50 | 4.6% |
| Convert Markdown to HTML | 50 | 4.6% |
| Text to Canvas | 50 | 4.6% |
| Convert React to HTML | 45 | 4.1% |
| Convert HTML to React | 45 | 4.1% |
| Convert Vue to HTML | 40 | 3.7% |
| Convert HTML to Vue | 40 | 3.7% |
| Convert Markdown to React | 30 | 2.8% |
| Convert HTML to Angular | 30 | 2.8% |
| Convert Markdown to Vue | 25 | 2.3% |
| Convert Vue to React | 15 | 1.4% |
| Convert Markdown to Angular | 10 | 0.9% |
| Convert React to Angular | 5 | 0.5% |

### Input Type分布

| Input Type | サンプル数 | 割合 |
|-----------|-----------|------|
| Text | 650 | 59.9% |
| Markdown | 115 | 10.6% |
| HTML | 115 | 10.6% |
| Matplotlib | 100 | 9.2% |
| Vue | 55 | 5.1% |
| React | 50 | 4.6% |

### Output Type分布

| Output Type | サンプル数 | 割合 |
|------------|-----------|------|
| HTML | 185 | 17.1% |
| React | 140 | 12.9% |
| Vue | 115 | 10.6% |
| TikZ | 100 | 9.2% |
| Angular | 95 | 8.8% |
| Latex | 50 | 4.6% |
| Markdown | 50 | 4.6% |
| Matplotlib | 50 | 4.6% |
| SVG | 50 | 4.6% |
| Tikz | 50 | 4.6% |
| Mermaid | 50 | 4.6% |
| Typst | 50 | 4.6% |
| Vega | 50 | 4.6% |
| Canvas | 50 | 4.6% |

---

## 📋 Non-renderable Data (rendering=False) - 950サンプル

### タスク内訳（19種類）

| タスク名 | サンプル数 | 割合 |
|---------|-----------|------|
| Text to JSON | 50 | 5.3% |
| Text to CSV | 50 | 5.3% |
| Text to TOML | 50 | 5.3% |
| Text to XML | 50 | 5.3% |
| Text to YAML | 50 | 5.3% |
| CSV to JSON | 50 | 5.3% |
| JSON to CSV | 50 | 5.3% |
| XML to JSON | 50 | 5.3% |
| JSON to XML | 50 | 5.3% |
| YAML to JSON | 50 | 5.3% |
| JSON to YAML | 50 | 5.3% |
| XML to CSV | 50 | 5.3% |
| CSV to XML | 50 | 5.3% |
| XML to YAML | 50 | 5.3% |
| YAML to XML | 50 | 5.3% |
| YAML to CSV | 50 | 5.3% |
| TOML to JSON | 50 | 5.3% |
| CSV to YAML | 50 | 5.3% |
| TOML to YAML | 50 | 5.3% |

### Input Type分布

| Input Type | サンプル数 | 割合 |
|-----------|-----------|------|
| Text | 250 | 26.3% |
| CSV | 150 | 15.8% |
| JSON | 150 | 15.8% |
| XML | 150 | 15.8% |
| YAML | 150 | 15.8% |
| TOML | 100 | 10.5% |

### Output Type分布

| Output Type | サンプル数 | 割合 |
|------------|-----------|------|
| JSON | 250 | 26.3% |
| YAML | 250 | 26.3% |
| CSV | 200 | 21.1% |
| XML | 200 | 21.1% |
| TOML | 50 | 5.3% |

---

## 🔍 主要な特徴

### Renderable Data（ビジュアル/UIフォーマット）
- **主な用途**: Webコンポーネントやビジュアライゼーションなど、レンダリング可能な出力
- **主要なタスク**:
  - テキストからWebフレームワーク（React, Vue, Angular）への変換
  - テキストから可視化フォーマット（TikZ, SVG, Matplotlib）への変換
  - フレームワーク間の相互変換（React ↔ HTML, Vue ↔ HTML など）
- **特徴**: 入力の59.9%がテキストで、様々なビジュアルフォーマットに変換

### Non-renderable Data（データ構造フォーマット）
- **主な用途**: データ構造化・シリアライゼーションフォーマット
- **主要なタスク**:
  - テキストからデータフォーマット（JSON, CSV, XML, YAML, TOML）への変換
  - データフォーマット間の相互変換
- **特徴**: すべてのタスクが均等に50サンプルずつ分散され、バランスの取れたデータセット構成

### データセットのバランス
- 各タスクタイプが概ね均等に分散（Non-renderableは完全に均等、Renderableは5〜100サンプルの範囲）
- 総計44種類の異なるタスク
- 多様なInput/Outputタイプの組み合わせ
