+++
title = "55. Zachman Framework"
date = 2026-05-01

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Zachman Framework는 기업 아키텍처의 모든 산출물을 '질문 축(What/How/Where/Who/When/Why)'과 '관점 축(Planner/Owner/Designer/Builder/Subcontractor/Enterprise)'의 6×6 매트릭스로 체계화하는 분류 체계(Ontology)다.
> 2. **가치**: 복잡한 기업 시스템을 바라보는 모든 이해관계자의 관점을 구조화하여 산출물 누락을 방지하고, 다양한 관점 간 일관성을 유지할 수 있다.
> 3. **판단 포인트**: Zachman은 절차가 아니라 분류 체계다. "무엇을 만들어야 하는가"를 정리하는 틀이지, "어떻게 만드는가"의 방법론이 아니다. TOGAF ADM 같은 방법론과 함께 사용할 때 완전해진다.

---

## Ⅰ. 개요 및 필요성

1987년 IBM의 존 자크만 (John Zachman)이 발표한 논문 "A Framework for Information Systems Architecture"에서 최초로 제안된 이 프레임워크는, 수십 년이 지난 현재도 기업 아키텍처(EA: Enterprise Architecture) 분야에서 가장 기본적인 분류 체계로 인정받고 있다.

기업 정보 시스템은 극도로 복잡하다. 비즈니스 전략, 데이터, 애플리케이션, 기술 인프라가 얽혀 있고, 보는 관점마다 요구사항이 다르다. CEO가 원하는 시스템과 DBA가 설계하는 데이터베이스, 개발자가 구현하는 코드 — 이 세 관점이 일관성을 유지하려면 공통 분류 체계가 필요하다.

Zachman Framework는 이 문제를 6×6 매트릭스로 해결한다. 행(Row)은 이해관계자의 관점을 나타내고, 열(Column)은 '무엇을, 어떻게, 어디서, 누가, 언제, 왜'라는 근본적 질문을 나타낸다. 각 셀(Cell)은 특정 관점에서 특정 질문에 대한 답변으로 구성된 하나의 아키텍처 산출물이다.

이 프레임워크를 사용하면 전체 기업 아키텍처에서 누락된 산출물을 한눈에 파악할 수 있고, 서로 다른 관점 간의 연결 관계를 체계적으로 관리할 수 있다.

- **📢 섹션 요약 비유**: Zachman Framework는 큰 도서관의 듀이 십진분류법(DDC)과 같다. 어떤 책(산출물)이 어느 선반(셀)에 있어야 하는지 체계적으로 정의하여, 찾기 쉽고 빠짐없이 관리할 수 있게 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Zachman 6×6 매트릭스 구조

```text
         What       How        Where      Who        When       Why
         (Data)     (Function) (Network)  (People)   (Time)     (Motivation)

Planner  목록       프로세스   위치 목록  조직 목록  이벤트 목록 목표 목록
(범위)   (엔터티)   (비즈니스) (노드)     (단위)     (주기)      (전략)

Owner    개념모델   비즈니스   물류네트   업무모델   마스터     비즈니스
(개념)   (ERD 초안) 프로세스   워크        (조직도)   스케줄     규칙

Designer 논리모델   애플리케   분산       인터페이   처리구조   비즈니스
(논리)   (관계형DB) 이션 구조  아키텍처   스 설계    (workflow) 규칙 설계

Builder  물리 모델  시스템     기술       프레임워   컨트롤     규칙
(물리)   (DDL)      설계       아키텍처   크 설계    구조       명세서

Sub-     데이터     프로그램   네트워크   사용자     타이밍     규칙
contractor 정의    (코드)     아키텍처   인터페이스 정의       정의
(구현)

Enter-   실데이터   실 함수    실 네트워  실 조직    실 일정    실 목표
prise    (인스턴스) (실행중)   크(실구축) (실운영)   (실수행)   (실동작)
(동작)
```

### 6가지 관점 축 (행)

| 관점 | 영문 | 대표 이해관계자 | 관심사 |
|:---|:---|:---|:---|
| Planner (범위) | Executive | CEO, 이사회 | 비즈니스 전략, 범위 정의 |
| Owner (개념) | Business Management | 사업부장, 업무 담당자 | 업무 개념, 비즈니스 규칙 |
| Designer (논리) | Architect | 시스템 아키텍트 | 논리적 설계, 구조 결정 |
| Builder (물리) | Engineer | 개발자, DBA | 물리적 구현, 기술 선택 |
| Subcontractor (구현) | Technician | 외주 개발자, 설치 담당 | 상세 코드, 물리적 구축 |
| Enterprise (동작) | Worker | 운영자, 사용자 | 실제 운영 데이터, 실행 |

### 6가지 질문 축 (열)

| 질문 | 영문 | 아키텍처 도메인 | 예시 산출물 |
|:---|:---|:---|:---|
| What | Data | 데이터 아키텍처 | ERD, 데이터 사전, DDL |
| How | Function | 애플리케이션 아키텍처 | 프로세스 맵, 시스템 구조도 |
| Where | Network | 기술 아키텍처 | 네트워크 다이어그램, 토폴로지 |
| Who | People | 조직 아키텍처 | 조직도, RACI, 역할 정의 |
| When | Time | 일정 아키텍처 | 마스터 스케줄, 이벤트 순서 |
| Why | Motivation | 비즈니스 동기 | 전략 목표, KPI, 비즈니스 규칙 |

### 핵심 원칙: 각 셀은 독립적

Zachman 프레임워크의 중요한 원칙은 각 셀이 고유하고 독립적이라는 것이다.
- 동일한 행의 셀들은 같은 관점에서 바라본 다른 측면이다.
- 동일한 열의 셀들은 같은 주제를 다른 추상화 레벨에서 다룬다.
- 각 셀의 산출물은 인접 셀과 일관성을 유지해야 하지만, 내용은 독립적이다.

- **📢 섹션 요약 비유**: 같은 집을 다양한 전문가(건축사, 전기기사, 배관공, 인테리어 디자이너)가 각자의 도면으로 표현하는 것과 같다. 도면의 종류(전기도, 배관도, 구조도)와 수준(개념도, 시공도, 준공도)이 교차하여 완전한 설계 문서가 된다.

---

## Ⅲ. 비교 및 연결

### Zachman Framework vs 다른 EA 프레임워크

| 비교 항목 | Zachman | TOGAF | FEAF | DoDAF |
|:---|:---|:---|:---|:---|
| 성격 | 분류 체계 (Ontology) | 방법론 | 방법론 | 방법론 |
| 목적 | 산출물 분류·누락 방지 | 아키텍처 개발 절차 | 연방 정부 IT | 국방 아키텍처 |
| 절차 | 없음 | ADM (9단계) | 있음 | 있음 |
| 거버넌스 | 정의 안 함 | 강력히 포함 | 포함 | 포함 |
| 강점 | 전체 조망, 누락 방지 | 실행 가이드 | 정부 호환성 | 군사 복잡계 |
| 약점 | 방법론 없음 | 무거운 절차 | 적용 범위 제한 | 민간 적용 어려움 |
| 함께 사용 | TOGAF와 보완적 | Zachman으로 산출물 분류 | - | - |

### Zachman + TOGAF 통합 활용

실무에서 Zachman과 TOGAF는 보완적으로 사용된다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">TOGAF ADM (Architecture Development Method):</div>
<div class="kb-diagram-note">Preliminary → Vision → Business → Data → Application → Technology → Migration</div>
<div class="kb-diagram-note">Zachman과의 연계:</div>
<div class="kb-diagram-tree-item" style="--depth:2">Business Architecture (Phase B) → Zachman의 Owner 행</div>
<div class="kb-diagram-tree-item" style="--depth:2">Data Architecture (Phase C) → Zachman의 What 열</div>
<div class="kb-diagram-tree-item" style="--depth:2">Application Architecture (Phase C) → Zachman의 How 열</div>
<div class="kb-diagram-tree-item" style="--depth:2">Technology Architecture (Phase D) → Zachman의 Where 열</div>
<div class="kb-diagram-note">결론:</div>
<div class="kb-diagram-note">TOGAF ADM이 "어떻게 아키텍처를 개발하는가"를 정의하고,</div>
<div class="kb-diagram-note">Zachman이 "어떤 산출물이 있어야 하는가"를 분류한다.</div>
</div>
</div>



- **📢 섹션 요약 비유**: Zachman은 서랍장 라벨 체계(무엇이 어디에 있는가 분류), TOGAF는 서랍을 정리하는 청소 절차(어떻게 정리하는가 방법)다. 두 가지가 함께 있어야 체계적으로 정리된 서랍장이 완성된다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 설계 판단 체크리스트

1. **모든 36개 셀이 정의 가능한가?**: 대규모 EA 프로젝트에서는 36개 셀 각각에 최소한 어떤 산출물이 있어야 하는지 목록을 만들어야 한다.
2. **상위 관점과 하위 관점 간 일관성이 있는가?**: Owner 행의 개념 모델이 Builder 행의 물리 모델과 충돌하지 않는지 검토한다.
3. **누락된 셀이 있는가?**: 특정 관점(예: Subcontractor 행)이나 특정 질문(예: When 열)이 완전히 비어 있다면 아키텍처의 공백이다.
4. **도구와 방법론이 Zachman과 연계되어 있는가?**: UML, ERD, ArchiMate 같은 도구의 다이어그램이 Zachman의 어느 셀에 해당하는지 매핑한다.
5. **절차가 아니라 분류 체계로 이해하는가?**: Zachman을 A단계 → B단계처럼 순서대로 수행하는 것은 잘못된 이해다.

### 실무 적용 시나리오

```text
대형 금융기관 디지털 전환 프로젝트:

CEO/이사회 (Planner 행):
  What: 핵심 금융 서비스 목록 (예금, 대출, 투자)
  How: 비즈니스 프로세스 지도 (영업, 심사, 리스크)
  Why: 디지털 전환 전략 목표 (3년 내 디지털 채널 80%)

업무 담당자 (Owner 행):
  What: 고객, 계좌, 거래 개념 모델 (ERD 초안)
  How: 비즈니스 프로세스 상세 (대출 심사 플로우)
  Who: 조직도, 업무 분장 (지점, 본점, 디지털팀)

아키텍트 (Designer 행):
  What: 논리 데이터 모델 (엔터티, 관계, 정규화)
  How: 마이크로서비스 아키텍처 (API 설계)
  Where: 클라우드 아키텍처 (AWS 리전, 가용영역)

개발자/DBA (Builder 행):
  What: 물리 데이터 모델 (DDL, 테이블, 인덱스)
  How: 코드 구조 (패키지, 클래스, 메서드)
  Where: 인프라 스펙 (서버, 스토리지, 네트워크)
```

### 안티패턴

- **프레임워크를 절차서로 오해**: Zachman을 "1단계 Planner 완료 → 2단계 Owner 진행" 방식으로 순차 적용하는 것은 프레임워크의 본질을 오해한 것이다. 이것은 분류 체계이지 방법론이 아니다.
- **표만 만들고 실제 산출물 미연계**: Zachman 셀 목록만 작성하고 실제 ERD, 아키텍처 다이어그램과 연결하지 않으면 공허한 관료적 문서가 된다.
- **모든 셀을 완벽히 채우려는 집착**: 소규모 프로젝트에서 36개 셀 모두를 채우는 것은 비현실적이다. 프로젝트 규모와 필요에 맞게 우선순위를 정한다.
- **한 셀에 여러 관점 혼합**: 셀의 독립성 원칙을 무시하고 Owner 관점의 내용을 Designer 셀에 넣으면 관점 간 혼란이 발생한다.

- **📢 섹션 요약 비유**: Zachman을 방법론으로 오해하는 것은, 음식 분류표(식이다/음식명/영양성분/조리법 분류)를 실제 요리 방법으로 착각하는 것과 같다. 분류표는 무엇이 있는지 알려주지, 어떻게 만드는지는 별도의 레시피가 필요하다.

---

## Ⅴ. 기대효과 및 결론

Zachman Framework는 기업 아키텍처의 완전성을 보장하는 가장 강력한 분류 체계다. 40년이 넘는 세월 동안 산업 표준으로 인정받아 온 이유는, 이해관계자 관점과 아키텍처 주제를 교차하는 6×6 매트릭스가 직관적이면서도 완전한 구조를 제공하기 때문이다.

정량적 효과로는 아키텍처 산출물 누락 감소 (모든 셀이 정의되어 있으므로), 이해관계자 간 의사소통 개선 (각 관점이 명확히 분리되어 있으므로), 아키텍처 일관성 향상 (행·열 간 관계로 정렬 확인 가능)을 들 수 있다.

미래 관점에서 Zachman Framework는 디지털 전환, 클라우드 마이그레이션, AI 기반 시스템 구축에서도 여전히 유효하다. 오히려 시스템이 복잡해질수록 전체 조망 능력이 더욱 중요해지며, Zachman의 6×6 매트릭스는 복잡성을 구조화하는 데 효과적이다.

기술사 답안에서는 "6×6 매트릭스 구조, 관점 축(Planner~Enterprise)과 질문 축(What~Why), 분류 체계이지 방법론이 아님, TOGAF와의 보완적 관계"를 핵심으로 설명한다.

- **📢 섹션 요약 비유**: Zachman Framework는 기업 아키텍처의 GPS 지도 격자다. 격자(6×6 매트릭스) 위에 현재 위치(산출물)를 표시하면 어디가 비어 있는지(누락된 산출물) 즉시 알 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| TOGAF ADM | Zachman 분류에 맞는 산출물을 개발하는 방법론 |
| ArchiMate | Zachman 셀을 시각화하는 모델링 언어 |
| FEAF (Federal EA Framework) | 미국 연방 정부의 Zachman 기반 EA 프레임워크 |
| DoDAF | 국방부 아키텍처 프레임워크, Zachman 영향 |
| 엔터프라이즈 아키텍처 (EA) | Zachman이 분류 체계를 제공하는 대상 |
| 이해관계자 관리 | Zachman의 6개 관점 = 6가지 이해관계자 그룹 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">정보 시스템의 복잡성 증가 (1980년대)</div>
<div class="kb-diagram-note">→ 다양한 이해관계자, 다양한 산출물 혼재</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">John Zachman "A Framework for Information Systems Architecture" (1987, IBM)</div>
<div class="kb-diagram-note">→ 6×6 매트릭스 최초 제안</div>
<div class="kb-diagram-note">→ What/How/Where/Who/When/Why × 6관점</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Zachman 개정 (1992)</div>
<div class="kb-diagram-note">→ Planner~Enterprise 관점 축 정교화</div>
<div class="kb-diagram-note">→ "Ontology"로 재정의 (분류 체계 강조)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">TOGAF 등 방법론과 연계 (2000년대)</div>
<div class="kb-diagram-note">→ Zachman으로 산출물 분류 + TOGAF ADM으로 개발 절차</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">ArchiMate 표준화 (2004~)</div>
<div class="kb-diagram-note">→ Zachman 셀 내용을 시각화하는 언어 등장</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">디지털 전환 시대 (현재)</div>
<div class="kb-diagram-note">→ 클라우드, AI, DevOps를 포함한 확장 적용</div>
<div class="kb-diagram-note">→ 전체 조망 도구로서 가치 지속</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. Zachman Framework는 큰 레고 세트를 정리하는 표예요. 색깔(관점)별로, 모양(질문)별로 나누어 정리하는 칸이 있어요.
2. 어떤 관점(CEO, 설계자, 개발자)에서 봐도 "이 칸에는 이게 있어야 해"를 알 수 있어요.
3. 그래서 빠진 레고 조각(산출물)을 쉽게 찾을 수 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 55 / 973

← **이전**: [54. 브룩스의 법칙 (Brooks' Law)](/knowledge-base/studynote/04_software_engineering/01_overview_principles/054_brooks_law/)
**다음**: [56. TOGAF EA Framework](/knowledge-base/studynote/04_software_engineering/01_overview_principles/056_togaf_ea_framework/) →

---
