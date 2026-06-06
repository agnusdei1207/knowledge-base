#!/usr/bin/env python3
"""
Fix _index.md titles under studynote by deriving proper titles from folder names.
Folder name format: NN_word_word_word -> "Word Word Word"
"""

import os
import re

BASE = "/home/user/study/content/studynote"

# Map folder name -> proper display title
def folder_to_title(folder_name: str) -> str:
    """Convert snake_case folder name (with leading number) to Title Case."""
    # Remove leading number prefix: "01_basic_electronics_logic" -> "basic_electronics_logic"
    parts = folder_name.split("_")
    # Skip leading numeric part(s)
    start = 0
    for i, p in enumerate(parts):
        if p.isdigit():
            start = i + 1
        else:
            break
    words = parts[start:]
    # Title case each word, with some abbreviation overrides
    abbr = {"ai", "iot", "isa", "os", "cpu", "gpu", "io", "ict", "sre", "devops", "fpga", "alu"}
    result = []
    for w in words:
        if w.lower() in abbr:
            result.append(w.upper())
        else:
            result.append(w.capitalize())
    return " ".join(result)

# Top-level subject folder titles (more curated)
SUBJECT_TITLES = {
    "01_computer_architecture":   "Computer Architecture",
    "02_operating_system":        "Operating System",
    "03_network":                 "Network",
    "04_software_engineering":    "Software Engineering",
    "05_database":                "Database",
    "06_ict_convergence":         "ICT Convergence",
    "07_enterprise_systems":      "Enterprise Systems",
    "08_algorithm_stats":         "Algorithm & Statistics",
    "09_security":                "Security",
    "10_ai":                      "Artificial Intelligence",
    "11_design_supervision":      "Design & Supervision",
    "12_it_management":           "IT Management",
    "13_cloud_architecture":      "Cloud Architecture",
    "14_data_engineering":        "Data Engineering",
    "15_devops_sre":              "DevOps & SRE",
    "16_bigdata":                 "Big Data",
}

# Sub-section title overrides per subject (curated)
SUB_TITLES = {
    "01_computer_architecture": {
        "01_basic_electronics_logic":         "Basic Electronics & Logic",
        "02_data_representation_arithmetic":  "Data Representation & Arithmetic",
        "03_architecture_basics_performance": "Architecture Basics & Performance",
        "04_instruction_set_architecture":    "Instruction Set Architecture (ISA)",
        "05_control_unit_pipelining":         "Control Unit & Pipelining",
        "06_memory_hierarchy_cache":          "Memory Hierarchy & Cache",
        "07_virtual_memory_os_integration":   "Virtual Memory & OS Integration",
        "08_io_storage_systems":              "I/O & Storage Systems",
        "09_system_bus_interconnects":        "System Bus & Interconnects",
        "10_parallel_processing_architecture":"Parallel Processing Architecture",
        "11_multicore_synchronization":       "Multicore & Synchronization",
        "12_accelerators_ai_hardware":        "Accelerators & AI Hardware",
        "13_reliability_power_management":    "Reliability & Power Management",
        "14_hardware_security_trends":        "Hardware Security & Trends",
        "15_advanced_topics":                 "Advanced Topics",
    },
}

def fix_index_md(filepath: str, new_title: str, weight: int):
    """Read _index.md, update title and weight in frontmatter, write back."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace title line
    content = re.sub(r'^title:.*$', f'title: "{new_title}"', content, count=1, flags=re.MULTILINE)
    # Replace or add weight
    if re.search(r'^weight:', content, re.MULTILINE):
        content = re.sub(r'^weight:.*$', f'weight: {weight}', content, count=1, flags=re.MULTILINE)
    else:
        # Add weight after title
        content = re.sub(r'(^title:.*$)', rf'\1\nweight: {weight}', content, count=1, flags=re.MULTILINE)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✅ {filepath} -> title: \"{new_title}\", weight: {weight}")

changed = 0

for subject_folder in sorted(os.listdir(BASE)):
    subject_path = os.path.join(BASE, subject_folder)
    if not os.path.isdir(subject_path):
        continue

    subject_index = os.path.join(subject_path, "_index.md")

    # Fix subject-level _index.md
    if os.path.exists(subject_index) and subject_folder in SUBJECT_TITLES:
        # Derive weight from leading number
        m = re.match(r'^(\d+)_', subject_folder)
        weight = int(m.group(1)) if m else 99
        fix_index_md(subject_index, SUBJECT_TITLES[subject_folder], weight)
        changed += 1

    # Fix sub-section _index.md files
    sub_map = SUB_TITLES.get(subject_folder, {})
    for sub_folder in sorted(os.listdir(subject_path)):
        sub_path = os.path.join(subject_path, sub_folder)
        if not os.path.isdir(sub_path):
            continue
        sub_index = os.path.join(sub_path, "_index.md")
        if not os.path.exists(sub_index):
            continue

        m = re.match(r'^(\d+)_', sub_folder)
        weight = int(m.group(1)) if m else 99

        if sub_folder in sub_map:
            title = sub_map[sub_folder]
        else:
            title = folder_to_title(sub_folder)

        fix_index_md(sub_index, title, weight)
        changed += 1

print(f"\n✅ 총 {changed}개 파일 수정 완료")
