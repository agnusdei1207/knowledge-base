---
sidebar:
  order: 56
  label: "056. DevOps 파이프라인"
  badge:
    text: "기출 • 50%"
    variant: note
title: "DevOps 파이프라인 (DevOps Pipeline)"
date: "2026-08-17T20:05:00+09:00"
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

- **CALMS 및 무한 순환 루프(CALMS & Infinity Loop)**: 문화(C), 자동화(A), 린(L), 측정(M), 공유(S)를 축으로 기획부터 모니터링까지 8자형 피드백을 지속 순환하는 체계.
- **사일로 장벽 및 리드타임(Silo Barrier & Lead-Time)**: 개발팀은 빠른 변경을 원하고 운영팀은 안정을 추구하여 조직 간 갈등과 배포 지연이 발생하는 한계.

</details>

- 정의/개념: 개발(Dev)과 운영(Ops)의 벽을 허물고 **CALMS 원칙과 무한 순환 루프(Infinity Loop)** 기반으로 소프트웨어 전 주기를 자동 연계하는 통합 파이프라인
- 배경/필요성: 개발과 운영 간 사일로(Silo) 장벽으로 인한 **배포 리드타임 장기화 및 장애 책임 공방과 품질 저하** 직면

#### 한줄 요약

- 개발·운영이 한 팀이 되어 기획에서 모니터링까지 자동화 도구 체인으로 연결하는 DevOps 파이프라인

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **DevOps Infinity Loop**: 기획→코딩→빌드→테스트→배포→운영→모니터링→피드백→기획으로 순환하는 DevOps의 무한 반복 생명주기.
- **DORA Metrics**: Google DevOps Research and Assessment가 정의한 DevOps 성숙도 4대 지표(배포 빈도·변경 리드타임·복구 시간 MTTR·배포 실패율).

</details>

- **CALMS Framework** 기반으로 문화·자동화·린·측정·공유를 추구
- 기획부터 모니터링까지 **DevOps Infinity Loop** 자동화 순환
- **DORA Metrics**로 조직의 DevOps 성숙도와 배포 성과를 정량 측정

#### 한줄 요약

- CALMS 문화 기반으로 무한 순환 루프를 자동화하고 DORA Metrics로 성숙도를 정량 측정

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **DevOps 툴체인(DevOps Toolchain)**: 기획(Jira)→소스(Git)→빌드(Jenkins)→배포(ArgoCD)→운영(K8s)→감시(Prometheus)로 연결된 각 단계별 자동화 도구 집합.

</details>

```text
[ DevOps 무한 루프 파이프라인 ]
기획 (Jira)
   │
소스 관리 (Git)
   │
빌드·통합 (Jenkins/GitHub Actions)
   │
배포 (ArgoCD/CD)
   │
운영 (Kubernetes/Cloud)
   │
감시 (Prometheus·Grafana)
   │ 피드백
   └──────────────▶ 기획 (Jira) [반복]
```

선의 의미: 화살표는 DevOps Infinity Loop의 각 단계 간 자동화 연결 관계, 마지막 피드백 화살표는 운영 관측 데이터가 기획 단계로 환류하는 관계

| 구성요소 | 책임 |
|:---|:---|
| **기획 (Jira)** | 백로그·이슈 관리·스프린트 계획 |
| **소스 관리 (Git)** | 코드 버전 관리·코드 리뷰 |
| **빌드·통합** | 자동 빌드·테스트·품질 게이트 실행 |
| **배포 (ArgoCD)** | 검증된 아티팩트의 운영 환경 자동 배포 |
| **운영 (K8s)** | 컨테이너 오케스트레이션·자원 관리 |
| **감시 (Prometheus)** | 메트릭·로그·알람으로 운영 상태 실시간 감시 |

#### 한줄 요약

- 기획→소스→빌드→배포→운영→감시→피드백의 자동화 도구 체인으로 DevOps Loop를 구성

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **교차기능 팀(Cross-Functional Team)**: 개발자·인프라 엔지니어·보안 전문가가 한 팀을 구성하여 기획에서 운영까지 전체를 책임지는 DevOps 조직 형태.

</details>

```text
1. 이슈 생성 (Jira) → 코드 작성 후 Git Push
   │
   ▼
2. CI 파이프라인 자동 실행 (빌드·테스트·품질 게이트)
   │
   ▼
3. 운영 환경 자동 배포 (ArgoCD → Kubernetes)
   │
   ▼
4. 운영 모니터링 (Prometheus·Grafana·Alertmanager)
   └─ 에러율·지연 시간·CPU 등 실시간 감시
   │
   ▼
5. 이상 감지 시 알람 발행 → Jira 이슈 생성 → 1단계 반복
```

**동작 원리**

1. **기획·코딩**: Jira 이슈를 기반으로 개발 후 Git에 커밋·Push
2. **CI 자동화**: 빌드·단위 테스트·품질 게이트를 자동 실행하고 결함 즉시 피드백
3. **CD 배포**: 검증된 아티팩트를 ArgoCD가 Kubernetes 클러스터에 자동 배포
4. **모니터링**: Prometheus·Grafana가 실시간으로 운영 지표를 감시하고 임계값 초과 시 알람 발행
5. **피드백 환류**: 운영 이슈가 Jira로 연결되어 다음 개발 주기의 입력 데이터가 됨

#### 한줄 요약

- 코딩→CI→CD→모니터링→피드백 환류의 무한 순환 자동화로 DevOps Loop를 실현

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **전통 사일로 vs DevOps**: 개발·운영 부서의 책임 분리로 인한 변경 전달 지연(사일로)과 개발·운영이 협업하여 전달 속도와 안정성을 동시에 달성하는 DevOps의 대비.

</details>

| 비교 항목 | 전통 사일로 조직 | DevOps |
|:---|:---|:---|
| 조직 구성 | 개발·운영 부서 분리 | **교차기능 팀(Cross-Functional)** |
| 배포 주기 | 수주~수개월 단위 대규모 배포 | **일 단위 고빈도 소규모 배포** |
| 책임 모델 | 부서 간 인계·책임 분리 | **You Build It, You Run It** |
| 자동화 수준 | 수동 배포·수동 설정 | **Pipeline as Code·IaC 자동화** |

#### 한줄 요약

- 사일로는 부서 간 인계로 속도가 저하되고, DevOps는 팀 협업과 자동화로 전달 속도와 안정성을 향상

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **You Build It, You Run It**: 소프트웨어를 개발한 팀이 운영까지 직접 책임지는 DevOps의 핵심 책임 원칙으로 운영 피드백이 개발 품질 향상으로 직결됨.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 도구만 변경하고 협업 문화는 기존 사일로 유지 | 도구 도입 전 **CALMS 기반 조직 문화** 변화 추진 | 실질적 개발-운영 협업 및 사일로 해소 |
| 자동 배포로 검증되지 않은 코드가 운영에 반영 | **자동화 테스트 강제 및 품질 게이트** 파이프라인 설정 | 운영 장애 빈도(배포 실패율) 감소 |
| 운영 장애를 늦게 인지하여 복구 지연 | **Prometheus + Grafana + Alertmanager** 실시간 알람 체계 구축 | MTTR 단축 및 사용자 영향 최소화 |

#### 한줄 요약

- 문화는 CALMS로, 코드 품질은 품질 게이트로, 장애 인지는 실시간 알람으로 보장

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **DevOps 파이프라인 구축 기준**: DORA Metrics 목표 수준·자동화 성숙도·조직 협업 문화를 기준으로 파이프라인 구성과 CD 방식을 결정하는 판단 기준.

</details>

- 고빈도 배포가 필요한 환경은 **DevOps 자동화 파이프라인 전면 적용**, 규제 환경은 **수동 승인 Delivery** 방식 병용

#### 한줄 요약

- DevOps는 도구가 아닌 문화의 변화로, CALMS 원칙 기반 파이프라인 자동화로 전달 속도와 안정성을 동시에 달성
