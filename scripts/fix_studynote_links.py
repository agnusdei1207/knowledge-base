import os
from pathlib import Path

CONTENT_DIR = Path("/home/user/knowledgebase/content")
markdown_files = list(CONTENT_DIR.rglob("*.md"))

print(f"Auditing and updating links in {len(markdown_files)} files...")

updated_count = 0

for filepath in markdown_files:
    try:
        content = filepath.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        print(f"Error reading {filepath.relative_to(CONTENT_DIR)}: {e}")
        continue
        
    original = content
    
    # Replace wiki links: [[study/studynote/ -> [[studynote/
    content = content.replace("[[study/studynote/", "[[studynote/")
    
    # Replace markdown links: (study/studynote/ -> (studynote/
    content = content.replace("(study/studynote/", "(studynote/")
    content = content.replace("/study/studynote/", "/studynote/")
    content = content.replace("study/studynote/", "studynote/") # just in case
    
    if content != original:
        try:
            filepath.write_text(content, encoding="utf-8")
            updated_count += 1
        except Exception as e:
            print(f"Error writing {filepath.relative_to(CONTENT_DIR)}: {e}")

print(f"Completed link updates. Updated {updated_count} files.")
