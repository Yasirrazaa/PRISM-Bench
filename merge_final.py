import json
import os

def merge_datasets():
    print("--- PRISM Dataset Merger (Final v2.1) ---")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    scenarios_dir = os.path.join(base_dir, "scenarios")
    
    files = [
        os.path.join(scenarios_dir, "prism_bench_320.jsonl"),
        os.path.join(scenarios_dir, "prism_bench_new_domains_250.jsonl"),
        os.path.join(scenarios_dir, "prism_bench_level3_retrofit.jsonl"),
    ]
    
    output_file = os.path.join(scenarios_dir, "prism_bench_final_submission.jsonl")
    total_count = 0
    ids = set()
    
    os.makedirs(scenarios_dir, exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as outfile:
        for file_path in files:
            if not os.path.exists(file_path):
                print(f"[WARN] File not found: {file_path}")
                continue
                
            print(f"Processing {os.path.basename(file_path)}...")
            with open(file_path, "r", encoding="utf-8") as infile:
                for line in infile:
                    try:
                        data = json.loads(line)
                        if data["id"] in ids:
                            print(f"Duplicate ID found: {data['id']}, skipping...")
                            continue
                            
                        ids.add(data["id"])
                        json.dump(data, outfile)
                        outfile.write("\n")
                        total_count += 1
                    except json.JSONDecodeError:
                        print("Skipping invalid JSON line")

    print(f"--- Done ---")
    print(f"Total Unique Scenarios: {total_count}")
    print(f"Saved to: {output_file}")
    
    if total_count >= 650:
        print("✅ SUCCESS: Target count (650) reached/exceeded.")
    else:
        print(f"⚠️  WARNING: Count {total_count} is below target 650.")

if __name__ == "__main__":
    merge_datasets()
