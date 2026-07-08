---
title: "PCIe 스위칭 아키텍처 (PCIe Switching)"
date: "2026-07-08"
tags:
  - "cspe-hardware"
weight: 94
extra:
  question_no: "094"
  exam_status: "미출제"
---

## 미리 알고가기

- PCIe는 point-to-point 방식의 고속 직렬 I/O 인터페이스임
- Root Complex는 CPU 쪽 PCIe 계층의 시작점임
- Switch는 하나의 상위 링크를 여러 하위 장치로 확장하는 중간 장치임

## Ⅰ. 개요

- **정의/개념**: PCIe 스위칭 아키텍처는 Root Complex와 여러 endpoint 사이에 PCIe switch를 두어 제한된 상위 링크를 다수 장치로 분기하고 패킷을 라우팅하는 확장형 I/O 구조임
- **배경/필요성**: 서버와 가속기 플랫폼은 GPU와 NVMe와 NIC 수요가 빠르게 늘지만 CPU가 제공하는 PCIe 레인 수는 제한적이므로, 장치 fan-out과 유연한 배치를 위해 스위치 기반 확장이 필요함

## Ⅱ. 특징

- 상위 링크 하나로 여러 downstream 장치를 수용해 확장성이 높음
- point-to-point 링크 구조를 유지하면서 패킷 라우팅과 오류 보고를 수행함
- upstream 공유 구조이므로 oversubscription이 발생할 수 있음
- P2P 전송과 hot-plug와 격리 기능 여부가 설계 품질에 큰 영향을 줌

## Ⅲ. 종류 및 비교

| 판단 기준 | 직접 연결 | PCIe 스위칭 |
|:---|:---|:---|
| 확장성 | CPU 레인 수에 직접 제한됨 | 다수 endpoint로 fan-out 가능 |
| 지연 | 가장 낮음 | switch hop만큼 추가 지연 발생 |
| 대역폭 구조 | 장치별 전용 경로 확보가 쉬움 | 상위 링크 공유로 병목 가능 |
| 운영 기능 | 단순 연결 중심 | P2P, hot-plug, AER, ACS 지원 가능 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Root Complex | 시스템 메모리 공간과 PCIe 계층을 연결하며 전체 PCIe 트리의 상위 기준점이 됨 |
| Upstream Port | 스위치가 CPU 쪽과 통신하는 단일 상위 경로로 전체 장치 집합의 공유 병목 지점이 될 수 있음 |
| Downstream Port | NVMe와 GPU와 NIC 같은 endpoint를 개별 포트로 수용해 확장성과 배치를 결정함 |
| Routing and Isolation Logic | TLP 라우팅과 ACS와 오류 보고를 담당해 성능뿐 아니라 DMA 격리 수준까지 좌우함 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 장치 열거      | --> | 주소 라우팅    | --> | 패킷 전달      | --> | 오류/격리 관리 |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **장치 열거**: 펌웨어와 OS가 스위치 하위 endpoint를 탐색하고 주소 공간을 할당함
2. **주소 라우팅**: switch가 TLP 목적지에 따라 적절한 downstream 포트를 선택함
3. **패킷 전달**: flow control과 레인 속도 규칙에 따라 데이터를 버퍼링하고 전달함
4. **오류 및 격리 관리**: AER과 ACS와 링크 상태 감시로 장애와 DMA 경계를 통제함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 하위 장치 총 요구 대역폭이 상위 링크를 초과하면 switch 구간에서 심한 oversubscription이 발생할 수 있음
   - 해결방안: workload별 대역폭 모델로 포트 배치를 최적화하고 upstream utilization과 oversubscription ratio로 검증함
2. 문제: switch hop과 버퍼링 지연이 쌓이면 지연 민감 I/O와 P2P 전송 성능이 눈에 띄게 저하될 수 있음
   - 해결방안: latency 민감 장치는 직접 연결하거나 hop 수를 최소화하고 p99 I/O latency와 P2P throughput으로 검증함
3. 문제: ACS와 IOMMU 설정이 부정확하면 endpoint 간 DMA 격리가 깨져 보안 위험이 커질 수 있음
   - 해결방안: ACS와 IOMMU group 검증 절차를 운영하고 isolation test result와 unauthorized DMA block rate로 검증함

## Ⅶ. 적용 사례

- GPU 확장 서버에서는 switch 하위에 가속기와 NVMe를 배치하고, upstream utilization과 job throughput으로 결과를 확인함
- AI 스토리지 노드에서는 P2P 경로를 설계해 GPU와 NVMe 간 이동을 최적화하고, P2P throughput과 p99 latency로 결과를 확인함
- 멀티테넌트 장비에서는 ACS와 IOMMU를 함께 검증해 DMA 격리를 보장하고, isolation test pass rate와 security incident count로 결과를 확인함

## Ⅷ. 결론

PCIe 스위칭은 포트 확장 장치가 아니라 공유 상위 링크와 격리 정책을 함께 설계해야 하는 패브릭이므로, 확장성보다 병목과 DMA 경계를 먼저 판단해야 함.
