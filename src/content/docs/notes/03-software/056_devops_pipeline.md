---
sidebar:
  order: 56
  label: "056. DevOps 파이프라인"
  badge:
    text: "기출 · 50%"
    variant: note
title: "DevOps 파이프라인 (DevOps Pipeline)"
date: "2026-08-27T00:47:00+09:00"
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

- **DevOps**: 개발(Development)과 운영(Operations)의 합성어로, 소통, 협업, 자동화를 통해 소프트웨어 제품을 신속하고 안정적으로 릴리즈하는 공학 문화이자 방법론.
- **CALMS 프레임워크**: 문화(Culture), 자동화(Automation), 린(Lean), 측정(Measurement), 공유(Sharing)의 DevOps 5대 핵심 가치.

</details>

- 정의/개념: 개발(Dev)과 운영(Ops)의 장벽을 허물고 **CALMS 원칙과 무한 순환 루프(Infinity Loop)** 로 소프트웨어 전 생애주기를 자동 연계하는 체계
- 배경/필요성: 개발과 운영 간 사일로(Silo) 장벽으로 인한 **배포 리드타임 장기화 및 장애 책임 공방과 품질 저하 해결 불가**

#### 한줄 요약
- 개발과 운영이 하나 되어 기획에서 모니터링까지 자동화 도구 체인으로 연결한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Infinity Loop(무한 루프)**: Plan $\to$ Code $\to$ Build $\to$ Test $\to$ Release $\to$ Deploy $\to$ Operate $\to$ Monitor $\to$ Plan으로 무한히 피드백되는 8자형 루프.
- **DORA 4대 핵심 지표**: 배포 빈도(Deployment Frequency), 변경 리드타임(Lead Time for Changes), 서비스 복구 시간(MTTR), 변경 실패율(Change Failure Rate).

</details>

- **CALMS Framework** 기반의 조직 문화 혁신 및 전 주기 도구 체인 자동화
- 기획부터 운영 피드백까지 유기적으로 순환하는 **DevOps Infinity Loop**
- **DORA 4대 핵심 지표** 기반 조직의 릴리즈 민첩성과 운영 안정성 정량 측정

#### 한줄 요약
- CALMS 문화를 바탕으로 8자형 무한 루프를 자동화하고 DORA 지표로 측정한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **DevOps Toolchain**: Jira(기획) $\to$ Git(코드) $\to$ Jenkins(빌드) $\to$ ArgoCD(배포) $\to$ K8s(운영) $\to$ Prometheus(모니터링)로 연결된 도구 집합.

</details>

| 구성요소 | 책임 |
|:---|:---|
| Plan & Code | **Jira·Git** 기반 백로그·코드 리뷰 관리 |
| Build & Test | **CI 품질 게이트** 기반 빌드·시험 자동화 |
| Release & Deploy | **GitOps** 기반 불변 이미지 무중단 배포 |
| Operate & Monitor | **SLO 메트릭** 감시와 이슈 피드백 |

#### 한줄 요약
- Plan/Code, Build/Test(CI), Release/Deploy(CD), Operate/Monitor(Ops)가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **피드백 환류(Feedback Loop)**: 운영 모니터링에서 발생한 APM 장애 로그 및 사용자 피드백이 즉각 Jira 이슈로 등록되어 다음 스프린트에 반영되는 체계.

</details>

```text
Jira 백로그 요구사항 기반 기능 개발 및 Git 푸시
        │
   CI 러너가 자동 트리거되어 빌드, 테스트, 정적 분석 실행 (품질 게이트 통과)
        │
   Harbor에 불변 이미지 태깅 후 ArgoCD가 K8s 프로덕션에 자동 배포
        │
   Prometheus & Alertmanager가 프로덕션 에러율/응답시간 실시간 감시
        │
   운영 이상 징후 감지 시 Slack 경보 발송 및 Jira 버그 티켓 자동 생성 (피드백 환류)
```

#### 한줄 요약
- 개발 푸시 → CI 검증 → GitOps 배포 → 모니터링 감시 → Jira 피드백 환류 순으로 순환한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **전통적 사일로 vs DevOps**: "내 코드는 내 컴퓨터에서 잘 돌아간다"며 넘기는 사일로와 "You Build It, You Run It"의 DevOps 책임 모델.

</details>

| 비교 항목 | 전통적 사일로(Silo) 조직 | DevOps 교차기능(Cross-Functional) 팀 |
|:---|:---|:---|
| 조직 문화 | 개발팀과 운영팀의 물리적 분리/대립 | **개발·운영·QA가 단일 목적 팀으로 통합** |
| 책임 모델 | 개발은 기능 릴리즈, 운영은 안정성 추구 | **"You Build It, You Run It" 공동 책임** |
| 배포 주기 | 수 주~수 개월 단위 대규모 빅뱅 배포 | **일 수십 회 소규모 고빈도 배포** |
| 자동화 수준 | 수동 서버 접속 배포 (Human Error) | **IaC 및 CI/CD 전 주기 100% 자동화** |
| DORA 지표 | 리드타임 수 개월, MTTR 수 일 소요 | **리드타임 1시간 이내, MTTR 1시간 이내** |

#### 한줄 요약
- 사일로는 인계 지연과 책임 공방을 유발하고, DevOps는 원팀 협업과 자동화로 민첩성을 극대화한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Platform Engineering & IDP**: 개발자가 셀프 서비스로 인프라와 배포를 다룰 수 있게 내부 개발자 플랫폼(Internal Developer Platform)을 제공하는 최신 엔지니어링 패러다임.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 도구만 도입하고 조직 문화는 여전히 사일로로 단절 | **CALMS 문화 교육 및 개발-운영 KPI 공동화(DORA 지표)** | 팀 간 장벽 해소 및 공동 책임 문화 정착 |
| 수십 개 MSA 서비스의 파이프라인 관리 복잡성 | **플랫폼 엔지니어링 및 내부 개발자 플랫폼(IDP) 구축** | 개발자 셀프 서비스 제공 및 인지 부하 감소 |
| 잦은 배포로 인한 보안 검증 누락 | **DevSecOps 도구 체인(SAST, DAST, SCA) 파이프라인 내재화** | 보안 취약점 조기 식별(Shift-Left) 달성 |
| 운영 경보 폭증으로 인한 알람 피로(Alert Fatigue) | **SLO/SLA 기반 핵심 알람 필터링 및 Runbook 자동화** | 불필요한 알람 차단 및 실질적 대응력 제고 |

#### 한줄 요약
- CALMS 문화 정착, 플랫폼 엔지니어링 도입, DevSecOps 내재화, 알람 최적화로 성공을 이끈다.

## Ⅶ. 결론

- 개발운영 연계는 **DevOps 도구체인**, 역량 측정은 **DORA 지표** 선택

#### 한줄 요약
- DevOps 파이프라인은 기획부터 모니터링까지 전 과정을 하나로 통합하여 비즈니스 가치를 가장 빠르고 안정적으로 전달하는 현대 IT 운영의 핵심 축이다.
