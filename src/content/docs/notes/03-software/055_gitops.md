---
sidebar:
  order: 55
  label: "055. GitOps"
  badge:
    text: "미출 · 50%"
    variant: note
title: "GitOps"
date: "2026-08-27T00:44:00+09:00"
tags:
  - "notes-software"
weight: 55
extra:
  question_no: "055"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "선언적 인프라와 Git 기반 지속적 배포 및 자동 동기화"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **GitOps**: Git 저장소를 시스템의 단일 진실 공급원(SSOT)으로 삼고, 선언적(Declarative) 매니페스트를 클러스터에 자동 동기화하는 운영 모델.
- **SSOT(Single Source of Truth)**: 시스템의 목표 상태(Desired State)를 정의하는 유일한 단일 권위 저장소(Git).

</details>

- 정의/개념: Git 저장소를 **단일 진실 공급원(SSOT)** 으로 삼고, 클러스터 내부 컨트롤러가 목표 상태를 자동 수렴시키는 **GitOps** 운영 모델
- 배경/필요성: `kubectl`로 클러스터를 직접 바꾸면 실제 상태와 문서가 어긋나는 형상 드리프트가 남고 CI 서버에 클러스터 관리자 권한까지 넘겨야 하므로, Git 저장소를 선언적 단일 원본으로 두고 클러스터 안 에이전트가 그 상태로 수렴시키는 풀 방식으로 바꿀 필요

#### 한줄 요약
- 선언적 인프라 명세를 Git에 버전 관리하고, 클러스터 내부 에이전트가 목표 상태를 자동 동기화한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Pull-based Deployment**: 외부 CI가 클러스터에 접속하는 대신, 클러스터 내부의 ArgoCD/Flux가 Git을 아웃바운드로 감시하여 상태를 당겨오는 방식.
- **Reconciliation Loop(조정 루프)**: Git의 선언 상태(Desired)와 K8s 실제 상태(Actual)의 차이(Drift)를 주기적으로 비교하여 일치시키는 제어 루프.

</details>

- **OpenGitOps 4대 원칙**(선언형 명세, Git 버전 제어, 풀 기반 자동 인입, 지속적 조정) 준수
- 클러스터 인바운드 방화벽 오픈 없는 **풀 기반(Pull-based)** 배포로 제로 트러스트 보안 달성
- 런타임 임의 수정 발생 시 Git 선언 상태로 강제 복구하는 **자가 치유(Self-Healing)**

#### 한줄 요약
- 풀 기반 수렴은 드리프트와 권한 노출을 없애는 대신 모든 변경이 Git을 거치게 하므로, 신속성을 감사 가능성과 맞바꾼 구조다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **ArgoCD / FluxCD**: Kubernetes 클러스터 내부에서 동작하며 Git 리포지토리의 YAML 변경을 감지하여 K8s API로 동기화하는 GitOps 컨트롤러.

</details>

```text
[GitOps 아키텍처 및 Pull 동기화 구조]
|-- Git 배포 저장소 (SSOT)
|-- GitOps 컨트롤러 (ArgoCD)
|-- Reconciliation Engine
`-- CI 파이프라인
```

선의 의미: 계층 및 클러스터 내부 컨트롤러의 아웃바운드 Pull 동기화 구조

| 구성요소 | 책임 |
|:---|:---|
| Git 배포 저장소 (SSOT) | 시스템 목표 상태를 정의하는 K8s 매니페스트(YAML)의 완전한 버전 보관 |
| GitOps 컨트롤러 (ArgoCD) | Git 저장소와 실제 클러스터 상태를 비교하여 **차이(Drift) 감지 및 자동 Sync** |
| Reconciliation Engine | K8s API Server를 호출하여 파드 생성, 서비스 갱신 등 **자가 치유(Self-Healing)** |
| CI 파이프라인 | 앱 빌드 후 **배포 Git 저장소의 이미지 태그(`image.tag`)만 갱신** |

#### 한줄 요약
- 조정 엔진이 Git의 선언 상태와 클러스터 실제 상태를 계속 비교하므로, 배포가 명령의 실행이 아니라 차이의 수렴으로 정의된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **OutOfSync**: Git에 정의된 매니페스트 내용과 실제 K8s 클러스터 리소스 상태 사이에 불일치가 발생한 상태.

</details>

```text
개발자가 배포 매니페스트 Git 저장소에 PR 병합 (예: image.tag: v2.0)
        │
   ArgoCD가 Webhook 또는 Polling을 통해 Git 신규 커밋 감지
        │
   Git 목표 상태(v2.0)와 클러스터 실제 상태(v1.0)를 비교하여 OutOfSync 판정
        │
   K8s API Server를 호출하여 신규 ReplicaSet 생성 및 롤링 배포 수행
        │
   클러스터 상태가 목표 상태(v2.0)와 일치(Synced)됨을 확인
        │
   (누군가 수동으로 kubectl delete pod 실행 시)
   ┌────┴─────┐
   │ 즉각 자가 치유(Self-Healing) 작동하여 Git 매니페스트 기준으로 원상 복구
```

#### 한줄 요약
- 사람이 클러스터를 직접 바꿔도 조정 루프가 다시 Git 상태로 되돌리므로, 자가치유는 곧 수동 개입을 무효로 만드는 성질이기도 하다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Push 기반 CI/CD vs Pull 기반 GitOps**: Jenkins가 K8s kubeconfig 관리자 권한을 쥐고 밀어넣는 Push와 ArgoCD가 내부에서 당겨오는 Pull 비교.

</details>

| 비교 항목 | 전통적 Push 기반 CI/CD (Jenkins) | Pull 기반 GitOps 모델 (ArgoCD) |
|:---|:---|:---|
| 배포 실행 주체 | **외부 CI 서버 (Jenkins, GitHub Actions)** | **클러스터 내부 컨트롤러 (ArgoCD, Flux)** |
| 클러스터 보안 | CI 서버에 **K8s Admin Token 영구 보관** | **외부 접근 차단 (아웃바운드 Git 통신만 수행)** |
| 형상 드리프트 대응 | 수동 변경 발생 시 방치됨 | **주기적 조정 루프로 감지 후 즉시 원복** |
| 롤백 절차 | 이전 빌드 파이프라인 재실행 | **`git revert` 커밋 하나로 수 초 내 롤백** |

#### 한줄 요약
- Push 방식의 보안 위험과 형상 드리프트를 Pull 방식 GitOps의 자가 치유와 제로 인바운드로 해결한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Sealed Secrets / External Secrets Operator**: Git에 비밀번호를 비대칭 암호화하여 커밋하고 클러스터 내부에서만 복호화하는 보안 솔루션.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| Git 저장소에 DB 암호 등 Secret 평문 노출 | **Sealed Secrets 또는 External Secrets Operator(Vault 연동)** | Git에 암호화된 비밀 저장 및 클러스터 안전 복호화 |
| 소스 코드와 배포 매니페스트 혼재로 인한 빌드 루프 | **애플리케이션 소스 레포와 배포 매니페스트 레포의 물리적 분리** | CI 무한 루프 차단 및 개발자/운영자 권한 격리 |
| 환경별(Dev, Stg, Prod) 매니페스트 중복 | **Kustomize Overlay 또는 Helm Chart** 템플릿 표준화 | 공통 Base 매니페스트 재사용 및 환경별 값만 오버레이 |
| 긴급 핫픽스 시 수동 변경의 원복 충돌 | 긴급 조치도 반드시 **Git 커밋/PR을 통해 수행하는 문화 정착** | 변경 이력 100% 추적성 및 거버넌스 사수 |

#### 한줄 요약
- 선언적 수렴은 드리프트와 권한 노출을 없애는 대신 긴급 상황에서도 Git을 거치게 만들므로, 핫픽스 경로까지 Git 기반으로 설계하고 기밀은 암호화해 저장소에 두어야 우회 유인이 사라진다.

## Ⅶ. 결론

- 선언적 배포는 **GitOps**, 형상 일치는 **조정 루프** 선택

#### 한줄 요약
- GitOps는 Git을 단일 진실 공급원으로 선언하고 자가 치유를 통해 인프라와 배포의 신뢰성을 극대화하는 클라우드 운영의 표준 패러다임이다.
