---
title: "NVLink 고대역폭 인터커넥트 (NVLink)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 132
extra:
  question_no: "132"
  exam_status: "기출"
  exam_history: "138회"
---

## 미리 알고가기

- Scale-up은 한 서버·컴퓨팅 도메인 안에서 GPU 수와 메모리 접근 대역폭을 확장하는 방식임
- Scale-out은 서버·랙을 네트워크로 연결해 계산 노드 수를 확장하는 방식임
- NVSwitch는 여러 GPU의 NVLink를 스위칭해 GPU 간 다중 경로를 제공함
- GPUDirect RDMA는 GPU 메모리와 네트워크 어댑터 사이의 직접 전송을 지원함

## Ⅰ. 개요

- **정의/개념**: NVLink는 GPU·CPU 등 가속기 사이에 메모리 접근과 데이터 전송 경로를 제공해 서버 내부 Scale-up 병렬 처리를 지원하는 인터커넥트임
- **배경/필요성**: 모델 파라미터와 활성값이 단일 GPU 메모리를 넘으면 GPU 간 데이터를 반복 교환하므로 CPU 중심 PCIe 경로의 대역폭과 토폴로지 제약을 보완할 연결이 필요함

## Ⅱ. 특징

- GPU 간 Peer-to-Peer 메모리 접근으로 CPU 메모리 경유 복사를 줄임
- 여러 NVLink를 묶어 GPU 쌍 사이의 전송 대역폭을 구성함
- NVSwitch가 다수 GPU 사이의 동시 통신과 경로 선택을 처리함
- 서버 내부 NVLink만으로 랙 간 통신을 처리할 수 없으므로 InfiniBand·RoCE와 역할을 분리함

## Ⅲ. 종류 및 비교

| 판단 기준 | PCIe | NVLink | InfiniBand·RoCE |
|:---|:---|:---|:---|
| 연결 범위 | CPU·장치 I/O | 서버·Scale-up 도메인의 GPU·CPU | 서버·랙 간 Scale-out 노드 |
| 경로 구조 | Root Complex와 PCIe 스위치 | GPU Peer Link와 NVSwitch | HCA·RNIC와 네트워크 스위치 |
| 메모리 접근 | 장치 DMA와 Peer-to-Peer | GPU 간 직접 메모리 접근 | GPUDirect RDMA로 원격 GPU 메모리 전송 |
| 주요 통신 | 장치 제어·범용 I/O | 텐서·활성값·그래디언트 교환 | 노드 간 집합 통신·스토리지 전송 |
| 적용 위치 | 범용 서버 내부 | 다중 GPU 서버·가속기 도메인 | 클러스터 패브릭 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 역할 |
|:---|:---|
| NVLink Port | GPU 사이의 직렬 링크와 데이터 전송을 담당함 |
| NVSwitch | 여러 GPU의 NVLink 경로를 스위칭함 |
| GPU 메모리 | Peer GPU가 읽고 쓰는 모델·활성값을 저장함 |
| NCCL | 토폴로지에 맞춰 All-Reduce 등 집합 통신을 실행함 |
| PCIe·NIC 연계 | 호스트 제어와 서버 외부 Scale-out 경로를 제공함 |

```text
GPU 0 --\
GPU 1 --- [NVSwitch Fabric] --- GPU 4·5·6·7
GPU 2 --/          |
               PCIe·NIC -> Scale-out Fabric
```

## Ⅴ. 원리 및 절차 흐름도

```text
토폴로지 탐색 -> Peer 경로 선택 -> GPU 메모리 전송 -> 집합 연산 -> 완료 동기화
```

1. **토폴로지 탐색**: 런타임이 GPU·NVLink·NVSwitch 연결과 링크 수를 확인함
2. **경로 선택**: NCCL이 링·트리 등 집합 통신 경로를 GPU 토폴로지에 맞춰 구성함
3. **메모리 전송**: GPU가 NVLink를 통해 Peer 메모리의 텐서 조각을 읽고 씀
4. **동기화**: 집합 연산의 모든 참여 GPU가 데이터 교환 완료를 확인한 뒤 계산을 계속함

> 요약: NVLink는 GPU 토폴로지에 맞춘 Peer 메모리 경로로 서버 내부 집합 통신을 수행함.

## Ⅵ. 실무 적용 및 유의점

1. 모델 병렬 학습은 GPU 배치와 NVLink 경로가 어긋나면 PCIe 우회가 발생하므로 GPU 쌍별 대역폭, NVLink 사용률, All-Reduce 시간을 확인해야 함
2. 서버 내부 Scale-up과 랙 간 Scale-out을 혼동하면 병목 위치를 잘못 판단하므로 NVLink와 InfiniBand·RoCE 구간을 분리 측정하고 GPU 대기 시간과 네트워크 통신 시간을 비교해야 함

## Ⅶ. 결론

NVLink는 GPU Peer 메모리와 NVSwitch를 이용한 Scale-up 인터커넥트이며, GPU 토폴로지와 서버 외부 Scale-out 경로를 함께 고려해야 함.
