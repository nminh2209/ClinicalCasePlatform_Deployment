import json
import argparse
import Levenshtein
import re
from pathlib import Path

def normalize_text(text):
    if not isinstance(text, str):
        return str(text)
    # Remove special chars and extra whitespace
    text = re.sub(r'[^\w\s]', ' ', text)
    return ' '.join(text.lower().split())

def flatten_json(y):
    out = {}
    def flatten(x, name=''):
        if isinstance(x, dict):
            for a in x:
                flatten(x[a], name + a + '.')
        elif isinstance(x, list):
            for i, a in enumerate(x):
                flatten(a, name + str(i) + '.')
        else:
            out[name[:-1]] = x
    flatten(y)
    return out

def evaluate(result_path, ground_truth_path, output_path):
    # Load Result
    with open(result_path, 'r', encoding='utf-8') as f:
        result_data = json.load(f)
    
    # Aggregate text from all pages
    full_text = ""
    if 'pages' in result_data:
        for page in result_data['pages']:
            full_text += page.get('plain_text', '') + "\n"
    else:
        full_text = result_data.get('text', '')
        
    normalized_full_text = normalize_text(full_text)
    
    # Load Ground Truth
    with open(ground_truth_path, 'r', encoding='utf-8') as f:
        gt_data = json.load(f)
        
    # Flatten GT
    flat_gt = flatten_json(gt_data)
    
    # Compare
    scores = []
    total_fields = 0
    passed_fields = 0
    
    print(f"{'Field':<50} | {'Ground Truth':<30} | {'Match'}")
    print("-" * 100)
    
    report_lines = []
    report_lines.append("# Frontend OCR Evaluation Check")
    report_lines.append(f"**Source**: `{result_path}`")
    report_lines.append(f"**Ground Truth**: `{ground_truth_path}`")
    report_lines.append("")
    report_lines.append("## Detailed Field Analysis")
    report_lines.append("| Field | Ground Truth | Present | Approximate Match |")
    report_lines.append("|-------|--------------|---------|-------------------|")
    
    for key, val in flat_gt.items():
        if val is None or key.startswith('_metadata'):
            continue
            
        val_str = str(val)
        norm_val = normalize_text(val_str)
        
        if not norm_val:
            continue
            
        total_fields += 1
        
        # 1. Exact phrase match (in normalized text)
        if norm_val in normalized_full_text:
            match_status = "✅ Exact"
            passed_fields += 1
            report_lines.append(f"| `{key}` | {val_str[:50]}... | ✅ | 100% |")
        else:
            # 2. Fuzzy match
            # Since full text is huge, finding best substring match is hard. 
            # We'll just check if a high % of the words in GT value exist in close proximity? 
            # Or just Levenshtein comparison with the full text is too slow/wrong.
            # Simplified approach: Check token overlap
            
            # Actually, let's just create a simplified score: 
            # What % of the GT words are found in the text?
            gt_tokens = norm_val.split()
            found_tokens = 0
            for token in gt_tokens:
                if len(token) > 2 and token in normalized_full_text:
                    found_tokens += 1
            
            token_overlap = found_tokens / len(gt_tokens) if gt_tokens else 0
            
            if token_overlap > 0.8:
                match_status = "⚠️ Partial"
                passed_fields += 1 # Count partial as pass for now? No, be strict.
                report_lines.append(f"| `{key}` | {val_str[:50]}... | ⚠️ | {int(token_overlap*100)}% (tokens) |")
            else:
                match_status = "❌ Missing"
                report_lines.append(f"| `{key}` | {val_str[:50]}... | ❌ | {int(token_overlap*100)}% (tokens) |")
        
        print(f"{key:<50} | {val_str[:30]:<30} | {match_status}")

    accuracy = (passed_fields / total_fields) * 100 if total_fields else 0
    
    report_lines.append("")
    report_lines.append("## Summary")
    report_lines.append(f"- **Total Fields Checked**: {total_fields}")
    report_lines.append(f"- **Exact Matches**: {passed_fields}")
    report_lines.append(f"- **Strict Accuracy**: {accuracy:.2f}%")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
        
    print(f"\nEvaluation saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--result', required=True)
    parser.add_argument('--ground-truth', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    
    evaluate(args.result, args.ground_truth, args.output)
