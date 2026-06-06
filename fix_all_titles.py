#!/usr/bin/env python3
"""
전과목 _index.md title & weight 전수 수정 스크립트
규칙: 폴더명 NN_word_word -> title: "Word Word", weight: NN
약어/특수케이스는 ABBR 딕셔너리로 처리
"""

import os
import re

BASE = "/home/user/study/content/studynote"

# ─── 약어 처리 ──────────────────────────────────────────────────────────────
ABBR = {
    "ai":      "AI",
    "iot":     "IoT",
    "isa":     "ISA",
    "os":      "OS",
    "cpu":     "CPU",
    "gpu":     "GPU",
    "io":      "I/O",
    "ict":     "ICT",
    "sre":     "SRE",
    "devops":  "DevOps",
    "fpga":    "FPGA",
    "alu":     "ALU",
    "llm":     "LLM",
    "nlp":     "NLP",
    "dl":      "DL",
    "ml":      "ML",
    "mlops":   "MLOps",
    "erp":     "ERP",
    "eai":     "EAI",
    "esb":     "ESB",
    "msa":     "MSA",
    "bi":      "BI",
    "dw":      "DW",
    "olap":    "OLAP",
    "nosql":   "NoSQL",
    "newsql":  "NewSQL",
    "cicd":    "CI/CD",
    "gitops":  "GitOps",
    "iac":     "IaC",
    "pki":     "PKI",
    "iam":     "IAM",
    "soc":     "SOC",
    "gof":     "GoF",
    "ea":      "EA",
    "isp":     "ISP",
    "sdlc":    "SDLC",
    "itil":    "ITIL",
    "itsm":    "ITSM",
    "pm":      "PM",
    "bi":      "BI",
    "np":      "NP",
    "k8s":     "K8s",
    "iaas":    "IaaS",
    "paas":    "PaaS",
    "saas":    "SaaS",
    "devsecops": "DevSecOps",
    "finops":  "FinOps",
    "ot":      "OT",
    "mux":     "MUX",
}

# ─── 과목별 상위 폴더 제목 ──────────────────────────────────────────────────
SUBJECT_TITLES = {
    "01_computer_architecture":   ("Computer Architecture",   1),
    "02_operating_system":        ("Operating System",        2),
    "03_network":                 ("Network",                 3),
    "04_software_engineering":    ("Software Engineering",    4),
    "05_database":                ("Database",                5),
    "06_ict_convergence":         ("ICT Convergence",         6),
    "07_enterprise_systems":      ("Enterprise Systems",      7),
    "08_algorithm_stats":         ("Algorithm & Statistics",  8),
    "09_security":                ("Security",                9),
    "10_ai":                      ("Artificial Intelligence", 10),
    "11_design_supervision":      ("Design & Supervision",    11),
    "12_it_management":           ("IT Management",           12),
    "13_cloud_architecture":      ("Cloud Architecture",      13),
    "14_data_engineering":        ("Data Engineering",        14),
    "15_devops_sre":              ("DevOps & SRE",            15),
    "16_bigdata":                 ("Big Data",                16),
}

# ─── 세부 섹션 제목 재정의 (폴더명 → 사람이 읽기 좋은 제목) ───────────────
SECTION_OVERRIDES = {
    # 01 Computer Architecture
    "01_basic_electronics_logic":          "Basic Electronics & Logic",
    "02_data_representation_arithmetic":   "Data Representation & Arithmetic",
    "03_architecture_basics_performance":  "Architecture Basics & Performance",
    "04_instruction_set_architecture":     "Instruction Set Architecture (ISA)",
    "05_control_unit_pipelining":          "Control Unit & Pipelining",
    "06_memory_hierarchy_cache":           "Memory Hierarchy & Cache",
    "07_virtual_memory_os_integration":    "Virtual Memory & OS Integration",
    "08_io_storage_systems":              "I/O & Storage Systems",
    "09_system_bus_interconnects":         "System Bus & Interconnects",
    "10_parallel_processing_architecture": "Parallel Processing Architecture",
    "11_multicore_synchronization":        "Multicore & Synchronization",
    "12_accelerators_ai_hardware":         "Accelerators & AI Hardware",
    "13_reliability_power_management":     "Reliability & Power Management",
    "14_hardware_security_trends":         "Hardware Security & Trends",
    "15_advanced_topics":                  "Advanced Topics",

    # 02 Operating System
    "01_process_thread":                   "Process & Thread",
    "02_scheduling":                       "Scheduling",
    "03_memory_management":                "Memory Management",
    "04_file_system":                      "File System",
    "05_io_system":                        "I/O System",
    "06_virtualization_container":         "Virtualization & Container",
    "07_distributed_os":                   "Distributed OS",
    "08_real_time_embedded":               "Real-Time & Embedded OS",
    "09_security_protection":              "Security & Protection",
    "10_modern_os_trends":                 "Modern OS Trends",

    # 03 Network
    "01_basics":                           "Basics",
    "02_data_link":                        "Data Link Layer",
    "03_network_layer":                    "Network Layer",
    "04_transport_layer":                  "Transport Layer",
    "05_application_layer":                "Application Layer",
    "06_wireless_mobile":                  "Wireless & Mobile",
    "07_network_security":                 "Network Security",
    "08_sdn_nfv":                          "SDN & NFV",
    "09_cloud_network":                    "Cloud Networking",
    "10_network_management":               "Network Management",

    # 04 Software Engineering
    "01_requirements":                     "Requirements Engineering",
    "02_design":                           "Software Design",
    "03_implementation":                   "Implementation",
    "04_testing_quality":                  "Testing & Quality",
    "05_devops_ci_cd":                     "DevOps & CI/CD",
    "06_software_architecture":            "Software Architecture",
    "07_object_oriented":                  "Object-Oriented Design",
    "08_security_compliance_devsecops":    "Security & DevSecOps",
    "09_cloud_native_ai_architecture":     "Cloud-Native & AI Architecture",
    "10_trends_pm_quality":                "Trends, PM & Quality",
    "11_testing_validation":               "Testing & Validation",
    "12_testing_maintenance":              "Testing & Maintenance",
    "uncategorized":                       "Uncategorized",

    # 05 Database
    "01_db_architecture_relational":       "DB Architecture & Relational",
    "02_modeling_normalization":           "Modeling & Normalization",
    "03_relational_model":                 "Relational Model",
    "04_transactions_concurrency":         "Transactions & Concurrency",
    "05_distributed_nosql_newsql":         "Distributed, NoSQL & NewSQL",
    "06_dw_olap_trends":                   "DW, OLAP & Trends",
    "08_core_deep_dives":                  "Core Deep Dives",

    # 06 ICT Convergence
    "01_blockchain":                       "Blockchain",
    "02_iot_mobility":                     "IoT & Mobility",
    "03_cloud_infrastructure":             "Cloud Infrastructure",
    "04_ai_llm":                           "AI & LLM",
    "05_data_science":                     "Data Science",

    # 07 Enterprise Systems
    "01_strategy_governance":              "Strategy & Governance",
    "02_erp_systems":                      "ERP Systems",
    "03_eai_esb_msa":                      "EAI, ESB & MSA",
    "04_process_consulting":               "Process & Consulting",
    "05_data_bi":                          "Data & BI",
    "08_cloud_finops":                     "Cloud & FinOps",
    "09_digital_transformation":           "Digital Transformation",
    "10_enterprise_security_governance":   "Enterprise Security & Governance",

    # 08 Algorithm & Statistics
    "01_basics":                           "Algorithm Basics",
    "02_sorting":                          "Sorting Algorithms",
    "03_graph_search":                     "Graph & Search",
    "04_datastructure":                    "Data Structures",
    "05_string":                           "String Algorithms",
    "06_np_theory":                        "NP Theory",
    "07_numerical":                        "Numerical Methods",
    "08_stats":                            "Statistics",
    "09_info_theory":                      "Information Theory",
    "10_linear_algebra":                   "Linear Algebra",
    "11_graph_algorithms":                 "Graph Algorithms",
    "12_graph_algorithms":                 "Graph Algorithms (Advanced)",
    "13_sorting_algorithms":               "Sorting Algorithms (Advanced)",

    # 09 Security
    "01_intro_principles":                 "Intro & Principles",
    "02_crypto":                           "Cryptography",
    "03_network_security":                 "Network Security",
    "04_endpoint_security":                "Endpoint Security",
    "05_web_app_security":                 "Web & App Security",
    "10_pki_protocol":                     "PKI & Protocols",
    "11_iam_access_control":               "IAM & Access Control",
    "12_identity_threat_advanced":         "Identity & Threat (Advanced)",
    "13_secops_ir_forensics":              "SecOps, IR & Forensics",
    "14_threat_hunting_adversarial":       "Threat Hunting & Adversarial",
    "15_malware_attack_vectors":           "Malware & Attack Vectors",
    "16_data_privacy":                     "Data Privacy",
    "17_framework_compliance":             "Frameworks & Compliance",
    "18_iot_ot_physical":                  "IoT, OT & Physical Security",
    "19_ai_advanced_security":             "AI & Advanced Security",

    # 10 AI
    "01_ai_basics":                        "AI Basics",
    "02_dl_architecture_new":              "DL Architecture",
    "03_llm_nlp":                          "LLM & NLP",
    "04_ai_ops_ethics":                    "AI Ops & Ethics",
    "05_data_science_ml":                  "Data Science & ML",

    # 11 Design & Supervision
    "01_audit_framework":                  "Audit Framework",
    "02_architecture_principles":          "Architecture Principles",
    "03_gof_creational_structural":        "GoF – Creational & Structural",
    "04_gof_behavioral":                   "GoF – Behavioral",
    "05_audit_deep_guide":                 "Audit Deep Guide",
    "09_design_principles":                "Design Principles",
    "10_patterns_antipatterns":            "Patterns & Anti-Patterns",

    # 12 IT Management
    "01_governance_strategy":              "Governance & Strategy",
    "02_itsm_itil":                        "ITSM & ITIL",
    "03_ea_isp":                           "EA & ISP",
    "04_sdlc_testing":                     "SDLC & Testing",
    "05_security_compliance":              "Security & Compliance",

    # 13 Cloud Architecture
    "01_virtualization":                   "Virtualization",
    "02_iaas_paas_saas":                   "IaaS, PaaS & SaaS",
    "03_msa_serverless":                   "MSA & Serverless",
    "04_devops_observability":             "DevOps & Observability",
    "05_data_engineering":                 "Data Engineering",
    "07_container_k8s":                    "Container & Kubernetes",

    # 14 Data Engineering
    "01_infrastructure":                   "Data Infrastructure",
    "02_math_mining":                      "Math & Data Mining",
    "03_ml_dl_llm":                        "ML, DL & LLM",
    "04_mlops":                            "MLOps",

    # 15 DevOps & SRE
    "01_culture_methodology":              "Culture & Methodology",
    "02_cicd_gitops":                      "CI/CD & GitOps",
    "03_sre_observability":                "SRE & Observability",
    "04_iac_cloud_native":                 "IaC & Cloud-Native",
    "05_devsecops":                        "DevSecOps",

    # 16 Big Data
    "01_intro":                            "Introduction",
    "02_hadoop":                           "Hadoop Ecosystem",
    "03_spark":                            "Apache Spark",
    "04_streaming":                        "Stream Processing",
    "05_analysis":                         "Data Analysis",
    "06_nosql":                            "NoSQL",
    "07_data_lake":                        "Data Lake",
    "08_visualization":                    "Visualization",
    "09_platform":                         "Big Data Platform",
    "10_governance":                       "Data Governance",
    "11_industry":                         "Industry Applications",
    "12_trends":                           "Trends",
    "13_intro_trends":                     "Intro & Trends",
}


def folder_to_title_auto(folder_name: str) -> str:
    """폴더명에서 자동으로 제목 생성: NN_word_word -> Word Word"""
    parts = folder_name.split("_")
    start = 0
    for i, p in enumerate(parts):
        if p.isdigit():
            start = i + 1
        else:
            break
    words = parts[start:]
    result = []
    for w in words:
        low = w.lower()
        if low in ABBR:
            result.append(ABBR[low])
        else:
            result.append(w.capitalize())
    return " ".join(result)


def get_weight(folder_name: str) -> int:
    m = re.match(r'^(\d+)', folder_name)
    return int(m.group(1)) if m else 99


def update_index_md(filepath: str, new_title: str, weight: int) -> bool:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"  ❌ 읽기 실패 {filepath}: {e}")
        return False

    original = content

    # title 교체
    if re.search(r'^title:', content, re.MULTILINE):
        content = re.sub(r'^title:.*$', f'title: "{new_title}"', content, count=1, flags=re.MULTILINE)
    else:
        # frontmatter 시작에 추가
        if content.startswith("---"):
            content = re.sub(r'^---\n', f'---\ntitle: "{new_title}"\n', content, count=1)
        else:
            content = f'---\ntitle: "{new_title}"\nweight: {weight}\n---\n\n' + content

    # weight 교체 또는 추가
    if re.search(r'^weight:', content, re.MULTILINE):
        content = re.sub(r'^weight:.*$', f'weight: {weight}', content, count=1, flags=re.MULTILINE)
    else:
        content = re.sub(r'^(title:.*$)', rf'\1\nweight: {weight}', content, count=1, flags=re.MULTILINE)

    if content == original:
        return False  # 변경 없음

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"  ❌ 쓰기 실패 {filepath}: {e}")
        return False


# ─── 메인 실행 ──────────────────────────────────────────────────────────────
total = 0
changed = 0
errors = []

print("=" * 70)
print("전과목 _index.md title & weight 전수 수정")
print("=" * 70)

for subject_dir in sorted(os.listdir(BASE)):
    subject_path = os.path.join(BASE, subject_dir)
    if not os.path.isdir(subject_path):
        continue

    # ── 과목 상위 _index.md
    subject_index = os.path.join(subject_path, "_index.md")
    if subject_dir in SUBJECT_TITLES:
        title, weight = SUBJECT_TITLES[subject_dir]
    else:
        title = folder_to_title_auto(subject_dir)
        weight = get_weight(subject_dir)

    if os.path.exists(subject_index):
        total += 1
        ok = update_index_md(subject_index, title, weight)
        status = "✅" if ok else "─"
        print(f"\n[{subject_dir}]  →  \"{title}\"  (weight:{weight})")
        if ok:
            changed += 1

    # ── 세부 섹션 _index.md
    for section_dir in sorted(os.listdir(subject_path)):
        section_path = os.path.join(subject_path, section_dir)
        if not os.path.isdir(section_path):
            continue
        section_index = os.path.join(section_path, "_index.md")
        if not os.path.exists(section_index):
            continue

        weight = get_weight(section_dir)
        if section_dir in SECTION_OVERRIDES:
            title = SECTION_OVERRIDES[section_dir]
        else:
            title = folder_to_title_auto(section_dir)

        total += 1
        ok = update_index_md(section_index, title, weight)
        status = "  ✅" if ok else "  ─ "
        print(f"  {status} [{section_dir}]  →  \"{title}\"  (weight:{weight})")
        if ok:
            changed += 1

print("\n" + "=" * 70)
print(f"완료: 총 {total}개 검사, {changed}개 수정")
print("=" * 70)
