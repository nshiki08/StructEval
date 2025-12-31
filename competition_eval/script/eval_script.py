#!/usr/bin/env python3
"""
StructEval-T Evaluation Script

This script evaluates StructEval-T (non-renderable output) tasks.
Supports JSON, YAML, CSV, TOML, and XML output formats.

Scoring Logic:
- render_score (20%): Whether the output can be parsed as valid format
- key_validation_score (80%): Whether the paths in raw_output_metric exist in the parsed structure

Final Score = 0.2 * render_score + 0.8 * key_validation_score
"""

import json
import yaml
import csv
import toml
import xmltodict
import re
import os
import codecs
import tempfile
import logging
from typing import Dict, List, Any, Tuple, Optional

# Configure logging for debugging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# =============================================================================
# Type Code Mapping
# =============================================================================
TYPE_CODES = {
    "Text": "00",
    "Angular": "01",
    "CSV": "02",
    "Canvas": "03",
    "HTML": "04",
    "JSON": "05",
    "LaTeX": "06",
    "Markdown": "07",
    "Matplotlib": "08",
    "Mermaid": "09",
    "TOML": "10",
    "React": "11",
    "SVG": "12",
    "Tikz": "13",
    "Typst": "14",
    "Vega": "15",
    "Vue": "16",
    "XML": "17",
    "YAML": "18",
}

# Reverse mapping: type_code -> format name
CODE_TO_TYPE = {v: k.lower() for k, v in TYPE_CODES.items()}


# =============================================================================
# Utility Functions
# =============================================================================
def determine_output_type(task_id: str) -> str:
    """
    Determine output type from task_id.

    Args:
        task_id: Task identifier (e.g., "000500" -> JSON)

    Returns:
        Output format type (json, yaml, csv, toml, xml)
    """
    if len(task_id) >= 4:
        type_code = task_id[2:4]
        return CODE_TO_TYPE.get(type_code, "")
    return ""


def extract_code_from_generation(text: str, output_type: str = "") -> str:
    """
    Extract code from generation output.

    Supports:
      1. <|BEGIN_CODE|> ... <|END_CODE|> format
      2. ```fenced``` code blocks
      3. Raw text fallback

    Args:
        text: The generated text containing code
        output_type: Expected output type for fence matching

    Returns:
        Extracted code string
    """
    # Decode unicode escape sequences
    try:
        text = text.replace("&lt;", "<").replace("&gt;", ">")
        text = text.replace("<think>\n\n</think>\n\n", "")
        text = codecs.decode(text, "unicode_escape")
    except Exception:
        pass  # Use original string if decoding fails

    # Pattern 1: <|BEGIN_CODE|> ... <|END_CODE|>
    begin_end_pat = (
        r"<\|BEGIN_CODE\|\>[ \t]*\n?"
        r"(?P<payload1>.*?)"
        r"(?:<\|END_CODE\|\>|$)"
    )

    # Pattern 2: ```fenced``` block
    fence_pat = (
        rf"```(?:{re.escape(output_type)}|[^\n]*)[ \t]*\n"
        r"(?P<payload2>.*?)"
        r"(?:```|$)"
    )

    pattern = rf"(?:{begin_end_pat})|(?:{fence_pat})"
    m = re.search(pattern, text, re.DOTALL | re.IGNORECASE)

    if m:
        payload = m.group("payload1") or m.group("payload2")
        return payload.strip()

    # Fallback: check for additional fence pattern
    m = re.search(fence_pat, text, re.DOTALL | re.IGNORECASE)
    if m:
        return m.group("payload2").strip()

    # Final fallback: return entire text
    return text.strip()


def parse_content(content: str, format_type: str) -> Tuple[Any, bool]:
    """
    Parse content string according to format type.

    Args:
        content: The content string to parse
        format_type: Format type (json, yaml, csv, toml, xml)

    Returns:
        (parsed_object, success_flag)
    """
    try:
        if format_type == "json":
            result = json.loads(content)
            return result, True
        elif format_type == "yaml":
            result = yaml.safe_load(content)
            return result, True
        elif format_type == "toml":
            result = toml.loads(content)
            return result, True
        elif format_type == "xml":
            result = xmltodict.parse(content)
            return result, True
        elif format_type == "csv":
            # Parse CSV into structured format
            reader = csv.DictReader(content.strip().split('\n'))
            rows = list(reader)
            return {"csv_headers": reader.fieldnames, "csv_rows": rows}, True
        else:
            logger.warning(f"Unsupported format type: {format_type}")
            return None, False
    except Exception as e:
        logger.debug(f"Parse error for {format_type}: {e}")
        return None, False


# =============================================================================
# Path Validation Functions
# =============================================================================
def tokenize_path(path: str) -> List[str]:
    """
    Tokenize a dot-notation path, handling back-ticks and array indices.

    Args:
        path: The path string (e.g., "users[0].name" or "museum.galleries.*.title")

    Returns:
        List of path tokens
    """
    # Special case: CSV header paths
    if path.startswith("csv::"):
        return [path]

    tokens, buf, in_bt = [], "", False
    i, n = 0, len(path)

    while i < n:
        ch = path[i]

        # Toggle back-tick state
        if ch == "`":
            in_bt = not in_bt
            i += 1
            continue

        # Dot delimiter (when not inside back-ticks)
        if ch == "." and not in_bt:
            if buf:
                tokens.append(buf)
                buf = ""
            i += 1
            continue

        # Bracket "[index]" treated as separate token
        if ch == "[" and not in_bt:
            if buf:
                tokens.append(buf)
                buf = ""
            j = path.find("]", i)
            if j == -1:
                raise ValueError(f"Unclosed '[' in path: {path}")
            tokens.append(path[i : j + 1])  # e.g., "[0]"
            i = j + 1
            continue

        # Regular character
        buf += ch
        i += 1

    if buf:
        tokens.append(buf)
    return tokens


def path_exists(data: Any, path: str) -> bool:
    """
    Check if a path exists in a structured data object.

    Supports:
      - Dot notation: "museum.name"
      - Array indices: "galleries[0].title"
      - Wildcards: "galleries.*.title"
      - CSV headers: "csv::column_name"

    Args:
        data: The structured data to check
        path: The path to check (dot notation)

    Returns:
        True if path exists, False otherwise
    """
    try:
        tokens = tokenize_path(path)
    except ValueError as e:
        logger.debug(f"Path tokenization error: {e}")
        return False

    def walk(node: Any, toks: List[str]) -> bool:
        if not toks:
            return True
        tok, *rest = toks

        # CSV header rule (root level only)
        if isinstance(node, dict) and "csv_headers" in node and tok.startswith("csv::"):
            header = tok[5:]
            return header in node["csv_headers"] and not rest

        # Wildcard
        if tok == "*":
            if isinstance(node, list):
                return any(walk(item, rest) for item in node)
            return False

        # Fixed index [n]
        if tok.startswith("[") and tok.endswith("]"):
            try:
                idx = int(tok[1:-1])
            except ValueError:
                return False
            return (
                isinstance(node, list)
                and 0 <= idx < len(node)
                and walk(node[idx], rest)
            )

        # Dict key handling (JSON/YAML/TOML/XML)
        if isinstance(node, dict):
            # Literal key match (works for "@id" too)
            if tok in node:
                return walk(node[tok], rest)

            # XML attribute fallback: "@id" -> "id"
            if tok.startswith("@"):
                attr = tok[1:]
                if attr in node:
                    return walk(node[attr], rest)

        return False

    return walk(data, tokens)


# =============================================================================
# Scoring Functions
# =============================================================================
def calculate_render_score(content: str, format_type: str) -> Tuple[float, Any]:
    """
    Calculate render score by checking if content can be parsed.

    Args:
        content: Extracted code content
        format_type: Expected format type

    Returns:
        (render_score, parsed_data)
        render_score: 1.0 if parseable, 0.0 otherwise
        parsed_data: Parsed data object if successful, None otherwise
    """
    if not content or not content.strip():
        return 0.0, None

    parsed_data, success = parse_content(content, format_type)

    if success and parsed_data:
        return 1.0, parsed_data
    return 0.0, None


def calculate_key_validation_score(
    parsed_data: Any,
    raw_output_metric: List[str]
) -> Tuple[float, Dict[str, bool]]:
    """
    Calculate key validation score by checking path existence.

    Args:
        parsed_data: Parsed data structure
        raw_output_metric: List of paths to check

    Returns:
        (score, path_results)
        score: Ratio of found paths to total paths
        path_results: Dictionary mapping each path to its existence status
    """
    if not raw_output_metric:
        return 0.0, {}

    path_results = {}
    matches = 0

    for path in raw_output_metric:
        exists = path_exists(parsed_data, path)
        path_results[path] = exists
        if exists:
            matches += 1

    score = matches / len(raw_output_metric)
    return score, path_results


def evaluate_single_item(item: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluate a single StructEval-T item.

    Args:
        item: Task item to evaluate

    Returns:
        Evaluation result with scores and debug info
    """
    task_id = item.get("task_id", "unknown")
    generation = item.get("generation", "")
    raw_output_metric = item.get("raw_output_metric", [])

    # Determine output type
    output_type = determine_output_type(task_id)

    result = {
        "task_id": task_id,
        "output_type": output_type,
        "render_score": 0.0,
        "key_validation_score": 0.0,
        "final_score": 0.0,
        "path_results": {},
        "error": None,
    }

    if not output_type:
        result["error"] = f"Unknown output type for task_id: {task_id}"
        return result

    # Extract code from generation
    try:
        extracted_code = extract_code_from_generation(generation, output_type)
    except Exception as e:
        result["error"] = f"Code extraction failed: {e}"
        return result

    result["extracted_code_preview"] = extracted_code[:500] if extracted_code else ""

    # Calculate render score
    render_score, parsed_data = calculate_render_score(extracted_code, output_type)
    result["render_score"] = render_score

    # Calculate key validation score (only if parsing succeeded)
    if render_score > 0 and parsed_data is not None:
        key_score, path_results = calculate_key_validation_score(
            parsed_data, raw_output_metric
        )
        result["key_validation_score"] = key_score
        result["path_results"] = path_results

    # Calculate final score: 20% render + 80% key validation
    final_score = (0.2 * result["render_score"]) + (0.8 * result["key_validation_score"])
    result["final_score"] = round(final_score, 4)

    return result


# =============================================================================
# Main Evaluator Class
# =============================================================================
class LLMEvaluator:
    """
    Evaluator for StructEval-T (non-renderable) tasks.
    """

    def __init__(self, debug: bool = False):
        """
        Initialize the evaluator.

        Args:
            debug: If True, print detailed debug information
        """
        self.debug = debug
        self.results: List[Dict[str, Any]] = []

    def evaluate_jsonl(self, jsonl_lines: List[str]) -> float:
        """
        Evaluate JSONL lines or JSON array and return mean score.

        Supports two formats:
        1. JSONL: One JSON object per line
        2. JSON array: Single JSON array spanning multiple lines

        Args:
            jsonl_lines: List of file line strings

        Returns:
            Mean final score across all evaluated items
        """
        # First, try to parse as a complete JSON array (joined lines)
        full_content = "".join(jsonl_lines)
        try:
            parsed = json.loads(full_content)
            if isinstance(parsed, list):
                logger.info(f"Parsed as JSON array with {len(parsed)} items")
                return self.evaluate_items(parsed)
            else:
                # Single object
                return self.evaluate_items([parsed])
        except json.JSONDecodeError:
            pass  # Fall through to JSONL parsing

        # Parse as JSONL (one object per line)
        all_items = []
        for line in jsonl_lines:
            line = line.strip()
            if not line:
                continue
            try:
                parsed = json.loads(line)
                # Handle both single object and array formats
                if isinstance(parsed, list):
                    all_items.extend(parsed)
                else:
                    all_items.append(parsed)
            except json.JSONDecodeError as e:
                logger.debug(f"Failed to parse JSONL line: {e}")
                continue

        return self.evaluate_items(all_items)

    def evaluate_json(self, json_content: str) -> float:
        """
        Evaluate JSON content (array format) and return mean score.

        Args:
            json_content: JSON string containing array of items

        Returns:
            Mean final score across all evaluated items
        """
        try:
            items = json.loads(json_content)
            if not isinstance(items, list):
                items = [items]
            return self.evaluate_items(items)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON content: {e}")
            return 0.0

    def evaluate_items(self, items: List[Dict[str, Any]]) -> float:
        """
        Evaluate a list of items and return mean score.

        Args:
            items: List of task items to evaluate

        Returns:
            Mean final score across all evaluated items
        """
        self.results = []
        scores = []

        # Filter to only non-renderable items (rendering: false)
        non_renderable_items = [
            item for item in items
            if item.get("rendering", False) is False
        ]

        if not non_renderable_items:
            logger.warning("No non-renderable items found in input")
            return 0.0

        logger.info(f"Evaluating {len(non_renderable_items)} non-renderable items")

        for idx, item in enumerate(non_renderable_items):
            result = evaluate_single_item(item)
            self.results.append(result)
            scores.append(result["final_score"])

            if self.debug:
                self._print_debug_info(result, idx + 1, len(non_renderable_items))

        mean_score = sum(scores) / len(scores) if scores else 0.0

        if self.debug:
            self._print_summary(scores, mean_score)

        return round(mean_score, 4)

    def _print_debug_info(self, result: Dict[str, Any], current: int, total: int):
        """Print debug information for a single result."""
        print(f"\n{'='*60}")
        print(f"Task {current}/{total}: {result['task_id']}")
        print(f"{'='*60}")
        print(f"Output Type: {result['output_type']}")
        print(f"Render Score: {result['render_score']}")
        print(f"Key Validation Score: {result['key_validation_score']:.4f}")
        print(f"Final Score: {result['final_score']:.4f}")

        if result.get("error"):
            print(f"Error: {result['error']}")

        if result.get("path_results"):
            print("\nPath Validation Results:")
            for path, exists in result["path_results"].items():
                status = "FOUND" if exists else "MISSING"
                print(f"  [{status}] {path}")

    def _print_summary(self, scores: List[float], mean_score: float):
        """Print evaluation summary."""
        print(f"\n{'='*60}")
        print("EVALUATION SUMMARY")
        print(f"{'='*60}")
        print(f"Total items evaluated: {len(scores)}")
        print(f"Mean score: {mean_score:.4f}")

        if scores:
            print(f"Min score: {min(scores):.4f}")
            print(f"Max score: {max(scores):.4f}")

            # Score distribution
            perfect = sum(1 for s in scores if s == 1.0)
            zero = sum(1 for s in scores if s == 0.0)
            partial = len(scores) - perfect - zero

            print(f"\nScore Distribution:")
            print(f"  Perfect (1.0): {perfect} ({100*perfect/len(scores):.1f}%)")
            print(f"  Partial (0-1): {partial} ({100*partial/len(scores):.1f}%)")
            print(f"  Zero (0.0): {zero} ({100*zero/len(scores):.1f}%)")

    def get_results(self) -> List[Dict[str, Any]]:
        """Return detailed results for all evaluated items."""
        return self.results

    def save_results(self, output_path: str):
        """Save detailed results to a JSON file."""
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        logger.info(f"Results saved to {output_path}")


# =============================================================================
# Main Function
# =============================================================================
def main():
    """
    Main function to evaluate responses from a JSON/JSONL file and print the mean score.
    """
    evaluator = LLMEvaluator()

    # Load file content from the specified file
    submission_path = os.environ.get("USERSUBMISSION")

    if not submission_path:
        logger.error("USERSUBMISSION environment variable not set")
        print(0.0)
        return

    if not os.path.exists(submission_path):
        logger.error(f"Submission file not found: {submission_path}")
        print(0.0)
        return

    with open(submission_path, encoding="utf-8") as file:
        jsonl_lines = file.readlines()

    # Evaluate the JSONL lines and calculate the mean score
    mean_score = evaluator.evaluate_jsonl(jsonl_lines)

    # Print the final mean score
    print(mean_score)


if __name__ == "__main__":
    main()
