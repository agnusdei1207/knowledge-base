import os
import re
import yaml
from pathlib import Path
from collections import Counter

content_dir = Path("/home/user/knowledgebase/content")
markdown_files = list(content_dir.rglob("*.md"))

total_files = len(markdown_files)
no_frontmatter = []
hugo_fields_found = Counter()
hugo_field_files = []
no_title = []
invalid_yaml = []
all_keys = Counter()

# Hugo specific fields we want to clean or examine
HUGO_FIELDS = {"weight", "layout", "type", "url", "slug"}

for md_path in markdown_files:
    # Read file content
    try:
        content = md_path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        print(f"Error reading {md_path}: {e}")
        continue
    
    # Check for frontmatter
    # Frontmatter starts with --- at the very beginning of the file
    if not content.startswith("---"):
        no_frontmatter.append(md_path)
        continue
    
    # Find the closing ---
    # We look for \n---\n or \r\n---\r\n
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", content, re.DOTALL)
    if not match:
        no_frontmatter.append(md_path)
        continue
    
    fm_text = match.group(1)
    
    try:
        fm_data = yaml.safe_load(fm_text)
        if not isinstance(fm_data, dict):
            invalid_yaml.append((md_path, "Not a dictionary"))
            continue
    except Exception as e:
        invalid_yaml.append((md_path, str(e)))
        continue
    
    # Track keys
    for k in fm_data.keys():
        all_keys[k] += 1
        if k in HUGO_FIELDS:
            hugo_fields_found[k] += 1
            hugo_field_files.append((md_path, k))
            
    # Check title
    if "title" not in fm_data or not str(fm_data["title"]).strip():
        no_title.append(md_path)

print(f"Total Markdown Files: {total_files}")
print(f"Files without Frontmatter: {len(no_frontmatter)}")
print(f"Files with Invalid YAML Frontmatter: {len(invalid_yaml)}")
print(f"Files missing 'title' in Frontmatter: {len(no_title)}")
print("\nHugo Fields Counter:")
for field, count in hugo_fields_found.items():
    print(f"  {field}: {count}")

print("\nAll Frontmatter Keys Counter (Top 20):")
for k, count in all_keys.most_common(20):
    print(f"  {k}: {count}")

# Print sample files without frontmatter
if no_frontmatter:
    print(f"\nSample files without Frontmatter (showing up to 10):")
    for f in no_frontmatter[:10]:
        print(f"  {f.relative_to(content_dir)}")

# Print sample files with Hugo fields
if hugo_field_files:
    print(f"\nSample files with Hugo fields (showing up to 10):")
    for f, field in hugo_field_files[:10]:
        print(f"  {f.relative_to(content_dir)} (contains '{field}')")

# Print sample files missing title
if no_title:
    print(f"\nSample files missing title (showing up to 10):")
    for f in no_title[:10]:
        print(f"  {f.relative_to(content_dir)}")
