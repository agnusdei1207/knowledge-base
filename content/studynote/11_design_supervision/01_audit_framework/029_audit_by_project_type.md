+++
title = "29. 프로젝트 유형별 감리 (Audit by Project Type)"
date = 2026-04-29

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [정보시스템 감리](/knowledge-base/studynote/12_it_management/05_security_compliance/187_information_system_audit/)는 프로젝트 특성(신규 개발, 운영·유지보수, 패키지 도입, 클라우드 전환)에 따라 감리 초점과 점검 항목이 달라진다. 단순히 체크리스트를 적용하는 것이 아니라 프로젝트 유형에 맞는 맞춤형 감리가 필요하다.
> 2. **가치**: 신규 개발 감리는 아키텍처 적절성·개발 품질·보안 설계에 집중하는 반면, 운영 감리는 [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) 이행·장애 대응 프로세스·변경 관리에 집중한다. 패키지 도입 감리는 커스터마이징 리스크와 밴더 의존성을, 클라우드 감리는 [CSP](/knowledge-base/studynote/09_security/05_web_app_security/475_csp/) 책임 분리와 보안 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)을 중점 점검한다.
> 3. **판단 포인트**: 클라우드·[AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 시스템의 감리 새 이슈가 등장했다. [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 모델의 편향성([Bias](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/094_bias/)) [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/), 설명 가능성([XAI](/knowledge-base/studynote/12_it_management/05_security_compliance/227_xai_explainable_ai_lime_shap/)), [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 출력 품질 감리가 현대 감리의 신규 영역이다. 기존 체크리스트는 이를 포함하지 않으므로 감리 기준 현행화가 시급하다.

---

## Ⅰ. 개요 및 필요성



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">프로젝트 유형별 감리 초점</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">유형 핵심 감리 영역</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">신규 개발 아키텍처, 보안 설계, 코드 품질</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">운영·유지보수 SLA, 변경 관리, 장애 대응</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">패키지 도입 커스터마이징, 밴더 의존, 데이터 이관</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">클라우드 전환 CSP 책임 분리, 보안 설정, 비용 관리</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">AI 시스템 모델 편향, 설명 가능성, 데이터 품질</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: 프로젝트 유형별 감리는 건물 종류별 안전 검사다. 새 건물(신규 개발)은 기초 공사·설계도 검사, 운영 중인 건물은 시설 유지·안전 점검, 리모델링(패키지 도입)은 구조 변경 안전성을 각각 다르게 검사한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 신규 개발 감리 핵심 항목

| 단계 | 주요 점검 항목 |
|:---|:---|
| **분석** | 요구사항 완전성·추적성, [이해관계자](/knowledge-base/studynote/04_software_engineering/03_design_architecture/173_stakeholder_identification_impact_matrix/) 합의 |
| **설계** | 아키텍처 적절성, 보안 by Design, 확장성 |
| **구현** | 코딩 표준, [코드 리뷰](/knowledge-base/studynote/04_software_engineering/06_software_architecture/330_code_review/), [단위 테스트](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/397_unit_test/) |
| **테스트** | [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)·보안·취약점 테스트 |
| **전환** | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이관 [정확성](/knowledge-base/studynote/16_bigdata/01_intro/002_bigdata_5v/), [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 계획 |

### 클라우드 전환 감리 핵심

```text
책임 공유 모델 검증:
  CSP 책임 vs 고객 책임 명확화
  (IaaS: OS·앱은 고객 책임)

보안 설정 기본값 점검:
  공개 S3 버킷, 과도한 IAM 권한, MFA 미설정
  → 클라우드 보안 설정 오류가 90% 이상 침해 원인

비용 관리:
  예산 알림, 미사용 리소스 정리 (FinOps)
```

- **📢 섹션 요약 비유**: 클라우드 감리의 책임 공유 모델 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)은 셋집 임차인 의무 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)이다. 집주인([CSP](/knowledge-base/studynote/09_security/05_web_app_security/475_csp/))은 건물 기초·배관을 책임지고, 세입자(고객)는 내부 인테리어·잠금장치를 책임진다 — 역할 경계가 명확해야 한다.

---

## Ⅲ. 비교 및 연결

| 비교 | 신규 개발 | 운영 | 클라우드 전환 |
|:---|:---|:---|:---|
| 시점 | 개발 중 | 운영 중 | 전환 전후 |
| 위험 | 설계 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/) | [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) 미달 | [보안 설정 오류](/knowledge-base/studynote/04_software_engineering/11_testing_validation/482_security_misconfiguration/) |
| 주요 도구 | [SAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/491_sast_static_analysis/), 설계 리뷰 | 모니터링 대시보드 | [CSPM](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/780_cspm_cloud_security_posture_management/) |

- **📢 섹션 요약 비유**: 감리 유형은 의사의 진료 종류다. 신규 개발은 신생아 검사(태어날 때부터 건강 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)), 운영 감리는 정기 건강검진, 클라우드 전환은 이민 전 건강검사다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 시스템 감리 신규 이슈

```text
모델 편향성 (Bias) 검증:
  - 인구 통계별 성능 차이 측정 (공정성 지표)
  - Demographic Parity, Equal Opportunity

설명 가능성 (XAI):
  - LIME/SHAP으로 예측 근거 설명 가능 여부
  - 금융·의료 AI: 법적 설명 의무

학습 데이터 품질:
  - 편향 데이터, 개인정보, 저작권 점검
  - 데이터 계보 추적 (Data Lineage)

생성 AI 출력 품질:
  - 환각(Hallucination) 비율
  - 유해 콘텐츠 필터링
  - RAG 검색 정확도
```

- **📢 섹션 요약 비유**: [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 감리는 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 의사 면허 시험이다. AI가 진단을 내릴 때 편향 없이(공정성), 이유를 설명하고([XAI](/knowledge-base/studynote/12_it_management/05_security_compliance/227_xai_explainable_ai_lime_shap/)), 잘못된 정보를 지어내지 않는지([환각](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/275_react_framework/) 방지) [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)해야 진료 허가를 받을 수 있다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| **품질 보증** | 프로젝트 유형별 맞춤 품질 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) |
| **위험 조기 발견** | 개발 중 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/) 조기 발견·수정 |
| **규제 준수** | 전자정부·[개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/)·금융 규정 충족 |

[AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)·클라우드 시대에 맞는 감리 기준 현행화가 시급하다. 기존 전자정부 [정보시스템 감리](/knowledge-base/studynote/12_it_management/05_security_compliance/187_information_system_audit/) 기준은 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 편향성·[생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 품질·클라우드 [CSP](/knowledge-base/studynote/09_security/05_web_app_security/475_csp/) 책임 분리를 명시적으로 다루지 않아, 새로운 [감리 프레임워크](/knowledge-base/studynote/11_design_supervision/01_audit_framework/006_audit_framework_3dimensional/) 개발이 필요하다.

- **📢 섹션 요약 비유**: [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 감리 기준 현행화는 도로교통법 개정이다. 자율주행차가 등장했지만 기존 교통법은 이를 규정하지 않아 새 규칙이 필요하듯, [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 시스템 감리도 새로운 기준이 필요하다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **책임 공유 모델** | 클라우드 감리의 핵심 프레임 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a> 공정성</strong> | [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 시스템 감리 신규 지표 |
| <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/227_xai_explainable_ai_lime_shap/">XAI</a></strong> | [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 결정 설명 가능성 감리 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/780_cspm_cloud_security_posture_management/">CSPM</a></strong> | 클라우드 보안 자세 관리 |
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 계보</strong> | [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 학습 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 추적 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">전통 감리 — 신규 개발·운영 체크리스트 중심</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">클라우드 감리 — CSP 책임 분리·보안 설정 검증</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">AI 시스템 감리 — 편향·설명 가능성·환각 검증</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">자동화 감리 — IaC 스캔·AI 기반 품질 분석</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">지속적 감리 — CI/CD 파이프라인 통합 자동화</div></div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. 프로젝트 유형마다 다른 검사가 필요해요! 새 건물(신규 개발), 리모델링(패키지), 이사(클라우드 전환) 때 각각 다른 안전 검사를 해요.
2. 클라우드 감리는 "집주인([CSP](/knowledge-base/studynote/09_security/05_web_app_security/475_csp/))과 세입자(고객)의 책임 경계"를 명확히 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해야 해요!
3. [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 시스템은 편향·설명·[환각](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/275_react_framework/)이라는 새로운 감리 항목이 생겼어요 — [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 의사 면허 시험처럼 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)이 필요하답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 34 / 530

← **이전**: [28. 시스템 아키텍처 보안 감리 (System Architecture Security Audit)](/knowledge-base/studynote/11_design_supervision/01_audit_framework/028_system_architecture_security_audit/)
**다음**: [29. 데이터베이스 영역 감리 (Database Area Audit)](/knowledge-base/studynote/11_design_supervision/01_audit_framework/029_database_area_audit/) →

---
