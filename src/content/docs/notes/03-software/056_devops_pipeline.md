---
sidebar:
  order: 56
  label: "056. DevOps 파이프라인 (DevOps Pipeline)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "DevOps 파이프라인 (DevOps Pipeline)"
date: "2026-08-13T15:51:00+09:00"
tags:
  - "notes-software"
weight: 56
extra:
  question_no: "056"
  source_status: "기출"
  source_history: "120회"
  priority: 50
  priority_note: "120회 기출, 개발•운영 협업 파이프라인"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **DevOps (Development + Operations)**: 소프트웨어 개발(Development)과 정보기술 운영(Operations) 조직 간의 장벽을 허물고, 애자일 문화 및 자동화 도구를 기반으로 빠른 변경 릴리스와 신뢰성을 달성하는 문화적/기술적 협업 패러다임.
- **CALMS Framework**: DevOps의 성공적 정착을 측정하는 5가지 척도 (Culture: 문화, Automation: 자동화, Lean: 린 프로세스, Measurement: 측정, Sharing: 공유).
- **Feedback Loop**: 실운영 환경의 모니터링 로그/지표를 개발팀으로 실시간 환류하여 다음 스프린트의 기능 개선에 즉시 피드백 반영하는 선순환 구조.

</details>

- 정의/개념: 소프트웨어 계획(Plan)부터 코딩, 빌드, 테스트, 출시, 배포, 운영 및 모니터링 무한 루프를 자동화된 도구 체인(Toolchain)으로 연결한 **DevOps Pipeline**
- 배경/필요성: 개발•운영 분업은 **인계 지연•책임 단절** 유발

#### 한줄 요약

- 데브옵스의 공동 책임과 피드백 루프를 자동 전달 과정에 연결하는 것이 핵심이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Infinity Loop (무한 루프 8자 고리)**: DevOps의 생명주기를 나타내는 표준 모델로, Plan $\rightarrow$ Code $\rightarrow$ Build $\rightarrow$ Test $\rightarrow$ Release $\rightarrow$ Deploy $\rightarrow$ Operate $\rightarrow$ Monitor 의 선순환 순환고리.
- **Continuous Everything (무한 연속성)**: 지속적 계획(Plan), 지속적 통합(CI), 지속적 테스트(CT), 지속적 배포(CD), 지속적 모니터링(CM)을 통합 추구.

</details>

- **CALMS Framework (Culture, Automation, Lean, Measurement, Sharing)** 지향
- **DevOps Infinity Loop** 8자 생명주기 자동화
- **DORA Metrics (Deployment Frequency, Lead Time for Changes, MTTR, Change Failure Rate)** 성과 측정

#### 한줄 요약

- 공동 소유, 지속적 통합, 피드백 루프가 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **DevOps Toolchain**: Plan부터 Monitor까지 각 단계별로 사용되는 최적 자동화 도구들의 유기적 조합 묶음 (Jira, Git, Jenkins, SonarQube, Terraform, K8s, Prometheus).

</details>

```text
       [Plan / Issue (Jira)] ─── [Code / Version (Git)]
                │                         │
                │                         │
     [Monitor (Prometheus)] ─── [Build & Test (Jenkins)]
                │                         │
                │                         │
     [Operate (Kubernetes)] ─── [Deploy (ArgoCD)]
```

선의 의미: Plan $\rightarrow$ Code $\rightarrow$ Build $\rightarrow$ Deploy $\rightarrow$ Operate $\rightarrow$ Monitor 과정이 끊임없이 순환 환류(Infinity Loop)되는 DevOps 파이프라인 도구 체인 구조.

| 구성요소 | 책임 |
|:---|:---|
| 계획 플랫폼 (Jira) | 요구사항•백로그와 작업 우선순위 관리 |
| 변경 저장소 (Git) | 소스 변경과 검토 이력 보관 |
| 통합 실행기 (Jenkins) | 빌드•시험•정적 분석 자동 실행 |
| 배포 제어기 (ArgoCD) | 승인 산출물을 대상 환경에 전달 |
| 운영 플랫폼 (Kubernetes) | 서비스 실행과 자원 상태 관리 |
| 관측 플랫폼 (Prometheus) | 운영 지표 수집과 피드백 제공 |

#### 한줄 요약

- 계획•변경•통합•배포•운영•관측 연결이 핵심이다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **DORA 4 Key Metrics**: DevOps 팀의 성숙도를 측정하는 4대 지표 (배포 빈도, 변경 리드타임, 서비스 복구 시간 MTTR, 변경 실패율).

</details>

```text
┌──────────────────────────────┐
│ Jira Issue / Git Branch 생성 │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. 변경 통합•시험            │
│ 2. 정적 보안 검증            │
│ 3. 승인 버전 배포            │
│ 4. 운영 지표 관측            │
│ 5. DORA 지표 환류            │
└──────────────┬───────────────┘
               ▼
 [다음 스프린트 피드백 환류 완료]
```

### 동작 원리

1. 변경 통합•시험: 실행기가 빌드와 단위•통합 시험 수행.
2. 정적 보안 검증: SAST 결과로 품질 게이트 판정.
3. 승인 버전 배포: 배포 제어기가 운영 플랫폼에 전달.
4. 운영 지표 관측: 오류율•지연시간•복구 상태 수집.
5. DORA 지표 환류: 성과 지표를 다음 개선 계획에 반영.

#### 한줄 요약

- 검증 산출물 등록, 승인 버전 전달, 개선 피드백 환류의 순환이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Traditional Waterfall Silo vs DevOps Cross-Functional**: Traditional은 개발/QA/운영이 장벽(Silo)으로 분리되어 책임 전가 발생, DevOps는 1개 전담 팀(Cross-Functional Team)이 계획부터 운영까지 전권 소유.

</details>

| 비교 항목 | Traditional Silo Structure | DevOps Cross-Functional Structure |
|:---|:---|:---|
| 조직 형태 | 개발팀, QA팀, 운영팀 완전 분리 (Silo) | **개발+운영 융합 전담 팀 (Cross-Functional)** |
| 릴리스 주기 | 수개월 단위의 대규모 릴리스 | **매일/수시 소규모 연속 릴리스 (Continuous)** |
| 책임 소재 | "배포 후엔 운영팀 책임" 책임 전가 | **"You Build It, You Run It" 공동 책임** |
| 인프라 관리 | 서버 관리자에 의한 수동 작업 | **Infrastructure as Code (IaC) 자동화** |

#### 한줄 요약

- 잦은 변경에는 DevOps 통합 운영, 엄격한 인수에는 단계별 인계가 적합하다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **You Build It, You Run It**: 아마존 CTO 버너 보겔스(Werner Vogels)가 주창한 멘토링 구호로, 코드를 작성한 개발자가 해당 서비스의 실운영(On-call)까지 직접 책임진다는 문화적 원칙.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 문화적 변화 없이 도구(Jenkins/K8s)만 도입하여 실패 | **CALMS 프레임워크 기반 멘탈리티 혁신 & C-Level 지원** | DevOps 조직 문화 정착 |
| 자동화 시험 부족으로 배포 결함 유입 | 위험 기반 **Test Automation** 강화 | 배포 변경 실패율 감소 |
| 운영 지표 가시성 부재 | **Prometheus + Grafana + OpenTelemetry** 연계 | 평균 복구 시간 단축 |

> 사례: **Atlassian Jira + Git + Jenkins + SonarQube + K8s + Grafana** 기반 DevOps 파이프라인 구축

#### 한줄 요약

- 개발•운영 공동 평가, 인프라 코드화, 관측성이 핵심이다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **DevOps 파이프라인 구축 기준(DevOps Pipeline Build Standards)**: DORA 지표 목표치, Toolchain 자동화율 및 조직 문화 성숙도에 의거한 체계.

</details>

- 빈번한 변경은 **DevOps 공동 운영**, 엄격한 인수는 **단계별 승인** 선택

#### 한줄 요약

- DevOps 통합 운영에서는 점진적 전달과 가드레일로 속도와 안정성을 함께 관리하는 것이 핵심이다.
