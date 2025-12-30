#!/usr/bin/env python3
import json
from collections import Counter

# Load the dataset
print("Loading dataset...")
with open('dataset/StructEval_dataset.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total samples: {len(data)}")
print()

# Check the structure of the first few items
print("=" * 80)
print("Sample data structure (first item):")
print("=" * 80)
if data:
    first_item = data[0]
    print(f"Keys: {list(first_item.keys())}")
    print()
    for key, value in first_item.items():
        if isinstance(value, str) and len(value) > 100:
            print(f"{key}: {value[:100]}...")
        else:
            print(f"{key}: {value}")
    print()

# Count all unique keys across all items
all_keys = set()
for item in data:
    all_keys.update(item.keys())
print(f"All unique keys in dataset: {sorted(all_keys)}")
print()

# Check for 'render' field
render_counts = Counter()
for item in data:
    render_counts[item.get('render', None)] += 1

print("Render field distribution:")
for render_val, count in render_counts.items():
    print(f"  render={render_val}: {count}")
print()

# Check for section/category fields
possible_section_fields = ['section', 'category', 'type', 'task_type', 'domain', 'difficulty']
for field in possible_section_fields:
    values = Counter()
    for item in data:
        if field in item:
            values[item[field]] += 1

    if values:
        print(f"\n{field.upper()} distribution:")
        for val, count in sorted(values.items()):
            percentage = (count / len(data)) * 100
            print(f"  {val}: {count} ({percentage:.1f}%)")
