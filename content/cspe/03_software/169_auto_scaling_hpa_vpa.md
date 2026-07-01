---
title: "오토 스케일링 HPA·VPA (Auto Scaling HPA VPA)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 169
---

# 📖 【암기용】 개념 완전 이해

> 목적: 오토 스케일링 HPA·VPA를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 부하 변화에 맞춰 컨테이너 개수나 자원 크기를 자동 조정하는 기술
- **왜 필요한가**: 트래픽은 시간대와 이벤트에 따라 변한다. 고정 용량은 피크 때 장애를 만들고, 평시에는 비용 낭비를 만든다.
- **핵심 직관**: HPA는 계산대를 더 여는 방식, VPA는 계산대 직원에게 더 큰 작업 공간과 도구를 주는 방식이다.

## 깊이 이해
- **배경·문제의식**: 클라우드 네이티브 서비스는 요청 수가 분 단위로 바뀐다. 사람이 수동으로 Pod 수와 CPU·메모리를 조정하면 반응이 늦고 설정 오류가 생긴다.
- **작동 원리**: HPA는 CPU, 메모리, QPS 같은 지표를 보고 Pod replica 수를 늘리거나 줄인다. VPA는 Pod의 CPU·메모리 request/limit을 조정한다. Kubernetes에서는 metrics-server, custom metrics, autoscaler controller가 지표를 읽어 desired state를 반영한다.
- **비유**: 고객 줄이 길면 창구를 더 여는 것이 HPA이고, 한 창구가 너무 복잡한 업무를 처리하면 더 넓은 책상과 장비를 주는 것이 VPA다.
- **구체 예시**: CPU 70% 초과 시 HPA min2/max20 범위에서 Pod를 늘리고, 메모리 부족이 반복되는 배치 Pod는 VPA가 request 512Mi에서 1Gi로 조정한다.
- **흔한 오해·주의점**: HPA와 VPA를 같은 자원 지표로 동시에 쓰면 충돌할 수 있다. HPA는 replica, VPA는 request 조정이라는 역할을 분리해야 한다.

## 연결 개념
- Docker 컨테이너 - 스케일링 대상 실행 단위
- Kubernetes - HPA·VPA가 동작하는 대표 오케스트레이션 환경
- FinOps - 필요 용량만 배정해 비용을 관리하는 운영 체계

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 오토 스케일링 답안은 "자동 확장" 설명이 아니라 지표, 임계값, replica/request 조정, 안정화 윈도우, 비용 지표를 함께 제시한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 오토 스케일링은 관측 지표를 기준으로 Pod 수(HPA) 또는 자원 요청량(VPA)을 자동 조정하는 제어 루프이다.
> 2. **가치**: 피크 트래픽에는 replica를 늘리고, 평시에는 자원을 줄여 SLO와 비용을 함께 관리한다.
> 3. **판단 포인트**: CPU·메모리·QPS·queue length 지표, min/max 범위, cooldown, VPA 재시작 영향이 설계 기준이다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| HPA·VPA 차이 확인 | HPA는 replica, VPA는 request/limit 조정 | 둘 다 "서버 증가"로만 설명 |
| 운영 설계 역량 확인 | metrics-server, custom metrics, 임계값, min/max | 지표와 안정화 조건 누락 |
| 장애·비용 판단 확인 | thrashing, cold start, 과소 request, 비용 증가 | 무조건 자동화가 해결책으로 단정 |

> 요약: 이 문제는 스케일링 대상, 지표, 제어 범위, 부작용 통제까지 묻는다.

---

## Ⅰ. 개요 및 필요성

오토 스케일링은 부하 지표에 따라 자원 규모를 자동 조정하는 기술이다. 클라우드 네이티브 서비스는 트래픽 변동이 크므로 고정 용량은 장애와 비용 낭비를 만든다. HPA와 VPA를 적절히 조합하면 SLO와 비용 지표를 함께 관리할 수 있다.

---

## Ⅱ. 구조 및 구성요소

```text
Metric Source -> Autoscaler Controller -> HPA Replica 조정
                                      -> VPA Request/Limit 조정
                                      -> Scheduler/Cluster Autoscaler
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Metric Source | CPU, 메모리, QPS, queue length 제공 | metrics-server, Prometheus |
| HPA | Pod replica 수 조정 | min2/max20, target CPU 70% |
| VPA | CPU·메모리 request/limit 추천·적용 | 재시작 영향 검토 |
| Cluster Autoscaler | 노드 수 조정 | Pod 배치 불가 시 노드 추가 |

> 요약: 오토 스케일링은 지표 수집, replica 조정, 자원 요청량 조정, 노드 확장으로 구성된다.

---

## Ⅲ. 동작원리 및 흐름도

```text
지표 수집 -> 목표값 비교 -> desired replica/request 계산
-> HPA/VPA 적용 -> 스케줄링 -> SLO/비용 재측정
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 지표 수집 | 15초~60초 주기, 결측률 1% 이하 |
| 2 | 목표값 비교 | CPU 70%, queue length 100 등 |
| 3 | 조정 실행 | HPA min/max, VPA update mode |
| 4 | 안정화 확인 | p95 지연, 오류율, 비용 변화 |

> 요약: 오토 스케일링은 지표 기반 제어 루프이며 조정 후 SLO와 비용을 재측정해야 한다.

---

## Ⅳ. 특징

| 구분 | 수동 스케일링 | HPA·VPA 오토 스케일링 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 반응 | 운영자 변경 | 지표 기반 자동 조정 | HPA 30~60초 주기 |
| 대상 | VM·Pod 수동 조정 | replica와 request/limit 분리 | HPA min2/max20 |
| 비용 | 피크 기준 상시 용량 | 평시 replica 축소 | CPU 사용률 50~70% 목표 |
| 위험 | 대응 지연 | thrashing, cold start | stabilization window 설정 |

> 요약: HPA는 수평 용량, VPA는 수직 자원 배정을 조정하며 안정화 윈도우로 반복 진동을 통제한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | HPA | VPA | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | replica 수 증가·감소 | CPU·메모리 request 조정 | 무상태 서비스 vs 자원 크기 불일치 |
| 비용/성능 | 처리량 증가, 노드 비용 증가 | 과소/과대 request 보정 | p95 지연과 OOMKilled 빈도 |
| 운영/위험 | cold start, thrashing | Pod 재시작, HPA와 충돌 | update mode와 지표 분리 |

> 요약: HPA는 트래픽 변동, VPA는 자원 요청량 보정에 적합하며 같은 지표 동시 제어는 피한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 반복 진동 | 임계값 과민, 짧은 주기 | stabilization window, cooldown | scale event 분당 1회 이하 |
| cold start | 이미지 크기, 초기화 지연 | pre-warming, 이미지 500MB 이하 | startup time 30초 이하 |
| 비용 증가 | max replica 과대 설정 | budget alert, max bound, queue metric | 월 비용 편차 10% 이하 |

> 요약: 스케일링 리스크는 진동, 시작 지연, 비용 증가이며 지표·범위·예산으로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 서비스 SLO | p95 지연 100ms 이하, 오류율 1% 이하 | APM, SLI 대시보드 |
| 스케일링 | HPA 반응 60초 이내, OOMKilled 0건 | Kubernetes event, Prometheus |
| 비용 | CPU 평균 50~70%, 월 예산 편차 10% 이하 | Billing, resource metrics |

> 요약: 오토 스케일링은 SLO, 스케일 이벤트, 비용 지표가 함께 충족될 때 유효하다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. HPA 설계: 무상태 API에 CPU 70% 또는 QPS 기준 HPA min2/max20, stabilization window 300초 적용
2. VPA 적용: 배치·백오피스 Pod에 VPA recommendation을 먼저 적용하고 OOMKilled 0건 확인 후 Auto 모드 검토
3. 비용·SLO 연계: p95 지연 100ms 이하, CPU 50~70%, 월 예산 편차 10% 이하를 스케일링 승인 기준으로 사용

**결론 (2줄):**
- 기술사 판단: 트래픽 변동은 HPA, 자원 요청량 오차는 VPA, 노드 부족은 Cluster Autoscaler로 역할을 분리함
- 향후 방향: 오토 스케일링은 KEDA, 이벤트 기반 스케일링, 예측 스케일링과 결합해 큐·일정·AI 예측 지표로 확장됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "오토 스케일링을 설명하시오" | 지표 수집과 제어 루프 | HPA·VPA 차이 |
| 요구사항 명시형 | "운영 방안을 제시하시오", "설계하시오" | 임계값, min/max, 안정화 윈도우 설계 | SLO·비용·리스크 기준 |

> 요약: 설명형은 원리, 운영형은 지표와 제어 범위 중심으로 목차를 전환한다.
