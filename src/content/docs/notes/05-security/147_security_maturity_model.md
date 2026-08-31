---
sidebar:
  order: 147
  label: "147. 보안 성숙도 모델 (Security Maturity Model)"
  badge:
    text: "미출 · 50%"
    variant: note
title: "엔터프라이즈 사이버보안 역량 평가 및 개선 프레임워크 : 보안 성숙도 모델 (SAMM vs BSIMM vs C2M2)"
date: "2026-08-31T10:48:00+09:00"
tags:
  - "notes-security"
weight: 147
extra:
  question_no: "147"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "보안 역량 평가 및 거버넌스 프레임워크, OWASP SAMM v2(처방적 Prescriptive 모델, 5 Business Functions & 15 Practices), BSIMM(실증적 Observational 벤치마킹 모델, 4 Domains & 12 Practices), DOE C2M2 v2.1(Cybersecurity Capability Maturity Model, MIL 0~3), 아티팩트 기반 증거(Artifact-based Evidence), 목표 프로파일(Target Profile) 및 위험 기반 로드맵"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **보안 성숙도 모델(Security Maturity Model / OWASP SAMM & DOE C2M2)**: 조직의 소프트웨어 개발, IT/OT 인프라, 거버넌스 및 운영 보안 관행(Security Practices)이 조직 내에서 얼마나 제도화(Institutionalized)되고, 측정 가능하며, 지속적으로 개선되고 있는지를 객관적인 역량 지표(Maturity Levels)로 정량 평가하고, 비즈니스 위험에 기반한 점진적 개선 로드맵을 수립하는 평가 프레임워크.
- **체크리스트 기반 단편적 평가 및 과도한 목표 설정 결함(Checklist & Over-engineering Defect)**: 단순 규제 점검표(컴플라이언스 준수 여부)나 솔루션 도입 개수에만 의존하여 실제 프로세스 내재화 수준을 파악하지 못하거나, 시스템 중요도를 고려하지 않고 모든 영역에 비현실적인 최고 등급(Level 3/MIL 3)을 맹목적으로 추구하여 예산과 인력을 낭비하는 구조적 결함.

</details>

- 정의/개념: 보안 투자의 실효성과 지속성을 보증하기 위해 **평가 모델 선정 $\rightarrow$ 아티팩트 기반 증거(Artifact-based Evidence) 수집 $\rightarrow$ 현재 성숙도(As-Is) 진단 $\rightarrow$ 위험 기반 목표 프로파일(To-Be Target Profile) 설정 $\rightarrow$ 격차(Gap) 분석 및 의존성 기반 로드맵 이행 $\rightarrow$ 지속적 재평가 피드백 루프** 를 집행하는 **보안 거버넌스 역량 고도화 아키텍처**
- 배경/필요성: 단순한 컴플라이언스 체크리스트 준수 여부나 보안 솔루션 도입 개수에만 의존하는 단편적 평가는 조직 내 실제 보안 프로세스의 제도화(Institutionalization) 및 반복 가능성을 측정하지 못하며, 자산의 중요도를 무시한 채 모든 영역에 최고 등급을 일괄 요구하는 맹목적 과잉 투자(Over-engineering)와 예산 낭비를 초래함에 따라, OWASP SAMM v2(처방적 모델), BSIMM(실증적 벤치마킹), DOE C2M2(IT/OT 역량 모델) 표준에 기반하여 CI/CD 로그 및 취약점 데이터 등 아티팩트 기반 증거(Artifact-based Evidence) 수집, 현재 성숙도(As-Is) 정량 진단, 위험 수용선에 따른 차등적 목표 프로파일(To-Be Target Profile) 설정 및 의존성 기반 단계적 로드맵을 결합하는 보안 성숙도 평가 프레임워크를 도입하여 **보안 역량의 객관적 제도화 측정, 보안 투자 대비 위험 감소 효과(ROI) 극대화 및 지속 가능한 보안 거버넌스 고도화**를 달성할 필요

#### 한줄 요약
- 보안 성숙도 모델은 SAMM/BSIMM/C2M2를 통해 조직의 보안 역량을 객관적으로 평가하고 위험 기반 로드맵을 제공한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **보안 성숙도 평가 3대 핵심 메커니즘**:
  - **아티팩트 기반 증거 수집 (Artifact-based Verification)**: 설문이나 인터뷰가 아닌 CI/CD 로그, SAST 리포트, IAM 정책 JSON 등 검증 가능한 시스템 산출물로 평가.
  - **처방적(Prescriptive) vs 실증적(Observational)**: SAMM처럼 이상적인 보안 활동을 제시하는 방식과 BSIMM처럼 실제 선도 기업들의 관행을 통계화하는 방식의 상호보완.
  - **차등적 목표 프로파일링 (Target Profiling)**: 모든 시스템에 최고 등급을 요구하지 않고 자산의 중요도와 위험 수용선(Risk Appetite)에 맞춰 차등 목표 설정.

</details>

- 수행 능력과 반복 정착도를 함께 보는 **제도화 측정**
- 선행 기반을 먼저 배치하는 **의존성 기반 로드맵**
- MTTR·빌드 차단율을 반영하는 **KPI·KRI 연계**

#### 한줄 요약
- 아티팩트 증거 기반 검증, 차등 목표 프로파일링, 처방/실증 모델 벤치마킹, 의존성 기반 로드맵을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **보안 성숙도 평가 프레임워크 4대 핵심 컴포넌트**:
  1. **Scoping & Target Profiler**: 비즈니스 영향 분석(BIA) 기반 목표 레벨 설정기.
  2. **Capability Assessment Matrix**: 영역(Domain)별 세부 보안 관행(Practices) 매트릭스.
  3. **Artifact Collector**: CI/CD 로그, DefectDojo 취약점 데이터, 정책서 수집기.
  4. **Risk-based Roadmap Engine**: As-Is vs To-Be 격차 분석 및 ROI 우선순위화 엔진.

</details>

```text
보안 성숙도 평가 프레임워크
├─ Scoping·Target Profiler
├─ Capability Assessment Matrix
├─ Artifact Collector
└─ Risk-based Roadmap Engine
```

선의 의미: 목표 프로파일 설정 후 역량 매트릭스를 통해 아티팩트 기반으로 현재 수준을 진단하고, 격차 분석을 통해 지속적 개선 로드맵을 환류하는 구조

| 구성요소 | 책임 |
|:---|:---|
| **Scoping·Target Profiler** | 위험과 규제에 맞춘 평가 범위·목표 설정 |
| **Capability Assessment Matrix** | 영역별 보안 관행과 역량 수준 평가 |
| **Artifact Collector** | 로그·정책·취약점 자료 등 객관적 증거 수집 |
| **Risk-based Roadmap Engine** | 격차·의존성·ROI 기반 개선 과제 배열 |

#### 한줄 요약
- 아티팩트 수집기가 자기 보고에 기대던 진단 근거를 CI/CD 로그와 취약점 데이터라는 실물 증거로 바꿔 놓고, 목표 프로파일러는 모든 영역을 최고 레벨로 끌어올리려는 과잉 투자를 차등 목표로 막으며, 로드맵 엔진은 격차가 큰 순서가 아니라 선행 의존성과 ROI로 착수 순서를 뒤집는다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **보안 성숙도 평가 및 개선 5단계 수명주기**:
  1. 비즈니스 환경 분석 및 평가 모델(SAMM/BSIMM/C2M2) 선정
  2. 시스템 아티팩트(CI/CD 로그, 정책서) 수집 및 현재 수준(As-Is) 평가
  3. 위험 허용선(Risk Appetite)에 따른 차등 목표 프로파일(To-Be) 수립
  4. 기술적 의존성 및 ROI를 고려한 위험 기반 개선 로드맵 수립
  5. 보안 통제 구현 및 정량 지표(MTTR) 기반 지속적 재평가

</details>

```text
1. [스코프 획정 및 모델 선정]
    ├─ 개발보안 내재화 목적 ➔ OWASP SAMM v2 채택
    └─ [전사 100개 마이크로서비스 및 핵심 결제 플랫폼을 평가 범위로 확정]
            │
            ▼
2. [아티팩트 수집 및 As-Is 진단]
    ├─ GitLab CI/CD 파이프라인 스크립트 + SonarQube 정적 분석 로그 API 연동
    ├─ [아티팩트 검증: 'Verification - Security Testing' 영역 Level 1 (기본 SAST만 수행) 판정]
    └─ [주관적 설문 없이 시스템 데이터 기반 현재 성숙도 확정]
            │
            ▼
3. [목표 프로파일(To-Be) 설정]
    ├─ 결제 코어 서비스 ➔ 금융 규제 및 고위험 고려하여 Level 3 (자동화 및 최적화) 설정
    └─ [내부 업무 포털 ➔ 위험 수용선 고려하여 Level 1 유지 (과잉 투자 방지)]
            │
            ▼
4. [격차 분석 및 로드맵 수립]
    ├─ [선행 과제] DefectDojo 중앙 취약점 포털 구축 (의존성 선행 인프라)
    ├─ [후행 과제] CI/CD 파이프라인 DAST/IAST 자동화 게이트 연동
    └─ [6개월 단위 3단계 실행 로드맵 수립 및 경영진 예산 승인 획득]
            │
            ▼
5. [실행 및 지속적 재평가 (Re-assessment)]
    ├─ 보안 통제 구현 후 실제 취약점 조치 시간(MTTR) 30일 ➔ 3일로 단축 확인
    └─ [1년 주기 재평가 수행 ➔ 성숙도 Level 2.5 달성 및 신규 To-Be 목표 갱신]
```

**동작 원리**

1. **스코프 획정 및 모델 선정**: 평가 목적에 맞는 모델 결정
2. **아티팩트 수집 및 As-Is 진단**: 객관적 증거로 현재 수준 판정
3. **목표 프로파일 설정**: 자산 위험에 따른 차등 목표 결정
4. **격차 분석 및 로드맵 수립**: 의존성과 위험 기반 과제 배열
5. **실행 및 지속적 재평가**: MTTR로 개선 효과 검증

#### 한줄 요약
- 모든 영역을 최고 단계로 올리는 비용은 어느 조직도 감당할 수 없으므로, 성숙도 모델의 실익은 점수를 높이는 데가 아니라 영역마다 다른 목표를 정당화하는 데 있다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **주요 보안 성숙도 모델 3대 프레임워크 비교**:
  - OWASP SAMM v2: 소프트웨어 개발보안 전주기 처방적(Prescriptive) 오픈소스 모델 (SDLC 최적화).
  - BSIMM (Building Security In Maturity Model): 글로벌 130개 이상 대기업의 실제 관찰된(Observational) 벤치마킹 모델 (통계 중심).
  - DOE C2M2 v2.1: 미국 에너지부 제정 전사 IT/OT 인프라 사이버보안 역량 모델 (MIL 0~3, 인프라 특화).

</details>

| 비교 항목 | OWASP SAMM v2 | BSIMM (실증 벤치마킹) | DOE C2M2 v2.1 |
|:---|:---|:---|:---|
| **성격 및 철학** | **처방적 (Prescriptive: 해야 할 이상적 가이드)**| **관찰적 (Observational: 타사 실제 관행 통계)**| **제도화 중심 (Capability & Institutionalization)**|
| **적용 도메인** | **소프트웨어 개발 생명주기 (DevSecOps/SDLC)** | 소프트웨어 보안 이니셔티브 (SSI 조직 비교)| **전사 IT 및 OT 산업제어시스템, 공급망** |
| **구조 체계** | **5 Business Functions / 15 Practices** | 4 Domains / 12 Practices / 130+ Activities | **10 Domains / 300+ Practices** |
| **성숙도 척도** | **Level 1 ~ 3 (초기 ~ 체계화 ~ 최적화)** | 12개 관행별 활동 수행 점수 백분위 벤치마킹| **MIL 0 ~ MIL 3 (Maturity Indicator Level)** |
| **주요 장점** | **오픈소스 무료, 구체적 구현 로드맵 수립 용이**| **동종 업계 대비 자사 보안 수준 객관적 비교**| 전사적 거버넌스 및 OT/ICS 인프라 포괄 |
| **단점/한계** | 조직 맥락 미반영 시 기계적 목표 설정 위험 | 구체적인 구현 방법(How-to) 처방 부족 | 소프트웨어 개발 단계의 상세 보안 평가 한계 |

#### 한줄 요약
- SAMM은 SDLC 처방적 로드맵, BSIMM은 기업 간 실증 벤치마킹, C2M2는 전사 IT/OT 역량 제도화에 특화된다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **NIST CSF (사이버보안 프레임워크) 및 OWASP SAMM**: 사이버보안 조직 프로파일링 및 역량 성숙도 평가 국제 표준.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 평가 항목마다 담당자에게 문서를 수동으로 요청하여 **평가 주기가 수개월씩 지연되고 담당자 피로도 폭증으로 평가 중단** | **CI/CD 파이프라인, DefectDojo, Jira API와 연동된 보안 측정 자동화(Automated Metrics) 아키텍처 구축** | 증거 수집 시간 80% 단축 및 실시간 성숙도 평가 달성 |
| 모든 시스템과 부서에 대해 맹목적으로 Level 3 최고 등급을 목표로 설정하여 **비핵심 시스템에 과도한 보안 예산이 낭비되는 오버엔지니어링 발생** | **NIST CSF 프로파일링 가이드를 적용하여 자산 중요도와 위험 수용선에 따른 차등적 목표 프로파일(Target Profile) 수립** | 보안 투자 대비 위험 감소 효과(ROI) 극대화 |
| 성숙도 점수는 높으나 실제 모의해킹 수행 시 쉽게 침해되는 **서류상으로만 존재하는 형식적 보안(Paper Security) 현상 발생** | **성숙도 검증 도메인에 BAS(침해 및 공격 시뮬레이션) 및 퍼플팀 실전 훈련 결과를 아티팩트로 강제 연동** | 실질적 방어 유효성(Effectiveness) 100% 검증 확보 |

#### 한줄 요약
- API 연동으로 증거 수집을 자동화하고, 차등 프로파일로 과잉 투자를 막으며, 실전 훈련 연계로 형식적 보안을 탈피한다.

## Ⅶ. 결론

- 형식적인 서류상 점검(Paper Security)을 탈피하여 실물 시스템 증거에 기반한 보안 프로세스의 제도화 수준을 객관적으로 측정하고 비즈니스 위험에 맞춤화된 진화 방향을 제시하는 **엔터프라이즈 사이버보안 역량 평가 및 거버넌스 로드맵(SAMM vs BSIMM vs C2M2 / Artifact-based / Target Profile)의 핵심 프레임워크**로 확고히 자리 잡았으며, DevSecOps 자동화 메트릭 및 침해 시뮬레이션(BAS) 연계로 실질적 방어 유효성을 입증하는 체계로 진화하는 가운데, 실무 보안 거버넌스 및 역량 평가 수립 시에는 **CI/CD·Jira API 연동을 통한 아티팩트 증거 수집 자동화, 자산 중요도 기반의 차등적 목표 프로파일(Target Profile) 설정을 통한 오버엔지니어링 방지, 기술적 선행 의존성과 ROI를 고려한 단계적 3개년 실행 로드맵 수립**을 결합하여 완벽한 엔터프라이즈 보안 성숙도를 완성

#### 한줄 요약
- 객관적 아티팩트 검증과 위험 기반 차등 프로파일링을 통해 무결점 보안 성숙도 개선 체계를 완성한다.
