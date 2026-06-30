#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
KEYWORD_LIST = ROOT / "content/exam/cs/keyword_list.md"
OUTPUT_DIR = ROOT / "content/exam/cs/keyword-worklists"


SUBJECTS = [
    ("10_ai", "10 인공지능", 110),
    ("09_security", "09 보안", 110),
    ("13_cloud_architecture", "13 클라우드 아키텍처", 70),
    ("04_software_engineering", "04 소프트웨어공학", 100),
    ("01_computer_architecture", "01 컴퓨터구조", 90),
    ("05_database", "05 데이터베이스", 80),
    ("02_operating_system", "02 운영체제", 80),
    ("03_network", "03 네트워크", 80),
    ("14_data_engineering", "14 데이터 엔지니어링", 45),
    ("15_devops_sre", "15 DevOps/SRE", 45),
    ("07_enterprise_systems", "07 엔터프라이즈 시스템", 45),
    ("12_it_management", "12 IT 경영", 40),
    ("06_ict_convergence", "06 ICT 융합", 35),
    ("16_bigdata", "16 빅데이터", 30),
    ("08_algorithm_stats", "08 알고리즘/통계", 25),
    ("11_design_supervision", "11 IT 설계/감리", 25),
]


SECTION_TO_FOLDER = {
    "10. 인공지능": "10_ai",
    "09. 보안": "09_security",
    "13. 클라우드 아키텍처": "13_cloud_architecture",
    "04. 소프트웨어공학": "04_software_engineering",
    "01. 컴퓨터구조": "01_computer_architecture",
    "05. 데이터베이스": "05_database",
    "02. 운영체제": "02_operating_system",
    "03. 네트워크": "03_network",
    "14. 데이터 엔지니어링": "14_data_engineering",
    "15. DevOps/SRE": "15_devops_sre",
    "07. 엔터프라이즈 시스템": "07_enterprise_systems",
    "12. IT 경영": "12_it_management",
    "06. ICT 융합": "06_ict_convergence",
    "16. 빅데이터": "16_bigdata",
    "08. 알고리즘/통계": "08_algorithm_stats",
    "11. IT 설계/감리": "11_design_supervision",
}


SUBJECT_FOCUS_CHAPTERS = {
    "01_computer_architecture": [
        (1, 10, "02_data_representation_arithmetic"),
        (11, 18, "03_architecture_basics_performance"),
        (19, 24, "04_instruction_set_architecture"),
        (25, 37, "05_control_unit_pipelining"),
        (38, 47, "06_memory_hierarchy_cache"),
        (48, 55, "07_virtual_memory_os_integration"),
        (56, 64, "10_parallel_processing_architecture"),
        (65, 71, "11_multicore_synchronization"),
        (72, 78, "08_io_storage_systems"),
        (79, 84, "12_accelerators_ai_hardware"),
        (85, 86, "13_reliability_power_management"),
        (87, 89, "14_hardware_security_trends"),
    ],
    "02_operating_system": [
        (1, 12, "01_overview_architecture"),
        (13, 24, "02_process_thread"),
        (25, 36, "03_cpu_scheduling"),
        (37, 48, "04_synchronization"),
        (49, 51, "05_deadlock"),
        (52, 60, "06_memory_management"),
        (61, 66, "07_virtual_memory"),
        (67, 72, "08_storage_and_io_systems"),
        (73, 77, "09_file_system"),
        (78, 82, "03_cpu_scheduling"),
    ],
    "03_network": [
        (1, 6, "01_data_communication"),
        (7, 13, "04_data_link_layer_error"),
        (14, 22, "05_lan_wan_l2_devices"),
        (23, 32, "06_network_layer_ip"),
        (33, 42, "07_network_layer_routing"),
        (43, 52, "08_transport_layer"),
        (53, 61, "09_application_layer_web_email"),
        (62, 66, "11_wireless_mobile_communication"),
        (67, 72, "13_network_security_basics"),
        (73, 80, "17_sdn_nfv"),
    ],
    "04_software_engineering": [
        (1, 12, "01_overview_principles"),
        (13, 24, "02_requirements_analysis"),
        (25, 42, "03_design_architecture"),
        (43, 58, "04_testing_quality"),
        (59, 72, "05_devops_ci_cd"),
        (73, 84, "06_software_architecture"),
        (85, 92, "07_object_oriented"),
        (93, 104, "08_security_compliance_devsecops"),
    ],
}


CATEGORY_CHAPTERS = {
    "10_ai": {
        "탐색·전통 ML 기초": "01_ai_basics",
        "앙상블·핵심 알고리즘": "05_data_science_ml",
        "딥러닝 기초·CNN·RNN": "02_dl_architecture_new",
        "Transformer·LLM·생성형 AI": "03_llm_nlp",
        "강화학습·MLOps·AI 인프라": "04_ai_ops_ethics",
    },
    "09_security": {
        "보안 원칙·거버넌스": "01_intro_principles",
        "암호학·PKI": "02_crypto",
        "네트워크 보안": "03_network_security",
        "시스템·엔드포인트 보안": "04_endpoint_security",
        "웹·API·인증 보안": "05_web_app_security",
        "보안운영(SecOps)·법규": "13_secops_ir_forensics",
    },
    "13_cloud_architecture": {
        "클라우드 모델·가상화": "02_iaas_paas_saas",
        "컨테이너·쿠버네티스": "07_container_k8s",
        "MSA·서버리스": "03_msa_serverless",
        "DevOps·옵저버빌리티": "04_devops_observability",
    },
    "05_database": {
        "모델링·정규화": "02_modeling_normalization",
        "SQL·옵티마이저·인덱스": "03_relational_model",
        "트랜잭션·동시성·복구": "04_transactions_concurrency",
        "분산·NoSQL·NewSQL": "05_distributed_nosql_newsql",
        "DW·OLAP·최신": "06_dw_olap_trends",
    },
    "14_data_engineering": {
        "분산처리 인프라": "01_infrastructure",
        "저장 아키텍처": "01_infrastructure",
        "파이프라인·스트리밍": "04_mlops",
        "NoSQL·분산이론": "01_infrastructure",
        "거버넌스·MLOps": "04_mlops",
    },
    "15_devops_sre": {
        "DevOps 문화·방법론": "01_culture_methodology",
        "CI/CD·GitOps": "02_cicd_gitops",
        "SRE·신뢰성": "03_sre_observability",
        "옵저버빌리티": "03_sre_observability",
        "IaC·클라우드 네이티브": "04_iac_cloud_native",
        "DevSecOps": "05_devsecops",
    },
    "07_enterprise_systems": {
        "IT전략·거버넌스": "01_strategy_governance",
        "ITSM·서비스관리": "01_strategy_governance",
        "ERP·SCM·CRM": "02_erp_systems",
        "애플리케이션 통합 아키텍처": "03_eai_esb_msa",
        "BI·데이터·프로세스": "05_data_bi",
    },
    "12_it_management": {
        "IT거버넌스·전략": "01_governance_strategy",
        "투자평가": "03_ea_isp",
        "ITSM·ITIL": "02_itsm_itil",
        "PM·비용산정·품질": "04_sdlc_testing",
        "보안·감리·컴플라이언스·신기술": "05_security_compliance",
    },
    "06_ict_convergence": {
        "블록체인·Web3": "01_blockchain",
        "IoT·통신": "02_iot_mobility",
        "모빌리티·공간": "02_iot_mobility",
        "지능형 융합": "04_ai_llm",
    },
    "16_bigdata": {
        "개론·특성": "01_intro",
        "저장·처리": "02_hadoop",
        "레이크하우스": "07_data_lake",
        "실시간·분석": "04_streaming",
        "거버넌스": "10_governance",
    },
    "08_algorithm_stats": {
        "복잡도·설계": "01_basics",
        "정렬·탐색": "02_sorting",
        "그래프·자료구조": "03_graph_search",
        "NP·계산이론": "06_np_theory",
        "확률·통계": "08_stats",
    },
    "11_design_supervision": {
        "감리 개요": "01_audit_framework",
        "감리 점검": "05_audit_deep_guide",
        "아키텍처 평가": "02_architecture_principles",
        "설계 원칙·패턴": "09_design_principles",
    },
}


EXAM_TAGS = {
    "캐시": "125,131,132,134",
    "교착상태": "131,132,134,136",
    "Deadlock": "131,132,134,136",
    "세마포어": "125,126,132",
    "VM vs 컨테이너": "128,131,132,137",
    "컨테이너 vs VM": "128,131,132,137",
    "TCP": "125,128,129,132",
    "IaaS": "125,131,132",
    "PaaS": "125,131,132",
    "SaaS": "125,131,132",
    "방화벽": "128,131,134,137",
    "침입": "128,131,134,137",
    "품질": "125,128,134,137",
    "감리": "125,128,134,137",
    "ISMP": "125,128,132,135",
    "ISP": "125,128,132,135",
    "제로 트러스트": "126,134,135,136",
    "Zero Trust": "126,134,135,136",
    "AI 가속기": "126,134,136,137",
    "GPU": "126,134,136,137",
    "NPU": "126,134,135,136,137,138",
    "파인튜닝": "131,132,135,136",
    "LoRA(": "131,132,135,136",
    "LLM": "135,136,137,138",
    "RAG": "135,136,137,138",
    "프롬프트": "135,136,137,138",
    "DevSecOps": "128,134,135,136",
    "Flynn": "131,134",
    "MMU": "125,135",
    "가상 메모리": "125,135",
    "TLB": "125,135",
    "인터럽트": "128,132",
    "스케줄링": "129,131,138",
    "스레싱": "129,131",
    "SOLID": "128,132,137",
    "애자일": "125,134,137",
    "SAFe": "125,134,137",
    "ACID": "129,131",
    "무결성": "128,134",
    "OSI": "125,134",
    "SDN": "129,131",
    "NFV": "129,131",
    "PQC": "126,129,135,136",
    "양자컴퓨터": "126,129,135,136",
    "양자내성": "126,129,135,136",
    "양자 오류 정정": "138",
    "강화학습": "131,132",
    "멀티모달": "134,136",
    "디지털 트윈": "125,128",
    "개인정보": "126,131,137",
    "CSAP": "128,132,136",
    "쿠버네티스": "135,136,137",
    "K8s": "135,136,137",
    "MLOps": "135,137",
    "FinOps": "135,136",
    "프롬프트 인젝션": "135,137,138",
    "CXL": "129",
    "HBM": "129,131,138",
    "PIM": "129,131",
    "칩렛": "131",
    "뉴로모픽": "128",
    "온디바이스": "134,135,138",
    "QKD": "126",
    "영지식": "132",
    "ZKP": "132",
    "SBOM": "134,135,138",
    "PET": "134,135",
    "CSRF": "131",
    "적대적": "131",
    "AI 거버넌스": "136,138",
    "SVM": "132",
    "데이터 메시": "135",
    "서버리스": "136",
    "GitOps": "136",
    "연합학습": "136",
    "CTEM": "136,137",
    "LSM": "137",
    "AIOps": "137,138",
    "DDD": "137",
    "추론 특화": "138",
    "DeepSeek": "138",
    "소버린": "138",
    "MCP": "138",
    "SDV": "138",
    "가상 스레드": "138",
    "Wi-Fi 7": "134",
    "Open RAN": "132",
    "5G": "128,136,137",
    "MCTS": "135",
    "WebAssembly": "136",
    "레이크하우스": "137",
    "그린 소프트웨어": "137",
    "고가용성": "137",
    "Agentic": "136,138",
    "AI 에이전트": "136,138",
    "Transformer": "137",
    "NoSQL": "137",
    "ISMS-P": "138",
    "ISMS": "138",
    "서비스 메시": "138",
    "GNN": "138",
    "SIEM": "138",
    "SOAR": "138",
    "Passkey": "138",
    "FIDO2": "138",
    "ADAS": "138",
    "ADS": "138",
    "Model DoS": "138",
    "Self-Attention": "138",
    "TTFT": "138",
    "TPOT": "138",
    "ISO/IEC 42001": "138",
    "모라벡": "138",
    "FRAM": "138",
    "시스템 콜": "138",
    "SNN": "138",
    "OWASP LLM": "138",
    "ISO/PAS 8800": "138",
    "Benchmark Test": "138",
    "PoC": "138",
    "Pilot Test": "138",
    "CPU 레지스터": "138",
    "ASN.1": "138",
    "BER": "138",
    "DER": "138",
    "CER": "138",
    "ROM": "138",
    "RaaS": "138",
    "상태 레지스터": "138",
    "스마트선박": "138",
    "SAN": "138",
    "INS": "138",
    "멀티미디어 스트리밍": "137",
    "클라우드 AI": "137",
    "지능형 엣지": "137",
    "IEEE": "137",
    "IEC": "137",
    "Secure OS": "137",
    "SIL": "137",
    "HIL": "137",
    "RISC-V": "137",
    "공공 마이데이터": "137",
    "소프트웨어 프로세스": "137",
    "기아현상": "137",
    "sLLM": "137",
    "소프트웨어 영향평가": "137",
    "DMA": "137",
    "SG-DMA": "137",
    "RDMA": "137",
    "IOMMU": "137",
    "OPC UA": "137",
    "우선순위 역전": "137",
    "Sandbox": "137",
    "Whitebox": "137",
    "시스템 버스": "137",
    "버스 중재": "137",
    "영상압축": "137",
    "AIaaS": "137",
    "QML": "137",
    "DNS": "137",
    "디지털서비스 전문계약": "137",
}


TREND_PATTERNS = [
    "추론 특화", "DeepSeek", "MCP", "Agentic", "AI 에이전트", "소버린", "PQC",
    "SDV", "가상 스레드", "Wi-Fi 7", "Open RAN", "CTEM", "그린 소프트웨어",
    "HBM", "CXL", "QEC", "양자 오류 정정", "EU AI Act", "SBOM", "VEX",
    "Prompt Injection", "프롬프트 인젝션", "멀티모달", "온디바이스", "SLM",
    "DeepSeek-R1", "소버린 AI",
]


FORECAST_PATTERNS = [
    "도메인 특화 언어모델", "멀티에이전트 시스템", "AI 슈퍼컴퓨팅", "피지컬 AI",
    "기밀 컴퓨팅", "디지털 출처 증명", "AI 보안 플랫폼", "선제적 사이버보안",
    "지오패트리에이션", "소버린 AI", "AI 네이티브", "골든패스",
    "플랫폼 엔지니어링", "Physical AI", "Digital Provenance", "Confidential Computing",
    "AI-Native", "Geopatriation", "Multiagent", "Sovereign AI",
]


ADDITIONS = {
    "10_ai": [
        ("03_llm_nlp", "추론 특화 LLM (Reasoning Model)"),
        ("03_llm_nlp", "DeepSeek-R1 효율화 (MoE Distillation)"),
        ("03_llm_nlp", "MCP 모델 컨텍스트 프로토콜 (Model Context Protocol)"),
        ("03_llm_nlp", "ReAct 패턴 (Reasoning and Acting)"),
        ("03_llm_nlp", "Tool Use 도구 호출 (Tool Use)"),
        ("03_llm_nlp", "멀티 에이전트 협업 (Multi-Agent Collaboration)"),
        ("03_llm_nlp", "함수 호출 (Function Calling)"),
        ("03_llm_nlp", "테스트 타임 컴퓨트 (Test-Time Compute)"),
        ("03_llm_nlp", "PagedAttention (vLLM PagedAttention)"),
        ("03_llm_nlp", "KV 캐시 최적화 (KV Cache Optimization)"),
        ("03_llm_nlp", "Toolformer 도구 학습 (Toolformer)"),
        ("04_ai_ops_ethics", "AI 안전성 레드팀 (AI Red Teaming)"),
        ("04_ai_ops_ethics", "모델 평가 벤치마크 (Model Evaluation Benchmark)"),
        ("04_ai_ops_ethics", "LLMOps 운영 체계 (Large Language Model Operations)"),
        ("03_llm_nlp", "프롬프트 라우팅 (Prompt Routing)"),
        ("03_llm_nlp", "검색 재순위화 Reranker (Neural Reranker)"),
        ("03_llm_nlp", "합성 데이터 생성 (Synthetic Data Generation)"),
        ("04_ai_ops_ethics", "AI 워터마킹 (AI Watermarking)"),
        ("03_llm_nlp", "TTFT와 TPOT 추론 지연 지표 (TTFT and TPOT)"),
        ("03_llm_nlp", "Self-Attention 메커니즘 (Self-Attention Mechanism)"),
        ("03_llm_nlp", "모라벡의 역설 (Moravec's Paradox)"),
        ("03_llm_nlp", "sLLM 소형 언어모델 (Small Large Language Model)"),
        ("04_ai_ops_ethics", "Model DoS 공격 (Model Denial of Service)"),
        ("04_ai_ops_ethics", "ISO/IEC 42001 AI 경영시스템 (AI Management System)"),
        ("04_ai_ops_ethics", "ISO/PAS 8800 AI 안전성 (AI Safety)"),
        ("05_data_science_ml", "양자 머신러닝 QML (Quantum Machine Learning)"),
        ("04_ai_ops_ethics", "AIaaS 도입 고려사항 (AI as a Service)"),
        ("03_llm_nlp", "도메인 특화 언어모델 (Domain-Specific Language Model)"),
        ("03_llm_nlp", "멀티에이전트 시스템 (Multiagent System)"),
        ("02_dl_architecture_new", "AI 슈퍼컴퓨팅 플랫폼 (AI Supercomputing Platform)"),
        ("04_ai_ops_ethics", "피지컬 AI 로보틱스 (Physical AI Robotics)"),
    ],
    "09_security": [
        ("13_secops_ir_forensics", "SIEM vs SOAR 비교 (SIEM vs SOAR)"),
        ("13_secops_ir_forensics", "CTI 위협 인텔리전스 (Cyber Threat Intelligence)"),
        ("13_secops_ir_forensics", "MISP 위협 공유 플랫폼 (Malware Information Sharing Platform)"),
        ("17_framework_compliance", "EU DORA 디지털 운영 복원력 (Digital Operational Resilience Act)"),
        ("17_framework_compliance", "사이버 레질리언스 법규 (Cyber Resilience)"),
        ("02_crypto", "패스키 FIDO2 (Passkey WebAuthn)"),
        ("02_crypto", "PQC 전환 Crypto Agility (Post-Quantum Migration)"),
        ("05_web_app_security", "OWASP LLM Top 10 (OWASP LLM Top 10)"),
        ("05_web_app_security", "간접 프롬프트 인젝션 (Indirect Prompt Injection)"),
        ("04_endpoint_security", "펌웨어 보안 (Firmware Security)"),
        ("04_endpoint_security", "임베디드 보안 (Embedded Security)"),
        ("13_secops_ir_forensics", "모바일 포렌식 (Mobile Forensics)"),
        ("01_intro_principles", "ISMS-P vs ISMS 비교 (ISMS-P vs ISMS)"),
        ("19_ai_advanced_security", "LLM 보안 위협 OWASP LLM Top 10 (OWASP LLM Top 10)"),
        ("04_endpoint_security", "보안 운영체제 Secure OS (Secure Operating System)"),
        ("13_secops_ir_forensics", "RaaS 랜섬웨어 생태계 (Ransomware-as-a-Service)"),
        ("16_data_privacy", "개인정보 유출 사고 대응 PET (Privacy Incident and PET)"),
        ("02_crypto", "기밀 컴퓨팅 TEE (Confidential Computing)"),
        ("17_framework_compliance", "디지털 출처 증명 (Digital Provenance)"),
        ("19_ai_advanced_security", "AI 보안 플랫폼 (AI Security Platform)"),
        ("13_secops_ir_forensics", "선제적 사이버보안 (Preemptive Cybersecurity)"),
    ],
    "13_cloud_architecture": [
        ("02_iaas_paas_saas", "클라우드 랜딩존 (Cloud Landing Zone)"),
        ("02_iaas_paas_saas", "클라우드 공유 책임 모델 (Shared Responsibility Model)"),
        ("02_iaas_paas_saas", "클라우드 데이터베이스 서비스 (Managed Cloud Database)"),
        ("03_msa_serverless", "서비스 메시 Istio (Istio Service Mesh)"),
        ("03_msa_serverless", "Envoy 사이드카 프록시 (Envoy Sidecar Proxy)"),
        ("04_devops_observability", "FinOps 비용 최적화 (Cloud FinOps)"),
        ("05_data_engineering", "그린 데이터센터 PUE (Green Data Center PUE)"),
        ("07_container_k8s", "쿠버네티스 NetworkPolicy (Kubernetes NetworkPolicy)"),
        ("02_iaas_paas_saas", "클라우드 AI vs 온디바이스 AI (Cloud AI vs On-Device AI)"),
        ("02_iaas_paas_saas", "지능형 엣지 컴퓨팅 (Intelligent Edge Computing)"),
        ("02_iaas_paas_saas", "클라우드 정보화사업 감리 (Cloud Project Audit)"),
        ("02_iaas_paas_saas", "클라우드 서비스 유형 IaaS PaaS SaaS FaaS (Cloud Service Models)"),
        ("02_iaas_paas_saas", "지오패트리에이션 데이터 주권 (Geopatriation)"),
        ("02_iaas_paas_saas", "소버린 AI 인프라 (Sovereign AI Infrastructure)"),
    ],
    "05_database": [
        ("03_relational_model", "B-Tree vs LSM-Tree 비교 (B-Tree vs LSM-Tree)"),
        ("03_relational_model", "커버링 인덱스 (Covering Index)"),
        ("05_distributed_nosql_newsql", "클라우드 DB RDS Aurora DynamoDB (Cloud Database Service)"),
        ("05_distributed_nosql_newsql", "DynamoDB 일관성 모델 (DynamoDB Consistency Model)"),
        ("06_dw_olap_trends", "데이터 레이크하우스 Delta Iceberg (Lakehouse)"),
        ("03_relational_model", "구체화 뷰 갱신 (Materialized View Refresh)"),
        ("03_relational_model", "쿼리 재작성 (Query Rewrite)"),
        ("03_relational_model", "복합 인덱스 선두 컬럼 (Composite Index Leading Column)"),
        ("04_transactions_concurrency", "스냅샷 격리 (Snapshot Isolation)"),
        ("05_distributed_nosql_newsql", "분산 합의 리더 선출 (Distributed Consensus Leader Election)"),
        ("06_dw_olap_trends", "벡터 인덱스 HNSW (Vector Index HNSW)"),
        ("05_distributed_nosql_newsql", "분산 데이터베이스 투명성 (Distributed Database Transparency)"),
    ],
    "14_data_engineering": [
        ("01_infrastructure", "오픈 테이블 포맷 (Open Table Format)"),
        ("01_infrastructure", "Apache Iceberg (Apache Iceberg)"),
        ("01_infrastructure", "Delta Lake (Delta Lake)"),
        ("04_mlops", "데이터 계약 (Data Contract)"),
        ("04_mlops", "데이터 관측성 (Data Observability)"),
        ("04_mlops", "품질 게이트 dbt Tests (dbt Test Quality Gate)"),
    ],
    "15_devops_sre": [
        ("02_cicd_gitops", "연속형 배포 (Continuous Deployment)"),
        ("02_cicd_gitops", "피처 플래그 점진 배포 (Feature Flag Progressive Delivery)"),
        ("05_devsecops", "VEX 취약점 악용 가능성 교환 (Vulnerability Exploitability eXchange)"),
        ("05_devsecops", "SLSA 공급망 보안 수준 (Supply-chain Levels for Software Artifacts)"),
        ("05_devsecops", "Sigstore Cosign 서명 (Sigstore Cosign)"),
        ("03_sre_observability", "SLO와 에러 버짓 운용 (SLO and Error Budget)"),
        ("02_cicd_gitops", "Benchmark Test PoC Pilot Test 비교 (Benchmark PoC Pilot)"),
        ("01_culture_methodology", "AI 네이티브 개발 플랫폼 (AI-Native Development Platform)"),
        ("01_culture_methodology", "플랫폼 엔지니어링 골든패스 (Platform Engineering Golden Path)"),
    ],
    "07_enterprise_systems": [
        ("09_digital_transformation", "초개인화 (Hyper-Personalization)"),
        ("09_digital_transformation", "고객 360도 뷰 (Customer 360 View)"),
        ("10_enterprise_security_governance", "고가용성 Active-Active (High Availability Active-Active)"),
        ("08_cloud_finops", "클라우드 마이그레이션 6R (Cloud Migration 6R)"),
        ("09_digital_transformation", "공공 마이데이터 활용 (Public MyData)"),
        ("09_digital_transformation", "디지털서비스 전문계약제도 (Digital Service Contract System)"),
        ("09_digital_transformation", "스마트선박 SAN INS (Smart Ship SAN INS)"),
    ],
    "12_it_management": [
        ("05_security_compliance", "EU DORA 규정 (Digital Operational Resilience Act)"),
        ("03_ea_isp", "디지털 정부 서비스 성숙도 (Digital Government Maturity)"),
        ("04_sdlc_testing", "소프트웨어 기술성 평가 (Software Technical Evaluation)"),
        ("04_sdlc_testing", "유지보수 대가산정 (Software Maintenance Cost Estimation)"),
        ("04_sdlc_testing", "소프트웨어 프로세스 품질인증 SP (Software Process Quality Certification)"),
        ("04_sdlc_testing", "소프트웨어 영향평가 (Software Impact Assessment)"),
        ("05_security_compliance", "IEEE 표준 vs IEC 국제표준 (IEEE vs IEC)"),
    ],
    "06_ict_convergence": [
        ("02_iot_mobility", "자율주행 V2X 보안 (Autonomous Vehicle V2X Security)"),
        ("02_iot_mobility", "NTN 비지상 네트워크 (Non-Terrestrial Network)"),
        ("02_iot_mobility", "엣지 TPU (Edge TPU)"),
        ("04_ai_llm", "양자 오류 정정 QEC (Quantum Error Correction)"),
        ("02_iot_mobility", "ADAS vs ADS 자율주행 비교 (ADAS vs ADS)"),
        ("02_iot_mobility", "SIL HIL 테스트 (Software-in-the-Loop Hardware-in-the-Loop)"),
        ("04_ai_llm", "OPC UA 스마트팩토리 표준 (OPC Unified Architecture)"),
        ("02_iot_mobility", "피지컬 AI와 로봇 자동화 (Physical AI and Robotics)"),
    ],
    "16_bigdata": [
        ("09_platform", "실시간 OLAP Druid Pinot (Real-Time OLAP)"),
        ("12_trends", "데이터 제품 (Data Product)"),
        ("12_trends", "데이터 주권 (Data Sovereignty)"),
        ("04_streaming", "멀티미디어 스트리밍 프로토콜 (Multimedia Streaming Protocol)"),
        ("05_analysis", "영상압축 무손실 손실 혼합 (Video Compression)"),
    ],
    "08_algorithm_stats": [
        ("03_graph_search", "몬테카를로 트리탐색 MCTS (Monte Carlo Tree Search)"),
        ("10_linear_algebra", "SVD 특이값 분해 (Singular Value Decomposition)"),
        ("09_info_theory", "엔트로피 정보이론 (Entropy Information Theory)"),
        ("07_numerical", "양자 오류 정정 표면 코드 (Surface Code QEC)"),
    ],
    "11_design_supervision": [
        ("02_architecture_principles", "ADR 아키텍처 의사결정 기록 (Architecture Decision Record)"),
        ("02_architecture_principles", "품질속성 시나리오 (Quality Attribute Scenario)"),
        ("05_audit_deep_guide", "클라우드 감리 CSAP (Cloud Security Assurance Program)"),
    ],
    "01_computer_architecture": [
        ("02_data_representation_arithmetic", "FRAM 강유전체 RAM (Ferroelectric RAM)"),
        ("03_architecture_basics_performance", "CPU 레지스터와 상태 레지스터 (CPU Register and Status Register)"),
        ("03_architecture_basics_performance", "ROM 종류 PROM EPROM EEPROM Flash (Read Only Memory)"),
        ("09_system_bus_interconnects", "시스템 버스와 버스 중재 (System Bus and Bus Arbitration)"),
        ("08_io_storage_systems", "DMA SG-DMA RDMA 비교 (DMA SG-DMA RDMA)"),
        ("08_io_storage_systems", "IOMMU 입출력 메모리 관리장치 (I/O Memory Management Unit)"),
        ("12_accelerators_ai_hardware", "SNN 스파이킹 신경망 하드웨어 (Spiking Neural Network Hardware)"),
    ],
    "02_operating_system": [
        ("01_overview_architecture", "시스템 콜 동작 원리 (System Call Mechanism)"),
        ("03_cpu_scheduling", "기아현상과 에이징 (Starvation and Aging)"),
        ("10_security", "샌드박스 보안 모델 (Sandbox Security Model)"),
    ],
    "03_network": [
        ("05_lan_wan_l2_devices", "이더넷 VLAN 802.1Q (Ethernet VLAN 802.1Q)"),
        ("05_lan_wan_l2_devices", "STP RSTP 루프 방지 (Spanning Tree Protocol)"),
        ("06_network_layer_ip", "ARP 스푸핑과 방어 (ARP Spoofing Defense)"),
        ("06_network_layer_ip", "IPv6 SLAAC NDP (IPv6 SLAAC NDP)"),
        ("07_network_layer_routing", "OSPFv3 IPv6 라우팅 (OSPFv3 Routing)"),
        ("07_network_layer_routing", "BGP 경로벡터 라우팅 (Border Gateway Protocol)"),
        ("07_network_layer_routing", "MPLS 라벨 스위칭 (Multiprotocol Label Switching)"),
        ("07_network_layer_routing", "QoS DiffServ DSCP (Quality of Service DiffServ)"),
        ("10_application_layer_dns_mgmt", "DNS 동작 원리와 보안 (DNS Operation and Security)"),
        ("10_application_layer_dns_mgmt", "DNSSEC 전자서명 검증 (DNS Security Extensions)"),
        ("10_application_layer_dns_mgmt", "SNMP 네트워크 관리 (Simple Network Management Protocol)"),
        ("09_application_layer_web_email", "HTTP/3 QUIC 전송 (HTTP/3 over QUIC)"),
        ("09_application_layer_web_email", "gRPC와 REST 비교 (gRPC vs REST)"),
        ("09_application_layer_web_email", "ASN.1 BER DER CER 인코딩 (ASN.1 BER DER CER)"),
        ("08_transport_layer", "멀티미디어 스트리밍 QoS (Multimedia Streaming QoS)"),
        ("11_wireless_mobile_communication", "5G 네트워크 슬라이싱 (5G Network Slicing)"),
        ("17_sdn_nfv", "SDN 컨트롤러 구조 (SDN Controller Architecture)"),
        ("17_sdn_nfv", "NFV MANO 구조 (NFV MANO Architecture)"),
    ],
    "04_software_engineering": [
        ("04_testing_quality", "Whitebox Test와 Blackbox Test 비교 (Whitebox vs Blackbox Test)"),
        ("04_testing_quality", "SIL HIL 테스트 전략 (Software-in-the-Loop Hardware-in-the-Loop)"),
        ("01_overview_principles", "소프트웨어 프로세스 품질인증 (Software Process Quality Certification)"),
        ("10_trends_pm_quality", "AI 네이티브 SDLC (AI-Native SDLC)"),
        ("10_trends_pm_quality", "그린 소프트웨어 SCI 지수 (Software Carbon Intensity)"),
        ("10_trends_pm_quality", "가상 스레드 동시성 모델 (Virtual Threads Concurrency Model)"),
    ],
}


def split_keywords(text: str) -> list[str]:
    items: list[str] = []
    buf: list[str] = []
    depth = 0
    pairs = {"(": ")", "[": "]", "{": "}"}
    closers = set(pairs.values())
    for ch in text:
        if ch in pairs:
            depth += 1
        elif ch in closers and depth:
            depth -= 1
        if ch == "," and depth == 0:
            item = "".join(buf).strip()
            if item:
                items.append(item)
            buf = []
        else:
            buf.append(ch)
    item = "".join(buf).strip()
    if item:
        items.append(item)
    return items


def parse_keyword_list() -> dict[str, list[tuple[str, str]]]:
    content = KEYWORD_LIST.read_text(encoding="utf-8")
    sections: dict[str, list[tuple[str, str]]] = {}
    current_folder: str | None = None
    for line in content.splitlines():
        m = re.match(r"^###\s+(.+)$", line)
        if m:
            current_folder = SECTION_TO_FOLDER.get(m.group(1).strip())
            if current_folder:
                sections.setdefault(current_folder, [])
            continue
        if not current_folder:
            continue
        m = re.match(r"^-\s+\*\*(.+?)\*\*:\s+(.+)$", line)
        if not m:
            continue
        category, raw_items = m.group(1).strip(), m.group(2).strip()
        chapter = CATEGORY_CHAPTERS.get(current_folder, {}).get(category, "01_overview")
        for item in split_keywords(raw_items):
            sections[current_folder].append((chapter, normalize_item(item)))
    return sections


def normalize_item(item: str) -> str:
    item = re.sub(r"\s+", " ", item).strip()
    item = item.replace("·", "·")
    return item


def read_subject_focus(folder: str) -> list[tuple[str, str]]:
    root = SUBJECT_FOCUS / folder
    if not root.exists():
        return []
    result = []
    for path in sorted(root.glob("*.md")):
        if path.name == "_index.md":
            continue
        match = re.match(r"^(\d+)_", path.name)
        if not match:
            continue
        weight = int(match.group(1))
        title = extract_title(path)
        result.append((chapter_for_weight(folder, weight), title))
    return result


def extract_title(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    m = re.search(r'^title:\s+"(.+?)"', text, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return path.stem


def chapter_for_weight(folder: str, weight: int) -> str:
    for start, end, chapter in SUBJECT_FOCUS_CHAPTERS.get(folder, []):
        if start <= weight <= end:
            return chapter
    return "01_overview"


def tag_for(item: str) -> str:
    tags: list[str] = []
    if "IOMMU" in item:
        tags.append("[출제:137회]")
    elif "양자화" in item:
        pass
    else:
        for key, rounds in EXAM_TAGS.items():
            if key.lower() in item.lower():
                tags.append(f"[출제:{rounds}회]")
                break
    if any(pattern.lower() in item.lower() for pattern in TREND_PATTERNS):
        tags.append("[전망]")
    if any(pattern.lower() in item.lower() for pattern in FORECAST_PATTERNS):
        tags.append("[전망]")
    tags = list(dict.fromkeys(tags))
    return " " + " ".join(tags) if tags else ""


def dedupe(items: list[tuple[str, str]]) -> list[tuple[str, str]]:
    seen = set()
    output = []
    for chapter, item in items:
        key = re.sub(r"[^0-9A-Za-z가-힣]+", "", item).lower()
        if key in seen:
            continue
        seen.add(key)
        output.append((chapter, item))
    return output


def build_subject_items(folder: str, parsed: dict[str, list[tuple[str, str]]]) -> list[tuple[str, str]]:
    base = parsed.get(folder, [])
    base.extend(ADDITIONS.get(folder, []))
    return dedupe(base)


def render_worklist(folder: str, subject_name: str, target: int, items: list[tuple[str, str]]) -> str:
    weight = int(subject_name.split()[0])
    out = [
        "---",
        f'title: "{subject_name} 기출-grounded 키워드 워크리스트"',
        'date: "2026-06-30"',
        "tags:",
        '  - "exam-keywords"',
        '  - "cspe"',
        '  - "keyword-worklist"',
        f"weight: {weight}",
        "---",
        "",
        f"# {subject_name} 기출-grounded 키워드 워크리스트 (목표 ~{target}개)",
        "> 출처: 120~138회 컴퓨터시스템응용기술사 기출 대조 + content/exam/cs/keyword_list.md + frequency.md + keyword-universe.md + 출제 전망.",
        "",
    ]
    grouped: dict[str, list[str]] = {}
    order: list[str] = []
    for chapter, item in items:
        if chapter not in grouped:
            grouped[chapter] = []
            order.append(chapter)
        grouped[chapter].append(item)
    seq = 1
    for chapter in order:
        out.append(f"## 챕터: {chapter}")
        for item in grouped[chapter]:
            out.append(f"{seq:03d}. {item}{tag_for(item)}")
            seq += 1
        out.append("")
    out.append(f"> 생성 기준: 총 {len(items)}개. 목표 수는 시험 출제 가능성 기준의 운영 상한이며, 지엽 키워드는 제외한다.")
    out.append("")
    return "\n".join(out)


def main() -> None:
    parsed = parse_keyword_list()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for folder, subject_name, target in SUBJECTS:
        items = build_subject_items(folder, parsed)
        rendered = render_worklist(folder, subject_name, target, items)
        (OUTPUT_DIR / f"{folder}.md").write_text(rendered, encoding="utf-8")
        print(f"{folder}: {len(items)}")


if __name__ == "__main__":
    main()
