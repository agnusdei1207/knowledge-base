---
title: "쿠버네티스 스토리지 — PVC·PV·StorageClass (Kubernetes Storage)"
date: "2026-07-14T02:30:00+09:00"
tags:
  - "cspe-software"
weight: 178
extra:
  question_no: "178"
  exam_status: "기출"
  exam_history: "133회"
---

## 미리 알고가기

- PV는 관리자가 만들거나 동적 프로비저닝한 클러스터 스토리지 자원이며 Pod와 수명이 분리됨
- PVC는 워크로드가 필요한 용량·접근 모드·StorageClass를 요청하는 객체임
- StorageClass는 provisioner·매개변수·회수 정책·바인딩 방식을 정의하는 스토리지 정책임
- 동적 프로비저닝은 일치하는 PV가 없을 때 StorageClass와 CSI가 실제 볼륨과 PV를 생성함
- 회수 정책 Retain은 PV 해제 후 데이터를 보존하고 Delete는 백엔드 볼륨 삭제를 요청함
- WaitForFirstConsumer는 Pod 배치 토폴로지를 확인한 뒤 볼륨을 프로비저닝·바인딩함
- CSI는 쿠버네티스와 스토리지 드라이버 사이의 볼륨 생성·연결·마운트 규약임
- ClaimRef는 PV가 어느 PVC에 바인딩됐는지 기록하는 참조 정보임

## 작성 근거(검토용)

- PVC·PV·StorageClass는 요청·자원·정책으로 역할이 분리되므로 세 객체의 관계를 중심에 둠
- 핵심 역할·선언 범위·수명과 결과의 정확히 3개 축으로 비교하고 바인딩·마운트·회수 절차로 연결함
- 제목부터 결론까지 5회 전수 검수하여 PVC 요청과 PV 실자원, StorageClass 정책을 구분함

## Ⅰ. 개요

- **정의/개념**: 쿠버네티스 스토리지는 PVC 요구·PV 자원·StorageClass 정책을 분리해 Pod에 볼륨을 제공하는 구조임
- **배경/필요성**: Pod 교체와 스토리지 수명을 분리하고 저장소 구현을 추상화하기 위해 요청·자원·정책 객체가 필요함

### 쉽게 이해하기 (학습용)
- PVC는 저장공간 요청서, PV는 실제 사용할 자원, StorageClass는 자원을 만드는 정책임

## Ⅱ. 특징

- PVC는 백엔드 제품 대신 용량·접근 모드·클래스 같은 사용 요구를 선언함
- PV는 클러스터 자원으로 존재하며 ClaimRef로 PVC와 바인딩됨
- StorageClass는 CSI provisioner와 매개변수로 요청 시 볼륨 생성을 자동화함
- 바인딩 모드·토폴로지·회수 정책이 Pod 배치와 PVC 삭제 후 데이터 처리를 결정함

### 쉽게 이해하기 (학습용)
- 저장소 위치와 보존 정책이 Pod가 어느 노드에 배치되고 삭제 뒤 데이터가 남는지를 좌우함

## Ⅲ. 객체별 비교

| 판단 기준 | PVC | PV | StorageClass |
|:---|:---|:---|:---|
| 핵심 역할 | 워크로드의 스토리지 사용 요구 선언 | 사용할 영속 스토리지 자원 표현 | 동적 생성과 운영 정책 정의 |
| 선언 범위 | 용량·접근 모드·클래스·선택자 | 용량·접근 모드·토폴로지·백엔드 정보 | provisioner·매개변수·회수·바인딩 정책 |
| 수명과 결과 | 요구 기간 동안 Bound 상태와 PV 참조 유지 | Pod와 분리된 자원으로 실제 볼륨·ClaimRef 유지 | 여러 PVC가 재사용하며 동적 볼륨·PV 생성 기준 제공 |

> 요약: PVC는 요구, PV는 자원, StorageClass는 동적 생성 정책을 담당함.

### 쉽게 이해하기 (학습용)
- 요청·실자원·생성 정책을 분리해 애플리케이션이 저장장치 구현을 직접 알지 않게 함

## Ⅳ. 구성요소 및 구조

| 구성요소 | 역할 |
|:---|:---|
| PVC | Pod가 사용할 용량·접근 모드·StorageClass를 요청함 |
| PV Controller | PVC와 PV를 일치시키거나 동적 프로비저닝을 요청함 |
| StorageClass | CSI provisioner·매개변수·회수·바인딩 정책을 제공함 |
| CSI Controller | 백엔드 볼륨을 생성·삭제하고 노드 연결을 관리함 |
| PV | 생성된 볼륨의 용량·접근·토폴로지와 상태를 표현함 |
| CSI Node·kubelet | 선택 노드에 볼륨을 연결·마운트해 Pod에 제공함 |

```text
Pod -> PVC -> PV Controller -> 기존 PV
          +-> StorageClass -> CSI -> 새 볼륨·PV
                                     |
                                  노드 마운트
```

> 요약: PVC는 기존 PV와 바인딩되거나 StorageClass·CSI를 통해 새 PV를 생성함.

### 쉽게 이해하기 (학습용)
- Controller와 CSI가 요청 조건에 맞는 볼륨을 찾거나 새로 만들고 노드에 연결함

## Ⅴ. 프로비저닝·바인딩 절차

```text
PVC 생성 -> PV 탐색·동적 생성 -> PVC·PV 바인딩 -> Pod 노드 선택 -> 볼륨 연결·마운트 -> 회수
```

1. **PVC 생성**: 워크로드가 용량·접근 모드·StorageClass 요구를 제출함
2. **PV 탐색·생성**: 일치하는 PV를 찾고 없으면 StorageClass의 CSI provisioner를 호출함
3. **바인딩**: Controller가 PVC와 PV를 일대일 연결하고 Bound 상태로 변경함
4. **노드 선택**: 스케줄러가 Pod 자원과 볼륨 토폴로지를 함께 만족하는 노드를 찾음
5. **연결·마운트**: CSI와 kubelet이 볼륨을 노드와 Pod 파일시스템에 연결함
6. **회수**: PVC 삭제 후 PV와 백엔드 볼륨을 Retain 또는 Delete 정책으로 처리함

> 요약: PVC 요구가 PV 생성·바인딩과 Pod 배치를 거쳐 실제 노드 마운트로 이어짐.

### 쉽게 이해하기 (학습용)
- 저장 요청이 자원과 연결되고 Pod 위치가 정해지면 해당 노드에 실제 볼륨을 붙임

## Ⅵ. 실무 사례

1. 데이터베이스 Pod는 WaitForFirstConsumer PVC를 쓰고 바인딩 시간·볼륨 연결 오류를 확인함
2. 백업 저장소는 Retain 정책을 적용하고 PVC 삭제 후 PV 상태·복구 시간을 확인함

### 쉽게 이해하기 (학습용)
- 빠른 생성뿐 아니라 PVC 삭제 뒤 데이터를 보존하거나 제거하는 결과까지 확인함

## Ⅶ. 결론

- Kubernetes 스토리지는 PVC 요구와 PV 자원, StorageClass의 토폴로지·회수 정책을 함께 설계해야 함

### 쉽게 이해하기 (학습용)
- 용량 요청만 보지 말고 저장 위치·접근 방식·삭제 후 처리까지 함께 정해야 함
