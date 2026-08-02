---
sidebar:
  order: 157
  label: "157. 쿠버네티스 스토리지: PVC·PV·StorageClass (Kubernetes Storage)"
  badge:
    text: "미출 · 50%"
    variant: note
title: "쿠버네티스 스토리지: PVC·PV·StorageClass (Kubernetes Storage)"
date: "2026-08-02T23:27:00+09:00"
tags:
  - "notes-software"
weight: 157
extra:
  question_no: "157"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "영속 볼륨의 요청·자원·정책 관계가 독립적임"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **쿠버네티스 영속 스토리지(Kubernetes Persistent Storage)**: PVC가 워크로드의 저장 요구를 선언하고 PV가 실제 저장 자원을 제공하며 StorageClass가 동적 프로비저닝 정책을 정의하는 구조이다.

</details>

- 정의/개념: PVC·PV·StorageClass로 **워크로드의 저장 요구와 인프라 구현**을 분리하는 쿠버네티스 영속 스토리지 구조
- 배경/필요성: 파드 로컬 저장은 재생성·노드 장애 시 **데이터 소실**

### 쉽게 이해하기 (학습용)
- 애플리케이션은 저장 제품을 직접 고르지 않고 PVC에 필요한 크기와 접근 방법만 적어 인프라 변경과 데이터 수명을 분리한다.

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **회수 정책**: 회수 정책은 PVC 해제 뒤 PV와 실제 저장 데이터를 삭제할지 보존할지 결정한다.

</details>

- **PVC·PV 분리** 기반 요구 추상화
- **StorageClass·CSI** 기반 동적 생성
- **회수 정책** 기반 삭제 후 보존

### 쉽게 이해하기 (학습용)
- PVC는 창고 요청서, PV는 배정된 창고, StorageClass는 창고를 만드는 표준으로 보면 세 객체의 책임이 구분된다.

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **StorageClass**: StorageClass는 동적 프로비저닝에 사용할 저장 유형, 프로비저너, 매개변수를 정의한다.

</details>

```mermaid
block
    columns 1
    A["PVC·PV 제어기"]
    B["StorageClass"]
    C["CSI Controller"]
    D["PV"]
    E["CSI Node·kubelet"]
    A --- B
    B --- C
    C --- D
    D --- E
```

| 구성요소 | 책임 |
|:---|:---|
| PVC·PV 제어기 | 요청 탐색·**볼륨 바인딩** |
| StorageClass | **생성·회수·바인딩** 정책 |
| CSI Controller | **볼륨 생성·삭제·연결** |
| PV | 용량·접근·**토폴로지 표현** |
| CSI Node·kubelet | **노드 게시·파드 마운트** |

### 쉽게 이해하기 (학습용)

- 제어기가 요청서에 맞는 창고를 찾고 없으면 StorageClass와 CSI로 새 창고를 만든 뒤 PV 자원표로 연결한다.

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **4. PV·PVC 바인딩 상태**: 용량, 접근 모드, 클래스 조건이 맞으면 PV와 PVC가 바인딩 상태가 된다.

</details>

```mermaid
sequenceDiagram
    participant A as API 서버
    participant C as 스토리지 제어기
    participant D as CSI 드라이버
    participant V as 백엔드 스토리지
    participant K as kubelet
    A->>C: 1. PVC 용량·접근 모드
    C->>D: 2. 클래스·토폴로지 공급 명세
    D->>V: 3. 백엔드 볼륨 생성 명세
    V-->>D: 볼륨 식별자·토폴로지
    D-->>C: 볼륨 생성 결과
    C->>A: 4. PV·PVC 바인딩 상태
    A->>K: 바인딩된 파드·볼륨 명세
    K->>D: 5. 노드 연결·마운트 명세
```

**동작 원리**

1. **PVC 용량·접근 모드**: 애플리케이션의 저장 조건 선언
2. **클래스·토폴로지 공급 명세**: 프로비저너와 배치 영역 확정
3. **백엔드 볼륨 생성 명세**: 접근 가능한 실제 저장소 생성 요청
4. **PV·PVC 바인딩 상태**: 볼륨 자원과 요청의 일대일 연결 기록
5. **노드 연결·마운트 명세**: 파드 경로에 파일시스템 게시

### 쉽게 이해하기 (학습용)

- 첫 소비자 대기를 사용하면 파드가 놓일 영역을 먼저 정하고 같은 영역에 볼륨을 만들어 지역 불일치로 인한 배치 실패를 막는다.

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **PV**: PV는 클러스터가 제공하는 지속성 저장 자원을 나타내는 API 리소스다.

</details>

| 저장 객체 | PVC | PV | StorageClass |
|:---|:---|:---|:---|
| 적용 기준 | **애플리케이션 저장 요구** | **실제 볼륨 자원 표현** | **동적 생성·수명 정책** |
| 핵심 특징 | 용량·**접근 모드·StorageClass** | 볼륨 식별자·**토폴로지·ClaimRef** | 프로비저너·**회수·바인딩 정책** |
| 한계 | **조건 불일치·StorageClass 오타** | **토폴로지·접근 모드 오류** | **삭제·즉시 바인딩 오설정** |

### 쉽게 이해하기 (학습용)
- PVC는 소비자의 요구, PV는 공급된 자원, StorageClass는 공급 방식을 나타내므로 저장 제품 변경을 파드 명세에서 숨길 수 있다.

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **삭제 전파**: 삭제 전파는 PVC나 PV 삭제가 실제 스토리지와 데이터 제거로 이어지는 범위를 뜻한다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 파드·볼륨의 **영역 불일치**로 스케줄링 실패 | **첫 소비자 대기** 적용 | 지역 **배치 실패** 방지 |
| 다중 노드 쓰기 요구와 백엔드 접근 모드 불일치 | CSI·백엔드 **접근 모드 시험** | 지원 범위 **오판** 방지 |
| 저장 성능 등급이 업무 부하보다 낮아 지연 증가 | 성능 등급별 **부하 시험** 적용 | **처리량·저장 지연** 사전 확인 |
| PVC 오삭제가 백엔드 볼륨 삭제로 전파 | 중요 데이터 **Retain·삭제 승인** | 백엔드 **삭제 전파** 방지 |
| 스냅숏만 보관해 애플리케이션 데이터 관계 불일치 | **일관 백업·별도 복사·복원 시험** | 실제 **복구 가능성** 검증 |

### 쉽게 이해하기 (학습용)
- 데이터베이스 파드의 영역과 볼륨 영역을 맞추고 PVC 삭제와 별개인 백업을 복원해 봐야 노드 손실과 오삭제를 모두 견딜 수 있다.

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **복구 목표**: 복구 목표는 장애 시 허용 가능한 데이터 손실량과 서비스 복구 시간을 기준으로 백업·복제 전략을 정한다.

</details>

- **접근 방식**으로 StorageClass를, 데이터 중요도·**복구 목표**로 회수 정책·백업 결정

### 쉽게 이해하기 (학습용)
- 용량만 요청하지 말고 파드 위치, 동시 접근, 삭제 후 보존, 다른 환경 복원까지 기준으로 저장 수명주기를 선택해야 한다.
