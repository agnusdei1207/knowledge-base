---
sidebar:
  order: 157
  label: "157. 쿠버네티스 스토리지"
  badge:
    text: "미출 · 50%"
    variant: note
title: "쿠버네티스 스토리지: PVC•PV•StorageClass (Kubernetes Storage)"
date: "2026-08-26T13:12:42+09:00"
tags:
  - "notes-software"
weight: 157
extra:
  question_no: "157"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "영속 볼륨의 요청•자원•정책 관계가 독립적임"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **쿠버네티스 스토리지 3대 요소**: PVC(사용자 요청서), PV(실제 영속 볼륨 자원), StorageClass(동적 프로비저닝 템플릿).
- **CSI(Container Storage Interface)**: K8s 코어 수정 없이 외부 스토리지(EBS, EFS, Ceph) 플러그인을 연결하는 표준 인터페이스.

</details>

- 정의/개념: 컨테이너 파드의 일시적 수명과 물리 스토리지 수명을 분리하기 위해 **PVC(요청), PV(자원), StorageClass(규격)로 추상화한 영속 스토리지 아키텍처**
- 배경/필요성: 컨테이너 쓰기 계층(CoW)의 휘발성으로 인해 발생하는 **파드 재시작 시 데이터 영구 유실 및 스토리지 벤더 변경 시 앱 재설계 해결 불가**

#### 한줄 요약
- 스토리지 요청과 물리 자원을 분리하고 동적 프로비저닝을 통해 데이터 영속성을 보장한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Dynamic Provisioning**: 사용자가 PVC를 제출하면 관리자 수동 개입 없이 CSI 드라이버가 클라우드 EBS/EFS 디스크를 자동 생성.
- **Access Modes**: 단일 노드 독점 쓰기(RWO: ReadWriteOnce), 다중 노드 읽기 전용(ROX: ReadOnlyMany), 다중 노드 동시 공유 쓰기(RWX: ReadWriteMany).

</details>

- PVC(요청)와 PV(자원)를 분리하여 인프라 결합도를 제거하는 **스토리지 추상화**
- StorageClass 및 CSI 드라이버를 통한 **클라우드 볼륨(EBS/EFS) 동적 프로비저닝**
- RWO, ROX, RWX 3대 접근 제어를 통한 **상태 기반 워크로드(Stateful) 완벽 지원**

#### 한줄 요약
- 스토리지 추상화, 실시간 동적 프로비저닝, 3대 접근 모드 제어를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **K8s 스토리지 계층 구조**: Pod/PVC(개발자 영역), PV/StorageClass(인프라 영역), CSI Driver/Cloud Disk(물리 영역).

</details>

```text
[쿠버네티스 스토리지 구성]
|-- PVC
|-- PV
|-- 스토리지 클래스
`-- CSI 드라이버
```

선의 의미: 계층 및 개발자가 PVC를 신청하면 StorageClass와 CSI 드라이버가 물리 디스크를 생성해 PV와 1:1 바인딩하는 구조

| 구성요소 | 책임 | 주요 특징 |
|:---|:---|:---|
| PVC (요청서) | 개발자가 필요한 스토리지 **용량, AccessMode, StorageClass 요구 선언** | 개발자 추상화 객체 |
| PV (볼륨 자원) | 클러스터에 프로비저닝된 **실제 물리 디스크 볼륨의 메타데이터 표현** | PVC와 1:1 바인딩 |
| 스토리지 클래스 (SC) | Provisioner, 볼륨 속성(`gp3/io2`), **재활용 정책(Retain/Delete) 정의** | 동적 생성 템플릿 |
| CSI 드라이버 | K8s 스토리지 API 요청을 받아 **실제 스토리지 생성, 노드 Attach/Mount 수행**| 표준 스토리지 플러그인 |

#### 한줄 요약
- PVC(요청서), PV(자원), StorageClass(규격), CSI 드라이버가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **동적 프로비저닝 5단계**: PVC 제출 $\to$ StorageClass 해석 $\to$ CSI 볼륨 생성 $\to$ PV-PVC 바인딩 $\to$ 노드 Attach 및 마운트.

</details>

```text
StatefulSet 데이터베이스 파드의 PVC 제출
        │
   [PVC 검증] API 서버가 PVC 명세(용량: 100Gi, AccessMode: RWO) 접수 및 유효성 검증
        │
   [StorageClass 선택] 명시된 `gp3-sc` 스토리지 클래스의 Provisioner(`ebs.csi.aws.com`) 호출
        │
   [CSI 볼륨 동적 생성] CSI 드라이버가 AWS API를 호출하여 실제 100Gi EBS gp3 디스크 생성
        │
   [PV 생성 및 바인딩] 생성된 EBS 디스크를 기반으로 PV 객체를 생성하고 PVC와 1:1 Bound 결합
        │
   파드가 배치된 워커 노드에 EBS를 Attach하고 컨테이너 디렉터리로 Mount 완료
```

#### 한줄 요약
- PVC 검증 → StorageClass 선택 → CSI 볼륨 생성 → PV-PVC 바인딩 → 노드 마운트 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **RWO vs ROX vs RWX**: 단일 노드 독점(RWO: EBS), 다중 노드 읽기 전용(ROX), 다중 노드 동시 읽기/쓰기 공유(RWX: EFS).

</details>

| 비교 항목 | ReadWriteOnce (RWO) | ReadOnlyMany (ROX) | ReadWriteMany (RWX) |
|:---|:---|:---|:---|
| 접근 허용 범위 | **단 1개 Node만 읽기/쓰기 독점 점유** | **다수 Node에서 읽기(Read) 전용 공유** | **다수 Node에서 읽기/쓰기 동시 공유** |
| 대표 지원 스토리지| **AWS EBS, GCP Persistent Disk** | **EBS Snapshot, 컨테이너 ISO 이미지** | **AWS EFS (NFS), CephFS, GlusterFS** |
| I/O 성능 특성 | **블록 스토리지 기반 초고속 I/O** | 블록/파일 기반 읽기 전용 | 네트워크 파일시스템(NFS) 오버헤드 |
| 최적 적용 워크로드| **MySQL, PostgreSQL, MongoDB 등 DB** | **정적 미디어 에셋, AI 모델 가중치 파일**| **웹 서버 공통 업로드 파일, CMS 시스템**|

#### 한줄 요약
- 고성능 데이터베이스는 RWO, 공유 파일 저장소는 RWX 스토리지를 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **WaitForFirstConsumer**: EBS 디스크가 파드보다 먼저 생성되어 다른 가용 영역(AZ)에 생기는 불일치(Multi-AZ Attach Fail)를 방지하는 바인딩 모드.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| EBS 볼륨과 Pod의 AZ가 불일치하여 디스크 마운트 실패 | **StorageClass에 `volumeBindingMode: WaitForFirstConsumer` 설정** | Pod 스케줄링된 AZ에 EBS 동적 생성 |
| 단일 EBS(RWO)로 여러 웹 파드가 로그 공유 쓰기 불가 | **스토리지를 AWS EFS(RWX 지원 관리형 NFS)로 전환 배포** | 다중 노드 동시 쓰기 지원 |
| PVC 실수 삭제 시 실제 백엔드 EBS 디스크 데이터 영구 파기 | **StorageClass의 `reclaimPolicy: Retain` 설정 강제** | 디스크 자동 삭제 방지 및 복구 보장 |
| 볼륨 용량 부족으로 데이터베이스 쓰기 락다운 | **`allowVolumeExpansion: true` 설정으로 무중단 PVC 용량 증설** | 가동 중 실시간 스토리지 확장 |

#### 한줄 요약
- WaitForFirstConsumer 설정, RWX(EFS) 전환, Retain 정책, 무중단 볼륨 확장으로 운영한다.

## Ⅶ. 결론

- 데이터 영속성은 **PV/PVC**, 자동 프로비저닝은 **CSI** 선택

#### 한줄 요약
- 쿠버네티스 스토리지는 PVC, PV, StorageClass의 3단계 추상화를 통해 인프라와 애플리케이션을 완벽히 분리하고 데이터 영속성을 보장하는 핵심 기술이다.
