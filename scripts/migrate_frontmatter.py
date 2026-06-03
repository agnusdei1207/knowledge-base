import os
import re
import yaml
import tomllib
from pathlib import Path

CONTENT_DIR = Path("/home/user/knowledgebase/content")

def clean_hugo_fields(data):
    """Remove Hugo/Zola specific keys that are not needed by Quartz v5."""
    hugo_keys = ["weight", "taxonomies", "sort_by", "insert_anchor_links", "render", "authors", "template"]
    for k in hugo_keys:
        if k in data:
            del data[k]
    return data

def extract_tags(data, relative_path):
    """Consolidate tags from various Hugo/Zola fields into a single list of tags."""
    tags = set()
    
    # 1. Check top-level tags
    if "tags" in data:
        t = data["tags"]
        if isinstance(t, list):
            tags.update(t)
        elif isinstance(t, str):
            tags.add(t)
            
    # 2. Check top-level categories
    if "categories" in data:
        c = data["categories"]
        if isinstance(c, list):
            tags.update(c)
        elif isinstance(c, str):
            tags.add(c)
            
    # 3. Check extra fields
    if "extra" in data and isinstance(data["extra"], dict):
        extra = data["extra"]
        if "categories" in extra:
            ec = extra["categories"]
            if isinstance(ec, list):
                tags.update(ec)
            elif isinstance(ec, str):
                tags.add(ec)
        if "category" in extra:
            ecat = extra["category"]
            if isinstance(ecat, list):
                tags.update(ecat)
            elif isinstance(ecat, str):
                tags.add(ecat)

    # 4. If no tags found, infer from directory structure
    if not tags:
        parent = relative_path.parent
        parts = parent.parts
        # If in study/studynote/03_network/...
        if len(parts) >= 3 and parts[0] == "study" and parts[1] == "studynote":
            cat = parts[2]
            # Strip number prefix like "03_"
            cat_clean = re.sub(r"^\d+_", "", cat)
            if cat_clean:
                tags.add(cat_clean)
        elif len(parts) >= 1:
            tags.add(parts[0])
        else:
            tags.add("general")

    # Clean up tags: filter out invalid tags like "_index.md", empty tags, etc.
    cleaned_tags = set()
    for tag in tags:
        tag_str = str(tag).strip()
        if tag_str and tag_str != "_index.md" and not tag_str.endswith(".md"):
            cleaned_tags.add(tag_str)

    return sorted(list(cleaned_tags))

def process_toml_file(filepath, content, relative_path, dry_run=True):
    match = re.match(r"^\+\+\+\r?\n(.*?)\r?\n\+\+\+\r?\n", content, re.DOTALL)
    if not match:
        return None
    
    toml_text = match.group(1)
    body_text = content[match.end():]
    
    try:
        data = tomllib.loads(toml_text)
    except Exception as e:
        print(f"Error parsing TOML in {relative_path}: {e}")
        return None
    
    # Extract kids_analogy and core_insights
    kids_analogy = None
    core_insights = None
    if "extra" in data and isinstance(data["extra"], dict):
        kids_analogy = data["extra"].get("kids_analogy")
        core_insights = data["extra"].get("core_insights")
    
    # Extract tags
    tags = extract_tags(data, relative_path)
    
    # Build clean yaml dict
    yaml_data = {}
    if "title" in data:
        yaml_data["title"] = data["title"]
    if "date" in data:
        yaml_data["date"] = str(data["date"])
    if "description" in data:
        yaml_data["description"] = data["description"]
    
    if tags:
        yaml_data["tags"] = tags
        
    # Clean Hugo keys
    yaml_data = clean_hugo_fields(yaml_data)
    
    # Generate frontmatter
    yaml_frontmatter = yaml.safe_dump(yaml_data, allow_unicode=True, default_flow_style=False, sort_keys=False)
    
    # Format new body text
    injected_blocks = []
    if kids_analogy:
        injected_blocks.append(f"> 🧸 **어린이를 위한 비유**\n> {kids_analogy.strip()}")
    if core_insights:
        if isinstance(core_insights, list):
            insights_md = "\n".join([f"> - {i.strip()}" for i in core_insights])
            injected_blocks.append(f"> 💡 **핵심 인사이트**\n{insights_md}")
        elif isinstance(core_insights, str):
            injected_blocks.append(f"> 💡 **핵심 인사이트**\n> {core_insights.strip()}")
            
    injected_text = ""
    if injected_blocks:
        injected_text = "\n" + "\n\n".join(injected_blocks) + "\n\n---"
        
    new_content = f"---\n{yaml_frontmatter.strip()}\n---\n{injected_text}{body_text}"
    return new_content

def process_no_frontmatter_file(filepath, content, relative_path, dry_run=True):
    # Try to find first H1 header in file
    h1_match = re.search(r"^\s*#\s+(.+)\r?\n", content)
    if h1_match and content.strip().startswith("#"):
        title = h1_match.group(1).strip()
        match_start = h1_match.start()
        match_end = h1_match.end()
        body_text = content[:match_start] + content[match_end:]
        body_text = body_text.lstrip()
    else:
        # Fallback to file name
        title = filepath.stem.replace("_", " ").title()
        title = re.sub(r"^\d+[\s_]+", "", title)
        body_text = content
        
    # Infer tags from path
    tags = extract_tags({}, relative_path)
        
    yaml_data = {
        "title": title,
    }
    if tags:
        yaml_data["tags"] = tags
    
    yaml_frontmatter = yaml.safe_dump(yaml_data, allow_unicode=True, default_flow_style=False, sort_keys=False)
    new_content = f"---\n{yaml_frontmatter.strip()}\n---\n\n{body_text}"
    return new_content

def process_yaml_file(filepath, content, relative_path, dry_run=True):
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", content, re.DOTALL)
    if not match:
        return None
    
    yaml_text = match.group(1)
    body_text = content[match.end():]
    
    try:
        data = yaml.safe_load(yaml_text)
    except Exception as e:
        print(f"Error parsing YAML in {relative_path}: {e}")
        return None
    
    if not isinstance(data, dict):
        return None
        
    # Extract tags just in case
    tags = extract_tags(data, relative_path)
    if tags:
        data["tags"] = tags
        
    # Clean Hugo keys
    data = clean_hugo_fields(data)
    
    # Generate new frontmatter
    yaml_frontmatter = yaml.safe_dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False)
    new_content = f"---\n{yaml_frontmatter.strip()}\n---\n{body_text}"
    return new_content

def main(dry_run=True):
    markdown_files = list(CONTENT_DIR.rglob("*.md"))
    print(f"Starting migration. Dry Run = {dry_run}")
    print(f"Found {len(markdown_files)} files.")
    
    toml_count = 0
    yaml_count = 0
    no_fm_count = 0
    
    for filepath in markdown_files:
        rel_path = filepath.relative_to(CONTENT_DIR)
        
        try:
            content = filepath.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            print(f"Failed to read {rel_path}: {e}")
            continue
            
        new_content = None
        
        if content.startswith("+++"):
            new_content = process_toml_file(filepath, content, rel_path, dry_run)
            toml_count += 1
        elif content.startswith("---"):
            new_content = process_yaml_file(filepath, content, rel_path, dry_run)
            yaml_count += 1
        else:
            new_content = process_no_frontmatter_file(filepath, content, rel_path, dry_run)
            no_fm_count += 1
            
        if new_content is not None and new_content != content:
            if dry_run:
                # Print sample output for validation
                if toml_count <= 2 or yaml_count <= 2 or no_fm_count <= 2:
                    print("="*80)
                    print(f"SAMPLE MIGRATION FOR: {rel_path}")
                    print("="*80)
                    print(new_content[:800])
                    print("...\n" + "="*80)
            else:
                try:
                    filepath.write_text(new_content, encoding="utf-8")
                except Exception as e:
                    print(f"Failed to write {rel_path}: {e}")

    print("\nSummary:")
    print(f"  Processed TOML (+++) files: {toml_count}")
    print(f"  Processed YAML (---) files: {yaml_count}")
    print(f"  Processed No-Frontmatter files: {no_fm_count}")

if __name__ == "__main__":
    import sys
    dry = True
    if len(sys.argv) > 1 and sys.argv[1] == "--write":
        dry = False
    main(dry_run=dry)
