#!/usr/bin/env python3
import json
from collections import Counter, defaultdict
import statistics

# Load the dataset
print("Loading dataset...")
with open('dataset/StructEval_dataset.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total samples: {len(data)}")
print()

# Separate by rendering flag
renderable = [item for item in data if item.get('rendering', False)]
nonrenderable = [item for item in data if not item.get('rendering', False)]

print("=" * 80)
print("DETAILED ANALYSIS - RENDERABLE DATA")
print("=" * 80)

# Analyze each task in detail for renderable
task_details_r = defaultdict(lambda: {
    'count': 0,
    'samples': [],
    'vqa_question_count': [],
    'metric_count': [],
    'input_lengths': [],
    'example_query_lengths': []
})

for item in renderable:
    task = item.get('task_name', 'unknown')
    task_details_r[task]['count'] += 1
    task_details_r[task]['samples'].append(item)

    # VQA analysis
    vqa = item.get('VQA', [])
    if vqa:
        task_details_r[task]['vqa_question_count'].append(len(vqa))

    # Metric analysis
    metrics = item.get('raw_output_metric', [])
    if metrics:
        task_details_r[task]['metric_count'].append(len(metrics))

    # Length analysis
    query = item.get('query', '')
    task_details_r[task]['input_lengths'].append(len(query))

    query_example = item.get('query_example', '')
    task_details_r[task]['example_query_lengths'].append(len(query_example))

# Print detailed statistics for each renderable task
for task in sorted(task_details_r.keys(), key=lambda x: task_details_r[x]['count'], reverse=True):
    details = task_details_r[task]
    print(f"\n{'='*80}")
    print(f"Task: {task}")
    print(f"{'='*80}")
    print(f"Sample count: {details['count']}")

    if details['vqa_question_count']:
        print(f"\nVQA Questions per sample:")
        print(f"  Average: {statistics.mean(details['vqa_question_count']):.1f}")
        print(f"  Min: {min(details['vqa_question_count'])}")
        print(f"  Max: {max(details['vqa_question_count'])}")
        print(f"  Median: {statistics.median(details['vqa_question_count']):.1f}")

    if details['metric_count']:
        print(f"\nOutput metrics per sample:")
        print(f"  Average: {statistics.mean(details['metric_count']):.1f}")
        print(f"  Min: {min(details['metric_count'])}")
        print(f"  Max: {max(details['metric_count'])}")
        print(f"  Median: {statistics.median(details['metric_count']):.1f}")

    if details['input_lengths']:
        print(f"\nQuery length (characters):")
        print(f"  Average: {statistics.mean(details['input_lengths']):.0f}")
        print(f"  Min: {min(details['input_lengths'])}")
        print(f"  Max: {max(details['input_lengths'])}")

    # Show first sample
    sample = details['samples'][0]
    print(f"\nExample sample (task_id: {sample.get('task_id', 'N/A')}):")
    print(f"  Query (first 200 chars): {sample.get('query', '')[:200]}...")

    if sample.get('VQA'):
        print(f"\n  VQA Questions (first 3):")
        for i, vqa in enumerate(sample['VQA'][:3], 1):
            q = vqa.get('question', '')
            a = vqa.get('answer', '')
            print(f"    {i}. Q: {q}")
            print(f"       A: {a}")

    if sample.get('raw_output_metric'):
        metrics = sample['raw_output_metric']
        print(f"\n  Raw output metrics ({len(metrics)} total):")
        print(f"    {metrics[:10]}")
        if len(metrics) > 10:
            print(f"    ... and {len(metrics) - 10} more")

print("\n\n" + "=" * 80)
print("DETAILED ANALYSIS - NON-RENDERABLE DATA")
print("=" * 80)

# Analyze each task in detail for non-renderable
task_details_nr = defaultdict(lambda: {
    'count': 0,
    'samples': [],
    'metric_count': [],
    'input_lengths': [],
    'example_query_lengths': []
})

for item in nonrenderable:
    task = item.get('task_name', 'unknown')
    task_details_nr[task]['count'] += 1
    task_details_nr[task]['samples'].append(item)

    # Metric analysis
    metrics = item.get('raw_output_metric', [])
    if metrics:
        task_details_nr[task]['metric_count'].append(len(metrics))

    # Length analysis
    query = item.get('query', '')
    task_details_nr[task]['input_lengths'].append(len(query))

    query_example = item.get('query_example', '')
    task_details_nr[task]['example_query_lengths'].append(len(query_example))

# Print detailed statistics for each non-renderable task
for task in sorted(task_details_nr.keys()):
    details = task_details_nr[task]
    print(f"\n{'='*80}")
    print(f"Task: {task}")
    print(f"{'='*80}")
    print(f"Sample count: {details['count']}")

    # Non-renderable doesn't have VQA
    print(f"VQA: Not applicable (non-renderable)")

    if details['metric_count']:
        print(f"\nOutput metrics per sample:")
        print(f"  Average: {statistics.mean(details['metric_count']):.1f}")
        print(f"  Min: {min(details['metric_count'])}")
        print(f"  Max: {max(details['metric_count'])}")
        print(f"  Median: {statistics.median(details['metric_count']):.1f}")

    if details['input_lengths']:
        print(f"\nQuery length (characters):")
        print(f"  Average: {statistics.mean(details['input_lengths']):.0f}")
        print(f"  Min: {min(details['input_lengths'])}")
        print(f"  Max: {max(details['input_lengths'])}")

    # Show first sample
    sample = details['samples'][0]
    print(f"\nExample sample (task_id: {sample.get('task_id', 'N/A')}):")
    print(f"  Query (first 200 chars): {sample.get('query', '')[:200]}...")

    if sample.get('raw_output_metric'):
        metrics = sample['raw_output_metric']
        print(f"\n  Raw output metrics ({len(metrics)} total):")
        print(f"    {metrics[:10]}")
        if len(metrics) > 10:
            print(f"    ... and {len(metrics) - 10} more")

print("\n\n" + "=" * 80)
print("VQA PATTERN ANALYSIS (Renderable only)")
print("=" * 80)

# Analyze VQA question patterns
all_questions = []
question_types = Counter()
answer_types = Counter()

for item in renderable:
    vqa = item.get('VQA', [])
    for qa in vqa:
        question = qa.get('question', '')
        answer = qa.get('answer', '')
        all_questions.append(question)

        # Categorize question types by first word
        first_word = question.split()[0].lower() if question else ''
        question_types[first_word] += 1

        # Categorize answer types
        if answer.isdigit():
            answer_types['numeric'] += 1
        elif len(answer.split()) == 1:
            answer_types['single_word'] += 1
        elif len(answer.split()) <= 5:
            answer_types['short_phrase'] += 1
        else:
            answer_types['long_answer'] += 1

print(f"\nTotal VQA questions: {len(all_questions)}")
print(f"\nTop question starter words:")
for word, count in question_types.most_common(15):
    percentage = (count / len(all_questions)) * 100
    print(f"  {word}: {count} ({percentage:.1f}%)")

print(f"\nAnswer type distribution:")
for atype, count in sorted(answer_types.items(), key=lambda x: -x[1]):
    percentage = (count / len(all_questions)) * 100
    print(f"  {atype}: {count} ({percentage:.1f}%)")

print("\n" + "=" * 80)
print("METRIC ANALYSIS")
print("=" * 80)

# Analyze raw_output_metric patterns
all_metrics_r = []
all_metrics_nr = []

for item in renderable:
    all_metrics_r.extend(item.get('raw_output_metric', []))

for item in nonrenderable:
    all_metrics_nr.extend(item.get('raw_output_metric', []))

print(f"\nRenderable metrics:")
print(f"  Total metrics across all samples: {len(all_metrics_r)}")
print(f"  Unique metrics: {len(set(all_metrics_r))}")
print(f"  Average per sample: {len(all_metrics_r) / len(renderable):.1f}")

metric_counter_r = Counter(all_metrics_r)
print(f"\n  Top 20 most common metrics:")
for metric, count in metric_counter_r.most_common(20):
    print(f"    {metric}: {count}")

print(f"\nNon-renderable metrics:")
print(f"  Total metrics across all samples: {len(all_metrics_nr)}")
print(f"  Unique metrics: {len(set(all_metrics_nr))}")
print(f"  Average per sample: {len(all_metrics_nr) / len(nonrenderable):.1f}")

metric_counter_nr = Counter(all_metrics_nr)
print(f"\n  Top 20 most common metrics:")
for metric, count in metric_counter_nr.most_common(20):
    print(f"    {metric}: {count}")
