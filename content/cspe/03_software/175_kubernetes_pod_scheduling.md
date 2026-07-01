---
title: "쿠버네티스 Pod 스케줄링 (Kubernetes Pod Scheduling)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 175
---

# 📖 【암기용】 개념 완전 이해

> 목적: Kubernetes Pod 스케줄링을 처음 보는 사람도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: Pod를 어떤 Node에 배치할지 자원, 정책, 제약, 선호도를 기준으로 결정하는 과정
- **왜 필요한가**: 모든 Pod를 빈 노드에만 놓으면 CPU 경합, 장애 도메인 집중, GPU 미사용, 규제 위반이 발생한다.
- **핵심 직관**: 스케줄러는 단순 자리 배정자가 아니라 요구 조건을 만족하는 좌석을 고르는 배치 심사관이다.

## 깊이 이해
- **배경·문제의식**: Kubernetes 클러스터에는 CPU, Memory, GPU, Zone, 보안 등급, 비용이 다른 노드가 섞인다. Pod마다 request, affinity, taint toleration 요구가 달라서 자동 배치 기준이 필요하다.
- **작동 원리**: Scheduler는 Pending Pod를 감지하고 Filter 단계에서 배치 불가능 노드를 제거한다. Score 단계에서 적합한 노드에 점수를 매긴 뒤 Bind 단계에서 Pod를 Node에 할당한다.
- **비유**: 호텔 예약에서 금연실, 침대 수, 전망, 가격 조건을 먼저 거르고 남은 객실 중 점수가 높은 방을 배정하는 방식이다.
- **구체 예시**: GPU request `nvidia.com/gpu: 1`이 있는 Pod는 GPU 노드만 통과하고, zone anti-affinity가 있으면 동일 장애 도메인에 replica가 몰리지 않게 배치한다.
- **흔한 오해·주의점**: limit만 설정하면 스케줄링 기준이 되지 않는다. Scheduler는 주로 request와 정책을 기준으로 배치 가능성을 계산한다.

## 연결 개념
- Resource Request/Limit - 배치 기준과 실행 제한의 차이
- Affinity/Anti-Affinity - 노드 또는 Pod 간 배치 선호와 제약
- Taint/Toleration - 특정 노드에 허용된 Pod만 배치하는 통제

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 스케줄링 답안은 Filter, Score, Bind 흐름과 request/affinity/taint 정책을 장애 도메인·비용·자원 활용 관점으로 연결해야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Pod 스케줄링은 Pending Pod를 자원과 정책 조건에 맞는 Node에 binding하는 의사결정 과정임.
> 2. **가치**: CPU/Memory/GPU request, affinity, taint로 자원 경합과 장애 집중을 통제함.
> 3. **판단 포인트**: 배치 실패는 용량 부족뿐 아니라 정책 충돌, taint 미허용, PVC zone 제약으로 분석해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 스케줄러 원리 이해 확인 | Filter, Score, Bind | 라운드로빈 배치로 설명 |
| 배치 정책 설계 확인 | request, affinity, taint, topology spread | limit와 request 혼동 |
| 장애 분석 역량 확인 | Pending 원인, event, resource pressure | CPU 부족만 원인으로 단정 |

> 요약: 스케줄링 문제는 배치 알고리즘과 정책 충돌 분석을 함께 써야 함.

---

## Ⅰ. 개요 및 필요성

- 개요: Pod 스케줄링은 Pod를 Node에 배치하는 과정임.
- 배경: 클러스터에는 자원, Zone, 보안 등급, 비용이 다른 노드가 존재한다.
- 필요성: request, affinity, taint, topology spread 기준으로 Pending, 자원 경합, 장애 도메인 집중을 통제한다.

---

## Ⅱ. 구조 및 구성요소

```text
Pending Pod -> Scheduler Queue -> Filter -> Score -> Bind -> kubelet 실행
  / Filter: resource, taint, volume
  / Score: spread, affinity, utilization
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Scheduling Queue | 배치 대기 Pod 관리 | priority 반영 |
| Filter Plugin | 배치 불가 노드 제거 | NodeResourcesFit, TaintToleration |
| Score Plugin | 후보 노드 점수화 | topology spread |
| Bind | 선택 노드에 Pod 할당 | API Server binding |

> 요약: Scheduler는 대기 Pod를 필터링, 점수화, 바인딩 단계로 처리함.

---

## Ⅲ. 동작원리 및 흐름도

```text
Pod 생성 -> request/정책 확인 -> 노드 필터링 -> 노드 점수화 -> 바인딩 -> kubelet 실행
  / 후보 없음 -> Pending
  / preemption 가능 -> 낮은 priority Pod 축출
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | Pending Pod 감지 | scheduling queue 입력 |
| 2 | request, nodeSelector, affinity, taint 확인 | 후보 노드 수 |
| 3 | Filter로 부적합 노드 제외 | Unschedulable event |
| 4 | Score로 최종 노드 선정 | plugin score |
| 5 | Bind 후 kubelet 실행 | assigned node, Ready |

> 요약: 스케줄러는 배치 불가 노드를 제거한 뒤 정책 점수를 반영해 최종 노드를 결정함.

---

## Ⅳ. 특징

| 구분 | 기본 배치 | 정책 기반 스케줄링 | 수치/판단 포인트 |
|:---|:---|:---|:---|
| 자원 | request 기준 | CPU/Memory/GPU request | Pending 0건 |
| 장애 분산 | 노드 여유 기준 | topology spread, anti-affinity | Zone별 replica 분산 |
| 전용 노드 | 구분 약함 | taint/toleration | GPU/보안 노드 |
| 우선순위 | 동일 처리 | priority, preemption | P1 workload 보호 |

> 요약: Kubernetes 스케줄링은 자원 충족, 장애 분산, 전용 노드, 우선순위를 함께 판단함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 수동 서버 지정 | Scheduler plugin 기반 배치 | 노드 10대 이상 |
| 비용/처리 | 과잉 증설 | request 기반 bin packing | CPU 사용률 40~70% |
| 운영/위험 | 장애 도메인 집중 | topology spread | Zone 장애 영향 |

> 요약: 대규모 클러스터는 request와 topology 정책을 함께 적용해야 비용과 장애 영향을 통제함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Pending 증가 | request 과다, taint 미허용 | event 분석, request 조정 | unschedulable Pod 수 |
| 노드 경합 | request 미설정 | LimitRange, VPA 권고 | CPU throttling |
| 장애 집중 | anti-affinity 부재 | topologySpreadConstraints | Zone별 replica 편차 |

> 요약: 스케줄링 리스크는 Pending, 자원 경합, 장애 집중 지표로 조기 식별함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 배치 지연 | scheduling latency p95 5초 이하 | scheduler metric |
| 자원 모델 | request 설정률 100% | policy report |
| 장애 분산 | Zone별 replica 편차 1 이하 | kube-state-metrics |

> 요약: 스케줄링 품질은 지연, request 설정률, topology 분산으로 검증함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 자원 기준화: 모든 Pod에 CPU/Memory request를 설정하고 LimitRange로 request 누락 0건 유지
2. 배치 정책화: P1 서비스는 topologySpreadConstraints와 podAntiAffinity로 Zone별 replica 편차 1 이하 적용
3. 전용 노드 운영: GPU, 보안, 배치 노드는 taint/toleration과 nodeSelector로 workload를 분리

**결론 (2줄):**
- 기술사 판단: Scheduler는 빈 노드 선택기가 아니라 자원, 정책, 장애 도메인을 동시에 평가하는 제어 구성요소임
- 향후 방향: Scheduler Framework, VPA, Cluster Autoscaler가 결합되어 정책 기반 용량 관리로 발전함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Pod 스케줄링을 설명하시오" | Filter, Score, Bind 흐름 | request, affinity, taint 비교 |
| 요구사항 명시형 | "배치 정책을 설계하시오", "Pending 원인을 설명하시오" | 정책 충돌과 event 분석 | topology, priority, 전용 노드 기준 |

> 요약: 설명형은 알고리즘 흐름, 설계형은 정책 조합과 장애 분석 중심으로 전환함.
