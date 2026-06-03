+++
title = "28. 소프트웨어 리엔지니어링 (Software Reengineering)"
date = 2026-04-29

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 소프트웨어 리엔지니어링(Software Reengineering)은 기존 레거시 시스템을 분석([역공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/029_reverse_engineering/), [Reverse Engineering](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/780_reverse_engineering/))하여 이해한 뒤, 개선된 형태로 재구조화(Restructuring)하거나 재구현([Forward](/knowledge-base/studynote/10_ai/03_llm_nlp/235_forward_backward_chaining/) Engineering)하는 소프트웨어 진화 활동이다.
> 2. **가치**: 레거시 시스템을 완전히 교체하면 비용·리스크가 크고 비즈니스 연속성이 위협받는다. 리엔지니어링은 기존 시스템의 비즈니스 로직을 보존하면서 [기술 부채](/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/)를 해소하고 현대화한다는 점에서 완전 재개발(Greenfield)보다 실용적인 경우가 많다.
> 3. **판단 포인트**: 리엔지니어링 vs. 완전 재개발 선택 기준 — 비즈니스 로직이 복잡하고 문서화가 미흡하면 리엔지니어링이 유리. 기술 스택이 완전히 구식이거나 아키텍처 자체가 현대화 불가능하면 재개발을 선택. 실무에서는 [스트랭글러 피그](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/310_strangler_fig_pattern/)([Strangler Fig](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/310_strangler_fig_pattern/)) 패턴으로 점진적 교체가 권장된다.

---

## Ⅰ. 개요 및 필요성



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">리엔지니어링 Horseshoe 모델</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">역공학</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">재구조화</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">←</div><div class="kb-diagram-node">순공학</div><div class="kb-diagram-connector">←</div><div class="kb-diagram-note">개선 설계 ←</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">좌측(역공학): 이해 단계 우측(순공학): 구현 단계</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: 리엔지니어링은 낡은 집을 리모델링하는 것이다. 집을 허물고 새로 짓는 대신(재개발), 기초(비즈니스 로직)는 유지하면서 내부 구조·배관·전기를 현대화한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 리엔지니어링 주요 활동

| 활동 | 정의 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/04_software_engineering/01_overview_principles/029_reverse_engineering/">역공학</a> (Reverse Eng.)</strong> | 소스 코드·바이너리에서 설계·요구사항 추출 |
| **재구조화 (Restructuring)** | 같은 기능을 더 명확한 구조로 변환 |
| **재문서화 (Redocumentation)** | 소스 코드에서 문서 자동 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) |
| **마이그레이션 (Migration)** | 다른 플랫폼·언어로 이식 |
| <strong>순공학 (<a href="/knowledge-base/studynote/10_ai/03_llm_nlp/235_forward_backward_chaining/">Forward</a> Eng.)</strong> | 추출된 설계를 기반으로 개선 구현 |

### [스트랭글러 피그 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/376_strangler_fig_summary/) ([Strangler Fig](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/310_strangler_fig_pattern/))

```text
기존 레거시 시스템 → 새 마이크로서비스가 기능별로 교체
                      점진적으로 레거시 기능을 래핑/대체

단계:
  1. 새 서비스 구축 (기존과 병행)
  2. 트래픽을 점진적으로 새 서비스로 전환
  3. 레거시 코드 폐기
```

- **📢 섹션 요약 비유**: [스트랭글러 피그](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/310_strangler_fig_pattern/)는 기존 나무를 새 나무가 감싸며 서서히 대체하는 식물 이름에서 유래했다. 기존 서비스를 중단 없이 운영하면서 새 코드로 기능을 하나씩 대체한다.

---

## Ⅲ. 비교 및 연결

| 비교 | 리엔지니어링 | 완전 재개발 | 유지보수 |
|:---|:---|:---|:---|
| 비즈니스 로직 | 보존 | 재구현 | 최소 변경 |
| 위험도 | 중간 | 높음 | 낮음 |
| 비용 | 중간 | 높음 | 낮음 |
| [기술 부채](/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/) 해소 | 부분 | 완전 | 없음 |

- **📢 섹션 요약 비유**: 리엔지니어링은 낡은 자동차의 엔진만 교체하는 것, 완전 재개발은 새 차 구매, 유지보수는 기름·필터 교체다. 상황에 맞는 전략이 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 레거시 COBOL → Java 마이그레이션
- [역공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/029_reverse_engineering/)으로 COBOL 비즈니스 로직 추출 → [UML](/knowledge-base/studynote/04_software_engineering/04_testing_quality/232_uml_unified_modeling_language_overview/) 다이어그램 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/).
- 자동화 도구(Micro Focus, IBM Rational) 활용.
- 점진적 마이그레이션: 모듈별 Java 재구현 → 스트랭글러 패턴 적용.

### [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 지원 리엔지니어링
- GitHub Copilot: 레거시 코드 설명 자동 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/), 현대 언어로 변환 제안.
- [LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/): COBOL → Java, C → Python 자동 번역 (90%+ 정확도).

- **📢 섹션 요약 비유**: [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 코드 마이그레이션은 자동 번역기다. 옛날 언어(COBOL)로 쓰인 소설을 현대 언어(Java)로 자동 번역하되, 내용(비즈니스 로직)은 그대로 유지한다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/">기술 부채</a> 해소</strong> | 레거시 아키텍처 현대화 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/">유지보수성</a> 향상</strong> | 코드 구조 개선, 문서화 |
| **비용 절감** | 완전 재개발 대비 저비용 |

GenAI 기반 코드 마이그레이션 도구(Amazon Q, IBM WCA)는 대규모 레거시 코드베이스를 자동으로 분석하고 현대 언어·아키텍처로 변환하는 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 리엔지니어링 플랫폼으로 발전하고 있다.

- **📢 섹션 요약 비유**: [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 리엔지니어링은 자동 도시 재개발 AI다. 낡은 건물(레거시 코드)의 구조도를 분석하고, 현대 건축 기준(현대 언어·아키텍처)에 맞게 자동으로 재설계안을 제시한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/04_software_engineering/01_overview_principles/029_reverse_engineering/">역공학</a></strong> | 리엔지니어링의 이해 단계 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/310_strangler_fig_pattern/">스트랭글러 피그</a></strong> | 점진적 레거시 교체 패턴 |
| <strong><a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/">기술 부채</a></strong> | 리엔지니어링의 해결 대상 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/">마이크로서비스</a></strong> | 리엔지니어링의 목표 아키텍처 |
| **GenAI 마이그레이션** | [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 자동 코드 변환 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">레거시 시스템 — 기술 부채 누적, 유지보수 어려움</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">역공학 — 코드에서 설계·요구사항 추출</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">재구조화/마이그레이션 — 현대 언어·아키텍처로 전환</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">스트랭글러 피그 — 점진적 마이크로서비스 교체</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">AI 리엔지니어링 — LLM 기반 자동 코드 변환</div></div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. 리엔지니어링은 낡은 집 리모델링이에요! 집을 허물고 새로 짓는 대신, 기초(비즈니스 로직)를 살리면서 내부만 새것으로 바꿔요.
2. [스트랭글러 피그 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/376_strangler_fig_summary/)은 새 나무가 기존 나무를 감싸며 서서히 대체하는 것처럼, 기존 서비스를 하나씩 새 코드로 바꿔나가요!
3. AI가 COBOL 코드를 Java로 자동 번역해주는 시대가 됐어요 — 기술자들이 직접 하던 어려운 작업을 AI가 도와준답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 28 / 973

← **이전**: [27. 변경 관리 (Change Management) — 소프트웨어 변경의 체계적 통제](/knowledge-base/studynote/04_software_engineering/01_overview_principles/027_change_management/)
**다음**: [29. 역공학 (Reverse Engineering)](/knowledge-base/studynote/04_software_engineering/01_overview_principles/029_reverse_engineering/) →

---
