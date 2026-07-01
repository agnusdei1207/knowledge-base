---
title: "GPU 클러스터 (GPU Cluster)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 234
---

# 📖 【암기용】 개념 완전 이해

> 목적: GPU 클러스터를 여러 GPU 서버를 고속 네트워크와 스케줄러로 묶어 AI 학습·추론을 병렬 처리하는 인프라로 이해하게 만든다.

## 한눈에
- **개요**: 다수 GPU 노드를 네트워크, 저장장치, 스케줄러로 연결한 병렬 AI 컴퓨팅 집합
- **왜 필요한가**: 단일 GPU 서버는 대형 모델 학습 메모리, 처리량, 장애 복구 요구를 충족하지 못한다.
- **핵심 직관**: 여러 작업자가 같은 설계도를 보고 일을 나누어 처리하되 무전망과 창고가 병목이 되면 전체 작업이 멈춘다.

## 깊이 이해
- **배경·문제의식**: LLM, 추천, 비전 모델은 데이터와 파라미터가 커서 여러 GPU의 HBM과 연산을 묶어야 한다.
- **작동 원리**: 노드 내부 GPU는 PCIe, NVLink, NVSwitch로 연결되고 노드 간은 InfiniBand 또는 RoCE로 gradient와 parameter를 교환한다.
- **비유**: 여러 주방이 같은 대형 주문을 나눠 만들지만 재료 창고와 주문 조율 시스템이 늦으면 모든 주방이 대기하는 구조다.
- **구체 예시**: 8-GPU 서버 32대를 묶은 클러스터는 256 GPU를 Slurm 또는 Kubernetes로 할당하고 NCCL all-reduce로 분산 학습을 수행한다.
- **흔한 오해·주의점**: GPU 클러스터는 GPU 장착 서버 목록이 아니다. 네트워크 토폴로지, 스토리지 대역폭, 이미지 관리, 자원 격리가 함께 필요하다.

## 연결 개념
- AI Supercomputing — GPU 클러스터를 포함하는 대규모 AI 인프라
- GPU — 클러스터의 기본 연산 장치
- Distributed Training — GPU 클러스터에서 실행되는 학습 방식

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: GPU 클러스터는 GPU 노드, 네트워크, 스토리지, 스케줄러, 관측성을 함께 설계해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: GPU Cluster는 다수 GPU 노드를 고속 네트워크와 스케줄러로 묶어 AI 학습·추론을 병렬 수행하는 인프라임.
> 2. **가치**: 단일 노드 한계를 넘어 모델 병렬화, 데이터 병렬화, 대규모 batch 처리를 가능하게 함.
> 3. **판단 포인트**: GPU utilization보다 낮은 network bandwidth, storage throughput, scheduler fragmentation이 실제 병목이 될 수 있음.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 클러스터 아키텍처 이해 확인 | GPU node, interconnect, storage, scheduler | GPU 사양만 나열 |
| 분산 학습 병목 판단 확인 | NCCL, all-reduce, topology | 네트워크 병목 누락 |
| 운영 통제 확인 | quota, isolation, monitoring, image 관리 | 사용자·작업 격리 누락 |

> 요약: 이 문제는 GPU를 여러 대 모으는 것이 아니라 병목 없는 클러스터 운영 구조를 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 다중 GPU 노드 병렬 컴퓨팅 인프라
- 배경: 대형 AI 모델은 단일 GPU 서버의 HBM, 연산량, 장애 허용 범위를 초과함.
- 필요성: GPU utilization 60% 이상, job queue time 30분 이하, node failure 복구 30분 이하 기준으로 운영해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
User Job -> Scheduler -> GPU Node Pool -> NVLink/NVSwitch -> InfiniBand/RoCE -> Shared Storage -> Monitoring
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| GPU Node | GPU, CPU, HBM, local NVMe 제공 | 4~8 GPU 서버 구성 빈번 |
| Interconnect | 노드 내·노드 간 통신 | NVLink, NVSwitch, InfiniBand, RoCE |
| Scheduler | job queue와 자원 할당 | Slurm, Kubernetes, Volcano |
| Shared Storage | 데이터셋과 checkpoint 제공 | 병렬 파일시스템 또는 object storage |

> 요약: GPU 클러스터는 연산 노드와 통신·저장·스케줄링 계층이 함께 동작해야 병렬 학습이 가능하다.

---

## Ⅲ. 동작원리 및 흐름도

```text
컨테이너 이미지 준비 -> job 제출 -> GPU 자원 할당 -> 분산 학습 실행 -> checkpoint 저장 -> metric 수집
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 사용자가 학습 job과 자원 요구량 제출 | GPU count, memory |
| 2 | scheduler가 노드와 GPU를 할당 | fragmentation rate |
| 3 | NCCL 기반 분산 학습 통신 수행 | all-reduce time |
| 4 | checkpoint 저장과 metric 수집 | checkpoint 성공률 |

> 요약: GPU 클러스터는 job 제출부터 자원 할당, 분산 통신, checkpoint까지 하나의 운영 흐름으로 관리된다.

---

## Ⅳ. 특징

| 구분 | 단일 GPU 서버 | GPU Cluster | 수치 기준 |
|:---|:---|:---|:---|
| 확장 범위 | 서버 내 GPU 수 제한 | 노드 수만큼 수평 확장 | 10~1000 GPU |
| 병목 | HBM·PCIe | 네트워크·스토리지·스케줄러 | all-reduce 시간 |
| 운영 | 단일 사용자 중심 | 멀티테넌트 자원 관리 | quota, isolation |

> 요약: GPU 클러스터는 수평 확장을 제공하지만 네트워크와 스케줄러 운영 복잡도가 증가한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 단일 노드 | 다중 노드 GPU 풀 | 모델이 단일 HBM을 초과할 때 |
| 비용/성능 | 초기 비용 낮음 | 네트워크·전력 비용 추가 | utilization 60% 이상 목표 |
| 운영/위험 | 관리 단순 | quota·격리·장애 복구 필요 | 멀티테넌트 여부 |

> 요약: GPU 클러스터는 대규모 학습 필요성과 운영 역량이 모두 있을 때 도입한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 낮은 활용률 | 작은 job과 큰 GPU 단편화 | MIG, gang scheduling, quota | GPU utilization |
| 통신 병목 | 노드 간 all-reduce 증가 | topology-aware placement, NCCL tuning | network throughput |
| 장애 전파 | 긴 학습 job 중 노드 장애 | checkpoint, retry, node health check | MTTR |

> 요약: GPU 클러스터 리스크는 활용률, 통신, 장애 복구이며 스케줄링과 checkpoint로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 자원 활용 | GPU utilization 60% 이상 | DCGM exporter |
| 대기 시간 | job queue time 30분 이하 | scheduler log |
| 통신 | all-reduce 시간이 step time의 20% 이하 | NCCL trace |

> 요약: GPU 클러스터 운영 품질은 활용률, 대기 시간, 통신 비중으로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 8-GPU 노드 단위로 랙과 네트워크 토폴로지를 설계하고 topology-aware scheduling을 적용함.
2. 연구용 소형 job은 MIG 또는 queue 분리로 처리하고 대형 학습 job은 gang scheduling으로 GPU를 동시 할당함.
3. DCGM, Prometheus, scheduler log를 연계해 GPU utilization, ECC error, job failure를 관측함.

**결론 (2줄):**
- 기술사 판단: GPU 클러스터는 모델 규모가 단일 서버를 초과하고 지속적인 학습 수요가 있을 때 TCO와 운영 역량을 기준으로 도입함.
- 향후 방향: GPU 클러스터는 AI 슈퍼컴퓨팅과 추론 팜으로 분화하며 액체 냉각과 에너지 인지 스케줄링을 포함함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "GPU 클러스터를 설명하시오" | job 실행과 분산 통신 흐름 | 단일 서버와 차이 |
| 요구사항 명시형 | "GPU 클러스터 운영 방안을 제시하시오" | 스케줄링·checkpoint 절차 | 활용률·통신·장애 리스크 |

> 요약: 설명형은 구조를, 운영형은 자원 활용과 장애 복구 지표를 중심으로 작성한다.
