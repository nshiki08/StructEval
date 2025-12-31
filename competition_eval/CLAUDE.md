# StructEval-T コンペティション評価スクリプト

## 概要

このディレクトリには、コンペティション環境でのStructEval-T（非レンダリング構造化出力）タスク評価スクリプトが含まれています。

## ファイル構成

- `eval_script.py`: メイン評価スクリプト

## 使用方法

### 環境変数

スクリプトは `USERSUBMISSION` 環境変数から提出ファイルのパスを読み取ります：

```bash
export USERSUBMISSION=/path/to/submission.json
python eval_script.py
```

### 入力形式

スクリプトはタスクアイテムの配列を含むJSONファイルを受け付けます：

```json
[
  {
    "task_id": "000500",
    "query": "Please output JSON code...",
    "feature_requirements": "",
    "task_name": "Text to JSON",
    "input_type": "Text",
    "output_type": "JSON",
    "VQA": [],
    "raw_output_metric": ["path.to.key", "another.path[0].value"],
    "rendering": false,
    "generation": "```json\n{...}\n```"
  }
]
```

### 出力

スクリプトは平均スコアを表す単一のfloat値（0.0 - 1.0）を出力します。

## 採点ロジック

### StructEval-T（非レンダリング出力）

`"rendering": false` のアイテムのみが評価対象です。対象フォーマット：
- JSON (task_id: xx05xx)
- YAML (task_id: xx18xx)
- CSV (task_id: xx02xx)
- TOML (task_id: xx10xx)
- XML (task_id: xx17xx)

### スコア計算

```
最終スコア = 0.2 * render_score + 0.8 * key_validation_score
```

#### render_score（20%）
- **1.0**: 出力が正しいフォーマット（JSON、YAMLなど）としてパース可能
- **0.0**: 出力がパース不可

#### key_validation_score（80%）
- `raw_output_metric` 内のパスのうち、パースされた構造に存在するパスの割合
- 例：5つのパスのうち3つが存在する場合、スコア = 0.6

### パス記法

`raw_output_metric` では以下のパス記法がサポートされています：

| 記法 | 例 | 説明 |
|------|---------|-------------|
| ドット記法 | `museum.name` | ネストされたキーにアクセス |
| 配列インデックス | `galleries[0].title` | 配列要素にアクセス |
| ワイルドカード | `galleries.*.title` | 任意の配列要素にマッチ |
| CSVヘッダー | `csv::column_name` | CSVカラムの存在確認 |
| バッククォートエスケープ | `` `special.key` `` | キー名内のドットをエスケープ |

## デバッグ

詳細なデバッグ出力を有効にするには、`debug=True` でエバリュエーターをインスタンス化します：

```python
evaluator = LLMEvaluator(debug=True)
```

出力内容：
- アイテムごとのスコアとパス検証結果
- サマリー統計（最小値、最大値、分布）

### デバッグ出力例

```
============================================================
Task 1/10: 000500
============================================================
Output Type: json
Render Score: 1.0
Key Validation Score: 0.8000
Final Score: 0.8400

Path Validation Results:
  [FOUND] museum.name
  [FOUND] museum.location.city
  [MISSING] museum.galleries[0].artworks.*.artist
  [FOUND] museum.contact.email
```

## APIリファレンス

### LLMEvaluatorクラス

```python
class LLMEvaluator:
    def __init__(self, debug: bool = False)
    def evaluate_jsonl(self, jsonl_lines: List[str]) -> float
    def evaluate_json(self, json_content: str) -> float
    def evaluate_items(self, items: List[Dict[str, Any]]) -> float
    def get_results(self) -> List[Dict[str, Any]]
    def save_results(self, output_path: str) -> None
```

### ユーティリティ関数

```python
def determine_output_type(task_id: str) -> str
def extract_code_from_generation(text: str, output_type: str = "") -> str
def parse_content(content: str, format_type: str) -> Tuple[Any, bool]
def path_exists(data: Any, path: str) -> bool
def evaluate_single_item(item: Dict[str, Any]) -> Dict[str, Any]
```

## タイプコード一覧

| コード | フォーマット | レンダリング対象 |
|------|--------|------------|
| 00 | Text | - |
| 01 | Angular | Yes |
| 02 | CSV | No |
| 04 | HTML | Yes |
| 05 | JSON | No |
| 06 | LaTeX | Yes |
| 07 | Markdown | Yes |
| 08 | Matplotlib | Yes |
| 09 | Mermaid | Yes |
| 10 | TOML | No |
| 11 | React | Yes |
| 12 | SVG | Yes |
| 17 | XML | No |
| 18 | YAML | No |

## 依存パッケージ

- `json`（標準ライブラリ）
- `yaml`（PyYAML）
- `csv`（標準ライブラリ）
- `toml`
- `xmltodict`
- `re`（標準ライブラリ）
- `codecs`（標準ライブラリ）
- `logging`（標準ライブラリ）
