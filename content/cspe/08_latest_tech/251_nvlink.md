---
title: "NVLink (NVLink)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 251
extra:
  question_no: "251"
  exam_status: "기출"
  exam_history: "138회"
  exam_note: "전망"
---

## 미리 알고가기

- NVLink는 CPU와 GPU 사이보다 주로 GPU와 GPU 사이의 고속 연결에 초점을 둔 인터커넥트임
- 대규모 AI 학습에서 노드 내부 GPU 간 집단 통신 병목을 줄이는 역할이 큼
- PCIe보다 더 높은 대역폭과 낮은 지연을 목표로 하는 구조로 이해하면 됨

## Ⅰ. 개요

- **정의/개념**: NVLink는 GPU와 GPU 또는 GPU와 일부 프로세서 간의 대용량 데이터 교환을 위해 설계된 고속 인터커넥트로 대역폭과 지연 특성을 개선해 AI와 HPC 통신 성능을 높이는 연결 기술임
- **배경/필요성**: 대규모 딥러닝은 연산보다 파라미터와 activation 교환이 병목이 되기 쉬워 노드 내부 가속기 간 고속 연결 기술이 학습 효율의 핵심 요소가 됨

## Ⅱ. 특징

- GPU 간 직접 고대역 통신으로 집단 연산 병목을 줄임
- 대형 모델 학습에서 메모리 공유와 데이터 교환 효율을 높임
- 서버 내부 토폴로지 설계에 따라 실효 성능 차이가 크게 남
- PCIe만 사용하는 구성보다 멀티 GPU 확장 효율이 높을 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | NVLink | PCIe | InfiniBand |
|:---|:---|:---|:---|
| 주 적용 범위 | 노드 내부 GPU 연결 | 범용 장치 연결 | 노드 간 고속 네트워크 |
| 대역폭 | 매우 높음 | 중간 | 높음 |
| 지연 | 낮음 | 중간 | 노드 내부보다는 높음 |
| 핵심 가치 | 멀티 GPU 병렬 효율 | 범용성과 호환성 | 클러스터 확장성 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| GPU Endpoint | 각 GPU가 NVLink 포트를 통해 다른 GPU와 직접 데이터를 교환하는 통신 종단점임 |
| NVLink Lane | 여러 레인을 병렬로 사용해 높은 대역폭을 제공하는 물리 연결 채널임 |
| Switch or Fabric Path | 다수 GPU 토폴로지에서 경로를 확장해 전체 통신 효율을 높이는 연결 구조임 |
| Memory Access Engine | 원격 GPU 메모리에 빠르게 접근해 데이터 이동 비용을 낮추는 통신 제어 계층임 |
| Topology Manager | GPU 배치와 링크 경로를 고려해 통신 집약 작업을 최적 노드에 배치하는 운영 계층임 |

```text
+-------+   NVLink   +-------+   NVLink   +-------+
| GPU 0 |<---------> | GPU 1 |<---------> | GPU 2 |
+-------+             +-------+             +-------+
     \_______________________________________________/
                     High-speed GPU fabric
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 연산 분할    | -> | GPU 메모리 준비 | -> | NVLink 전송  | -> | 원격 데이터 결합 | -> | 동기화 완료    |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **연산 분할**: 병렬 학습 작업을 여러 GPU에 나눔
2. **GPU 메모리 준비**: 각 GPU가 필요한 activation과 gradient를 준비함
3. **NVLink 전송**: 링크를 통해 고속으로 데이터를 교환함
4. **원격 데이터 결합**: 집단 연산이나 파라미터 업데이트를 수행함
5. **동기화 완료**: 다음 연산 단계로 이동함

## Ⅵ. 문제점 및 해결 방안

1. 문제: GPU 토폴로지가 통신 패턴과 맞지 않으면 NVLink가 있어도 일부 경로에 병목이 집중되어 확장 효율이 떨어질 수 있음
   - 해결방안: topology aware placement와 communication scheduling을 적용하고 peer to peer bandwidth와 scaling efficiency로 검증함
2. 문제: NVLink 의존 구성이 커질수록 특정 플랫폼과 하드웨어 생태계에 종속될 위험이 커질 수 있음
   - 해결방안: portability aware architecture와 fallback interconnect design을 적용하고 migration effort index와 heterogeneous deployment readiness로 검증함
3. 문제: 노드 내부는 빨라도 노드 간 통신이 느리면 전체 분산 학습 병목이 외부 네트워크로 이동할 수 있음
   - 해결방안: NVLink와 InfiniBand를 결합한 balanced fabric design을 적용하고 intra node to inter node communication ratio와 end to end step time으로 검증함

## Ⅶ. 적용 사례

- 멀티 GPU 학습 서버가 토폴로지 인식 작업 배치를 적용하며 확인 지표는 peer to peer bandwidth와 scaling efficiency임
- 하이브리드 클러스터가 이식성 고려 설계를 운영하며 확인 지표는 migration effort index와 heterogeneous deployment readiness임
- 대규모 LLM 학습 환경이 내부와 외부 패브릭 균형을 조정하며 확인 지표는 intra node to inter node communication ratio와 end to end step time임

## Ⅷ. 결론

NVLink는 노드 내부 멀티 GPU 효율을 크게 높이는 핵심 인터커넥트이므로 토폴로지와 외부 네트워크까지 함께 설계해야 전체 학습 성능이 살아남.
