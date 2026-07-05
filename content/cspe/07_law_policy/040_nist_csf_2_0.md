---
title: "NIST Cybersecurity Framework 2.0 (NIST CSF 2.0)"
date: "2026-07-01"
tags:
  - "cspe-law-policy"
weight: 40
---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **NIST Cybersecurity Framework 2** | NIST Cybersecurity Framework 2.0 (NIST CSF 2.0)의 핵심 개념 | 이 주제의 본질 |

---

# 📖 【암기용】 개념 완전 이해

> 목적: NIST CSF 2.0을 처음 봐도 왜 Govern 기능이 추가됐고 조직이 이 프레임워크로 무엇을 판단하는지 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 조직의 사이버보안 리스크를 Govern·Identify·Protect·Detect·Respond·Recover 6개 기능으로 관리하도록 미국 NIST가 제시한 자율 채택형 프레임워크
- **왜 필요한가**: 조직마다 보안 통제 수준과 용어가 달라 경영진·실무자·감사자 간 소통이 어렵다. CSF는 공통 언어와 Profile·Tier로 현재 수준과 목표 수준을 비교 가능하게 만든다.
- **핵심 직관**: 회사 건강검진표처럼 6개 항목(거버넌스·식별·보호·탐지·대응·복구) 점수를 매겨 현재 상태와 목표 상태의 차이를 보는 구조다.

## 깊이 이해
- **배경·문제의식**: 2014년 CSF 1.0은 미국 대통령령(EO 13636)에 따라 critical infrastructure(전력, 금융 등) 보호 목적으로 만들어졌다.
- 2018년 1.1은 공급망 리스크 관리 항목을 보강했지만 핵심 기능은 Identify·Protect·Detect·Respond·Recover 5개로 유지됐다.
- 2024년 2월 발표된 CSF 2.0은 이 5개 기능에 **Govern을 신규 추가**해 6개 기능 체계로 바뀌었다.
- CSF 2.0은 적용 대상도 critical infrastructure 중심에서 규모·업종 불문 모든 조직으로 넓혔다.
- **작동 원리**: Functions 아래 Categories, 그 아래 Subcategories로 계층화하고 각 Subcategory에 ISO 27001, COBIT 같은 표준을 매핑한 Informative References를 제공한다.
- 조직은 현재 이행 수준을 Current Profile로, 목표 수준을 Target Profile로 문서화하고 두 Profile의 gap을 개선 계획으로 삼는다.
- Tier(Partial, Risk Informed, Repeatable, Adaptive)는 리스크 관리 프로세스의 엄격도를 설명하는 지표이며 조직 성숙도를 서열화하는 점수표가 아니다.
- **비유**: Govern은 병원 경영진이 정하는 진료 방침이고, 나머지 5개 기능은 그 방침에 따라 움직이는 접수·검진·진단·처치·회복 부서다.
- **구체 예시**: Govern 예시 — 이사회가 연 1회 사이버 리스크 appetite를 승인하고 공급망 3rd party 보안 요건을 계약에 반영한다.
- Identify 예시 — 자산 대장에 서버 500대, 주요 데이터 흐름 20건을 등록하고 위험도를 상/중/하로 분류한다.
- Protect 예시 — 전 직원 phishing 모의훈련을 분기 1회 실시하고 특권 계정에 MFA를 강제한다.
- **흔한 오해·주의점**: CSF 2.0을 "5개에서 6개로 기능만 늘어난 개정판"으로 암기하면 안 되고, Govern이 다른 5개 기능을 총괄하는 상위 축으로 재편됐다는 구조 변화가 핵심이다.
- Tier는 성숙도 모델(CMMI)과 다르다. Tier가 높다고 보안 수준이 자동으로 우수한 것이 아니라 리스크 관리 프로세스의 반복성·적응성을 설명할 뿐이다.
- CSF는 강제 규제(mandatory regulation)가 아니라 자율 채택 프레임워크이며, 특정 통제를 이행했다고 법적 컴플라이언스를 보장하지 않는다.

## 연결 개념
- ISO/IEC 27001 — 정보보안경영시스템(ISMS) 인증 기반의 유사 통제 프레임워크
- NIST AI RMF — AI 시스템 신뢰성·리스크 관리에 특화된 자매 프레임워크
- 공급망 리스크 관리(C-SCRM) — CSF 2.0 Govern 기능에서 강화된 3rd party·벤더 리스크 통제 영역
---
# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: NIST CSF 2.0 답안은 Govern 신규 추가 배경, 6개 기능 구조, Profile·Tier 활용법, 적용 범위 확대를 함께 제시한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: NIST CSF 2.0은 사이버보안 리스크 관리를 Govern·Identify·Protect·Detect·Respond·Recover 6개 기능으로 조직화한 자율 채택 프레임워크이다.
> 2. **가치**: Current Profile과 Target Profile 비교로 조직 간·부서 간 보안 수준을 공통 언어로 진단하고 gap을 개선 우선순위로 전환한다.
> 3. **판단 포인트**: 2018년 1.1의 5개 기능 대비 2024년 2.0은 Govern을 신규 추가해 거버넌스가 나머지 5개 기능을 총괄하는 구조로 재편됐다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 1.1 대비 2.0 변화 이해 확인 | Govern 기능 신규 추가, 적용 대상 확대 | 5개 기능만 나열하고 Govern 누락 |
| 프레임워크 구조 이해 확인 | Functions-Categories-Subcategories, Informative References | 단순 체크리스트로 오설명 |
| 실무 활용법 이해 확인 | Current/Target Profile, Tier의 의미와 한계 | Tier를 성숙도 서열(CMMI)로 혼동 |

> 요약: 이 문제는 6개 기능 나열보다 Govern 신규 추가 배경과 Profile·Tier 활용 판단력을 보여야 한다.
---
## Ⅰ. 개요 및 필요성

- 개요: 조직 사이버보안 리스크를 6개 기능으로 관리하는 NIST 자율 프레임워크
- 배경: 2014년 1.0은 critical infrastructure 보호 목적, 2018년 1.1은 공급망 리스크 보강, 2024년 2월 2.0은 Govern 신규 추가와 전 조직 적용 확대
- 필요성: 조직·산업 간 보안 수준 비교 언어 부재 문제를 Current/Target Profile과 4단계 Tier로 해결
---
## Ⅱ. 구조 및 구성요소

```text
Govern (조직 리스크 전략/역할/정책/공급망 감독)
  -> Identify (자산관리, 위험평가, 업무환경 이해)
  -> Protect (접근통제, 인식교육, 데이터보안, 보호기술)
  -> Detect (이상징후/이벤트 탐지, 지속 모니터링)
  -> Respond (대응계획, 커뮤니케이션, 완화조치)
  -> Recover (복구계획, 개선, 커뮤니케이션)
  -> Informative References (ISO 27001, COBIT 매핑)
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Govern | 리스크 관리 전략, 역할·책임, 정책, 공급망 리스크 감독 | 2.0에서 신규 추가된 6번째 기능 |
| Categories/Subcategories | 기능을 세부 통제 항목으로 분해 | 각 항목에 Informative References 매핑 |
| Current Profile | 현재 이행 중인 통제 상태 문서화 | 조직별 실제 구현 수준 반영 |
| Target Profile | 목표로 하는 통제 상태 문서화 | 경영진 리스크 appetite 반영 |
| Tier | 리스크 관리 프로세스의 반복성·적응성 수준 | Partial/Risk Informed/Repeatable/Adaptive 4단계 |

> 요약: CSF 2.0은 Govern이 나머지 5개 기능을 총괄하는 구조로 Categories·Subcategories와 Informative References를 통해 다른 표준과 연결된다.
---
## Ⅲ. 동작원리 및 흐름도

```text
조직 컨텍스트 파악 -> Govern 정책/리스크 전략 수립
  -> Identify 자산·위험 목록화 -> Current Profile 작성
  -> Target Profile 설정 -> Gap 분석
  -> Protect/Detect/Respond/Recover 통제 이행
  -> Tier 평가 -> 개선 계획 갱신
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | Govern 단계에서 리스크 appetite와 역할·책임을 이사회가 승인 | 승인 문서, 검토 주기(연 1회 이상) |
| 2 | Identify 단계에서 자산·데이터 흐름·3rd party 목록을 작성 | 자산 등록률, 위험도 분류 완료율 |
| 3 | Current Profile과 Target Profile을 비교해 gap을 도출 | Subcategory별 미이행 항목 수 |
| 4 | Protect~Recover 통제를 이행하고 Tier로 프로세스 성숙도를 평가 | Tier 단계 상승 여부, 사고 대응 훈련 횟수 |
| 5 | 개선 결과를 재평가하고 Profile을 갱신 | 재평가 주기, 잔여 gap 감소율 |

> 요약: CSF 2.0은 Govern 정책 수립을 출발점으로 Profile gap 분석과 Tier 평가를 반복하는 순환 구조다.
---
## Ⅳ. 특징

| 구분 | CSF 1.1 (2018) | CSF 2.0 (2024) | 수치·표준 포인트 |
|:---|:---|:---|:---|
| 핵심 기능 수 | 5개 (Identify~Recover) | 6개 (Govern 신규 추가) | 발표 시점 2024년 2월 |
| 적용 대상 | critical infrastructure 중심 | 규모·업종 불문 전 조직 | EO 13636 기반에서 범용화 |
| 공급망 리스크 | 1.1에서 항목 일부 보강 | Govern 내 공급망 리스크 관리 명시적 강화 | C-SCRM 서브카테고리 확대 |
| 구조 표기 | Functions-Categories-Subcategories | 동일 구조 유지, Community Profile 확대 | Informative References ISO 27001/COBIT 매핑 |

> 요약: 1.1 대비 2.0의 핵심 차이는 기능 개수(5->6)와 Govern 신설, 적용 대상의 전 조직 확대다.
---
## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 (ISO 27001) | 본 키워드 (NIST CSF 2.0) | 선택 기준 |
|:---|:---|:---|:---|
| 인증 여부 | 제3자 인증 취득 가능 | 인증 제도 없음, 자가 진단 중심 | 고객·규제기관이 인증서를 요구하면 ISO 27001 병행 |
| 구조 | ISMS PDCA 사이클, Annex A 통제 | 6개 Function 기반 Profile/Tier | 경영진 리스크 소통 언어가 필요하면 CSF 우선 |
| 상호 운용성 | 국제 표준으로 해외 거래에 유리 | Informative References로 ISO 27001 매핑 가능 | 두 프레임워크를 배타적으로 보지 않고 병행 매핑 |

> 요약: ISO 27001은 인증 취득이 필요할 때, CSF 2.0은 경영진 리스크 소통과 Profile 비교가 필요할 때 우선 적용한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Govern 형식화 | 이사회 승인이 서류상 절차로만 존재 | 리스크 appetite 검토를 분기 1회 안건으로 고정 | 이사회 안건 상정 횟수 |
| Profile 갱신 지연 | Current/Target Profile을 1회성 문서로 방치 | 연 1회 이상 재평가 주기를 정책에 명시 | Profile 최종 갱신일 |
| 공급망 gap | 3rd party 보안 요건 계약 누락 | 신규 벤더 계약에 C-SCRM 조항 포함 | 계약서 내 보안조항 포함률 |

> 요약: CSF 2.0 운영 리스크는 Govern의 형식화와 Profile 방치이므로 주기적 재평가 지표로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| Profile gap 해소율 | Target 대비 미이행 Subcategory 감소 추세 | 연 1회 Current Profile 재작성 비교 |
| Tier 상승 여부 | Risk Informed 이상 유지 | 내부 감사, 리스크 관리 프로세스 검토 |
| 공급망 통제 반영률 | 신규 계약 내 C-SCRM 조항 포함 | 계약 검토 체크리스트 |

> 요약: 도입 성공 여부는 Profile gap 감소, Tier 유지·상승, 공급망 조항 반영률로 판단한다.
---
## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. Govern 단계에서 이사회 승인 리스크 appetite와 역할·책임을 문서화하고 분기 1회 검토함
2. Identify~Recover 5개 기능별 Current Profile을 작성하고 Target Profile과의 gap을 우선순위화함
3. 공급망 3rd party 계약에 C-SCRM 조항을 반영하고 Informative References로 ISO 27001 통제와 매핑함

**결론 (2줄):**
- 기술사 판단: CSF 2.0의 핵심은 Govern 신규 추가로 거버넌스가 나머지 5개 기능을 총괄하는 구조 전환이며 전 조직 적용 확대가 동반됨
- 향후 방향: NIST AI RMF, ISO 27001과의 Informative References 매핑을 확장해 조직 내 다중 프레임워크 통합 관리 체계로 발전해야 함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "NIST CSF 2.0을 설명하시오" | 6개 기능 흐름, Profile 작성 절차 | 1.1 대비 Govern 신규 추가와 적용 대상 확대 |
| 요구사항 명시형 | "CSF 2.0 도입 방안을 제시하시오" | 이사회 승인, gap 분석, Tier 평가 절차 | 공급망 리스크 통제와 확인 지표 |

> 요약: 설명형은 6개 기능 구조, 방안형은 Profile·Tier 기반 이행 절차와 지표 중심으로 답안 축을 바꾼다.
