---
title: "TOGAF ADM (TOGAF ADM)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 298
---

# 📖 【암기용】 개념 완전 이해

> 목적: TOGAF ADM을 처음 봐도 완전히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: 기업 아키텍처를 비즈니스 목표부터 기술 구현까지 반복적으로 수립·전환·관리하는 방법론
- **왜 필요한가**: 부서별 시스템이 따로 움직이면 중복 투자, 데이터 불일치, 기술 표준 미준수가 발생한다.
- **핵심 직관**: 도시 전체 교통·상하수도·전력 계획을 세우고 단계별 공사와 변경 관리를 수행하는 도시계획 절차이다.

## 깊이 이해
- **배경·문제의식**: 기업 시스템은 업무, 데이터, 애플리케이션, 기술이 얽혀 있다. 프로젝트 단위 최적화만 하면 전체 표준과 전략 정렬이 깨진다.
- **작동 원리**: Preliminary에서 아키텍처 원칙을 정하고, Architecture Vision에서 목표를 합의한다. Business, Data, Application, Technology Architecture를 정의한 뒤 기회·솔루션, 마이그레이션 계획, 구현 거버넌스, 변경 관리를 반복한다.
- **비유**: 회사 이전을 할 때 새 건물 구조, 부서 배치, 네트워크, 이사 순서, 공사 감독, 변경 요청을 한 계획에서 관리하는 것과 같다.
- **구체 예시**: 고객 360 플랫폼 구축 시 비즈니스 프로세스, 고객 데이터 모델, CRM·DW 애플리케이션, 클라우드 기술 표준을 ADM 단계별 산출물로 정리한다.
- **흔한 오해·주의점**: TOGAF는 문서 양산 절차가 아니다. gap analysis와 migration roadmap을 통해 투자 우선순위와 변경 통제를 만드는 것이 목적이다.

## 연결 개념
- Enterprise Architecture - 비즈니스·데이터·애플리케이션·기술 아키텍처 통합
- Architecture Repository - 표준·원칙·산출물 저장소
- Architecture Governance - 아키텍처 준수와 변경 승인 체계

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

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
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
