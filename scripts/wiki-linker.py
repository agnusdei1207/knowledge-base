#!/usr/bin/env python3
import os
import re
import sys
from pathlib import Path
import time

CONTENT_DIR = Path("/home/user/knowledgebase/content")
STUDYNOTE_DIR = CONTENT_DIR / "study/studynote"

def extract_keywords_from_title(title):
    title = re.sub(r'^\d+[\.\:]\s*', '', title)
    title = title.strip()
    
    keywords = []
    match = re.match(r'^([^(\[.]+)\s*[(\[]([^)]+)[)\]]', title)
    if match:
        k1 = match.group(1).strip()
        k2 = match.group(2).strip()
        if k1: keywords.append(k1)
        if k2: keywords.append(k2)
    else:
        if title:
            keywords.append(title)
            
    valid_keywords = []
    for k in keywords:
        k_clean = re.sub(r'[^a-zA-Z0-9가-힣\s_&-]', '', k).strip()
        if len(k_clean) >= 2:
            valid_keywords.append(k_clean)
            
    return valid_keywords

def build_keyword_map():
    keyword_map = {}
    print("Parsing files for keywords...")
    
    file_count = 0
    for root, _, files in os.walk(STUDYNOTE_DIR):
        for file in files:
            if not file.endswith(".md") or file == "_index.md" or file.startswith("."):
                continue
                
            file_path = Path(root) / file
            file_count += 1
            
            target_name = file_path.stem
            
            # 파일 이름 자체에서도 키워드 추출
            file_keyword = re.sub(r'^\d+_', '', target_name).replace('_', ' ').strip()
            if len(file_keyword) >= 3:
                keyword_map[file_keyword.lower()] = target_name
            
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                title_match = re.search(r'title\s*=\s*["\']([^"\']+)["\']', content)
                if title_match:
                    title = title_match.group(1)
                    kws = extract_keywords_from_title(title)
                    for kw in kws:
                        keyword_map[kw.lower()] = target_name
                        
            except Exception as e:
                pass
                
    print(f"Keyword map built with {len(keyword_map)} terms from {file_count} files.")
    return keyword_map

def apply_wiki_links(content, keyword_map, current_stem):
    placeholders = []
    
    def add_placeholder(match):
        placeholder = f"___PLACEHOLDER_{len(placeholders)}___"
        placeholders.append((placeholder, match.group(0)))
        return placeholder

    # 1. Frontmatter 및 코드 블럭 보호
    content = re.sub(r'^---.*?---', add_placeholder, content, flags=re.DOTALL)
    content = re.sub(r'^\+\+\+.*?\+\+\+', add_placeholder, content, flags=re.DOTALL)
    content = re.sub(r'```.*?```', add_placeholder, content, flags=re.DOTALL)
    content = re.sub(r'`[^`]+`', add_placeholder, content)
    content = re.sub(r'!\[[^\]]*\]\([^)]+\)', add_placeholder, content)
    content = re.sub(r'\[[^\]]+\]\([^)]+\)', add_placeholder, content)
    content = re.sub(r'\[\[[^\]]+\]\]', add_placeholder, content)
    
    self_targets = {current_stem.lower(), re.sub(r'^\d+_', '', current_stem).replace('_', ' ').strip().lower()}
    
    content_lower = content.lower()
    
    # 2. 본문에 등장하는 단어 토큰 추출
    words = re.findall(r'[a-zA-Z0-9가-힣_&-]+', content_lower)
    
    # 3. N-gram 추출 (1, 2, 3어절)
    candidates = set()
    n_words = len(words)
    for i in range(n_words):
        w1 = words[i]
        candidates.add(w1)
        
        if i < n_words - 1:
            w2 = words[i+1]
            candidates.add(w1 + ' ' + w2)
            
            if i < n_words - 2:
                w3 = words[i+2]
                candidates.add(w1 + ' ' + w2 + ' ' + w3)
                
    # 4. 해시 테이블 O(1) 조회로 실제 존재하는 키워드만 선별
    matched_kws = [c for c in candidates if c in keyword_map]
    
    # 키워드가 긴 것부터 정렬하여 부분 매치 방지
    matched_kws = sorted(list(set(matched_kws)), key=len, reverse=True)
    
    # 5. 선별된 대상들에 대해서만 1대1 정규식 치환 적용 (어마어마하게 빠름)
    for kw in matched_kws:
        target = keyword_map[kw]
        
        if target.lower() in self_targets:
            continue
            
        is_korean = re.search(r'[가-힣]', kw) is not None
        if not is_korean:
            pattern = re.compile(r'\b(' + re.escape(kw) + r')\b', re.IGNORECASE)
        else:
            pattern = re.compile(r'(?<![a-zA-Z0-9가-힣_\[])(' + re.escape(kw) + r')(?![\]])')
            
        def repl(match):
            matched_text = match.group(1)
            token = f"___WIKILINK_{len(placeholders)}___"
            placeholders.append((token, f"[[{target}|{matched_text}]]"))
            return token
            
        content = pattern.sub(repl, content)

    # 6. 토큰 역순 복원
    for placeholder, original in reversed(placeholders):
        content = content.replace(placeholder, original)
        
    return content

def main():
    start_time = time.time()
    print("🚀 Starting 4th-gen Lightning-Fast N-Gram Wiki Linker...")
    
    keyword_map = build_keyword_map()
    
    print("\nLinking documents...")
    file_count = 0
    modified_count = 0
    
    for root, _, files in os.walk(STUDYNOTE_DIR):
        for file in files:
            if not file.endswith(".md") or file == "_index.md" or file.startswith("."):
                continue
                
            file_path = Path(root) / file
            file_count += 1
            if file_count % 1000 == 0:
                print(f"  Processed {file_count} files...")
                
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                original_content = content
                new_content = apply_wiki_links(content, keyword_map, file_path.stem)
                
                if new_content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    modified_count += 1
                    
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                
    end_time = time.time()
    elapsed = end_time - start_time
    print(f"\n✨ Done! Processed {file_count} files. Linkified {modified_count} files.")
    print(f"⏱️ Total elapsed time: {elapsed:.2f} seconds.")

if __name__ == "__main__":
    main()
