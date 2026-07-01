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
- **개요**: Pod가 사라져도 데이터를 보존하기 위해 PVC, PV, StorageClass로 외부 저장소를 연결하는 구조
- **왜 필요한가**: Pod의 로컬 파일시스템은 재생성 때 사라질 수 있으므로 DB, 로그, 파일 업로드 같은 상태 데이터에는 영속 저장소가 필요하다.
- **핵심 직관**: Pod는 임시 작업자이고, PVC는 저장소 신청서, PV는 실제 창고, StorageClass는 창고 자동 배정 규칙이다.

## 깊이 이해
- **배경·문제의식**: 컨테이너는 stateless 배포에 적합하지만 모든 애플리케이션이 무상태는 아니다. 데이터베이스, 메시지 큐, 분석 작업은 Pod 교체와 무관하게 데이터가 유지되어야 한다.
- **작동 원리**: 사용자가 PVC로 용량과 접근 모드를 요청하면 Kubernetes가 기존 PV를 bind하거나 StorageClass와 CSI 드라이버를 통해 동적 PV를 만든다. Pod는 PVC를 volume으로 mount한다.
- **비유**: 직원이 사물함 신청서(PVC)를 내면 관리자가 빈 사물함(PV)을 배정하거나 새 사물함을 설치(StorageClass)하고, 직원은 사물함 번호만 사용한다.
- **구체 예시**: `ReadWriteOnce`, 100Gi, `fast-ssd` PVC를 생성하면 CSI 드라이버가 SSD 볼륨을 만들고 Pod에 mount한다. StatefulSet은 replica별 PVC를 만들어 `data-web-0`, `data-web-1`처럼 보관한다.
- **흔한 오해·주의점**: PVC가 삭제되어도 reclaimPolicy가 Retain이면 실제 PV 데이터가 남는다. Delete이면 클라우드 디스크가 제거될 수 있어 백업 정책이 필요하다.

## 연결 개념
- CSI - Kubernetes와 외부 저장소를 연결하는 표준 인터페이스
- StatefulSet - Pod별 고유 PVC와 네트워크 ID 제공
- VolumeSnapshot - PV 백업과 복구에 사용하는 스냅샷 객체

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

Kubernetes 스토리지는 Pod와 데이터를 분리하는 구조임. Pod는 재생성될 수 있으므로 상태 데이터는 외부 저장소에 보관해야 한다. PVC, PV, StorageClass는 저장소 요청, 할당, 자동 생성을 표준화한다.

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
