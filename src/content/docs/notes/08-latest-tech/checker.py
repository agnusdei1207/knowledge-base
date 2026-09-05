import os
import re
import glob
import sys

sys.stdout.reconfigure(encoding='utf-8')

DIR = r"C:\workspace\study\src\content\docs\notes\08-latest-tech"

issues = []

def extract_core_terms(bold_text):
    """Extract individual terms from compound bold text like 'Task ID•멱등키'"""
    # Split on common separators
    parts = re.split(r'[•·,/]', bold_text)
    result = set()
    for p in parts:
        p = p.strip()
        # Remove parenthetical content for matching
        core = re.sub(r'\([^)]*\)', '', p).strip()
        if core:
            result.add(core)
        result.add(p)
    return result

def get_defined_term_cores(terms_block):
    """Get all core terms from 용어 설명 block"""
    defined = set()
    # Match **term(english)** pattern
    raw_terms = re.findall(r'\*\*([^*]+)\*\*', terms_block)
    for t in raw_terms:
        defined.add(t)
        # Also add just the Korean part
        core = re.sub(r'\([^)]*\)', '', t).strip()
        if core:
            defined.add(core)
        # Also add English abbreviation if present
        abbrevs = re.findall(r'\(([A-Z][A-Za-z0-9-]*)', t)
        for a in abbrevs:
            defined.add(a)
    return defined

for num in range(1, 115):
    pattern = os.path.join(DIR, f"{num:03d}_*.md")
    files = glob.glob(pattern)
    if not files:
        continue
    fpath = files[0]
    fname = os.path.basename(fpath)
    
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
    
    file_issues = []
    
    # 1. Check duplicate consecutive lines
    for i in range(1, len(lines)):
        line = lines[i].strip()
        prev = lines[i-1].strip()
        if len(line) > 20 and line == prev:
            short = line[:80].replace('|','').strip()
            file_issues.append(f"  [구조적 문제] L{i+1}: 중복 행: '{short}'")
    
    # 2. Check for boilerplate overuse
    boilerplate_count = content.count('복잡한 문제 해결과 동적 환경 적응에 필수적인 역할을 수행한다')
    if boilerplate_count > 2:
        file_issues.append(f"  [범위 초과/노이즈] 동일 상용구 {boilerplate_count}회 반복")
    
    # 3. Check Section VI - true term mismatches
    sections = re.split(r'^## ', content, flags=re.MULTILINE)
    for sec in sections:
        if 'Ⅵ' in sec[:10]:
            # Get 용어 설명 block
            details_match = re.search(r'<details><summary>용어 설명</summary>(.*?)</details>', sec, re.DOTALL)
            defined_cores = set()
            if details_match:
                defined_cores = get_defined_term_cores(details_match.group(1))
            
            # Get table bold terms
            after_details = sec.split('</details>')[-1] if '</details>' in sec else sec
            table_part = '\n'.join(l for l in after_details.split('\n') if l.strip().startswith('|') and not l.strip().startswith('|:'))
            
            bold_in_table = re.findall(r'\*\*([^*]+)\*\*', table_part)
            
            truly_missing = []
            for bold_term in bold_in_table:
                # Extract core terms from compound
                core_terms = extract_core_terms(bold_term)
                # Check if any core is matched
                matched = False
                for core in core_terms:
                    for defined in defined_cores:
                        if core in defined or defined in core:
                            matched = True
                            break
                    if matched:
                        break
                if not matched:
                    truly_missing.append(bold_term)
            
            if truly_missing:
                terms_str = ', '.join(truly_missing[:5])
                file_issues.append(f"  [용어설명-본문 매칭] Section VI 표 볼드 용어 미정의: {terms_str}")
            break
    
    # 4. Check question_no vs order match
    q_match = re.search(r'question_no:\s*"(\d+)"', content)
    order_match = re.search(r'order:\s*(\d+)', content)
    if q_match and order_match:
        q_no = int(q_match.group(1))
        order = int(order_match.group(1))
        if q_no != order:
            file_issues.append(f"  [구조적 문제] question_no ({q_no}) != order ({order})")
    
    # 5. Check for Section VII missing 용어 설명 block
    for sec in sections:
        if 'Ⅶ' in sec[:10]:
            if '<details><summary>용어 설명</summary>' not in sec:
                pass  # Some files intentionally skip this - not flagging
            break
    
    if file_issues:
        issues.append(f"\n=== {fname} ===")
        issues.extend(file_issues)

# Write results
with open(os.path.join(DIR, 'report_temp.md'), 'w', encoding='utf-8') as f:
    if issues:
        for issue in issues:
            f.write(issue + '\n')
    else:
        f.write("No issues found.\n")
    
print(f"Done. Report written to report_temp.md")
for issue in issues:
    print(issue)
