+++
title = "CMDB — 구성 관리 데이터베이스 (Configuration Management Database)"
description = "CMDB의 구성 항목(CI), ITSM/ITIL과의 관계, 자동 탐색(Auto-Discovery), ServiceNow 구현 패턴을 다룬다."
date = 2025-01-01

[taxonomies]
tags = ["CI", "CMDB", "ITIL", "ITSM", "ServiceNow", "asset management", "auto discovery", "configuration management", "studynote-enterprise"]

[extra]
tags = ["CI", "CMDB", "ITIL", "ITSM", "ServiceNow", "asset management", "auto discovery", "configuration management", "studynote-enterprise"]
+++

> **핵심 인사이트 3줄**
> 1. [CMDB](/knowledge-base/studynote/12_it_management/02_itsm_itil/091_cmdb/)([Configuration Management Database](/knowledge-base/studynote/12_it_management/02_itsm_itil/091_cmdb/))는 IT 인프라의 모든 구성 항목([CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/), [Configuration Item](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/))과 그 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 저장·관리하는 중앙 저장소다.
> 2. [ITIL](/knowledge-base/studynote/12_it_management/02_itsm_itil/062_itil/) v4에서 CMDB는 [ITSM](/knowledge-base/studynote/12_it_management/02_itsm_itil/096_iso_iec_20000_itsm_certification/) 프로세스(변경, 인시던트, [문제 관리](/knowledge-base/studynote/12_it_management/02_itsm_itil/077_problem_management/))의 공통 기반 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 작동하며 자동 탐색(Auto-Discovery)이 정확도의 핵심이다.
> 3. CMDB의 성패는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질([정확성](/knowledge-base/studynote/16_bigdata/01_intro/002_bigdata_5v/)·최신성)에 달려 있으며, 인간 수동 입력보다 자동화된 에이전트·[API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 연동이 필수적이다.

---

## Ⅰ. [CMDB](/knowledge-base/studynote/12_it_management/02_itsm_itil/091_cmdb/) 개요

### 1.1 구성 항목 ([CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/))

```
CMDB
├── 하드웨어 CI: 서버, 네트워크 장비, 스토리지
├── 소프트웨어 CI: OS, 미들웨어, 애플리케이션
├── 서비스 CI: 비즈니스 서비스, IT 서비스
├── 계약 CI: 라이선스, SLA
└── 관계(Relationship): CI 간 의존성, 위치, 소유
```

### 1.2 CMDB와 자산 관리 차이

| 항목      | 자산 관리 (Asset Mgmt) | [CMDB](/knowledge-base/studynote/12_it_management/02_itsm_itil/091_cmdb/)                   |
|----------|----------------------|------------------------|
| 초점      | 재무·계약 정보        | 기술 구성·[관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)          |
| 범위      | 구매~폐기 생애주기    | 운영 중 구성 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)       |
| [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 표현 | 미흡                  | 핵심 기능               |

📢 **섹션 요약 비유**: CMDB는 건물 설계도 — 각 방([CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/))의 위치와 배관([관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/))을 모두 기록해서 수리 시 영향도 파악.

---

## Ⅱ. ITIL과 [CMDB](/knowledge-base/studynote/12_it_management/02_itsm_itil/091_cmdb/) 통합

### 2.1 [ITSM](/knowledge-base/studynote/12_it_management/02_itsm_itil/096_iso_iec_20000_itsm_certification/) 프로세스와의 연계

```
인시던트 관리 ←→ CMDB ←→ 변경 관리
      ↓                       ↓
   영향 CI 조회           변경 영향도 분석
      ↑                       ↑
문제 관리 ←────────────────────
```

### 2.2 [변경 관리](/knowledge-base/studynote/12_it_management/02_itsm_itil/079_change_enablement/) 시나리오

```
변경 요청(CR) 접수
    ↓
CMDB에서 변경 대상 CI 조회
    ↓
관련 CI 의존성 그래프 분석
    ↓
영향 받는 서비스 목록 산출
    ↓
변경 승인 여부 결정 (Change Advisory Board)
```

📢 **섹션 요약 비유**: 건물 배관 공사 전에 설계도([CMDB](/knowledge-base/studynote/12_it_management/02_itsm_itil/091_cmdb/))를 보고 어느 층이 영향받는지 미리 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 것.

---

## Ⅲ. 자동 탐색 (Auto-Discovery)

### 3.1 탐색 방법

| 방법           | 설명                                        |
|--------------|---------------------------------------------|
| 에이전트 기반   | CI에 에이전트 설치 → 실시간 정보 수집        |
| 에이전트리스   | [SSH](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/538_ssh_vs_telnet_secure_remote/)/WMI/SNMP로 원격 탐색                    |
| [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 통합       | 클라우드(AWS, Azure) API로 리소스 수집       |
| 네트워크 스캔  | NMAP 등으로 IP 범위 스캔                    |

### 3.2 조정(Reconciliation)

여러 탐색 소스의 중복·충돌 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 통합:

```
소스1 (에이전트): hostname=web01, IP=10.0.0.1
소스2 (네트워크 스캔): IP=10.0.0.1, MAC=aa:bb:cc
조정 결과: CI{hostname=web01, IP=10.0.0.1, MAC=aa:bb:cc}
```

📢 **섹션 요약 비유**: 자동 탐색은 드론이 건물 전체를 스캔하는 것 — 사람이 방마다 돌아다니는 것보다 빠르고 정확하다.

---

## Ⅳ. ServiceNow [CMDB](/knowledge-base/studynote/12_it_management/02_itsm_itil/091_cmdb/) 구현

### 4.1 [CMDB](/knowledge-base/studynote/12_it_management/02_itsm_itil/091_cmdb/) 기본 클래스 계층

```
cmdb_ci (최상위)
├── cmdb_ci_hardware
│   ├── cmdb_ci_server
│   └── cmdb_ci_netgear
├── cmdb_ci_software
│   ├── cmdb_ci_os
│   └── cmdb_ci_appl
└── cmdb_ci_service
    └── cmdb_ci_business_service
```

### 4.2 [CMDB](/knowledge-base/studynote/12_it_management/02_itsm_itil/091_cmdb/) Health Dashboard

ServiceNow [CMDB](/knowledge-base/studynote/12_it_management/02_itsm_itil/091_cmdb/) Health 점수 (0~100):
- <strong><a href="/knowledge-base/studynote/16_bigdata/01_intro/002_bigdata_5v/">정확성</a></strong>: 실제 환경과 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 일치도
- **완전성**: 필수 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 채워진 비율
- **적시성**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 갱신 주기 준수 여부

📢 **섹션 요약 비유**: [CMDB](/knowledge-base/studynote/12_it_management/02_itsm_itil/091_cmdb/) 헬스 점수는 설계도의 [신뢰도](/knowledge-base/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/) — 현실과 다른 설계도(낮은 점수)는 수리 시 오히려 방해가 된다.

---

## Ⅴ. [CMDB](/knowledge-base/studynote/12_it_management/02_itsm_itil/091_cmdb/) 거버넌스와 성공 요소

### 5.1 공통 실패 원인

| 실패 원인              | 해결책                         |
|-----------------------|-------------------------------|
| 수동 입력 의존          | 자동 탐색 의무화               |
| 오너십 불명확          | [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/) Owner 지정 + 책임 체계      |
| 과도한 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/) 범위          | 핵심 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/) 우선 정의 후 확장      |
| 업데이트 프로세스 미비  | [변경 관리](/knowledge-base/studynote/12_it_management/02_itsm_itil/079_change_enablement/)와 [CMDB](/knowledge-base/studynote/12_it_management/02_itsm_itil/091_cmdb/) 연동 의무화   |

### 5.2 [CMDB](/knowledge-base/studynote/12_it_management/02_itsm_itil/091_cmdb/) 성숙도 모델

```
Level 1: 기본 하드웨어 CI 수동 관리
Level 2: 자동 탐색 도입, 소프트웨어 CI 추가
Level 3: ITSM 전 프로세스 연계
Level 4: 동적 클라우드 CI 자동 갱신
Level 5: AI 기반 이상 CI 탐지·자동 교정
```

📢 **섹션 요약 비유**: [CMDB](/knowledge-base/studynote/12_it_management/02_itsm_itil/091_cmdb/) 성숙도는 설계도 관리 수준 — 종이 설계도(Level 1)에서 실시간 3D BIM 모델(Level 5)로 진화.

---

## 📌 관련 개념 맵

```
CMDB
├── 구성 요소
│   ├── CI (Configuration Item)
│   ├── 관계 (Relationship)
│   └── 속성 (Attribute)
├── ITSM 연계
│   ├── 인시던트 관리
│   ├── 변경 관리
│   └── 문제 관리
├── 자동화
│   ├── Auto-Discovery
│   └── Reconciliation
└── 구현 플랫폼
    ├── ServiceNow
    ├── BMC Helix CMDB
    └── Micro Focus UCMDB
```

---

## 📈 관련 키워드 및 발전 흐름도

```
수동 자산 대장 (스프레드시트, 1980s~)
     │  ITIL v2 등장
     ▼
CMDB 개념 정립 (ITIL v2, 2000s)
     │  자동화 요구
     ▼
Auto-Discovery 도입 (에이전트/에이전트리스)
     │  클라우드 확산
     ▼
동적 CMDB (클라우드 API 연동, 2010s)
     │  AI/ML 적용
     ▼
지능형 CMDB (이상 탐지, 자동 교정, 2020s~)
```

**핵심 키워드**: [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/), [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/), Auto-Discovery, Reconciliation, [ITIL](/knowledge-base/studynote/12_it_management/02_itsm_itil/062_itil/), ServiceNow, [CMDB](/knowledge-base/studynote/12_it_management/02_itsm_itil/091_cmdb/) Health

---

## 👶 어린이를 위한 3줄 비유 설명

1. CMDB는 학교 교실 배치도 — 어느 반에 누가 앉고, 복도가 어떻게 연결되는지 전부 적혀 있어.
2. 배치가 바뀌면(자동 탐색) 지도가 즉시 업데이트되어야 선생님이 화재 대피 경로를 정확히 안내할 수 있어.
3. 지도가 틀리면(낮은 [CMDB](/knowledge-base/studynote/12_it_management/02_itsm_itil/091_cmdb/) 품질) 비상 시 엉뚱한 방향으로 대피 — [정확성](/knowledge-base/studynote/16_bigdata/01_intro/002_bigdata_5v/)이 전부야.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 50 / 482

← **이전**: [049. 서비스 카탈로그 — Service Catalog](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/049_service_catalog/)
**다음**: [051. 헬프 데스크, 서비스 데스크, SPOC](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/051_help_desk_service_desk_spoc/) →

---
