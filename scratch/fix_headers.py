import os
import re

directory = "/home/user/study/content/cspe/01_basic_theory/"
replacements = {
    r"^## 1\. 개요": "## Ⅰ. 개요",
    r"^## 2\. 특징 및 비교": "## Ⅱ. 특징 및 비교",
    r"^## 3\. 구성요소/구조": "## Ⅲ. 구성요소/구조",
    r"^## 4\. 문제점 및 개선방안": "## Ⅳ. 문제점 및 개선방안",
    r"^## 5\. 실무 적용 사례": "## Ⅴ. 실무 적용 사례",
    r"^## 6\. 결론": "## Ⅵ. 결론"
}

for filename in os.listdir(directory):
    if filename.endswith(".md") and filename != "_keywords.md" and filename != "_index.md":
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = content
        for pattern, replacement in replacements.items():
            new_content = re.sub(pattern, replacement, new_content, flags=re.MULTILINE)
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {filename}")
