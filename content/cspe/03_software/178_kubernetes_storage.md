---
title: "쿠버네티스 스토리지 - PVC·PV·StorageClass (Kubernetes Storage)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 178
---

# 📖 【암기용】 개념 완전 이해

> 목적: Kubernetes 스토리지를 처음 보는 사람도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: Kubernetes 스토리지는 Pod의 생명주기와 데이터를 분리하는 **영속 볼륨(Persistent Volume) 추상화 계층**이며, PVC(요청)·PV(실제 자원)·StorageClass(동적 프로비저닝 정책)·CSI(표준 연결 인터페이스)로 구성된다.
- **왜 필요한가**: Pod의 로컬 파일시스템(overlay fs)은 Pod가 재생성되면 사라진다. 하지만 DB, 메시지 큐, 파일 업로드처럼 Pod 교체와 무관하게 유지되어야 하는 데이터가 있어, 저장소를 Pod 바깥으로 분리해야 한다.
- **핵심 직관**: Pod는 임시 작업자, PVC는 저장소 신청서, PV는 실제 창고, StorageClass는 "필요할 때마다 창고를 새로 지어주는 자동 발주 규정", CSI는 어느 창고 브랜드든 꽂히는 표준 규격 잠금장치다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| 영속 볼륨(Persistent Volume) 추상화 | Pod 생명주기와 무관하게 유지되는 저장소 구조 전체 — 이 개념이 속하는 상위 카테고리 | Pod와 분리된 별도 창고 체계 |
| PVC (PersistentVolumeClaim) | 사용자가 용량·접근모드를 "요청"하는 오브젝트, namespace 범위 | 사물함 신청서 |
| PV (PersistentVolume) | 실제 저장소 자원을 나타내는 cluster 범위 오브젝트 | 실제로 배정된 사물함 |
| StorageClass | provisioner와 reclaimPolicy 등 정책을 담아 PV를 동적으로 생성시키는 템플릿 | 필요할 때 창고를 새로 짓는 자동 발주 규정 |
| CSI (Container Storage Interface) | Kubernetes와 외부 스토리지 벤더(EBS, Ceph 등)를 연결하는 표준 플러그인 인터페이스 | 브랜드 상관없이 꽂히는 표준 커넥터 |
| accessMode (RWO/ROX/RWX) | 볼륨을 몇 개의 노드가 어떤 방식(읽기/쓰기)으로 동시에 마운트할 수 있는지 | 1인 전용실 / 열람 전용 도서관 / 공용 회의실 |
| reclaimPolicy (Retain/Delete) | PVC 삭제 시 PV와 실제 데이터를 남길지 지울지 정하는 정책 | 계약 해지 시 짐을 보관할지 폐기할지 |
| volumeBindingMode (Immediate/WaitForFirstConsumer) | PV를 PVC 생성 즉시 만들지, Pod 스케줄링 후 만들지 결정 | 방을 미리 배정 vs 입주자 확정 후 배정 |

## 깊이 이해

### 왜 이 구조가 필요했나 (배경)
- 컨테이너는 기본적으로 stateless 배포에 최적화되어 있다. Pod가 재생성되면 컨테이너 내부 파일시스템(overlay fs)은 통째로 사라진다. 그런데 DB, 메시지 큐, 로그 저장, 사용자 업로드 파일은 Pod 교체와 무관하게 데이터가 살아 있어야 한다.
- 그래서 Kubernetes는 "저장소를 원하는 요청(PVC)"과 "실제 저장소 자원(PV)"을 분리했다 — 애플리케이션 개발자는 "100Gi RWO SSD 하나 주세요"만 선언하고, 그것이 어느 클라우드의 어떤 디스크인지는 신경 쓰지 않는다.

### PVC-PV-StorageClass-CSI 관계를 수치로 이해
- **정적 프로비저닝(옛 방식)**: 관리자가 미리 PV 여러 개를 만들어두고 PVC가 조건에 맞는 PV와 bind된다. 규모가 커지면 사람이 미리 다 만들어야 해 관리 비용이 커진다.
- **동적 프로비저닝(현재 표준)**: PVC가 StorageClass 이름(예: `fast-ssd`)만 지정하면, 그 StorageClass의 provisioner(CSI 드라이버)가 즉석에서 볼륨을 만들어 PV로 등록하고 bind한다. 예: `ReadWriteOnce, 100Gi, storageClassName: fast-ssd` PVC를 생성하면 AWS EBS CSI 드라이버가 실제 100GiB gp3 볼륨을 만드는 데 보통 수 초~수십 초(운영 목표 p95 60초 이내) 걸린다.
- StatefulSet은 replica마다 별도 PVC를 volumeClaimTemplates로 자동 생성한다. 3-replica StatefulSet `web`이면 `data-web-0`, `data-web-1`, `data-web-2` PVC가 각각 별도 PV에 bind되고, Pod가 재시작돼도 같은 순번의 PVC를 다시 mount해 데이터가 유지된다.

### accessMode를 실제 상황으로 구분
- **RWO(ReadWriteOnce)**: 한 번에 노드 1개만 read-write로 마운트. EBS, GCP PD 같은 대부분의 블록 스토리지가 이 방식 — DB 인스턴스 하나가 자기 디스크를 독점하는 상황에 맞는다.
- **ROX(ReadOnlyMany)**: 여러 노드가 동시에 읽기 전용으로 마운트. 정적 자산 배포 등 드물게 쓰인다.
- **RWX(ReadWriteMany)**: 여러 노드가 동시에 read-write. NFS, EFS, CephFS 같은 파일 스토리지에서만 지원 — 여러 Pod가 업로드 파일을 함께 써야 하는 공유 폴더 시나리오에 쓴다.
- **판별 원리**: "이 볼륨을 몇 개의 Pod가 동시에 쓰기까지 해야 하는가"로 결정한다. DB는 RWO, 공유 파일 서버는 RWX.

### reclaimPolicy를 시나리오로 이해
- **Delete(동적 프로비저닝의 기본값)**: PVC 삭제 -> PV도 삭제 -> 클라우드 디스크(EBS 등)도 실제로 삭제된다. 실수로 PVC를 지우면 데이터가 영구 손실될 수 있다.
- **Retain**: PVC를 삭제해도 PV와 실제 디스크는 남고 상태가 `Released`로 바뀐다 — 관리자가 수동으로 회수·재바인딩해야 한다. DB처럼 손실 피해가 큰 워크로드는 Retain과 VolumeSnapshot(예: 15분 주기)을 함께 쓴다.
- **판별 원리**: 재현 불가능한 데이터(DB, 사용자 업로드)는 Retain, 캐시성 임시 데이터는 Delete.

### volumeBindingMode가 필요한 이유 (zone mismatch)
- **Immediate**: PVC 생성 즉시 PV를 만든다. 클라우드 디스크는 특정 가용영역(AZ)에 종속되는데, Pod가 나중에 다른 AZ 노드에 스케줄링되면 볼륨을 마운트하지 못해 Pending 상태에 빠질 수 있다.
- **WaitForFirstConsumer**: PV 생성을 Pod가 스케줄링될 때까지 미룬다 — 스케줄러가 정한 노드의 AZ에 맞춰 볼륨을 만들어 zone mismatch를 원천적으로 막는다. 멀티 AZ 클러스터에서는 사실상 필수 설정이다.

### 비유와 흔한 오해
- **비유**: PVC는 사물함 신청서, PV는 실제로 배정된 사물함, StorageClass는 "SSD형/HDD형 사물함을 필요할 때마다 새로 설치해주는 자동 발주 규정", CSI는 어느 제조사 사물함이든 꽂을 수 있는 표준 규격 잠금장치다.
- **오해**: "PVC를 지우면 Pod만 못 쓰게 될 뿐 데이터는 항상 안전하다" — 틀렸다. reclaimPolicy가 Delete면 실제 데이터까지 사라진다. 백업(VolumeSnapshot)은 PVC/PV 구조와 별개로 반드시 설계해야 한다.

## 연결 개념
- CSI - PV 생성을 실제 스토리지 벤더에 연결하는 표준 인터페이스
- StatefulSet - volumeClaimTemplates로 Pod별 PVC를 자동 생성해 이 구조를 그대로 활용
- VolumeSnapshot - reclaimPolicy와 별개로 데이터 복구를 보장하는 백업 메커니즘

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: Kubernetes 스토리지 답안은 PVC/PV/StorageClass 관계와 CSI, reclaimPolicy, accessMode 선택 기준을 함께 써야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: PVC는 저장소 요청, PV는 실제 저장소, StorageClass는 동적 프로비저닝 정책임.
> 2. **가치**: Pod 생명주기와 데이터를 분리해 상태 저장 애플리케이션을 Kubernetes에서 운영 가능하게 함.
> 3. **판단 포인트**: accessMode, reclaimPolicy, volumeBindingMode, backup RPO/RTO를 업무 특성에 맞춰 선택해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 스토리지 추상화 이해 확인 | PVC, PV, StorageClass, CSI | volumeMount만 설명 |
| 상태 데이터 운영 판단 확인 | RWO/RWX, reclaimPolicy, snapshot | 데이터 삭제 리스크 누락 |
| 장애 복구 설계 확인 | backup, snapshot, zone binding | Pod 재시작을 백업으로 오해 |

> 요약: 스토리지 문제는 객체 관계와 데이터 보존 정책을 함께 제시해야 함.

---

## Ⅰ. 개요 및 필요성

- 개요: Kubernetes 스토리지는 Pod와 데이터를 분리하는 구조임.
- 배경: Pod는 재생성될 수 있으므로 상태 데이터는 외부 저장소에 보관해야 한다.
- 필요성: PVC, PV, StorageClass로 저장소 요청, 할당, 동적 프로비저닝 절차를 표준화한다.

---

## Ⅱ. 구조 및 구성요소

```text
Pod -> PVC -> PV -> CSI Driver -> Storage Backend
StorageClass -> Dynamic Provisioning -> PV 생성
  / reclaimPolicy
  / volumeBindingMode
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| PVC | 용량, accessMode 요청 | namespace 범위 |
| PV | 실제 저장소 리소스 | cluster 범위 |
| StorageClass | provisioner, policy 정의 | 동적 생성 |
| CSI Driver | 외부 저장소 연동 | attach, mount, snapshot |

> 요약: PVC가 요청을 표현하고 StorageClass와 CSI가 실제 PV를 생성해 Pod에 연결함.

---

## Ⅲ. 동작원리 및 흐름도

```text
PVC 생성 -> StorageClass 선택 -> CSI가 볼륨 생성 -> PV/PVC bind -> Pod mount -> snapshot/backup
  / WaitForFirstConsumer -> 스케줄링 후 생성
  / Retain -> 삭제 후 데이터 보존
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | PVC로 용량과 accessMode 요청 | Bound/Pending 상태 |
| 2 | StorageClass가 provisioner와 정책 제공 | className 일치 |
| 3 | CSI가 외부 볼륨 생성 | PV 생성, volumeHandle |
| 4 | Pod가 PVC를 volumeMount | mount 성공 |
| 5 | snapshot, backup, restore 수행 | RPO/RTO 충족 |

> 요약: Kubernetes 스토리지는 요청, 프로비저닝, 바인딩, 마운트, 백업 단계로 운영됨.

---

## Ⅳ. 특징

| 구분 | emptyDir/로컬 | PVC/PV/StorageClass | 수치/판단 포인트 |
|:---|:---|:---|:---|
| 생명주기 | Pod 삭제 시 손실 | Pod와 분리 | 데이터 보존 |
| 생성 | 수동 볼륨 준비 | 동적 프로비저닝 | 생성 p95 60초 |
| 접근 | 노드/Pod 제한 | RWO, ROX, RWX | DB vs 공유파일 |
| 복구 | 재생성 중심 | snapshot, backup | RPO 15분 |

> 요약: 상태 데이터는 PVC 기반 영속 저장소와 별도 백업 정책으로 운영해야 함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | Pod local storage | PVC/PV 추상화 | 데이터 보존 필요 |
| 비용/처리 | 고정 수동 디스크 | 동적 생성, class별 tier | IOPS, 용량 |
| 운영/위험 | 삭제 시 데이터 손실 | reclaimPolicy, snapshot | RPO/RTO |

> 요약: 데이터 보존과 복구 요구가 있으면 PVC와 백업 정책을 함께 설계해야 함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| PVC Pending | StorageClass 오류, zone 불일치 | WaitForFirstConsumer, event 분석 | Pending PVC 수 |
| 데이터 삭제 | reclaimPolicy Delete 오설정 | Retain, snapshot, backup | 복구 테스트 성공 |
| I/O 병목 | 부적합 storage tier | IOPS 기준 class 분리 | p95 I/O latency |

> 요약: 스토리지 리스크는 Pending, 삭제 정책, I/O 지연으로 나타남.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 프로비저닝 | PVC Bound p95 60초 이하 | CSI metric |
| 복구 | RPO 15분, RTO 30분 | restore drill |
| I/O | DB p95 write latency 10ms 이하 | storage metric |

> 요약: 저장소 운영 품질은 PVC 바인딩 시간, 복구 목표, I/O 지연으로 검증함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. Class 표준화: `fast-ssd`, `standard`, `shared-rwx` 등 StorageClass를 업무 IOPS와 accessMode 기준으로 분리
2. 삭제 통제: DB 계열 PV는 reclaimPolicy Retain, VolumeSnapshot 15분 주기, 월 1회 restore drill 적용
3. Zone 정합성: `WaitForFirstConsumer`로 Pod 스케줄링 후 볼륨을 생성해 zone mismatch로 인한 Pending을 줄임

**결론 (2줄):**
- 기술사 판단: 상태 저장 워크로드는 PVC/PV/StorageClass와 RPO/RTO를 함께 설계해야 함
- 향후 방향: CSI Snapshot, 데이터 서비스 Operator, 정책 기반 백업이 Stateful workload 운영의 기본 요소가 됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Kubernetes 스토리지를 설명하시오" | PVC 바인딩과 CSI 프로비저닝 흐름 | PVC/PV/StorageClass 역할 |
| 요구사항 명시형 | "상태 저장 애플리케이션 설계 방안을 제시하시오" | snapshot, backup, zone binding 흐름 | accessMode, reclaimPolicy, RPO/RTO 기준 |

> 요약: 설명형은 객체 관계, 설계형은 데이터 보존과 복구 기준 중심으로 전환함.
