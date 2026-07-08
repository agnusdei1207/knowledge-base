---
title: "NUMA 인지 스케줄링 (NUMA-aware Scheduling)"
date: "2026-07-08"
tags:
  - "cspe-software"
weight: 31
extra:
  question_no: "031"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- NUMA는 CPU 소켓마다 로컬 메모리 접근 지연이 다른 구조임
- NUMA 인지 스케줄링은 스레드와 메모리를 같은 노드에 가깝게 배치하는 정책임
- 원격 메모리 접근이 많아지면 지연과 대역폭 비용이 크게 증가함

## Ⅰ. 개요

- **정의/개념**: NUMA 인지 스케줄링은 멀티소켓 시스템에서 스레드와 메모리와 장치를 같은 NUMA 노드 근처에 배치해 원격 메모리 접근을 줄이고 캐시 지역성을 높이는 스케줄링 정책임
- **배경/필요성**: 멀티소켓 서버에서는 CPU 수를 늘려도 원격 메모리 지연과 interconnect 트래픽이 커지면 성능이 급격히 악화되므로, 단순 부하 균형보다 지역성을 반영한 배치가 필요함

## Ⅱ. 특징

- 동일한 CPU 활용률이라도 NUMA 배치 품질에 따라 성능 차이가 크게 남
- 메모리 first-touch와 CPU affinity가 기본 제어 수단이 됨
- VM과 DB와 in-memory workload처럼 메모리 민감 서비스에서 효과가 큼
- 과도한 migration은 locality 개선보다 오히려 캐시 손실을 키울 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | NUMA 무시 스케줄링 | NUMA 인지 스케줄링 |
|:---|:---|:---|
| 배치 기준 | 전체 CPU 공정성 중심 | CPU와 메모리 지역성 중심 |
| 장점 | 단순함 | 원격 메모리 비용 절감 |
| 한계 | 원격 접근 급증 가능 | 정책과 계측 복잡도 증가 |
| 적합 환경 | 단일 소켓 또는 저민감 workload | 멀티소켓 메모리 집약 workload |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| NUMA Node Topology | 소켓과 메모리와 장치의 물리 배치를 표현해 배치 정책의 기준 좌표가 됨 |
| CPU Affinity Policy | 특정 스레드가 같은 코어 집합에 머물게 해 캐시와 메모리 지역성을 높임 |
| Memory Binding | 페이지를 특정 NUMA 노드에 우선 할당해 원격 접근을 줄이는 핵심 정책임 |
| Migration Controller | 성능 개선을 위해 스레드나 페이지를 옮기되 과도한 이동은 억제함 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 토폴로지 파악   | --> | 초기 배치      | --> | 접근 패턴 관찰 | --> | 재배치 조정    |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **토폴로지 파악**: OS가 NUMA 노드와 장치 위치를 인식함
2. **초기 배치**: 스레드와 메모리를 같은 노드 주변에 우선 배치함
3. **접근 패턴 관찰**: 원격 접근과 interconnect 트래픽을 관측함
4. **재배치 조정**: 필요 시 migration이나 memory rebinding을 수행함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 스레드와 메모리 페이지가 다른 소켓에 흩어지면 원격 메모리 지연이 누적될 수 있음
   - 해결방안: first-touch와 memory binding을 적용하고 remote memory access ratio와 p99 latency로 검증함
2. 문제: 자동 migration이 과도하면 캐시가 깨지고 스케줄러 오버헤드가 증가할 수 있음
   - 해결방안: migration threshold와 affinity 정책을 조정하고 migration count와 cache miss delta로 검증함
3. 문제: VM이나 컨테이너 배치가 NUMA를 무시하면 호스트 튜닝 효과가 크게 줄어들 수 있음
   - 해결방안: 오케스트레이션 계층까지 NUMA 정책을 연동하고 locality compliance와 throughput stability로 검증함

## Ⅶ. 적용 사례

- 대형 DB 서버에서는 NUMA 메모리 바인딩을 적용하고 확인 지표는 remote memory access ratio와 p99 latency임
- 가상화 호스트에서는 VM을 소켓 단위로 묶어 배치하고 확인 지표는 locality compliance와 throughput stability임
- 메모리 집약 분석 노드에서는 migration 정책을 조정하고 확인 지표는 migration count와 cache miss delta임

## Ⅷ. 결론

NUMA 인지 스케줄링은 CPU를 고르게 쓰는 기술이 아니라 메모리와 실행 위치를 가깝게 두어 멀티소켓 비용을 상쇄하는 지역성 최적화 기술임.
