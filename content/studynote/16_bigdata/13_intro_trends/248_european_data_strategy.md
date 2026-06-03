+++
title = "036. 유럽 데이터 전략과 데이터 공간 (European Data Strategy & Data Spaces)"
date = 2026-03-03

[taxonomies]
tags = ["studynote-bigdata"]

[extra]
tags = ["studynote-bigdata"]
+++

> **핵심 인사이트**
> 1. 유럽 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)(European [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/), 2020)은 개인 [데이터 주권](/knowledge-base/studynote/09_security/16_data_privacy/809_data_sovereignty/)과 산업 [데이터 공유](/knowledge-base/studynote/05_database/06_dw_olap_trends/386_data_clean_room_sharing/)를 동시에 실현하는 "[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 공간([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Spaces)" 생태계 구축을 핵심으로 하며, GAIA-X 클라우드 연합이 인프라를 제공한다.
> 2. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 공간은 참여자 간 [데이터 주권](/knowledge-base/studynote/09_security/16_data_privacy/809_data_sovereignty/)을 유지하면서 안전하게 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 교환하는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 아키텍처로, 중앙집중식 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장소 없이 커넥터([IDS](/knowledge-base/studynote/02_operating_system/10_security/601_ids_ips_syscall_tracing/) Connector) 기반 [P2P](/knowledge-base/studynote/03_network/18_optical_nextgen_automation/916_p2p_peer_to_peer_networking_super_node_gnutella/) 교환을 사용한다.
> 3. [데이터 거버넌스](/knowledge-base/studynote/12_it_management/01_governance_strategy/052_data_governance_framework/) 법([Data Governance](/knowledge-base/studynote/12_it_management/01_governance_strategy/052_data_governance_framework/) Act, 2022)·[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 법([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Act, 2024)·[AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 법([AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) Act, 2024)이 연동되어 EU 디지털 단일 시장의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 규제 트리플 축을 형성하고 있다.

---

## I. 유럽 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 배경

```
배경: 미국·중국의 빅테크 데이터 독점에 대한 유럽의 대응

목표:
  1. 데이터 주권 확보 (GDPR 확장 개념)
  2. EU 내 데이터 단일 시장 구축
  3. 산업 데이터 공유 활성화
  4. 신뢰할 수 있는 AI 데이터 생태계

3대 가치:
  + 개방성 (Openness)
  + 신뢰 (Trust)
  + 지속 가능성 (Sustainability)
```

| 핵심 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 문서          | 발표 연도 | 핵심 내용                         |
|-------------------|---------|---------------------------------|
| European [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | 2020 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 공간 9개 분야 구축 계획      |
| [Data Governance](/knowledge-base/studynote/12_it_management/01_governance_strategy/052_data_governance_framework/) Act    | 2022 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 중개자·이타적 공유 프레임워크 |
| [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Act               | 2024 | [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 접근권·기업 간 공유     |
| [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) Act                 | 2024 | [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 시스템 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) 기반 규제         |

> 📢 **섹션 요약 비유**: 미국·중국이 대형 마트로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 독점한다면, 유럽은 공정 거래 규칙이 있는 시장 광장 — 모두가 공정하게 참여하고 주권을 유지한다.

---

## II. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 공간 ([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Spaces) 아키텍처



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">데이터 공간 핵심 원칙:</div>
<div class="kb-diagram-note">데이터 제공자가 데이터를 직접 보유</div>
<div class="kb-diagram-note">(중앙 저장소 없음!)</div>
<div class="kb-diagram-note">IDS (International Data Spaces) 커넥터:</div>
<div class="kb-diagram-note">제공자 측 커넥터 &lt;-&gt; 소비자 측 커넥터</div>
<div class="kb-diagram-note">P2P 암호화 채널로 데이터 교환</div>
<div class="kb-diagram-note">사용 정책(Usage Policy)이 데이터에 내장</div>
<div class="kb-diagram-note">구조:</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">데이터 제공자</div><div class="kb-diagram-cell">데이터 소비자</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(예: 자동차 제조)</div><div class="kb-diagram-cell">(예: 보험사)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">IDS Connector</div><div class="kb-diagram-cell">&lt;---&gt;</div><div class="kb-diagram-cell">IDS Connector</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">+ Usage Policy</div><div class="kb-diagram-cell">+ 동의 및 계약</div></div>
<div class="kb-diagram-note">GAIA-X 연합 인프라</div>
<div class="kb-diagram-note">(신뢰 레이어 + 카탈로그)</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 물건은 집에 두고, 서로 신뢰 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)된 우편 시스템으로만 교환하는 것 — 중앙 창고가 없어서 한 곳에 독점이나 침해가 생기지 않는다.

---

## III. GAIA-X — 유럽 클라우드 연합

```
GAIA-X (2019, 독일·프랑스 주도):

목표:
  유럽 클라우드 인프라 주권 확보
  AWS/Azure/GCP 의존도 감소

아키텍처:
  Federation Services:
    신원 인증 (Identity & Trust)
    카탈로그 (서비스/데이터셋 등록)
    주권 사용 제어
    컴플라이언스
  
  참여 조건:
    GAIA-X 정책 준수
    EU 법 적용 가능한 법인
    데이터 현지화 옵션

현황:
  300개 이상 기업/기관 참여
  실제 유스케이스: CATENA-X (자동차), EHDSi (의료)
```

> 📢 **섹션 요약 비유**: 미국 빅테크 클라우드에 유럽 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 맡기는 것이 불편한 유럽이, 유럽인이 운영하고 유럽 법이 적용되는 공동 클라우드를 만든 것.

---

## [IV](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/). 9개 산업 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 공간

```
EU 데이터 전략 9대 데이터 공간:

1. Health Data Space       의료 데이터 공유 (EHDS)
2. Industrial/Manufacturing CATENA-X (자동차 공급망)
3. Green Deal Data Space   탄소 발자국, 환경 데이터
4. Mobility               스마트 모빌리티, 교통
5. Energy                 스마트 그리드, ESG
6. Agriculture            농업 데이터 (Agri-Data Space)
7. Financial              금융 오픈 데이터
8. Public Administration  공공 데이터 플랫폼
9. Skills                 교육·직업 훈련 데이터
```

| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 공간        | 대표 프로젝트        | 주요 참여자                 |
|----------------|-------------------|--------------------------|
| CATENA-X       | 자동차 [공급망](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/)       | BMW, VW, Siemens, SAP    |
| EHDS           | 유럽 의료 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)    | 27개 EU 회원국 보건부       |
| Green Deal     | 탄소 추적          | Airbus, Schneider Electric|

> 📢 **섹션 요약 비유**: 각 산업별로 전용 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 시장을 만든 것 — 의료 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 의료 시장에서만, 자동차 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 자동차 시장에서만 안전하게 거래.

---

## V. 실무 시나리오 — CATENA-X (자동차 [공급망](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/))



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">문제:</div>
<div class="kb-diagram-note">자동차 1대는 3만여 개 부품 + 수백 개 공급업체</div>
<div class="kb-diagram-note">탄소 발자국 추적, 배터리 이력 관리 필요 (EU 배터리 규정)</div>
<div class="kb-diagram-note">CATENA-X 솔루션:</div>
<div class="kb-diagram-note">각 공급업체가 자체 데이터 보유 (IDS 커넥터)</div>
<div class="kb-diagram-note">완성차 업체(BMW, VW)는 필요 시 요청</div>
<div class="kb-diagram-note">배터리 디지털 여권: 원산지 -&gt; 제조 -&gt; 재활용까지 추적</div>
<div class="kb-diagram-note">탄소 발자국 증명: 공급망 전체 CO2 계산</div>
<div class="kb-diagram-note">기술 스택:</div>
<div class="kb-diagram-note">Eclipse Dataspace Components (EDC)</div>
<div class="kb-diagram-note">IDS 커넥터 구현체</div>
<div class="kb-diagram-note">GAIA-X 신뢰 레이어</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 자동차 한 대의 "탄소 여권" — 어디서 채굴된 배터리, 어느 공장에서 만든 부품인지 [공급망](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) 전체가 투명하게 추적되는 것.

---

## 📌 관련 개념 맵

```
유럽 데이터 전략
+-- 법·정책
|   +-- GDPR (데이터 개인 보호)
|   +-- Data Governance Act
|   +-- Data Act
|   +-- AI Act
+-- 데이터 공간
|   +-- IDS 커넥터 (P2P 교환)
|   +-- Usage Policy (사용 정책)
|   +-- 9개 산업 데이터 공간
+-- 인프라
|   +-- GAIA-X (유럽 클라우드 연합)
|   +-- EDC (Eclipse Dataspace Components)
+-- 사례
    +-- CATENA-X (자동차)
    +-- EHDS (의료)
    +-- Agri-Data Space (농업)
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[GDPR 시행 (2018)]
개인 데이터 주권 강화
      |
      v
[European Data Strategy (2020)]
산업 데이터 공유 + 데이터 공간 개념 수립
GAIA-X 프로젝트 시작
      |
      v
[Data Governance Act (2022)]
데이터 중개자 인증, 이타적 데이터 공유
      |
      v
[CATENA-X 운영 시작, Data Act (2024)]
첫 번째 산업 데이터 공간 실제 운영
IoT 데이터 접근권 법제화
      |
      v
[현재: AI Act + EHDS 시행 (2024~2026)]
EU AI 시스템 규제 강화
유럽 의료 데이터 공간 단계적 구현
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 유럽은 구글·아마존 같은 미국 회사들이 유럽 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 다 가져가는 게 싫어서, 유럽만의 [데이터 공유](/knowledge-base/studynote/05_database/06_dw_olap_trends/386_data_clean_room_sharing/) 규칙을 만들었어요.
2. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 공간은 물건을 창고에 모아두지 않고, 각자 집에 보관하면서 필요할 때만 안전하게 빌려주는 시스템이에요.
3. 자동차 회사들이 공급업체 부품의 탄소 발자국을 투명하게 추적하는 것이 좋은 예예요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 248 / 262

← **이전**: [035. 오픈데이터 원칙 — FAIR](/knowledge-base/studynote/16_bigdata/13_intro_trends/247_open_data_fair/)
**다음**: [037. 국가 데이터 정책 — 데이터기본법 · 데이터 산업 진흥법](/knowledge-base/studynote/16_bigdata/13_intro_trends/249_national_data_policy/) →

---
