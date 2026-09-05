import os
import re
import json
from datetime import datetime, timedelta

DIR = r"C:\workspace\study\src\content\docs\notes\02-hardware"

# Section titles mapping
SECTION_MAP = {
    "Ⅰ": "Ⅰ. 개요",
    "Ⅱ": "Ⅱ. 특징",
    "Ⅲ": "Ⅲ. 구조 및 구성요소",
    "Ⅳ": "Ⅳ. 흐름도",
    "Ⅴ": "Ⅴ. 종류 및 비교",
    "Ⅵ": "Ⅵ. 실무 고려사항 및 대책",
    "Ⅶ": "Ⅶ. 결론"
}

def check_bold_terms_bidirectional(content):
    # This is a basic check.
    # Extract terms in <details><summary>용어 설명</summary>...
    details_pattern = re.compile(r"<details>\s*<summary>용어 설명</summary>(.*?)</details>", re.DOTALL)
    details_match = details_pattern.search(content)
    
    defined_terms = set()
    if details_match:
        details_text = details_match.group(1)
        # Find all **term** in the details text
        for m in re.finditer(r"\*\*(.*?)\*\*", details_text):
            defined_terms.add(m.group(1).strip())
            
    # Extract terms in Ⅰ~Ⅶ sections
    main_pattern = re.compile(r"(Ⅰ\..*)", re.DOTALL)
    main_match = main_pattern.search(content)
    
    used_terms = set()
    if main_match:
        main_text = main_match.group(1)
        # Exclude the details block from main text search to avoid double counting
        if details_match:
            main_text = main_text.replace(details_match.group(0), "")
        for m in re.finditer(r"\*\*(.*?)\*\*", main_text):
            used_terms.add(m.group(1).strip())
            
    missing_in_details = used_terms - defined_terms
    missing_in_main = defined_terms - used_terms
    
    return missing_in_details, missing_in_main

def process_file(filepath, time_offset):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    modified = False
    reasons = []

    # 1. Fix Section Headers
    for numeral, correct_title in SECTION_MAP.items():
        # Match e.g. "Ⅲ. 회로 구성" or "### Ⅲ. 회로 구성"
        pattern = re.compile(rf"^(#*\s*){numeral}\.\s+.*$", re.MULTILINE)
        
        def header_repl(m):
            nonlocal modified
            old = m.group(0)
            new = f"{m.group(1)}{correct_title}"
            if old != new:
                modified = True
                if f"Fixed header {numeral}" not in reasons:
                    reasons.append(f"Fixed header {numeral}")
            return new
            
        content = pattern.sub(header_repl, content)

    # 2. Fix Ⅵ 실무 고려사항 table headers
    vi_idx = content.find("Ⅵ. 실무 고려사항 및 대책")
    vii_idx = content.find("Ⅶ. 결론")
    if vi_idx != -1:
        end_idx = vii_idx if vii_idx != -1 else len(content)
        vi_section = content[vi_idx:end_idx]
        
        table_match = re.search(r"\|(.*)\|(.*)\|(.*)\|\n\|[-\s]*\|[-\s]*\|[-\s]*\|", vi_section)
        if table_match:
            old_header = table_match.group(0)
            if "문제" not in old_header or "대책" not in old_header or "효과" not in old_header:
                new_header = "| 문제 | 대책 | 효과 |\n|---|---|---|"
                content = content[:vi_idx] + vi_section.replace(old_header, new_header, 1) + content[end_idx:]
                modified = True
                reasons.append("Fixed VI table header")

    # 3. Fix Ⅲ 구성요소 표
    iii_idx = content.find("Ⅲ. 구조 및 구성요소")
    iv_idx = content.find("Ⅳ. 흐름도")
    if iii_idx != -1:
        end_idx = iv_idx if iv_idx != -1 else len(content)
        iii_section = content[iii_idx:end_idx]
        
        table_match = re.search(r"\|(.*)\|(.*)\|\n\|[-\s]*\|[-\s]*\|", iii_section)
        if table_match:
            old_header = table_match.group(0)
            if "구성요소" not in old_header or "책임" not in old_header:
                new_header = "| 구성요소 | 책임 |\n|---|---|"
                content = content[:iii_idx] + iii_section.replace(old_header, new_header, 1) + content[end_idx:]
                modified = True
                reasons.append("Fixed III table header")

    # 4. Check V table header
    v_idx = content.find("Ⅴ. 종류 및 비교")
    vi_idx2 = content.find("Ⅵ. 실무 고려사항 및 대책")
    if v_idx != -1:
        end_idx2 = vi_idx2 if vi_idx2 != -1 else len(content)
        v_section = content[v_idx:end_idx2]
        
        # Look for table where the rows might be wrong
        table_match = re.search(r"\|(.*)\|(.*)\|(.*)\|\n\|[-\s]*\|[-\s]*\|[-\s]*\|\n\|([^|]+)\|", v_section)
        if table_match:
            row1_header = table_match.group(4).strip()
            if row1_header != "적용 기준":
                reasons.append("Review V table rows (needs '적용 기준', '핵심 특징', '한계')")

    missing_in_details, missing_in_main = check_bold_terms_bidirectional(content)
    if missing_in_details:
        reasons.append(f"Review needed: Terms in main missing from details: {list(missing_in_details)}")
    if missing_in_main:
        reasons.append(f"Review needed: Terms in details missing from main: {list(missing_in_main)}")

    # 5. Update date if modified
    if modified:
        dt = datetime.fromisoformat("2026-09-06T00:10:00+09:00") + timedelta(seconds=time_offset)
        new_date = dt.strftime("%Y-%m-%dT%H:%M:%S+09:00")
        
        content = re.sub(r"^date:\s*.*$", f"date: {new_date}", content, flags=re.MULTILINE)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    return modified, reasons

def main():
    files = [f for f in os.listdir(DIR) if f.endswith('.md') and f != 'index.md' and f != 'audit.py']
    files.sort()
    
    results = {
        "total": len(files),
        "modified": [],
        "passed": [],
        "review_needed": []
    }
    
    offset = 0
    for f in files:
        filepath = os.path.join(DIR, f)
        try:
            modified, reasons = process_file(filepath, offset)
            
            # Identify if the reasons contain "Review needed" or "Review V"
            review_reasons = [r for r in reasons if "Review" in r]
            mod_reasons = [r for r in reasons if "Review" not in r]
            
            if modified:
                offset += 1
                results["modified"].append({"file": f, "reasons": mod_reasons})
                if review_reasons:
                    results["review_needed"].append({"file": f, "reasons": review_reasons})
            else:
                if review_reasons:
                    results["review_needed"].append({"file": f, "reasons": review_reasons})
                else:
                    results["passed"].append(f)
                    
        except Exception as e:
            results["review_needed"].append({"file": f, "error": str(e)})

    with open(os.path.join(DIR, 'audit_report.json'), 'w', encoding='utf-8') as rf:
        json.dump(results, rf, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
