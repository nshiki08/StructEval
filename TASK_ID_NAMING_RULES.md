# StructEval タスクID命名規則

## 📋 概要

StructEvalのタスクIDは**6桁の数字**で構成され、以下のルールに従っています：

```
[Input Code][Output Code][Sequential Number]
   (2桁)      (2桁)          (2桁)
```

### 例
- `000100` = Text (00) → Angular (01), サンプル#00
- `041144` = HTML (04) → React (11), サンプル#44
- `180549` = YAML (18) → JSON (05), サンプル#49
- `08XX99` = Matplotlib (08) → TikZ (XX), サンプル#99

---

## 🔢 Input Type コード（最初の2桁）

| コード | Input Type | サンプル数 |
|--------|-----------|-----------|
| `00` | Text | 900 |
| `02` | CSV | 150 |
| `04` | HTML | 115 |
| `05` | JSON | 150 |
| `07` | Markdown | 115 |
| `08` | Matplotlib | 100 |
| `10` | TOML | 100 |
| `11` | React | 50 |
| `16` | Vue | 55 |
| `17` | XML | 150 |
| `18` | YAML | 150 |

### Input Codeの特徴
- **00**: Textが最大（900サンプル、18種類の出力タイプ）
- **02, 05, 17, 18**: データフォーマット系（各150サンプル）
- **04, 07**: マークアップ/フレームワーク系（115サンプル）
- **08, 10**: 可視化/設定ファイル系（100サンプル）
- **11, 16**: フロントエンドフレームワーク（50-55サンプル）

---

## 🎯 Output Type コード（3-4桁目）

| コード | Output Type | サンプル数 |
|--------|------------|-----------|
| `01` | Angular | 95 |
| `02` | CSV | 200 |
| `03` | Canvas | 50 |
| `04` | HTML | 185 |
| `05` | JSON | 250 |
| `07` | Markdown | 50 |
| `08` | Matplotlib | 50 |
| `09` | Mermaid | 50 |
| `10` | TOML | 50 |
| `11` | React | 140 |
| `12` | SVG | 50 |
| `13` | Tikz | 50 |
| `14` | Typst | 50 |
| `15` | Vega | 50 |
| `16` | Vue | 115 |
| `17` | XML | 200 |
| `18` | YAML | 250 |
| `XX` | Latex / TikZ* | 150 |

**注**: `XX`は特殊コードで、LatexとTikZ（大文字）に使用されています。

### Output Codeの特徴
- **05, 18**: JSON, YAMLが最多（各250サンプル）
- **02, 17**: CSV, XMLが次に多い（各200サンプル）
- **04**: HTMLも多い（185サンプル）
- **11, 16**: React, Vueはフレームワーク間変換が多い
- **XX**: 特殊ケースとして使用

---

## 🔄 Sequential Number（最後の2桁）

### ルール
- **範囲**: `00` 〜 `99`
- **用途**: 同じInput→Output組み合わせ内での連番
- **分布**: ほぼ均等（各番号が43-44回出現）

### 例
```
Text to Angular タスク（50サンプル）:
000100, 000101, 000102, ..., 000149

CSV to JSON タスク（50サンプル）:
020500, 020501, 020502, ..., 020549

Convert Vue to HTML タスク（40サンプル）:
160400, 160401, 160402, ..., 160439
```

---

## 📊 タスクID例一覧

### Renderable タスク

#### Text-to-Visual
| タスク | ID範囲 | Input | Output | サンプル数 |
|--------|--------|-------|--------|-----------|
| Text to Angular | 000100-000149 | 00 | 01 | 50 |
| Text to Canvas | 000300-000349 | 00 | 03 | 50 |
| Text to HTML | 000400-000449 | 00 | 04 | 50 |
| Text to Latex | 00XX00-00XX49 | 00 | XX | 50 |
| Text to Markdown | 000700-000749 | 00 | 07 | 50 |
| Text to Matplotlib | 000800-000849 | 00 | 08 | 50 |
| Text to Mermaid | 000900-000949 | 00 | 09 | 50 |
| Text to React | 001100-001149 | 00 | 11 | 50 |
| Text to SVG | 001200-001249 | 00 | 12 | 50 |
| Text to Tikz | 001300-001349 | 00 | 13 | 50 |
| Text to Typst | 001400-001449 | 00 | 14 | 50 |
| Text to Vega | 001500-001549 | 00 | 15 | 50 |
| Text to Vue | 001600-001649 | 00 | 16 | 50 |

#### Framework Conversions
| タスク | ID範囲 | Input | Output | サンプル数 |
|--------|--------|-------|--------|-----------|
| HTML to Angular | 040100-040129 | 04 | 01 | 30 |
| HTML to React | 041100-041144 | 04 | 11 | 45 |
| HTML to Vue | 041600-041639 | 04 | 16 | 40 |
| Markdown to Angular | 070100-070109 | 07 | 01 | 10 |
| Markdown to HTML | 070400-070449 | 07 | 04 | 50 |
| Markdown to React | 071100-071129 | 07 | 11 | 30 |
| Markdown to Vue | 071600-071624 | 07 | 16 | 25 |
| Matplotlib to TikZ | 08XX00-08XX99 | 08 | XX | 100 |
| React to Angular | 110100-110104 | 11 | 01 | 5 |
| React to HTML | 110400-110444 | 11 | 04 | 45 |
| Vue to HTML | 160400-160439 | 16 | 04 | 40 |
| Vue to React | 161100-161114 | 16 | 11 | 15 |

### Non-renderable タスク

#### Text-to-Data
| タスク | ID範囲 | Input | Output | サンプル数 |
|--------|--------|-------|--------|-----------|
| Text to CSV | 000200-000249 | 00 | 02 | 50 |
| Text to JSON | 000500-000549 | 00 | 05 | 50 |
| Text to TOML | 001000-001049 | 00 | 10 | 50 |
| Text to XML | 001700-001749 | 00 | 17 | 50 |
| Text to YAML | 001800-001849 | 00 | 18 | 50 |

#### Format Conversions
| タスク | ID範囲 | Input | Output | サンプル数 |
|--------|--------|-------|--------|-----------|
| CSV to JSON | 020500-020549 | 02 | 05 | 50 |
| CSV to XML | 021700-021749 | 02 | 17 | 50 |
| CSV to YAML | 021800-021849 | 02 | 18 | 50 |
| JSON to CSV | 050200-050249 | 05 | 02 | 50 |
| JSON to XML | 051700-051749 | 05 | 17 | 50 |
| JSON to YAML | 051800-051849 | 05 | 18 | 50 |
| TOML to JSON | 100500-100549 | 10 | 05 | 50 |
| TOML to YAML | 101800-101849 | 10 | 18 | 50 |
| XML to CSV | 170200-170249 | 17 | 02 | 50 |
| XML to JSON | 170500-170549 | 17 | 05 | 50 |
| XML to YAML | 171800-171849 | 17 | 18 | 50 |
| YAML to CSV | 180200-180249 | 18 | 02 | 50 |
| YAML to JSON | 180500-180549 | 18 | 05 | 50 |
| YAML to XML | 181700-181749 | 18 | 17 | 50 |

---

## 🔍 特殊ケース: "XX" コード

### 使用箇所
1. **Text to Latex**: `00XX00` 〜 `00XX49`
2. **Convert Matplotlib to TikZ**: `08XX00` 〜 `08XX99`

### 理由（推測）
- **Latex / TikZ (大文字)**: 他のフォーマットと区別するため
- **特別な変換処理**: 数値コードではなく、特殊な識別子として使用
- **将来の拡張性**: 数値コードが不足した場合の拡張

---

## 📈 コード割り当てパターン

### Input Codeの規則性
```
00 = Text (基本)
02 = CSV
04 = HTML
05 = JSON
07 = Markdown
08 = Matplotlib
10 = TOML
11 = React
16 = Vue
17 = XML
18 = YAML
```

**観察**:
- 偶数が多い（00, 02, 04, 08, 10, 16, 18）
- 連番ではなく、スキップがある（03, 06, 09, 12-15は未使用）
- フォーマットの種類ごとにグループ化されている可能性

### Output Codeの規則性
```
01 = Angular
02 = CSV
03 = Canvas
04 = HTML
05 = JSON
07 = Markdown
08 = Matplotlib
09 = Mermaid
10 = TOML
11 = React
12 = SVG
13 = Tikz
14 = Typst
15 = Vega
16 = Vue
17 = XML
18 = YAML
XX = Latex / TikZ
```

**観察**:
- ほぼ連番に近い（06は未使用）
- データフォーマット: 02, 05, 10, 17, 18
- Webフレームワーク: 01, 04, 11, 16
- 可視化: 08, 09, 12, 13, 14, 15
- ドキュメント: 07, XX

---

## 🎯 使用方法

### タスクIDからタスク情報を推測
```python
task_id = "041144"

input_code = task_id[0:2]   # "04" = HTML
output_code = task_id[2:4]  # "11" = React
seq_num = task_id[4:6]      # "44" = 45番目のサンプル

# => "Convert HTML to React, Sample #44"
```

### タスク情報からタスクIDを生成
```python
input_type = "Markdown"   # Code: 07
output_type = "Vue"       # Code: 16
sample_num = 20           # Sequential: 20

task_id = f"071620"
# => Markdown to Vue タスクの21番目のサンプル
```

---

## 📊 統計サマリー

| カテゴリ | 値 |
|---------|-----|
| 総タスクID数 | 2,035 |
| Input Typeコード数 | 11種類 |
| Output Typeコード数 | 19種類（XXを含む） |
| 最大Sequential Number | 99 |
| 最小Sequential Number | 00 |
| 特殊コード | XX (Latex/TikZ) |

### Input Code使用頻度
1. Text (00): 900サンプル
2. CSV, JSON, XML, YAML (02, 05, 17, 18): 各150サンプル
3. HTML, Markdown (04, 07): 各115サンプル
4. Matplotlib, TOML (08, 10): 各100サンプル
5. Vue (16): 55サンプル
6. React (11): 50サンプル

### Output Code使用頻度
1. JSON, YAML (05, 18): 各250サンプル
2. CSV, XML (02, 17): 各200サンプル
3. HTML (04): 185サンプル
4. Latex/TikZ (XX): 150サンプル
5. React (11): 140サンプル
6. Vue (16): 115サンプル
7. その他: 各50-95サンプル

---

## 💡 命名規則の利点

✅ **一目でタスク内容が分かる**: IDだけで変換元と変換先が判明
✅ **体系的な整理**: Input/Outputの組み合わせで自動的にグループ化
✅ **拡張性**: 新しいフォーマットを追加しやすい
✅ **検索・フィルタが容易**: 前方一致で特定のInputタイプを検索可能
✅ **エラーチェック**: IDの妥当性を簡単に検証可能

---

生成日時: 2025-12-30
分析スクリプト: `analyze_task_id_pattern.py`
