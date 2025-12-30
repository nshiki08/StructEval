#!/usr/bin/env python3
import json
from collections import Counter

# Load the dataset
print("Loading dataset...")
with open('dataset/StructEval_dataset.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total samples: {len(data)}")
print()

# Separate by rendering flag
renderable = []
nonrenderable = []

for item in data:
    if item.get('rendering', False):
        renderable.append(item)
    else:
        nonrenderable.append(item)

print(f"Renderable (rendering=True): {len(renderable)}")
print(f"Non-renderable (rendering=False): {len(nonrenderable)}")
print()

# Analyze task breakdown for renderable data
print("=" * 80)
print("RENDERABLE DATA (rendering=True) - Task Breakdown")
print("=" * 80)

task_counts_r = Counter()
for item in renderable:
    task = item.get('task_name', 'unknown')
    task_counts_r[task] += 1

print(f"\nTotal unique tasks: {len(task_counts_r)}")
print(f"Total samples: {len(renderable)}")
print("\nTask breakdown:")
for task, count in sorted(task_counts_r.items(), key=lambda x: -x[1]):
    percentage = (count / len(renderable)) * 100 if renderable else 0
    print(f"  {task}: {count} ({percentage:.1f}%)")

# Analyze input/output types for renderable
print("\nInput type distribution (Renderable):")
input_types_r = Counter(item.get('input_type', 'unknown') for item in renderable)
for itype, count in sorted(input_types_r.items(), key=lambda x: -x[1]):
    percentage = (count / len(renderable)) * 100 if renderable else 0
    print(f"  {itype}: {count} ({percentage:.1f}%)")

print("\nOutput type distribution (Renderable):")
output_types_r = Counter(item.get('output_type', 'unknown') for item in renderable)
for otype, count in sorted(output_types_r.items(), key=lambda x: -x[1]):
    percentage = (count / len(renderable)) * 100 if renderable else 0
    print(f"  {otype}: {count} ({percentage:.1f}%)")

# Analyze task breakdown for non-renderable data
print()
print("=" * 80)
print("NON-RENDERABLE DATA (rendering=False) - Task Breakdown")
print("=" * 80)

task_counts_nr = Counter()
for item in nonrenderable:
    task = item.get('task_name', 'unknown')
    task_counts_nr[task] += 1

print(f"\nTotal unique tasks: {len(task_counts_nr)}")
print(f"Total samples: {len(nonrenderable)}")
print("\nTask breakdown:")
for task, count in sorted(task_counts_nr.items(), key=lambda x: -x[1]):
    percentage = (count / len(nonrenderable)) * 100 if nonrenderable else 0
    print(f"  {task}: {count} ({percentage:.1f}%)")

# Analyze input/output types for non-renderable
print("\nInput type distribution (Non-renderable):")
input_types_nr = Counter(item.get('input_type', 'unknown') for item in nonrenderable)
for itype, count in sorted(input_types_nr.items(), key=lambda x: -x[1]):
    percentage = (count / len(nonrenderable)) * 100 if nonrenderable else 0
    print(f"  {itype}: {count} ({percentage:.1f}%)")

print("\nOutput type distribution (Non-renderable):")
output_types_nr = Counter(item.get('output_type', 'unknown') for item in nonrenderable)
for otype, count in sorted(output_types_nr.items(), key=lambda x: -x[1]):
    percentage = (count / len(nonrenderable)) * 100 if nonrenderable else 0
    print(f"  {otype}: {count} ({percentage:.1f}%)")

# Combined summary
print()
print("=" * 80)
print("OVERALL SUMMARY")
print("=" * 80)
all_tasks = set(task_counts_r.keys()) | set(task_counts_nr.keys())
print(f"\nTask comparison:")
print(f"{'Task':<40} {'Renderable':>15} {'Non-renderable':>15} {'Total':>10}")
print("-" * 85)
for task in sorted(all_tasks, key=lambda x: (task_counts_r.get(x, 0) + task_counts_nr.get(x, 0)), reverse=True):
    r_count = task_counts_r.get(task, 0)
    nr_count = task_counts_nr.get(task, 0)
    total = r_count + nr_count
    print(f"{task:<40} {r_count:>15} {nr_count:>15} {total:>10}")

print("-" * 85)
print(f"{'TOTAL':<40} {len(renderable):>15} {len(nonrenderable):>15} {len(data):>10}")

print()
print("=" * 80)
print("INPUT/OUTPUT TYPE SUMMARY")
print("=" * 80)
all_input_types = set(input_types_r.keys()) | set(input_types_nr.keys())
print(f"\nInput type comparison:")
print(f"{'Input Type':<30} {'Renderable':>15} {'Non-renderable':>15} {'Total':>10}")
print("-" * 75)
for itype in sorted(all_input_types):
    r_count = input_types_r.get(itype, 0)
    nr_count = input_types_nr.get(itype, 0)
    total = r_count + nr_count
    print(f"{itype:<30} {r_count:>15} {nr_count:>15} {total:>10}")

print()
all_output_types = set(output_types_r.keys()) | set(output_types_nr.keys())
print(f"Output type comparison:")
print(f"{'Output Type':<30} {'Renderable':>15} {'Non-renderable':>15} {'Total':>10}")
print("-" * 75)
for otype in sorted(all_output_types):
    r_count = output_types_r.get(otype, 0)
    nr_count = output_types_nr.get(otype, 0)
    total = r_count + nr_count
    print(f"{otype:<30} {r_count:>15} {nr_count:>15} {total:>10}")
