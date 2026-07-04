---
title: "TOGAF ADM (TOGAF ADM)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 298
---

# 📖 【암기용】 개념 완전 이해

> 목적: TOGAF ADM의 단계별 절차와 반복(iteration) 구조를 처음 봐도 완전히 이해하게 만든다. 233번 TOGAF 문서가 프레임워크 전체(ADM+Architecture Content+Governance) 구성을 다룬다면, 이 문서는 **ADM 자체의 단계 진행·반복 메커니즘**에 집중해 차별화한다.

## 한눈에
- **개요**: TOGAF ADM(Architecture Development Method)은 **엔터프라이즈 아키텍처(EA)**를 Preliminary부터 H단계까지 순서대로, 필요하면 되돌아가며 반복 수립하는 **원형(cyclic) 단계 절차**이다.
- **왜 필요한가**: EA는 범위가 너무 넓어 "어디서부터 손대야 하는가"가 항상 문제다. ADM은 그 순서(비전→업무→정보시스템→기술→전환계획→거버넌스)를 표준화해 프로젝트마다 절차를 재발명하지 않게 한다.
- **핵심 직관**: ADM은 한 바퀴 돌면 끝나는 직선 절차가 아니라, 중심에 Requirements Management를 둔 **원형 시계**다. A~H는 시계 눈금이고, 요구사항 변경이 생기면 중심을 거쳐 관련 눈금으로 되돌아가 재작업한다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| EA (Enterprise Architecture) | ADM이 만들어내는 결과물 — 업무·데이터·응용·기술을 아우르는 전사 설계도 | 도시 전체 마스터플랜 |
| ADM (Architecture Development Method) | EA를 만드는 표준 절차(Preliminary + A~H) | 마스터플랜을 그리는 작업 순서표 |
| Requirements Management | 원 중심에서 전 단계 요구사항을 계속 추적·통제하는 상시 활동(고유 phase 번호 없음) | 시계 중심축 — 모든 바늘이 여기를 기준으로 돈다 |
| Preliminary | 원칙·범위·거버넌스 프레임을 준비하는 0단계 | 공사 착수 전 인허가·규정 확인 |
| Phase A (Architecture Vision) | 이해관계자 합의, 사업 목표, 상위 범위 확정 | 리모델링 전 "무엇을 왜 바꾸는가" 합의서 |
| Phase B (Business Architecture) | 업무 프로세스·조직·역량의 현행/목표 정의 | 부서 배치도 |
| Phase C (Information Systems Architecture) | 데이터+애플리케이션 아키텍처(현행/목표) | 배관·전선 설계도 |
| Phase D (Technology Architecture) | 인프라·플랫폼 기술 구조(현행/목표) | 건물 골조·설비 사양 |
| Phase E (Opportunities & Solutions) | B~D의 gap을 묶어 solution building block·실행 패키지로 그룹화 | 공사 항목을 발주 단위로 묶기 |
| Phase F (Migration Planning) | 실행 패키지에 우선순위·일정·비용을 부여해 로드맵 확정 | 웨이브별 공사 일정표 |
| Phase G (Implementation Governance) | 실제 구현 프로젝트가 목표 아키텍처를 지키는지 준수 심의 | 감리 |
| Phase H (Architecture Change Management) | 완료 후 변경 요청을 평가해 새 ADM 사이클 착수 여부 결정 | 준공 후 리모델링 요청 접수창구 |
| Gap Analysis | 현행(Baseline)과 목표(Target) 아키텍처를 항목별로 대조해 빠지거나 달라진 부분을 표로 뽑는 기법 | 이사 전 체크리스트 대조 |
| Iteration(반복) | Preliminary~H를 한 번에 완주하지 않고, 필요한 범위만 좁혀 여러 번 도는 것(4가지 유형) | 리모델링을 방 하나씩 여러 번 도는 것 |

## 깊이 이해

### 왜 원형(cycle)인가 — 직선 절차의 한계
- 전통적 SDLC처럼 A→B→C→D를 한 번에 끝까지 밀고 나가면, D단계(기술 구조)에서 발견한 제약이 B단계(업무 설계)를 다시 바꿔야 하는 상황을 받아내지 못한다.
- ADM은 그래서 Preliminary~H를 하나의 **원(cycle)**으로 그리고, 중심에 Requirements Management를 둔다. 어느 단계에서든 새 요구사항·제약이 나오면 중심을 거쳐 관련 단계로 되돌아간다 — H단계(변경관리)에서 나온 변경 요청이 다시 Preliminary/A로 이어져 다음 사이클을 여는 것이 대표 사례다.

### Gap Analysis를 숫자로 이해하기
- 절차: 현행(Baseline) 구성요소 목록과 목표(Target) 구성요소 목록을 같은 항목 축으로 늘어놓고 4가지로 분류한다 — ① 유지(현행=목표) ② 폐기(현행에만 존재) ③ 신규(목표에만 존재) ④ 변경(둘 다 존재하나 속성이 다름).
- **예시**: 고객 데이터 플랫폼 전환 프로젝트에서 애플리케이션 축을 정리했더니 현행 12개, 목표 9개 애플리케이션이 나왔다. 대조 결과 유지 5개, 폐기 7개(레거시 CRM 등), 신규 4개(고객 360 API 등)로 분류됐다. 이 표가 Phase E의 solution building block 묶음의 입력이 된다.
- gap이 없는 축(현행=목표)은 더 반복할 필요가 없고, gap이 가장 많은 축(위 예시에서는 애플리케이션)이 Migration Planning에서 1순위가 된다.

### Phase E~F: gap을 실행 로드맵으로 바꾸는 계산
- Phase E는 gap 항목들을 "함께 바꿔야 실익이 나는" 단위(work package)로 묶는다. 예: 레거시 CRM 폐기 + 고객 360 API 신규 + 고객 데이터 통합은 서로 의존하므로 하나의 work package로 묶인다.
- Phase F는 work package에 비용·리스크·의존성을 매겨 우선순위를 정하고 마이그레이션 웨이브(wave)로 나눈다. 예: 18개월 전환 계획을 6개월 단위 3개 웨이브로 나누고, 의존성이 없는 신규 API부터 웨이브 1에 배치해 리스크를 낮춘다.

### Iteration의 4가지 유형 — "매번 A~H를 다 돌지 않는다"
- **Architecture Capability iteration**: Preliminary~Vision을 반복해 EA 조직·원칙 자체를 성숙시킨다.
- **Architecture Development iteration**: B~D(업무·정보시스템·기술)를 반복해 목표 아키텍처 상세도를 높인다.
- **Transition Planning iteration**: E~F를 반복해 로드맵을 구체화한다.
- **Architecture Governance iteration**: G~H를 반복해 구현 프로젝트를 감리·통제한다.
- "한 번 사이클을 완주해야 다음 프로젝트를 시작할 수 있다"는 오해가 흔하지만, 실제로는 이미 확정된 Vision(A) 위에서 B~D만 여러 번 도는 식으로 조직·프로젝트 상황에 맞게 범위를 좁혀 반복한다(233의 tailoring 개념과 연결).

### 왜 답안에서 "단계 명칭 나열"이 감점인가
- ADM 문제의 채점 포인트는 phase 이름 암기가 아니라 "Requirements Management가 중심에서 전 단계를 통제한다"는 원형 구조 이해와, "gap → work package → 로드맵" 흐름을 수치로 설명할 수 있는가이다. 이름만 나열하면 절차를 이해하지 못했다는 신호로 읽힌다.

## 연결 개념
- 233 TOGAF (상위 개념 — TOGAF 프레임워크 전체 중 ADM은 절차 축, Architecture Content·Governance는 별도 축)
- Architecture Repository — ADM 각 단계 산출물이 축적되는 저장소
- Architecture Governance (Phase G/H) — 구현 프로젝트의 목표 아키텍처 준수를 심의하는 별도 상시 체계

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. ADM 단계 암기보다 현행·목표·전환계획·거버넌스를 연결한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: TOGAF ADM은 기업 아키텍처를 수립하고 전환하며 변경을 관리하는 반복형 방법론이다.
> 2. **가치**: 비즈니스 목표와 IT 투자, 표준, 데이터, 애플리케이션, 기술 로드맵을 하나의 거버넌스로 정렬한다.
> 3. **판단 포인트**: As-Is/To-Be gap, migration roadmap, architecture board가 없으면 단계 나열에 그친다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| EA 방법론 이해 확인 | ADM phases, Architecture Vision, gap analysis | A~H 단계 명칭만 나열 |
| 전환 계획 수립 역량 확인 | roadmap, work package, dependency, governance | 목표 아키텍처 작성 후 구현 계획 누락 |
| IT 거버넌스 판단 확인 | Architecture Board, compliance review, change management | 프로젝트 방법론과 혼동 |

> 요약: 이 문제는 ADM 절차를 통해 전략 정렬, 전환 계획, 준수 통제를 어떻게 수행하는지 묻는다.

---

## Ⅰ. 개요 및 필요성

- 개요: TOGAF ADM은 기업 아키텍처 수립·전환 절차이다.
- 배경: 부서별 시스템 최적화는 중복 투자와 데이터 불일치를 만든다.
- 필요성: 비즈니스, 데이터, 애플리케이션, 기술 아키텍처를 통합해 목표 구조와 전환 로드맵을 관리해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Preliminary -> Architecture Vision -> Business/Data/Application/Technology Architecture
             -> Opportunities/Solutions -> Migration Planning -> Implementation Governance -> Change Management
             / Requirements Management
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Preliminary | 원칙·범위·거버넌스 정의 | architecture board 구성 |
| Architecture Vision | 목표와 이해관계자 합의 | business case 포함 |
| BDAT Architecture | 업무·데이터·앱·기술 구조 정의 | As-Is/To-Be gap 분석 |
| Migration/Governance | 전환 계획·준수 검토 | work package, compliance |

> 요약: ADM은 요구사항 관리를 중심에 두고 비전, BDAT 정의, 전환 계획, 구현 거버넌스를 반복한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
전략 요구 수집 -> 현행 분석 -> 목표 아키텍처 정의 -> gap 도출 -> 로드맵 수립 -> 구현 준수 검토 -> 변경 반영
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 경영 전략·규제·업무 요구 수집 | 이해관계자 승인 |
| 2 | As-Is/To-Be BDAT 모델 작성 | gap 목록 100% 추적 |
| 3 | 솔루션 후보와 migration roadmap 수립 | 의존성·우선순위 명시 |
| 4 | 구현 프로젝트 준수 검토와 변경 관리 | compliance waiver 관리 |

> 요약: 동작은 요구에서 목표 아키텍처와 gap을 도출하고, 로드맵과 준수 검토로 실행을 통제한다.

---

## Ⅳ. 특징

| 구분 | 프로젝트 단위 설계 | TOGAF ADM | 수치·판단 기준 |
|:---|:---|:---|:---|
| 범위 | 단일 시스템 | 기업 BDAT 전 영역 | 사업부 2개 이상 영향 |
| 기준 | 프로젝트 요구 | 아키텍처 원칙·표준 | 표준 준수율 90% 이상 |
| 실행 | 구현 중심 | 로드맵·거버넌스 포함 | work package 추적 |
| 한계 | 적용 가벼움 | 산출물 관리 부담 | 핵심 산출물 10개 내외로 조정 |

> 요약: ADM은 프로젝트 설계를 기업 전환 계획으로 확장하지만, 산출물 범위를 조직 규모에 맞춰 조정해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 개별 시스템 아키텍처 | 기업 아키텍처 ADM | 전사 데이터·애플리케이션 정합성 필요 |
| 비용/성능 | 초기 문서 적음 | EA 조직·저장소 필요 | 중복 시스템 비용 연 10% 이상 |
| 운영/위험 | 표준 위반 사후 발견 | architecture compliance review | 규제·감사 대상 조직 |

> 요약: 전사 정렬과 규제 준수가 필요한 조직은 프로젝트 설계보다 ADM 기반 EA 거버넌스가 적합하다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 문서 과다 | 모든 산출물 동일 수준 작성 | tailoring, 핵심 산출물 정의 | 산출물 승인 소요 |
| 실행 단절 | 로드맵과 예산 미연계 | portfolio governance 연동 | roadmap 실행률 |
| 현행화 실패 | 변경관리 부재 | architecture repository, review cycle | 모델 최신성 90% 이상 |

> 요약: ADM 실패는 문서 과다, 실행 단절, 현행화 실패에서 발생하며 tailoring과 포트폴리오 연계가 필요하다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 전략 정렬 | 투자 과제 100% 목표 아키텍처 매핑 | portfolio review |
| 표준 준수 | compliance pass 90% 이상 | architecture board 기록 |
| 전환 실행 | roadmap milestone 준수 85% 이상 | PMO 리포트 |

> 요약: 성공 여부는 전략 매핑, 표준 준수율, 로드맵 실행률로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. Preliminary 단계에서 architecture principle 10개 이하, 표준 기술목록, Architecture Board 승인 절차를 정의
2. BDAT별 As-Is/To-Be와 gap을 작성하고 work package 단위로 dependency, 비용, 위험, 우선순위 산정
3. 구현 프로젝트 gate마다 compliance review를 수행하고 waiver는 만료일·대체 통제·재심사 조건과 함께 관리

**결론 (2줄):**
- 기술사 판단: 전사 전환·규제·중복투자 이슈가 있는 조직은 TOGAF ADM을 적용하고, 단일 서비스 개선은 경량 ADR·C4로 축소
- 향후 방향: EA repository와 CMDB·cloud inventory를 연결해 목표 아키텍처와 실제 운영 상태의 차이를 주기적으로 측정해야 함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "설명하시오", "기술하시오" | ADM 단계와 요구사항 관리 흐름 | 프로젝트 설계와 EA 방법론 차이 |
| 요구사항 명시형 | "방안을 제시하시오", "설계하시오", "비교하시오" | gap 분석, migration roadmap, compliance review | 산출물 tailoring, 실행 지표 |

> 요약: 설명형은 ADM 전체 흐름, 방안형은 gap 기반 전환계획과 거버넌스를 중심으로 전환한다.
