import csv
import os
import yaml
from datetime import datetime
from pathlib import Path

# --------------------------------------------------------------
# 1. Load Reference Ranges from YAML
# --------------------------------------------------------------
def load_rules(rules_dir="data/nutrition/rules"):
    rules = {}
    rules_path = Path(rules_dir)
    for yaml_file in rules_path.rglob("*.yaml"):
        with open(yaml_file, 'r') as f:
            try:
                data = yaml.safe_load(f)
                if data and 'name' in data:
                    # Store by name and also by biomarker if available
                    rules[data['name'].lower()] = data
                    
                    # Handle synonyms
                    if 'synonyms' in data and isinstance(data['synonyms'], list):
                        for syn in data['synonyms']:
                            rules[syn.lower()] = data
                    
                    if 'biomarker' in data:
                        # Handle cases where biomarker might be a list or have aliases
                        if isinstance(data['biomarker'], str):
                            rules[data['biomarker'].lower()] = data
                        elif isinstance(data['biomarker'], list):
                            for bm in data['biomarker']:
                                rules[bm.lower()] = data
            except yaml.YAMLError as exc:
                print(f"Error loading {yaml_file}: {exc}")
    return rules

# --------------------------------------------------------------
# 2. Core analysis function
# --------------------------------------------------------------
def analyze_sample(sample_row, rules):
    """
    sample_row - dict with 'test_name', 'value', 'unit'
    rules - loaded YAML rules
    returns analysis result
    """
    test_name = sample_row['test_name']
    value = float(sample_row['value'])
    unit = sample_row['unit']
    
    rule = rules.get(test_name.lower())
    
    if not rule:
        return {
            "test_name": test_name,
            "value": value,
            "unit": unit,
            "status": "UNKNOWN",
            "message": "No reference rule found for this test.",
            "recommendation": ""
        }

    thresholds = rule.get('thresholds', {})
    recs = rule.get('recommendations', {})
    status = "NORMAL"
    message = ""
    recommendation = recs.get('normal', "Levels are within normal range.")

    # Logic to handle different YAML structures
    # Structure A: deficient: { value: X, unit: Y }, normal: { range: [A, B] }
    # Structure B: deficient: X, insufficient: Y, optimal: [A, B]
    
    # Check for deficiency first
    def_data = thresholds.get('deficient')
    if def_data:
        if isinstance(def_data, dict):
            if value < def_data.get('value', 0):
                status = "LOW"
                recommendation = recs.get('deficient', "")
        elif isinstance(def_data, (int, float)):
            if value < def_data:
                status = "LOW"
                recommendation = recs.get('deficient', "")

    # Check for insufficiency
    ins_data = thresholds.get('insufficient')
    if ins_data and status == "NORMAL":
        if isinstance(ins_data, (int, float)):
            if value < ins_data:
                status = "INSUFFICIENT"
                recommendation = recs.get('insufficient', "")

    # Check for high/toxic
    toxic_data = thresholds.get('toxic')
    if toxic_data:
        if isinstance(toxic_data, (int, float)):
            if value > toxic_data:
                status = "TOXIC"
                recommendation = recs.get('toxic', "")
    
    high_data = thresholds.get('high')
    if high_data and status == "NORMAL":
        if isinstance(high_data, dict):
            if value > high_data.get('value', 999999):
                status = "HIGH"
                recommendation = recs.get('high', "")
        elif isinstance(high_data, (int, float)):
            if value > high_data:
                status = "HIGH"
                recommendation = recs.get('high', "")

    return {
        "test_name": test_name,
        "value": value,
        "unit": unit,
        "status": status,
        "message": f"{rule.get('name')} ({rule.get('biomarker', '')})",
        "recommendation": recommendation,
        "functions": rule.get('functions', [])
    }

# --------------------------------------------------------------
# 3. Main execution
# --------------------------------------------------------------
if __name__ == "__main__":
    rules = load_rules()
    sample_path = "data/samples/example_blood_test.csv"
    
    if not os.path.exists(sample_path):
        print(f"Error: {sample_path} not found.")
        exit(1)

    reports = []
    with open(sample_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            reports.append(analyze_sample(row, rules))

    # ---------- pretty printing ----------
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"\n--- Nutrient‑hint report ({now}) ---\n")
    
    for report in reports:
        status_str = report['status']
        color_start = ""
        color_end = ""
        if status_str in ["LOW", "INSUFFICIENT", "TOXIC", "HIGH"]:
            color_start = "\033[91m" # Red
            color_end = "\033[0m"
        elif status_str == "NORMAL":
            color_start = "\033[92m" # Green
            color_end = "\033[0m"

        print(f"{report['test_name']:15}: {report['value']:6.2f} {report['unit']:<6} → {color_start}{status_str}{color_end}")
        if report['status'] != "NORMAL" and report['status'] != "UNKNOWN":
            print(f"  [!] {report['recommendation']}")
            if report.get('functions'):
                print(f"  [i] Key Functions: {', '.join(report['functions'][:2])}...")

    print("\n--- Summary ---")
    concerns = [r for r in reports if r['status'] not in ["NORMAL", "UNKNOWN"]]
    if concerns:
        print(f"Detected {len(concerns)} potential nutritional concerns.")
    else:
        print("No nutritional concerns detected based on the available rules.")
