#!/usr/bin/env python3
import json
from collections import defaultdict, Counter

# Load the dataset
print("Loading dataset...")
with open('dataset/StructEval_dataset.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total samples: {len(data)}\n")

# Analyze task_id patterns
task_id_analysis = defaultdict(list)

for item in data:
    task_id = item.get('task_id', '')
    task_name = item.get('task_name', 'unknown')
    input_type = item.get('input_type', '')
    output_type = item.get('output_type', '')
    rendering = item.get('rendering', False)

    task_id_analysis[task_name].append({
        'task_id': task_id,
        'input_type': input_type,
        'output_type': output_type,
        'rendering': rendering
    })

# Print task_id patterns for each task
print("=" * 100)
print("TASK ID PATTERN ANALYSIS")
print("=" * 100)

for task_name in sorted(task_id_analysis.keys()):
    items = task_id_analysis[task_name]
    print(f"\nTask: {task_name}")
    print(f"Count: {len(items)}")

    # Get first, last, and a few middle task_ids
    task_ids = [item['task_id'] for item in items]
    task_ids_sorted = sorted(task_ids)

    print(f"First task_id: {task_ids_sorted[0]}")
    if len(task_ids_sorted) > 1:
        print(f"Last task_id:  {task_ids_sorted[-1]}")

    if len(task_ids_sorted) > 5:
        print(f"Sample IDs: {task_ids_sorted[:5]} ...")
    else:
        print(f"All IDs: {task_ids_sorted}")

    # Analyze the pattern
    if items:
        first_item = items[0]
        print(f"Input type: {first_item['input_type']} -> Output type: {first_item['output_type']}")
        print(f"Rendering: {first_item['rendering']}")

    # Extract prefix pattern (first 2-4 digits)
    prefixes_2 = Counter(tid[:2] for tid in task_ids)
    prefixes_4 = Counter(tid[:4] for tid in task_ids)

    if len(prefixes_2) <= 3:
        print(f"2-digit prefixes: {dict(prefixes_2)}")
    if len(prefixes_4) <= 5:
        print(f"4-digit prefixes: {dict(prefixes_4)}")

# Analyze overall pattern
print("\n\n" + "=" * 100)
print("OVERALL PATTERN ANALYSIS")
print("=" * 100)

# Group by first 2 digits
prefix_2_groups = defaultdict(list)
for item in data:
    task_id = item.get('task_id', '')
    prefix = task_id[:2] if len(task_id) >= 2 else ''
    task_name = item.get('task_name', '')
    input_type = item.get('input_type', '')
    output_type = item.get('output_type', '')

    prefix_2_groups[prefix].append({
        'task_name': task_name,
        'input_type': input_type,
        'output_type': output_type,
        'task_id': task_id
    })

print("\nGrouping by first 2 digits of task_id:")
for prefix in sorted(prefix_2_groups.keys()):
    items = prefix_2_groups[prefix]
    print(f"\nPrefix '{prefix}': {len(items)} samples")

    # Get unique task names
    task_names = set(item['task_name'] for item in items)
    input_types = set(item['input_type'] for item in items)
    output_types = set(item['output_type'] for item in items)

    print(f"  Input types: {input_types}")
    print(f"  Output types: {output_types}")
    print(f"  Tasks: {task_names if len(task_names) <= 3 else f'{len(task_names)} different tasks'}")

    # Show a few example IDs
    example_ids = sorted(set(item['task_id'] for item in items))[:5]
    print(f"  Example IDs: {example_ids}")

# Try to decode the pattern
print("\n\n" + "=" * 100)
print("PATTERN HYPOTHESIS")
print("=" * 100)

# Create input/output type to code mapping
input_type_codes = defaultdict(set)
output_type_codes = defaultdict(set)

for item in data:
    task_id = item.get('task_id', '')
    input_type = item.get('input_type', '')
    output_type = item.get('output_type', '')

    if len(task_id) >= 2:
        input_type_codes[input_type].add(task_id[:2])
    if len(task_id) >= 4:
        output_type_codes[output_type].add(task_id[2:4])

print("\nInput Type -> First 2 digits mapping:")
for input_type in sorted(input_type_codes.keys()):
    codes = sorted(input_type_codes[input_type])
    print(f"  {input_type:15s} -> {codes}")

print("\nOutput Type -> Digits 3-4 mapping:")
for output_type in sorted(output_type_codes.keys()):
    codes = sorted(output_type_codes[output_type])
    print(f"  {output_type:15s} -> {codes}")

# Analyze last 2 digits
print("\n\nLast 2 digits analysis:")
last_2_counter = Counter(item.get('task_id', '')[-2:] for item in data)
print(f"Unique last 2-digit combinations: {len(last_2_counter)}")
print(f"Range: {min(last_2_counter.keys())} to {max(last_2_counter.keys())}")
print(f"Most common last 2 digits:")
for digits, count in last_2_counter.most_common(10):
    print(f"  {digits}: {count} times")
