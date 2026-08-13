---
sidebar:
  order: 55
  label: "055. GitOps"
  badge:
    text: "미출 • 50%"
    variant: note
title: "GitOps"
date: "2026-08-13T15:47:00+09:00"
tags:
  - "notes-software"
weight: 55
extra:
  question_no: "055"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "GitOps는 선언형 배포•조정 루프 현안"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **GitOps**: Weaveworks에서 제안한 Cloud-Native 인프라 및 애플리케이션 배포 운용 패러다임으로, Git 리포지토리를 시스템 상태의 '유일한 진실의 원천(Single Source of Truth)'으로 삼고 Pull 기반의 에이전트가 이를 클러스터에 자동 동기화(Reconciliation)하는 방식.
- **Single Source of Truth (SSOT)**: 모든 인프라(IaC) 및 애플리케이션 K8s 매니페스트 설정의 불변 원본을 오직 Git 저장소 단 한 곳으로 통합 정의하는 사상.
- **Declarative Infrastructure**: "어떻게(How)" 스크립트를 실행할지가 아닌 "무엇을(What)" 배치할 것인지를 K8s YAML 매니페스트로 선언하여 관리하는 방식.

</details>

- 정의/개념: Git 저장소를 유일한 진실의 원천(Single Source of Truth)으로 선언하고, K8s 클러스터 내부 에이전트가 Git 매니페스트 상태를 상시 감시하여 자동 배포 및 드리프트(Drift) 복구를 수행하는 패러다임인 **GitOps**
- 배경/필요성: 외부 배포 권한과 수동 변경은 **키 유출•드리프트** 유발

#### 한줄 요약

- Git의 선언적 구성을 실제 상태와 지속해서 맞추는 깃옵스가 핵심이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Reconciliation Loop (조정 루프)**: GitOps 컨트롤러가 Git 저장소의 Desired State와 K8s 클러스터의 Actual State 간의 차이(Drift)를 주기적으로(e.g., 3분) 비교하고 자동 수정 동기화하는 무한 루프.
- **Pull-based Deployment**: K8s 내부의 GitOps 에이전트(ArgoCD)가 외부 Git 저장소에서 상태를 끌어와(Pull) 배포함으로써, 클러스터 외부로의 6443/TCP 포트 오픈 및 보안 키 유출을 차단하는 기술.

</details>

- 4대 핵심 원칙 (**Declarative, Versioned/Immutable, Pulled Automatically, Continuously Reconciled**)
- Push 기반과 대비되는 **Pull 기반 배포 아키텍처**
- 자동 **Drift Detection & Self-healing (자동 복구)** 제공

#### 한줄 요약

- Git 선언 기준선, 풀 기반 제어기, 드리프트 복구가 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **ArgoCD / FluxCD**: CNCF 아키텍처 상의 표준 GitOps 툴로, Kubernetes Custom Resource Definition(CRD)을 기반으로 Git의 YAML 파일과 K8s 상태를 실시간 동기화.

</details>

```text
[개발자 Commit & PR] ──► [Git Manifest Repository (SSOT)]
                                    ▲
                                    │ (Pull & Watch)
 [K8s Cluster 내 ArgoCD Engine] ─────┴─────► [K8s Target Cluster (Actual State)]
```

선의 의미: Git 저장소가 SSOT 역할을 수행하고, K8s 내부에 상주하는 ArgoCD Engine이 Git의 Desired State를 주기적 Watch/Pull 하여 Target Cluster에 Apply 하는 구조.

| 구성요소 | 책임 |
|:---|:---|
| 개발자 | 선언 상태 변경과 PR 검토 수행 |
| Git 매니페스트 저장소 | 원하는 상태와 변경 이력 보관 |
| GitOps 제어기 | 선언•실제 상태 비교와 조정 수행 |
| K8s 대상 클러스터 | 실제 워크로드 상태 실행•보고 |

#### 한줄 요약

- 변경 주체•상태 저장소•제어기•클러스터가 핵심이다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **OutOfSync & Synced**: ArgoCD 상에서 Git의 선언 상태와 K8s 실물 상태가 다를 때 `OutOfSync`, 완벽히 일치할 때 `Synced`로 표시되는 상태 구분.

</details>

```text
┌──────────────────────────────┐
│ Git Manifest PR Approved     │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. 선언 상태 기록            │
│ 2. 저장소 변경 관찰          │
│ 3. 상태 차이 판정            │
│ 4. 목표 상태 적용            │
│ 5. 드리프트 복구             │
└──────────────┬───────────────┘
               ▼
  [Synced & Healthy 상태 유지]
```

### 동작 원리

1. **선언 상태 기록**: 승인된 매니페스트 변경을 Git에 기록.
2. **저장소 변경 관찰**: 제어기가 새 커밋과 선언 상태 감지.
3. **상태 차이 판정**: 원하는 상태와 실제 상태의 차이 식별.
4. **목표 상태 적용**: 제어기가 K8s API로 변경 사항 반영.
5. **드리프트 복구**: 수동 변경을 감지해 선언 상태로 조정.

#### 한줄 요약

- 실제 상태 관찰, 상태 차이 판정, 목표 상태 적용의 순환이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Push-based CI/CD vs Pull-based GitOps**: Push 기반(Jenkins, GitHub Actions)은 CI 서버가 K8s 6443 포트에 직접 접속하여 명령 전송, Pull 기반(ArgoCD)은 K8s 내부 에이전트가 Git을 끌어당겨 내부 적용.

</details>

| 비교 항목 | Traditional Push-based CI/CD (Jenkins, Actions) | GitOps Pull-based Pattern (ArgoCD, Flux) |
|:---|:---|:---|
| 배포 주체 | 외부 CI/CD 서버 | **K8s 클러스터 내부 에이전트** |
| 방화벽 / 보안 | 외부 실행기에 K8s API 권한 부여 | **내부 제어기가 저장소를 조회해 권한 경계 축소** |
| 수동 변경 대응 | 별도 드리프트 탐지•복구 절차 필요 | **Self-healing으로 선언 상태 재조정** |
| 롤백 (Rollback) | CI 파이프라인 재구동 | **`git revert` 후 제어기의 상태 재조정** |

#### 한줄 요약

- 선언 상태는 깃옵스, 명령 작업은 푸시 배포가 핵심이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Sealed Secrets**: Git-first 사상을 유지하기 위해 DB 암호나 토큰을 비대칭키로 암호화하여 Git에 안전하게 commit 한 후, K8s 내부 컨트롤러만 복호화하게 만드는 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| Git 저장소에 K8s Secret 비밀키 평문 저장 위험 | **Sealed Secrets / External Secrets Operator + Vault** | 평문 비밀정보 노출 위험 축소 |
| 수십~수백 개 앱 매니페스트 관리 복잡도 | **ArgoCD ApplicationSet + Helm / Kustomize** | 매니페스트 중복 제거 |
| CI 파이프라인과 CD 파이프라인의 저장소 엉킴 | **App Source Repo 대 Deployment Manifest Repo 분리** | 권한 및 보안 격리 |

> 사례: **Kubernetes + ArgoCD + Kustomize + Sealed Secrets** 기업 표준 GitOps 스택

#### 한줄 요약

- 정책 검증, 외부 비밀 저장소, 최소 권한에 기반한 조정 통제가 핵심이다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **GitOps 채택 기준(GitOps Adoption Criteria)**: K8s 오케스트레이션 사용 유무, Zero-Trust 보안 수준 및 CI/CD 자동화 성숙도에 따른 체계.

</details>

- 선언 상태 조정이 필요한 K8s는 **GitOps**, 명령형 작업은 **Push 파이프라인** 선택

#### 한줄 요약

- 깃옵스의 자동 복구와 운영 감사성을 확보할 수 있는지가 핵심이다.
