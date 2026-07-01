---
title: "Chiplet 칩렛 (Chiplet)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 246
---

# 📖 【암기용】 개념 완전 이해

> 목적: 칩렛을 대형 단일 다이의 수율·비용 문제를 분할 제조와 패키징으로 푸는 방식으로 이해하게 만든다.

## 한눈에
- **개요**: CPU, GPU, I/O, cache 같은 기능 블록을 작은 die로 나눠 제조한 뒤 하나의 package 안에서 연결하는 설계 방식
- **왜 필요한가**: 선단 공정에서 큰 단일 die는 결함 하나로 전체 폐기될 확률이 높고, 모든 블록을 동일 공정으로 만드는 비용 부담이 크다.
- **핵심 직관**: 큰 유리판 하나를 만들다 흠집 하나로 버리는 대신, 작은 유리판 여러 장을 선별해 조립하는 방식이다.

## 깊이 이해
- **배경·문제의식**: die 면적이 커질수록 defect 포함 확률이 증가해 monolithic die 수율이 낮아지고 칩당 원가가 상승한다.
- **작동 원리**: 기능 블록별 chiplet을 다른 공정 노드로 제작하고 Known-Good-Die를 선별한 뒤 interposer, EMIB, Foveros, CoWoS 같은 패키징으로 결합한다.
- **비유**: 모든 방을 한 번에 시공하는 건물 대신, 검증된 모듈 방을 만든 뒤 현장에서 조립하는 모듈러 건축과 같다.
- **구체 예시**: CPU core die는 선단 공정, I/O die는 성숙 공정을 쓰는 조합으로 수율과 비용을 동시에 관리할 수 있다.
- **흔한 오해·주의점**: 칩렛의 본질은 무조건 더 높은 성능이 아니라 수율, 비용, 공정 혼합, 재사용성이다. die-to-die link 지연과 전력은 별도 설계 과제다.

## 연결 개념
- UCIe — 멀티벤더 칩렛 연결 표준
- 2.5D/3D Packaging — 칩렛을 물리적으로 조립하는 기술
- HBM — 칩렛 패키지와 함께 배치되는 대표 메모리

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: 칩렛은 수율·공정 혼합 이점과 die-to-die 지연·패키징 리스크를 함께 써야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Chiplet은 대형 기능을 여러 작은 die로 분할 제조하고 package 내부에서 연결하는 반도체 설계 방식임.
> 2. **가치**: 작은 die의 수율 이점, 공정 노드 혼합, IP 재사용으로 대형 SoC 비용을 낮춤.
> 3. **판단 포인트**: die-to-die latency, package yield, thermal density를 monolithic die와 비교해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 수율 경제성 이해 확인 | die area, defect density, KGD | 단순 성능 향상 기술로 서술 |
| 패키징 구조 확인 | interposer, 2.5D/3D, die-to-die link | 여러 칩을 붙인다는 수준으로 설명 |
| 트레이드오프 판단 확인 | 지연, 전력, 열, 검증 복잡도 | 칩렛이 항상 monolithic보다 우위라고 단정 |

> 요약: 칩렛 문제는 수율·비용 이점과 패키지 내부 연결 오버헤드를 균형 있게 묻는다.

---

## Ⅰ. 개요 및 필요성

- 개요: 다중 die 패키지 설계
- 배경: 선단 공정 대형 die는 결함 확률 증가로 수율과 원가 문제가 커짐.
- 필요성: 기능 블록별 공정 최적화와 Known-Good-Die 선별로 대형 AI·HPC 칩의 제조 리스크를 낮춰야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Function Partitioning -> CPU Chiplet / GPU Chiplet / I-O Die / Cache Die
-> Known-Good-Die Test -> Interposer / 3D Package -> Die-to-Die Link -> Single Package
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Compute Chiplet | CPU/GPU/NPU 연산 블록 | 선단 공정 적용 |
| I/O Die | PCIe, CXL, memory controller 제공 | 성숙 공정으로 비용 절감 |
| Interposer/Bridge | die 간 배선 제공 | CoWoS, EMIB 등 |
| Die-to-Die Link | chiplet 간 데이터 전송 | UCIe 또는 독자 규격 |

> 요약: 칩렛은 기능 분할, KGD 선별, 고급 패키징, die-to-die link가 결합된 구조다.

---

## Ⅲ. 동작원리 및 흐름도

```text
기능 분할 -> 공정 노드 선정 -> 개별 die 제조 -> KGD 선별
-> package assembly -> die-to-die link training -> system boot -> 단일 칩처럼 동작
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 기능 블록을 chiplet 단위로 분할 | partition dependency |
| 2 | 블록별 공정 노드와 die 크기 결정 | yield model |
| 3 | KGD를 선별해 package 조립 | die test pass rate |
| 4 | die-to-die link 초기화 후 운영 | link error rate |

> 요약: 칩렛은 개별 die를 먼저 검증하고 패키지에서 연결해 단일 시스템으로 동작시킨다.

---

## Ⅳ. 특징

| 구분 | Monolithic Die | Chiplet | 수치·판단 기준 |
|:---|:---|:---|:---|
| 수율 | die 면적 증가 시 수율 하락 | 작은 die 선별 조립 | KGD pass rate |
| 공정 혼합 | 단일 공정 중심 | 블록별 공정 노드 선택 | I/O는 성숙 공정 활용 |
| 지연 | on-die wire | die-to-die link 추가 | latency budget |
| 검증 | 단일 die 검증 | die+package+link 검증 | package yield |

> 요약: 칩렛은 수율과 공정 혼합에서 이점을 얻지만 지연·검증·열 설계가 추가된다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | monolithic SoC | multi-die package | die size와 수율 |
| 비용/성능 | 설계 단순, 대형 die 비용 증가 | packaging 비용 추가, die 비용 절감 | yield model 기반 TCO |
| 운영/위험 | 검증 범위 단순 | link·thermal·package 검증 필요 | 검증 역량 |

> 요약: 대형 고성능 칩은 칩렛으로 제조 리스크를 낮추고, 작은 지연 민감 칩은 monolithic을 유지한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| link 병목 | die 간 traffic 예측 실패 | traffic simulation, UCIe lane sizing | link utilization |
| thermal hotspot | 3D 적층·고밀도 배치 | thermal floorplan, liquid cooling | junction temperature |
| package yield 저하 | assembly alignment와 bump defect | KGD, package-level test | final package yield |

> 요약: 칩렛 리스크는 link, thermal, package yield이며 설계 초기 floorplan과 test 전략이 필요하다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 수율 | monolithic 대비 원가 개선 | yield model, wafer test |
| link | latency·bandwidth 목표 충족 | die-to-die benchmark |
| 열 | junction temperature 기준 이내 | thermal simulation, sensor |

> 요약: 칩렛 성과는 원가, die-to-die 성능, 열 한계를 동시에 측정해야 한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. AI/HPC 대형 die는 compute, I/O, cache를 chiplet으로 분할해 die 크기와 수율을 관리함.
2. I/O와 analog block은 성숙 공정, compute block은 선단 공정으로 배치해 공정 비용을 분리함.
3. UCIe 또는 독자 link를 선택하기 전 traffic pattern과 latency budget을 package simulation으로 검증함.

**결론 (2줄):**
- 기술사 판단: die가 크고 공정 혼합 이점이 크면 칩렛, 지연과 설계 단순성이 우선이면 monolithic을 선택함.
- 향후 방향: 칩렛은 UCIe와 3D packaging 확산으로 멀티벤더 이종 통합 플랫폼으로 발전함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "칩렛을 설명하시오" | 기능 분할과 package 조립 흐름 | monolithic 대비 수율·지연 차이 |
| 요구사항 명시형 | "차세대 반도체 설계 방안을 제시하시오" | partition·KGD·link 검증 절차 | 공정 혼합과 thermal 리스크 |

> 요약: 설명형은 칩렛 구조를, 설계형은 수율 모델과 패키지 검증을 중심으로 작성한다.
