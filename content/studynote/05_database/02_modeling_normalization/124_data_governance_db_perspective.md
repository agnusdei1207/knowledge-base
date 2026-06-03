+++
title = "124. 데이터 거버넌스 (Data Governance) - 데이터 품질·보안·표준의 전사 관리 체계"
date = 2026-04-19

[taxonomies]
tags = ["studynote-database"]

[extra]
tags = ["studynote-database"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [데이터 거버넌스](/knowledge-base/studynote/12_it_management/01_governance_strategy/052_data_governance_framework/)는 <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>의 <a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">가용성</a>·<a href="/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/">무결성</a>·보안·품질을 보장하기 위한 <a href="/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/">정책</a>·프로세스·조직·기술의 통합 관리 체계</strong>이며, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 기업 자산으로 관리하는 전사적 프레임워크다.
> 2. **가치**: 거버넌스 없이는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 중복·불일치·보안 사고·규제 위반이 발생하며, [GDPR](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/)·[개인정보보호법](/knowledge-base/studynote/09_security/16_data_privacy/783_pipa_korea/) 등 <strong>규제 준수(<a href="/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/058_it_compliance_sox_basel_gdpr_isms/">Compliance</a>)</strong>를 위해서도 필수적이다.
> 3. **판단 포인트**: DAMA-DMBOK이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 관리 11개 영역을 정의하며, [데이터 스튜어드](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/067_data_steward_data_quality/)([Data Steward](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/067_data_steward_data_quality/))가 도메인별 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질의 책임자 역할을 수행한다.

---

## Ⅰ. 개요 및 필요성



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">데이터 거버넌스 프레임워크</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">전략</div><div class="kb-diagram-note">데이터 전략·비전·원칙</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">조직</div><div class="kb-diagram-note">CDO · 데이터 스튜어드 · 거버넌스 위원회</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">정책</div><div class="kb-diagram-note">데이터 표준·품질 규칙·보안 정책·접근 제어</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">프로세스</div><div class="kb-diagram-note">메타데이터 관리·MDM·품질 모니터링</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">기술</div><div class="kb-diagram-note">데이터 카탈로그·리니지 추적·DQ 도구</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: [데이터 거버넌스](/knowledge-base/studynote/12_it_management/01_governance_strategy/052_data_governance_framework/)는 도시의 <strong>도로교통법</strong>이다. 차([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))가 많아지면 법([정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/))·경찰(스튜어드)·신호등(기술)이 없으면 사고([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 오류)가 난다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### DAMA-DMBOK 11대 영역

| 영역 | 설명 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/12_it_management/01_governance_strategy/052_data_governance_framework/">데이터 거버넌스</a></strong> | 전사 의사결정 체계 |
| <strong><a href="/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/">데이터 아키텍처</a></strong> | [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/)·흐름 설계 |
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/">데이터 모델</a>링</strong> | ERD·[논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)/물리 모델 |
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 품질</strong> | [정확성](/knowledge-base/studynote/16_bigdata/01_intro/002_bigdata_5v/)·완전성·[일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) |
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/">메타데이터</a></strong> | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 대한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) |
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 보안</strong> | 접근 제어·암호화 |

- **📢 섹션 요약 비유**: DAMA-DMBOK는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 관리의 <strong>백과사전</strong>이며, 거버넌스는 그 백과사전의 **총론** 챕터이다.

---

## Ⅲ. 비교 및 연결

| 비교 | 거버넌스 없음 | 거버넌스 적용 |
|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 품질</strong> | 오류 빈발 | **정제·모니터링** |
| **규제 준수** | 위반 위험 | <strong><a href="/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/">GDPR</a>·PIPA 준수</strong> |
| **의사결정** | 불신 | <strong>신뢰 가능 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a></strong> |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 거버넌스 도구
- <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/">데이터 카탈로그</a></strong>: DataHub, Amundsen.
- <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/214_data_lineage_tracking/">데이터 리니지</a></strong>: Apache Atlas, dbt lineage.
- **DQ 도구**: Great Expectations, Soda.

---

## Ⅴ. 기대효과 및 결론

[데이터 거버넌스](/knowledge-base/studynote/12_it_management/01_governance_strategy/052_data_governance_framework/)는 <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>를 기업의 <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a> 자산으로 관리</strong>하는 체계이며, [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 시대에 학습 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 보장·편향 방지를 위해 더욱 중요해지고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **DAMA-DMBOK** | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 관리 표준 프레임워크 |
| <strong><a href="/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/067_data_steward_data_quality/">데이터 스튜어드</a></strong> | 도메인별 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 책임자 |
| <strong><a href="/knowledge-base/studynote/05_database/07_exam_summary/539_mdm_master_data_management/">MDM</a></strong> | 거버넌스의 기술적 구현 |
| <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/">데이터 카탈로그</a></strong> | [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 검색·관리 도구 |
| <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/214_data_lineage_tracking/">데이터 리니지</a></strong> | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 흐름 추적 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">수동 데이터 관리 (엑셀, 2000s)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">DAMA-DMBOK 1판 (2009) — 데이터 관리 표준</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">데이터 거버넌스 솔루션 (Collibra, 2015~)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">데이터 메시 (2020~) — 분산 거버넌스</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">현재: AI 거버넌스 — 모델·학습 데이터 품질 관리</div></div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명
1. [데이터 거버넌스](/knowledge-base/studynote/12_it_management/01_governance_strategy/052_data_governance_framework/)는 도시의 <strong>교통법규</strong>예요. 차([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))가 많으면 법이 필요해요.
2. <strong>경찰(<a href="/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/067_data_steward_data_quality/">데이터 스튜어드</a>)</strong>이 교통([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질)을 관리하고, <strong>신호등(기술 도구)</strong>이 흐름을 조절해요.
3. 법규가 없으면 사고([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 오류)가 나서 <strong>모두가 불편</strong>해진답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 124 / 600

← **이전**: [123. 참조 데이터 & 코드 테이블 (Reference Data & Code Tables) - 코드성 데이터 표준화](/knowledge-base/studynote/05_database/02_modeling_normalization/123_reference_data_code_tables/)
**다음**: [125. 메타데이터 관리 시스템 (MMS) - 데이터에 대한 데이터 관리](/knowledge-base/studynote/05_database/02_modeling_normalization/125_metadata_management_system_mms/) →

---
