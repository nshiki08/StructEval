#!/usr/bin/env python3
"""
StructEval Inference Script

This script runs inference on the evaluation dataset using a specified LLM
and saves the results to a JSON file.

Usage:
    python run_inference.py \
        --llm_model_name "meta-llama/Llama-3.1-8B-Instruct" \
        --llm_engine "vllm" \
        --input_path "dataset/StructEval_dataset.json" \
        --output_path "output/inference_results.json"
"""

import argparse
import json
import os
import sys
from datetime import datetime
from typing import List, Dict, Any

# Add structeval to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "structeval"))

from inference import run_inference


def create_prompt(query: str, model_name: str) -> str:
    """Create a formatted prompt for the LLM."""
    prompt = f"""{query}

IMPORTANT: Only output the required output format. You must start the format/code with <|BEGIN_CODE|> and end the format/code with <|END_CODE|>. No other text output (explanation, comments, etc.) are allowed. Do not use markdown code fences."""

    # Special handling for Qwen3-4B
    if model_name == "Qwen/Qwen3-4B":
        prompt += "\n\n/no_think"

    return prompt


def run_structeval_inference(
    llm_model_name: str,
    llm_engine: str,
    input_path: str,
    output_path: str,
    **kwargs
) -> str:
    """
    Run inference on the dataset and save results.

    Args:
        llm_model_name: Name of the LLM model to use
        llm_engine: Engine to use (e.g., "vllm", "openai")
        input_path: Path to input dataset JSON
        output_path: Path to save inference results
        **kwargs: Additional arguments for the LLM

    Returns:
        Path to the output file
    """
    # Load input dataset
    print(f"Loading dataset from: {input_path}")
    with open(input_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    print(f"Loaded {len(data)} tasks")

    # Create prompts for each task
    queries = [create_prompt(item["query"], llm_model_name) for item in data]

    # Run inference
    print(f"Running inference with model: {llm_model_name} (engine: {llm_engine})")
    generations = run_inference(llm_model_name, llm_engine, queries, **kwargs)

    # Combine results
    output_data = []
    for item, generation in zip(data, generations):
        result = item.copy()
        result["generation"] = generation
        output_data.append(result)

    # Create output directory if needed
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # Add metadata
    metadata = {
        "inference_metadata": {
            "model_name": llm_model_name,
            "engine": llm_engine,
            "timestamp": datetime.now().isoformat(),
            "total_tasks": len(data)
        }
    }

    # Save results
    print(f"Saving inference results to: {output_path}")
    with open(output_path, "w", encoding="utf-8") as out_file:
        json.dump(output_data, out_file, indent=2, ensure_ascii=False)

    # Also save metadata separately
    metadata_path = output_path.replace(".json", "_metadata.json")
    with open(metadata_path, "w", encoding="utf-8") as meta_file:
        json.dump(metadata, meta_file, indent=2)

    print(f"Inference complete! Results saved to: {output_path}")
    print(f"Metadata saved to: {metadata_path}")

    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Run StructEval inference on a dataset",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Using vLLM with a local model
    python run_inference.py \\
        --llm_model_name "meta-llama/Llama-3.1-8B-Instruct" \\
        --llm_engine "vllm" \\
        --input_path "dataset/StructEval_dataset.json" \\
        --output_path "output/llama_results.json"

    # Using OpenAI API
    python run_inference.py \\
        --llm_model_name "gpt-4" \\
        --llm_engine "openai" \\
        --input_path "dataset/StructEval_dataset.json" \\
        --output_path "output/gpt4_results.json"
"""
    )

    parser.add_argument(
        "--llm_model_name",
        type=str,
        required=True,
        help="Name of the LLM model to use (e.g., 'meta-llama/Llama-3.1-8B-Instruct', 'gpt-4')"
    )
    parser.add_argument(
        "--llm_engine",
        type=str,
        required=True,
        help="Inference engine to use (e.g., 'vllm', 'openai', 'huggingface')"
    )
    parser.add_argument(
        "--input_path",
        type=str,
        required=True,
        help="Path to the input dataset JSON file"
    )
    parser.add_argument(
        "--output_path",
        type=str,
        required=True,
        help="Path to save the inference results JSON file"
    )

    args = parser.parse_args()

    # Validate input file exists
    if not os.path.exists(args.input_path):
        print(f"Error: Input file not found: {args.input_path}")
        sys.exit(1)

    # Run inference
    run_structeval_inference(
        llm_model_name=args.llm_model_name,
        llm_engine=args.llm_engine,
        input_path=args.input_path,
        output_path=args.output_path
    )


if __name__ == "__main__":
    main()
