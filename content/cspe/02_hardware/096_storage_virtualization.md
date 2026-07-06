---
title: "스토리지 가상화 (Storage Virtualization)"
date: "2026-07-06"
tags:
  - "cspe-hardware"
weight: 96
---

## 미리 알고가기

- 논리 볼륨: 여러 물리 디스크나 LUN(Logical Unit Number)을 추상화해 제공하는 저장 단위임
- I/O(Input/Output): 호스트와 저장장치 사이에서 발생하는 읽기·쓰기 요청임
- Thin Provisioning: 실제 사용량만큼 물리 용량을 할당하면서 큰 논리 용량을 보이는 방식임
- Snapshot: 특정 시점의 데이터 상태를 논리적으로 보존하는 기능임
- Pooling: 여러 저장장치의 용량과 성능을 하나의 자원 풀로 묶는 방식임

## Ⅰ. 개요

- **정의**: 스토리지 가상화는 물리 디스크, 배열, LUN을 논리 볼륨과 스토리지 풀로 추상화해 위치와 장치 차이를 숨기는 저장 자원 관리 기술임. 용량 활용률, 마이그레이션, 복제, 장애 대응을 운영 정책 기준으로 통합하기 위해 사용함.
- **배경/필요성**: 물리 장치 중심 운영은 서버별 용량 단편화와 벤더 종속, 중단 없는 이전의 어려움을 만듦. 추상화 계층을 두면 애플리케이션은 동일한 볼륨을 사용하면서 백엔드 장치를 교체하거나 확장할 수 있음.
- **비유**: 여러 창고의 위치와 크기를 숨기고 사용자에게는 하나의 가상 창고 번호만 제공하는 관리 시스템임.

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 저장 자원 추상화와 운영 효과 설명 | pooling, logical volume, snapshot, migration, thin provisioning | 서버 가상화와 동일시 |

> 요약: 스토리지 가상화는 물리 저장장치를 논리 자원으로 묶어 운영 유연성과 관리성을 높이는 기술임.

## Ⅱ. 특징/비교

| 판단 기준 | 물리 스토리지 직접 운영 | 스토리지 가상화 |
|:---|:---|:---|
| 용량 관리 | 장치별 할당과 증설이 필요함 | pool 기반 할당과 thin provisioning 가능 |
| 데이터 이동 | 장치 교체 시 중단과 복잡한 복사가 필요함 | 볼륨 migration과 tiering으로 투명 이동 가능 |
| 운영 기능 | 장비별 기능과 관리 도구에 의존함 | snapshot, clone, replication을 논리 계층에서 제공 |
| 위험 | 구조가 단순하고 지연 예측이 쉬움 | mapping 계층 장애와 성능 오버헤드가 생길 수 있음 |

> 요약: 스토리지 가상화는 운영 유연성을 얻는 대신 추상화 계층의 성능과 장애를 관리해야 함.

- **적용 조건**: 용량 풀링 이득이 데이터 경로 지연과 장애 범위 증가를 상쇄해야 함
- **선택 지표**: virtualization latency, pool free capacity, failover time을 함께 봐야 함
- **운영 관점**: 가상화 계층의 메타데이터와 정책을 별도 보호 대상으로 관리해야 함

## Ⅲ. 구성요소

```text
+----------+      +----------------+      +--------------+
| Host I/O | ---> | Virtual volume | ---> | Storage pool |
+----------+      +----------------+      +--------------+
                         |                         |
                         v                         v
                  +--------------+          +--------------+
| Mapping table|          | Physical vol |
                  +--------------+          +--------------+
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| 호스트 인터페이스 | 서버에 논리 디스크, LUN, 파일시스템을 제공함 | 창구 |
| 가상화 엔진 | 논리 주소를 물리 위치로 매핑하고 정책을 적용함 | 주소 번역 관리자 |
| 스토리지 풀 | 여러 디스크·어레이·클래스를 묶은 자원 집합임 | 통합 창고 |
| 데이터 서비스 | snapshot, clone, replication, tiering 기능을 제공함 | 부가 관리 서비스 |

> 요약: 스토리지 가상화는 호스트 요청을 논리 볼륨으로 받고 매핑 계층이 물리 풀에 배치함.

## Ⅳ. 절차

```text
+----------+      +----------+      +----------+      +----------+
| Pool     | ---> | Allocate | ---> | Map      | ---> | Policy   |
+----------+      +----------+      +----------+      +----------+
```

1. **풀 구성** — 성능, 용량, 보호 수준이 다른 물리 저장장치를 자원 풀로 등록함
2. **볼륨 할당** — 업무 요구에 따라 논리 볼륨, thin/thick 속성, 접근 권한을 설정함
3. **주소 매핑** — 호스트 논리 블록 주소를 물리 위치와 RAID(Redundant Array of Independent Disks)/tier 정책에 연결함
4. **정책 운영** — snapshot, replication, migration, capacity threshold를 관리함

> 요약: 가상화된 스토리지는 물리 자원을 풀링한 뒤 논리 볼륨과 정책으로 업무에 제공됨.

## Ⅴ. 문제점 및 개선방안

- **P1 매핑 계층 병목**: 가상화 엔진의 CPU(Central Processing Unit), 캐시, 메타데이터 I/O가 전체 경로의 병목이 될 수 있음
- **P1 대응**: 가상화 엔진 이중화, 캐시 sizing, 메타데이터 분리, I/O profile 튜닝을 수행함 (확인: virtualization latency overhead)
- **P2 용량 과할당 위험**: thin provisioning을 과도하게 사용하면 물리 용량 부족 시 쓰기 실패가 발생함
- **P2 대응**: thin pool threshold, 자동 증설, quota, capacity forecasting을 적용함 (확인: physical free capacity)
- **P3 장애 영향 확대**: 중앙 가상화 계층 장애가 여러 업무 볼륨에 동시에 영향을 줄 수 있음
- **P3 대응**: controller HA(High Availability), multipath, 정기 failover test로 가상화 계층 장애 범위를 검증함 (확인: failover time)

> 요약: 스토리지 가상화는 추상화 계층을 별도 운영 대상과 장애 도메인으로 관리해야 함.

## Ⅵ. 실무 적용 사례

| 적용 영역 | 적용 방식 | 확인 지표 |
|:---|:---|:---|
| 통합 스토리지 풀 운영 | 이기종 스토리지를 논리 풀로 묶고 업무별 볼륨, QoS, tier 정책을 표준으로 제공함 | provisioning time, capacity utilization |
| Thin provisioning 관리 | 물리 용량 임계치, 자동 증설, quota를 운영 정책으로 두어 쓰기 실패를 예방함 | physical free capacity, threshold breach count |
| 재해복구·이중화 | controller HA, replication, multipath failover를 정기 시험해 가상화 계층 장애 범위를 확인함 | failover time, data loss, path recovery rate |

> 요약: 실무에서는 추상화 편의보다 성능 오버헤드, 용량 위험, 장애 도메인을 운영 지표로 관리해야 함.

## Ⅶ. 전망

- **발전 방향**: SDS(Software-Defined Storage), HCI(Hyper-Converged Infrastructure), cloud block storage, NVMe-oF(Non-Volatile Memory Express over Fabrics)와 결합해 정책 기반 저장 자원 자동화로 확장됨
- **기술사적 판단**: 도입 평가는 기능 수보다 데이터 경로 지연, 장애 격리, 벤더 종속, 운영 자동화 수준을 기준으로 해야 함
- **기술사 제언**: 용량 풀링을 시작하기 전에 critical workload별 성능 기준선과 복구 절차를 문서화해야 함
