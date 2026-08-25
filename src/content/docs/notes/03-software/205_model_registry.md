---
sidebar:
  order: 205
  label: "205. 모델 레지스트리"
  badge:
    text: "기출 · 50%"
    variant: note
title: "모델 레지스트리 (Model Registry)"
date: "2026-08-25T11:00:00+09:00"
tags:
  - "notes-software"
weight: 205
extra:
  question_no: "205"
  source_status: "기출"
  source_history: "135회"
  priority: 50
  priority_note: "모델 승인•버전•배포 연결이 최근 출제됨"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **모델 레지스트리 (Model Registry)**: 머신러닝 모델 아티팩트의 불변 버전, 계보(Lineage), 검증 증적, 승인 배포 상태를 중앙 집중 관리하는 MLOps 거버넌스 저장소.
- **Model Lineage**: 모델 아티팩트가 어떤 학습 코드(Git), 훈련 데이터셋(DVC), 하이퍼파라미터로 생성되었는지 역추적하는 계보.

</details>

- 정의/개념: 학습된 머신러닝 모델 아티팩트의 **버전, 메타데이터, 계보(Lineage) 및 승인 배포 상태를 중앙 통제하는 MLOps 저장소**
- 배경/필요성: 모델 파일의 수동 공유 및 버전 미관리로 인한 **학습 데이터 출처 유실, 미검증 모델의 무단 배포 및 규제 감사 추적 불가 해결 불가**

#### 한줄 요약
- 불변 아티팩트와 Lineage 추적 및 2인 승인 거버넌스를 통해 모델의 안전한 승격과 무중단 롤백을 실현한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Immutable Versioning**: 한 번 등록된 모델 파일과 메타데이터는 수정이나 덮어쓰기가 불가능한 불변 보존 원칙.
- **Production Alias**: 서빙 엔드포인트가 모델 버전 번호가 아닌 `champion` 논리적 별칭을 바라보게 하여 무중단 전환을 지원하는 기법.

</details>

- 한 번 등록된 아티팩트는 변조 및 덮어쓰기가 불가능한 **불변 버전 관리(Immutable Versioning)**
- 성능 지표, 보안 스캔, 규제 적합성을 통과해야 승격되는 **승인 게이트(Approval Gate)**
- 서빙 엔드포인트가 바라보는 논리적 포인터를 변경하는 **프로덕션 별칭(Production Alias)**

#### 한줄 요약
- 불변 버전, 승인 게이트, 프로덕션 별칭을 통해 모델 배포의 안전성과 거버넌스를 보장한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **모델 레지스트리 4대 구성요소**: Artifact Store(바이너리/해시), Lineage Graph(코드/데이터 계보), Validation & RBAC(검증/2인 승인), Production Alias(챔피언 별칭).

</details>

```text
[모델 레지스트리(Model Registry) 거버넌스 및 배포 아키텍처]
|-- 1. Model Artifact Store (S3 / GCS: `model.onnx` + SHA-256 무결성 해시 불변 저장)
`-- 2. Lineage & Metadata Graph (MLflow / W&B)
    |-- Git Commit Hash + DVC Dataset Hash + Hyperparameters 1:1 결속
    `-- Model Signature: 입력/출력 텐서 스키마(Tensor Schema) 정의
`-- 3. Validation & Approval Layer (4-Eyes Approval: 데이터 사이언티스트 등록 -> 엔지니어 승인)
`-- 4. Production Alias Layer (Serving Endpoint -> `champion` Alias -> 신규 Model v3.0 전환)
```

선의 의미: 계층 및 아티팩트와 계보가 등록되면 검증 증적에 따라 2인 승인을 거쳐 Production Alias가 신규 버전으로 전환되는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **아티팩트 저장소 (Artifact)**| 모델 바이너리 파일과 **SHA-256 무결성 해시, 입출력 모델 서명(Signature) 불변 보관** | S3 불변 스토리지 |
| **계보 그래프 (Lineage)** | 코드 커밋, **훈련 데이터 스냅샷, 피처 버전, 하이퍼파라미터 간의 1:1 관계 추적**| 메타데이터 그래프 |
| **검증 및 승인 (Approval)** | 오프라인 벤치마크 점수와 보안 검사를 검토하여 **2인 승인(4-Eyes)을 거쳐 Production 승격**| RBAC 거버넌스 |
| **별칭 제어기 (Alias)** | `champion` 별칭 포인터를 변경하여 **추론 API의 무중단 배포 및 즉각 롤백 수행** | 무중단 라우팅 |

#### 한줄 요약
- 아티팩트 저장소, 계보 그래프, 검증/승인 계층, 별칭 제어기가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **모델 레지스트리 5단계**: 아티팩트 등록 $\to$ 계보 결속 및 검증 $\to$ 2인 승인 심사 $\to$ Champion Alias 전환 $\to$ 이상 시 즉각 롤백.

</details>

```text
머신러닝 모델 학습 완료 및 승격 파이프라인
        │
   1. [아티팩트 등록] Kubeflow 파이프라인이 `model.onnx`와 SHA-256 해시를 MLflow에 등록
        │
   2. [계보 결속 및 검증] Git 커밋과 DVC 데이터셋 해시를 연결하고 AUC 0.95 리포트 첨부
        │
   3. [2인 승인 심사] ML 엔지니어와 아키텍트가 검증 증적을 검토하고 전자서명으로 승격 승인
   ┌────┴───────────────────────────┐
  승인 완료 (적합)                 승인 거부 (결격)
   │                                 │
4A. [Champion Alias 전환]           4B. [재실험 요구]
   `champion` 포인터를 v3.0으로 갱신    파라미터 및 데이터셋 재학습
   │                                 │
   ▼                                 │
5. 운영 중 이상 감지 시 즉각 v2.0 롤백│
   │                                 │
   └────┬────────────────────────────┘
        ▼
   안전하고 검증된 프로덕션 모델 서빙 완료
```

#### 한줄 요약
- 아티팩트 등록 → 계보 결속 → 2인 승인 → 별칭 전환 → 즉각 롤백 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Model Registry vs Experiment Tracker vs Artifact Store**: 승인 및 배포 통제(Registry), 실험 파라미터 비교(Tracker), 단순 바이너리 저장소(Artifact Store).

</details>

| 비교 항목 | 모델 레지스트리 (Model Registry) | 실험 추적기 (Experiment Tracker) | 아티팩트 저장소 (Artifact Store) |
|:---|:---|:---|:---|
| 핵심 관리 목적 | **상용 환경 배포 승인, 거버넌스 감사, 롤백** | **개발 단계 하이퍼파라미터 튜닝 메트릭 비교**| **대용량 모델 가중치 파일의 물리적 안전 보관** |
| 핵심 관리 대상 | **승인 상태(Staging/Prod), Champion Alias** | **Run별 파라미터, Loss 손실 함수 그래프** | **S3 객체 스토리지, SHA-256 바이너리 파일** |
| 배포 승인 기능 | **2인 승인(4-Eyes) 워크플로우 내장** | 승인 워크플로우 부재 | 승인 기능 부재 |
| 최적 적용 단계 | **프로덕션 릴리즈 및 운영 거버넌스 단계** | 모델 연구 및 초기 실험 단계 | 빌드 및 아티팩트 영속화 단계 |

#### 한줄 요약
- 실험 비교는 Experiment Tracker, 물리 저장은 Artifact Store, 운영 승인과 거버넌스는 Model Registry를 적용한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **4-Eyes Principle (2인 승인)**: 단일 엔지니어가 독단적으로 모델을 배포하지 못하도록 승인 권한자를 분리하는 규제 준수 통제.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 단일 개발자가 검증되지 않은 모델을 운영에 임의 배포 | **`RBAC` 역할 분리 및 `4-Eyes Approval (2인 승인)` 워크플로우 강제** | 무단 배포 사고 원천 차단 |
| 데이터셋 출처가 누락되어 운영 모델 결함 원인 규명 불가 | **`Artifact Hash + Git Commit + DVC 해시` 계보(Lineage) 필수 결속** | 모델 100% 추적성 및 재현성 확보 |
| 모델 레지스트리 장애 시 전체 서빙 엔드포인트 연쇄 마비 | **Alias 라우팅 메타데이터 로컬 캐싱 및 레지스트리 다중화 구성** | 레지스트리 장애 격리 및 가용성 확보 |
| 모델 파일 크기 폭증으로 인한 서빙 인스턴스 다운로드 지연 | **모델 양자화(INT8) 및 P2P/로컬 캐시 기반 모델 배포 가속화** | 모델 기동 및 페일오버 시간 단축 |

#### 한줄 요약
- 2인 승인 강제, 3중 계보 결속, 별칭 캐싱, 양자화 배포로 운영한다.

## Ⅶ. 결론

- 엔터프라이즈 AI 모델의 배포 안전성과 글로벌 규제 준수를 확립하기 위해 **MLflow 기반의 불변 아티팩트 저장소와 3중 계보(Lineage) 추적 체계를 전사 표준 구축**하고, **2인 승인(4-Eyes) 거버넌스와 Champion 별칭 기반 무중단 롤백**을 결합하여 고신뢰 MLOps 레지스트리 완성

#### 한줄 요약
- 모델 레지스트리는 불변 버전 관리, 계보 추적, 2인 승인 거버넌스를 통해 검증된 AI 모델만을 안전하게 배포하는 핵심 MLOps 인프라다.