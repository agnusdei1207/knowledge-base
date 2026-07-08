---
title: "스토리지 가상화 (Storage Virtualization)"
date: "2026-07-08"
tags:
  - "cspe-hardware"
weight: 96
extra:
  question_no: "096"
  exam_status: "미출제"
---

## 미리 알고가기

- 논리 볼륨은 여러 물리 저장장치를 추상화해 제공하는 저장 단위임
- pooling은 여러 장치의 용량과 성능을 하나의 자원 집합으로 묶는 방식임
- thin provisioning은 실제 사용량 기준으로 물리 용량을 늦게 할당하는 방식임

## Ⅰ. 개요

- **정의/개념**: 스토리지 가상화는 물리 디스크와 어레이와 LUN을 논리 볼륨과 스토리지 풀로 추상화해 위치와 장치 차이를 숨기고 정책 중심으로 저장 자원을 제공하는 기술임
- **배경/필요성**: 물리 장치 단위 운영은 용량 단편화와 벤더 종속과 중단 없는 이전의 어려움을 키우므로, 운영 유연성과 자원 활용률을 높이기 위해 가상화 계층이 필요함

## Ⅱ. 특징

- 물리 장치와 서비스 제공 단위를 분리해 용량 풀링과 논리 볼륨 구성이 쉬움
- snapshot과 replication과 migration 같은 데이터 서비스를 중앙 정책으로 제공할 수 있음
- thin provisioning으로 초기 증설 비용을 줄일 수 있지만 과할당 위험이 생김
- 가상화 엔진 자체가 새로운 성능 경로이자 장애 도메인이 됨

## Ⅲ. 종류 및 비교

| 판단 기준 | 물리 직접 운영 | 스토리지 가상화 |
|:---|:---|:---|
| 자원 관리 | 장치별 개별 할당 | pool 기반 중앙 할당 |
| 데이터 이동 | 이전 시 중단과 수작업 부담 큼 | migration으로 논리적 이동 가능 |
| 운영 기능 | 장비별 도구 의존 | snapshot, clone, replication 통합 |
| 위험 | 구조가 단순함 | 매핑 계층 병목과 장애 영향 확대 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Host Interface | 서버에 논리 볼륨을 제공해 애플리케이션이 물리 장치 위치를 직접 알지 않도록 만듦 |
| Virtualization Engine | 논리 주소를 물리 위치에 매핑하고 thin provisioning과 migration 정책을 집행함 |
| Storage Pool | 성능과 보호 수준이 다른 물리 저장장치를 묶어 용량 활용률과 확장 유연성을 높임 |
| Data Service Layer | snapshot과 clone과 replication을 논리 계층에서 제공해 운영 자동화와 복구 체계를 지원함 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 풀 구성        | --> | 논리 볼륨 할당 | --> | 주소 매핑      | --> | 정책 운영      |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **풀 구성**: 물리 저장장치를 성능과 보호 수준별 자원 풀로 등록함
2. **논리 볼륨 할당**: 업무 요구에 맞는 논리 볼륨과 용량 정책을 설정함
3. **주소 매핑**: 논리 블록 주소를 실제 디스크와 RAID 배치에 연결함
4. **정책 운영**: snapshot과 복제와 마이그레이션과 임계치 관리를 수행함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 가상화 엔진의 메타데이터 처리와 캐시 경로가 병목이 되면 전체 스토리지 지연이 증가할 수 있음
   - 해결방안: 엔진 이중화와 캐시 sizing과 메타데이터 분리를 적용하고 virtualization latency overhead와 cache hit rate로 검증함
2. 문제: thin provisioning을 과도하게 사용하면 실제 물리 용량 부족 시 쓰기 실패가 대규모 서비스 장애로 이어질 수 있음
   - 해결방안: threshold 기반 증설 정책과 quota를 운영하고 physical free capacity와 threshold breach count로 검증함
3. 문제: 중앙 가상화 계층 장애는 여러 업무 볼륨에 동시 영향을 주어 장애 범위를 확대할 수 있음
   - 해결방안: controller HA와 multipath와 정기 failover test를 운영하고 failover time과 path recovery rate로 검증함

## Ⅶ. 적용 사례

- 통합 스토리지 운영에서는 이기종 장비를 논리 풀로 묶고, provisioning time과 capacity utilization로 결과를 확인함
- DR 환경에서는 replication과 snapshot 정책을 표준화하고, failover time과 RPO 준수율로 결과를 확인함
- 가상 서버 환경에서는 thin provisioning을 적용해 초기 할당량을 줄이고, pool free capacity와 overcommit ratio로 결과를 확인함

## Ⅷ. 결론

스토리지 가상화의 가치는 추상화 자체보다 성능 오버헤드와 용량 과할당과 장애 도메인을 통제하면서 운영 유연성을 얻는 데 있음.
