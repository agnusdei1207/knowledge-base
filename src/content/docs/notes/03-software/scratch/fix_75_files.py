import os
import re
import datetime

# Directory path
dir_path = r"C:\workspace\study\src\content\docs\notes\03-software"

def update_date(content, time_offset):
    # RFC 3339 format
    base_time = datetime.datetime(2026, 9, 6, 0, 10, 0)
    new_time = base_time + datetime.timedelta(seconds=time_offset)
    new_time_str = new_time.strftime("%Y-%m-%dT%H:%M:%S+09:00")
    
    # Replace date field in frontmatter
    new_content = re.sub(
        r"^date:\s*.*",
        f"date: {new_time_str}",
        content,
        flags=re.MULTILINE
    )
    return new_content

def fix_headers(content):
    modified = False
    
    headers_map = [
        (r"^#+\s*(Ⅰ|I)\.\s*.*", "## Ⅰ. 개요"),
        (r"^#+\s*(Ⅱ|II)\.\s*.*", "## Ⅱ. 특징"),
        (r"^#+\s*(Ⅲ|III)\.\s*.*", "## Ⅲ. 구조 및 구성요소"),
        (r"^#+\s*(Ⅳ|IV)\.\s*.*", "## Ⅳ. 흐름도"),
        (r"^#+\s*(Ⅴ|V)\.\s*.*", "## Ⅴ. 종류 및 비교"),
        (r"^#+\s*(Ⅵ|VI)\.\s*.*", "## Ⅵ. 실무 고려사항 및 대책"),
        (r"^#+\s*(Ⅶ|VII)\.\s*.*", "## Ⅶ. 결론")
    ]
    
    new_content = content
    for pattern, replacement in headers_map:
        def repl_func(match):
            nonlocal modified
            original = match.group(0).strip()
            hash_prefix_match = re.match(r"^(#+)", original)
            hash_prefix = hash_prefix_match.group(1) if hash_prefix_match else "##"
            new_header = f"{hash_prefix} {replacement.split(' ', 1)[1]}"
            if original != new_header:
                modified = True
            return new_header
        
        new_content = re.sub(pattern, repl_func, new_content, flags=re.MULTILINE)
        
    return new_content, modified

def fix_section_3_table(content):
    modified = False
    parts = re.split(r"^(#+\s*Ⅲ\.\s*.*)$", content, flags=re.MULTILINE)
    if len(parts) > 2:
        sec_content = parts[2]
        table_header_pattern = re.compile(r"^\|(.*)\|\n\|([\s\-\|]+)\|$", re.MULTILINE)
        match = table_header_pattern.search(sec_content)
        if match:
            original_header = match.group(0)
            columns = original_header.split('\n')[0].strip('|').split('|')
            if len(columns) == 2 and ("구성요소" not in columns[0] or "책임" not in columns[1]):
                new_header = "| 구성요소 | 책임 |\n|---|---|"
                sec_content = sec_content.replace(original_header, new_header, 1)
                parts[2] = sec_content
                modified = True
        return "".join(parts), modified
    return content, modified

def fix_section_6_table(content):
    modified = False
    parts = re.split(r"^(#+\s*Ⅵ\.\s*.*)$", content, flags=re.MULTILINE)
    if len(parts) > 2:
        sec_content = parts[2]
        table_header_pattern = re.compile(r"^\|(.*)\|\n\|([\s\-\|]+)\|$", re.MULTILINE)
        match = table_header_pattern.search(sec_content)
        if match:
            original_header = match.group(0)
            columns = original_header.split('\n')[0].strip('|').split('|')
            if len(columns) == 3 and ("문제" not in columns[0] or "대책" not in columns[1] or "효과" not in columns[2]):
                new_header = "| 문제 | 대책 | 효과 |\n|---|---|---|"
                sec_content = sec_content.replace(original_header, new_header, 1)
                parts[2] = sec_content
                modified = True
        return "".join(parts), modified
    return content, modified

def fix_section_5_table(content):
    modified = False
    parts = re.split(r"^(#+\s*Ⅴ\.\s*.*)$", content, flags=re.MULTILINE)
    if len(parts) > 2:
        sec_content = parts[2]
        lines = sec_content.split('\n')
        table_start_idx = -1
        for i, line in enumerate(lines):
            if re.match(r"^\|.*\|.*\|", line):
                if i+1 < len(lines) and re.match(r"^\|[\s\-\|]+\|$", lines[i+1]):
                    table_start_idx = i
                    break
        
        if table_start_idx != -1:
            if table_start_idx + 4 < len(lines):
                row_3 = lines[table_start_idx + 4]
                if row_3.startswith('|'):
                    cells = row_3.split('|')
                    if len(cells) > 1:
                        first_cell = cells[1].strip()
                        if first_cell not in ["한계", ""]:
                            cells[1] = " 한계 "
                            lines[table_start_idx + 4] = "|".join(cells)
                            modified = True
            
            if table_start_idx + 2 < len(lines):
                row_1 = lines[table_start_idx + 2]
                if row_1.startswith('|'):
                    cells = row_1.split('|')
                    if len(cells) > 1:
                        first_cell = cells[1].strip()
                        if first_cell not in ["적용 기준", ""]:
                            cells[1] = " 적용 기준 "
                            lines[table_start_idx + 2] = "|".join(cells)
                            modified = True
                            
            if table_start_idx + 3 < len(lines):
                row_2 = lines[table_start_idx + 3]
                if row_2.startswith('|'):
                    cells = row_2.split('|')
                    if len(cells) > 1:
                        first_cell = cells[1].strip()
                        if first_cell not in ["핵심 특징", ""]:
                            cells[1] = " 핵심 특징 "
                            lines[table_start_idx + 3] = "|".join(cells)
                            modified = True
                            
        if modified:
            parts[2] = '\n'.join(lines)
            return "".join(parts), modified

    return content, modified

def process_files():
    import glob
    
    files = glob.glob(os.path.join(dir_path, "*.md"))
    files.sort()
    
    target_files = []
    for f in files:
        basename = os.path.basename(f)
        if basename == "index.md": continue
        try:
            num = int(basename.split('_')[0])
            if 155 <= num <= 229:
                target_files.append(f)
        except ValueError:
            pass
            
    print(f"Total files to process: {len(target_files)}")
    
    modified_count = 0
    passed_count = 0
    modifications = {}
    
    time_offset = 0
    
    for f in target_files:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
            
        c1, m1 = fix_headers(content)
        c2, m2 = fix_section_3_table(c1)
        c3, m3 = fix_section_6_table(c2)
        c4, m4 = fix_section_5_table(c3)
        
        is_modified = m1 or m2 or m3 or m4
        
        if is_modified:
            final_content = update_date(c4, time_offset)
            with open(f, 'w', encoding='utf-8') as file:
                file.write(final_content)
                
            modified_count += 1
            reasons = []
            if m1: reasons.append("Fixed section headers")
            if m2: reasons.append("Fixed Section III table headers")
            if m3: reasons.append("Fixed Section VI table headers")
            if m4: reasons.append("Fixed Section V comparison table rows")
            
            modifications[os.path.basename(f)] = ", ".join(reasons)
        else:
            passed_count += 1
            
        time_offset += 1
            
    print(f"Total audited: {len(target_files)}")
    print(f"Files modified: {modified_count}")
    print(f"Files passed: {passed_count}")
    
    print("Modifications:")
    for k, v in modifications.items():
        print(f" - {k}: {v}")

if __name__ == "__main__":
    process_files()
