---
sidebar:
  order: 205
  label: "205. 모델 레지스트리 (Model Registry)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "모델 레지스트리 (Model Registry)"
date: "2026-08-06T23:27:50+09:00"
tags: ["notes-software"]
weight: 205
extra:
  question_no: "205"
  source_status: "기출"
  source_history: "135회"
  priority: 50
  priority_note: "모델 승인•버전•배포 연결이 최근 출제됨"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Model Registry (모델 레지스트리)**: 학습 완료된 ML 모델의 불변 버전(Immutable Version)에 코드·데이터·학습 환경의 계보(Lineage)와 평가 결과·승인 상태를 연결하여, 어떤 버전이 운영에 배포되었는지를 중앙에서 통제하는 MLOps 핵심 저장소.
- **Model Lineage (모델 계보)**: 특정 모델 버전을 생성하는 데 사용된 학습 코드(Git 커밋)·데이터 버전·피처 버전·하이퍼파라미터·학습 실행 환경을 DAG로 연결한 이력. 모델 품질 문제 발생 시 원인 규명에 필수.
- **Production Alias (운영 별칭)**: 실제 운영 추론 서비스가 호출하는 논리 이름(예: `champion`). 이 별칭이 가리키는 불변 버전 번호만 바꾸면 다운타임 없이 배포·롤백 가능.

</details>

- 정의/개념: ML 모델의 불변 버전·계보·평가 증적·승인 상태를 연결하여 "어떤 버전이 언제 누구에 의해 승인되어 운영에 배포되었는가"를 추적하고 롤백까지 통제하는 **Model Registry 중앙 거버넌스 체계**
- 배경/필요성: 파일 시스템에 모델 파일만 저장하면 어떤 데이터로 학습했는지·누가 운영 승인했는지·현재 운영 중인 정확한 버전이 무엇인지 추적 불가하고, 장애 시 신속한 롤백을 위한 검증 버전 관리 체계 요구성

#### 한줄 요약

- 모델마다 출생 기록과 시험 성적표를 붙이고 승인된 번호만 운영 이름표가 가리키게 한다.

## Ⅱ. 특징 (Model Registry의 4대 핵심 특성)

<details><summary>핵심 용어</summary>

- **Artifact Hash (산출물 해시)**: 모델 파일의 바이너리 내용으로 계산한 SHA-256 등의 요약값. 동일한 해시값 = 동일한 모델 파일 보장. 배포 시 무결성 검증 및 변조 탐지에 사용.

</details>

- **Immutable Version (불변 버전)**: 한 번 등록된 모델 버전은 덮어쓰기 불가(v1, v2, v3... 누적). 변경이 필요하면 반드시 새 버전을 등록하여 이전 버전과의 비교·롤백을 항상 보장.
- **Approval Gate (승인 게이트)**: Staging 단계에서 Production으로 승격 시, 성능 기준(정확도·F1) + 계보 완전성 + 보안 검토 + 규제 준수를 모두 충족해야 통과하는 다중 합격 관문.
- **Audit Log (감사 로그)**: 모델 등록·승인·별칭 변경·배포·롤백의 모든 행위에 대해 "누가(Principal)·언제(Timestamp)·무엇을(Action)·어떤 이유로(Reason)"를 변경 불가 형태로 기록하는 감사 이력.

#### 한줄 요약

- 모델 파일을 고치지 않고 새 번호로 쌓아 두면 운영 이름표만 이전 번호로 돌려 같은 모델을 다시 배포할 수 있다.

## Ⅲ. 구조 및 구성요소 (Model Registry 아키텍처)

<details><summary>핵심 용어</summary>

- **Model Signature (모델 서명)**: 모델이 입력으로 받는 데이터의 이름·자료형·형상(shape)과 출력하는 예측값의 스키마를 명시한 계약. 배포 전 입출력 형식 호환성 검증에 활용.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                      Model Registry Architecture                       │
├────────────────────────────────────────────────────────────────────────┤
│ [학습 파이프라인] ─────► [후보 버전 등록]                               │
│   - 모델 산출물(Artifact Hash)                                         │
│   - 계보(코드·데이터·피처 버전)                                         │
│   - 모델 서명(입출력 스키마)                                            │
│              │                                                         │
│              ▼                                                         │
│ [평가·계보 검증] ── 성능·무결성·출처 합격 여부 판정                     │
│              │                                                         │
│              ▼ (승인 게이트 통과)                                       │
│ [승인 상태 전환] ── Staging → Production 상태 변경 + Audit Log 기록     │
│              │                                                         │
│              ▼                                                         │
│ [Production Alias 갱신] ── `champion` → v23 (다운타임 없는 전환)        │
│              │                                                         │
│ [감사 로그] ── 모든 행위 불변 이력 저장                                 │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 학습 파이프라인이 후보 버전을 등록(하)→평가 검증(중)→승인 상태 전환(상)→Production Alias 갱신(최상)의 단방향 승격 흐름과, 장애 시 이전 별칭으로 즉시 롤백 가능한 구조.

| 구성요소 | 핵심 역할 및 기능 | 대표 도구 |
|:---|:---|:---|
| **Model Artifact** | **불변 모델 파일·해시·모델 서명 안전 보관** | MLflow, S3 |
| **Model Lineage** | **코드·데이터·피처·학습 실행 관계 DAG 추적** | MLflow, Neptune.ai |
| **Validation Evidence** | **성능·무결성·출처 합격 근거 기록** | 평가 보고서, 테스트 결과 |
| **Approval Policy** | **단계 상태와 Production Alias 전환 권한 통제** | RBAC 정책, 4-Eyes Rule |
| **Audit Log** | **등록·승인·배포·롤백 행위 불변 이력** | Immutable Storage |

#### 한줄 요약

- 모델 파일과 학습 출처·시험 결과를 묶고 승인 정책이 운영 이름표를 바꾼 기록까지 남긴다.

## Ⅳ. 흐름도 (Model Registry 승격·배포·롤백 흐름)

<details><summary>핵심 용어</summary>

- **Four-Eyes Approval (2인 승인)**: 고위험 행위(Production 배포, 금융 모델 승격 등)를 한 명이 단독으로 실행하지 못하도록, 반드시 별개의 승인자가 확인·승인해야 완료되는 내부 통제 방식.

</details>

```text
 1. [후보 버전 등록] ─── Artifact Hash + Lineage + Model Signature 불변 등록
          │
          ▼
 2. [평가·계보 검증] ─── 성능 기준 + 계보 완전성 + 규제 준수 확인
          │
          ├─(미달)────────► 승격 거부, 증적 보완 후 재검증
          │
          └─(통과)────────► Staging 상태로 변경
                                      │
                                      ▼ (4-Eyes Approval)
 3. [Production 승인 전환] ── 2인 승인 완료 + 승인 이유 Audit Log 기록
          │
          ▼
 4. [Production Alias 갱신] ── champion alias → 신규 버전 (무중단 전환)
          │
          ▼
 5. [운영 모니터링 연계] ─── 배포 버전·성능·롤백 이력 Registry에 연결
          │
          └─(장애 발생)────► Production Alias를 이전 검증 버전으로 즉시 복귀
```

### 동작 원리

1. **불변 버전 등록**: Artifact Hash로 모델 파일 무결성을 보증하고 재현 가능성 확보.
2. **승인 게이트**: 4-Eyes Approval로 단독 오배포를 차단하고 Audit Log에 근거 기록.
3. **Production Alias 롤백**: 별칭이 가리키는 버전 번호만 변경하면 즉각 이전 모델 복귀 (**Model Registry 사이클 완결**).

#### 한줄 요약

- 후보 모델의 파일·출처·성적을 확인해 승인하고 운영 이름표를 해당 번호로 바꾼다.

## Ⅴ. 종류 및 비교 (MLOps 저장소 역할 1:1 비교)

<details><summary>핵심 용어</summary>

- **Experiment Tracker (실험 추적기)**: 각 학습 실행(Run)의 하이퍼파라미터·코드 버전·데이터 버전·평가 지표를 자동 기록하여 여러 실험을 비교하고 최적 조합을 찾는 도구. 모델 레지스트리와 연동하여 우수 실험을 후보 버전으로 승격.

</details>

| MLOps 저장소 역할 | Model Registry | Experiment Tracker | Artifact Store |
|:---|:---|:---|:---|
| **핵심 목적** | **운영 배포 승인·버전·롤백 통제** | **후보 실험 비교·재현·선별** | **대용량 모델 파일 불변 보관** |
| **주요 데이터** | 승인 상태·Production Alias·Audit Log | 파라미터·지표·코드·데이터 버전 | 모델 바이너리·Artifact Hash |
| **사용 시점** | 배포·롤백·거버넌스 의사결정 | 학습·실험 비교 단계 | 모델 파일 저장·불러오기 |

#### 한줄 요약

- 파일 창고와 실험 기록은 재료를 보관하고 레지스트리는 그 증거로 운영할 모델 번호를 승인한다.

## Ⅵ. 실무 고려사항 및 대책 (Model Registry 3대 실무 난제 대책)

<details><summary>핵심 용어</summary>

- **RBAC (Role-Based Access Control, 역할 기반 접근 제어)**: 데이터 사이언티스트(모델 등록만 가능)·ML 엔지니어(Staging 승격)·승인자(Production 전환)·감사자(조회만)처럼, 역할별로 Model Registry 접근 권한을 분리하는 통제.

</details>

| 3대 실무 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. 승인 없는 Production 배포** | 단일 계정이 등록·승인·배포 모두 수행 가능 | **RBAC로 역할별 권한 분리 + 4-Eyes Approval 정책 강제화** |
| **2. 계보 불완전으로 재현 불가** | 데이터 버전·피처 버전이 Lineage에 미연결 | **Artifact Hash + Data Snapshot + Feature Store 버전을 Lineage에 강제 연결** |
| **3. 레지스트리 장애 시 배포 불가** | 레지스트리가 단일 장애점으로 작동 | **Active-Active 이중화 및 Alias 정보 외부 캐시 + 정기 복구 훈련** |

> 사례: **MLflow Model Registry를 활용한 금융 신용평가 모델의 4-Eyes Approval 배포 통제 및 규제 감사 로그 보존, Vertex AI Model Registry의 Production Alias 기반 무중단 모델 교체 사례**

#### 한줄 요약

- 신용 모델은 누가 어떤 데이터로 만든 버전을 승인했는지 함께 확인한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **Model Promotion·Rollback Criteria (모델 승격·복귀 기준)**: 성능·계보·규제 요건을 모두 충족한 불변 버전만 Production 승격을 허용하고, 장애·품질 저하 시 즉각 검증된 이전 버전으로 Production Alias를 복귀하는 의사결정 기준.

</details>

- **모델 승격·복귀 기준**에 따라 RBAC·4-Eyes Approval·Audit Log 기반 **Production Alias 통제 및 장애 시 즉각 롤백 체계** 필수 적용

#### 한줄 요약

- 파일·학습 출처·시험 결과를 함께 승인하고 운영 이름표를 이전 번호로 돌릴 수 있어야 한다.
