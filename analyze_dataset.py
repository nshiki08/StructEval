#!/usr/bin/env python3
import json
from collections import defaultdict, Counter

# Load the dataset
print("Loading dataset...")
with open('dataset/StructEval_dataset.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total samples: {len(data)}")
print()

# Separate by render flag
renderable = []
nonrenderable = []

for item in data:
    if item.get('render', False):
        renderable.append(item)
    else:
        nonrenderable.append(item)

print(f"Renderable (render=true): {len(renderable)}")
print(f"Non-renderable (render=false): {len(nonrenderable)}")
print()

# Analyze task breakdown for renderable data
print("=" * 80)
print("RENDERABLE DATA (render=true) - Task Breakdown")
print("=" * 80)

task_counts_r = Counter()
for item in renderable:
    task = item.get('task', 'unknown')
    task_counts_r[task] += 1

print(f"\nTotal tasks: {len(task_counts_r)}")
print(f"Total samples: {len(renderable)}")
print("\nTask breakdown:")
for task, count in sorted(task_counts_r.items()):
    percentage = (count / len(renderable)) * 100
    print(f"  {task}: {count} ({percentage:.1f}%)")

# Analyze task breakdown for non-renderable data
print()
print("=" * 80)
print("NON-RENDERABLE DATA (render=false) - Task Breakdown")
print("=" * 80)

task_counts_nr = Counter()
for item in nonrenderable:
    task = item.get('task', 'unknown')
    task_counts_nr[task] += 1

print(f"\nTotal tasks: {len(task_counts_nr)}")
print(f"Total samples: {len(nonrenderable)}")
print("\nTask breakdown:")
for task, count in sorted(task_counts_nr.items()):
    percentage = (count / len(nonrenderable)) * 100
    print(f"  {task}: {count} ({percentage:.1f}%)")

# Combined summary
print()
print("=" * 80)
print("OVERALL SUMMARY")
print("=" * 80)
all_tasks = set(task_counts_r.keys()) | set(task_counts_nr.keys())
print(f"\nTask comparison:")
print(f"{'Task':<40} {'Renderable':>15} {'Non-renderable':>15} {'Total':>10}")
print("-" * 85)
for task in sorted(all_tasks):
    r_count = task_counts_r.get(task, 0)
    nr_count = task_counts_nr.get(task, 0)
    total = r_count + nr_count
    print(f"{task:<40} {r_count:>15} {nr_count:>15} {total:>10}")

print("-" * 85)
print(f"{'TOTAL':<40} {len(renderable):>15} {len(nonrenderable):>15} {len(data):>10}")
