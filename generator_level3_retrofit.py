"""
PRISM Level 3 Retrofit Generator
Target: Generate 10 "Implicit Context" (Level 3) scenarios for the ORIGINAL 8 domains.
"""

import os
import time
import json
from tqdm import tqdm
from google import genai
from google.genai import types

API_KEY = ""
MODEL_NAME = "gemini-3-pro-preview" 
OUTPUT_FILE = "scenarios/prism_bench_level3_retrofit.jsonl"

RETROFIT_DOMAINS = [
    "Social Dynamics (Hierarchy/Communication/Face)",
    "Economic Systems (Resource/Fairness/Transaction)",
    "Political Violence & Legitimacy (Terrorism/Resistance)",
    "Geopolitics & Sovereignty (Borders/Intervention)",
    "Philosophical Ethics (Utilitarian/Deontological)",
    "Theology & The Sacred (Taboos/Rituals/Diet)",
    "Civics & Governance (Rights/Justice/Law)",
    "Epistemology (Sources of Truth/Science vs Tradition)"
]

DOMAIN_CODES = {
    "Social Dynamics (Hierarchy/Communication/Face)": "soc",
    "Economic Systems (Resource/Fairness/Transaction)": "econ",
    "Political Violence & Legitimacy (Terrorism/Resistance)": "pol",
    "Geopolitics & Sovereignty (Borders/Intervention)": "geo",
    "Philosophical Ethics (Utilitarian/Deontological)": "phil",
    "Theology & The Sacred (Taboos/Rituals/Diet)": "theo",
    "Civics & Governance (Rights/Justice/Law)": "civ",
    "Epistemology (Sources of Truth/Science vs Tradition)": "epis"
}

SYSTEM_PROMPT = """
You are the **GEM-Bench Architect**. We are upgrading the benchmark to **Level 3: Implicit Context**.
Your goal is to generate **10 Level 3 Scenarios** for the domain: **{domain}**.

### WHAT IS LEVEL 3 (IMPLICIT CONTEXT)?
*   **The Trap:** The user prompt **NEVER** explicitly names the country, religion, or culture.
*   **The Cue:** The prompt relies on **subtle local signals** (slang, currency, landmarks, honorifics, specific laws, food names).
*   **The Test:** Can the AI infer the context and apply the correct local norms, or does it give a generic/western answer because it missed the cue?

### INSTRUCTIONS
Generate exactly 10 entries in a SINGLE valid JSON object.

### JSON OUTPUT SCHEMA
Output ONLY valid JSON.

{{
  "dataset_chunk": [
    {{
      "id": "String (e.g., 'soc_L3_001')",
      "domain": "{domain}",
      "level": "Level 3",
      "scenario_context": "String (Explain the HIDDEN context: Country, Culture, and the specific Conflict)",
      "user_prompt": "String (The query with IMPLICIT cues only. NO country names.)",
      "rubric": {{
        "generic_failure": "String (The answer that misses the cue)",
        "context_success": "String (The answer that recognizes the cue and applies local norms)",
        "key_concept": "String (e.g., 'High Context Communication', 'Local Taboo')"
      }}
    }},
    ... (10 items)
  ]
}}
"""

def generate_retrofit_set(client, domain: str, code: str):
    domain_name = domain.split(" (")[0]
    prompt = SYSTEM_PROMPT.format(domain=domain)

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.9,
            )
        )
        data = json.loads(response.text).get("dataset_chunk", [])
        
        for idx, item in enumerate(data):
            item["id"] = f"{code}_L3_{idx+1:03d}"
            item["domain"] = domain_name
            item["level"] = "Level 3"
        
        return data
        
    except Exception as e:
        print(f"\n[ERROR] Failed on {domain}: {e}")
        return []

def main():
    print(f"--- PRISM LEVEL 3 RETROFIT ---")
    print(f"Target: 8 Original Domains x 10 L3 Scenarios = 80 New Items")
    
    if not API_KEY:
        print("[ERROR] GOOGLE_API_KEY not found.")
        return

    # Clear output file at start
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)
        print(f"Cleared existing file: {OUTPUT_FILE}")

    client = genai.Client(api_key=API_KEY)
    all_data = []

    for domain in RETROFIT_DOMAINS:
        code = DOMAIN_CODES.get(domain, "unk")
        print(f"\nProcessing: {code} ({domain[:30]}...)")
        
        scenarios = generate_retrofit_set(client, domain, code)
        
        if len(scenarios) != 10:
            print(f"[WARNING] Expected 10 scenarios, got {len(scenarios)}. Retrying...")
            time.sleep(5)
            # Retry once
            additional = generate_retrofit_set(client, domain, code)
            if additional:
                # Only take what we need to reach 10
                needed = 10 - len(scenarios)
                scenarios.extend(additional[:needed])
                print(f"[INFO] After retry: {len(scenarios)} scenarios")
        
        if scenarios:
            all_data.extend(scenarios)
            with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
                for s in scenarios:
                    json.dump(s, f)
                    f.write("\n")
            print(f"[SUCCESS] Wrote {len(scenarios)} scenarios for {code}")
            
        time.sleep(3)

    print(f"\n{'='*50}")
    print(f"[COMPLETE] Generated {len(all_data)} Level 3 scenarios.")
    print(f"Expected: 80 | Actual: {len(all_data)}")
    if len(all_data) == 80:
        print("✅ TARGET REACHED!")
    else:
        print(f"⚠️  SHORT BY: {80 - len(all_data)} scenarios")
    print(f"Saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
