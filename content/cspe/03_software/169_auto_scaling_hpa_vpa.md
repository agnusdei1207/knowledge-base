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
- **개요**: **쿠버네티스 오토스케일링(Autoscaling)** 중 파드 개수를 늘리고 줄이는 **수평적 확장**(HPA)과 파드 하나의 자원 할당량을 조정하는 **수직적 확장**(VPA)을 가리킨다.
- **왜 필요한가**: 트래픽은 시간대·이벤트에 따라 분 단위로 바뀐다. 사람이 수동으로 Pod 수나 CPU·메모리 설정을 바꾸면 반응이 늦어 피크 때는 장애, 평시에는 비용 낭비가 생긴다.
- **핵심 직관**: HPA는 계산대(파드)를 더 여는 방식이고, VPA는 계산대 한 곳에 더 넓은 작업 공간(CPU·메모리)을 주는 방식이다 — 사람 수를 늘리느냐, 한 사람 책상을 키우느냐의 차이다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| 오토스케일링 | 관측 지표에 따라 자원을 자동 조정하는 기술 전체 — HPA·VPA·Cluster Autoscaler의 상위 개념 | 자동 온도 조절기 |
| 수평적 확장(Horizontal Scaling) | 실행 단위 개수를 늘려 처리량을 키움 — HPA가 담당 | 계산대 창구 수 늘리기 |
| 수직적 확장(Vertical Scaling) | 실행 단위 하나의 자원 크기를 키움 — VPA가 담당 | 창구 직원 책상·장비 키우기 |
| HPA(Horizontal Pod Autoscaler) | CPU·메모리·QPS 지표를 보고 Pod replica 수를 조정하는 컨트롤러 | 손님 줄 길이 보고 창구 수 결정 |
| VPA(Vertical Pod Autoscaler) | Pod의 CPU·메모리 request/limit을 추천·적용하는 컨트롤러 | 업무량 보고 책상 크기 재배정 |
| Cluster Autoscaler | Pod를 배치할 노드 자체가 부족하면 노드를 추가·제거 | 매장이 꽉 차면 지점을 늘림 |
| metrics-server / Custom Metrics | CPU·메모리 등 표준 지표(metrics-server), QPS·큐 길이 등 애플리케이션 지표(Custom Metrics)를 제공 | 매장 CCTV(표준) vs POS 판매 데이터(커스텀) |
| request/limit | Pod가 요청하는 최소 자원(request)과 넘지 못하는 상한(limit) | 예약 좌석 수(request)와 정원(limit) |
| 안정화 윈도우(Stabilization Window) | 지표가 잠깐 튀어도 즉시 반응하지 않게 판단을 지연시키는 구간 | 신호가 잠깐 바뀌어도 몇 초 더 지켜보는 것 |

## 깊이 이해

### 왜 필요한가 (배경·문제의식)
- 클라우드 네이티브 서비스는 요청 수가 분 단위, 심지어 초 단위로 바뀐다. 고정된 Pod 개수나 고정된 CPU·메모리 할당으로는 피크 트래픽에서 요청이 밀리고, 평시에는 쓰지도 않는 자원에 비용을 낸다.
- 사람이 매번 `kubectl scale`이나 자원 설정을 수동으로 바꾸는 것은 반응 속도가 느리고 설정 실수가 생기기 쉽다. 그래서 지표를 자동으로 관찰하고 조정하는 제어 루프(control loop)가 필요했다.

### HPA 작동 원리 — 수치로 이해
- HPA는 기본 15초 주기(`--horizontal-pod-autoscaler-sync-period`)로 지표를 확인하고, 다음 공식으로 목표 replica 수를 계산한다.
  - `desiredReplicas = ceil( currentReplicas × ( currentMetricValue ÷ desiredMetricValue ) )`
- **워크드 예제**: 현재 Pod 4개, 평균 CPU 사용률 80%, 목표(target) CPU 50%라면 `ceil(4 × 80/50) = ceil(6.4) = 7`개로 늘어난다. 반대로 현재 10개, 평균 사용률 20%, 목표 50%라면 `ceil(10 × 20/50) = 4`개로 줄어든다.
- 아주 작은 변동에도 계속 재조정하지 않도록 기본 허용 오차(tolerance) 10%를 두어, 목표값 ±10% 이내면 조정하지 않는다. 축소는 진동을 막기 위해 기본 5분(300초)의 안정화 윈도우를 두지만, 확장은 장애를 막는 게 우선이라 기본적으로 즉시 반영한다.

### VPA 작동 원리 — 수치로 이해
- VPA는 세 구성요소로 동작한다. **Recommender**가 과거 사용량 이력을 분석해 적정 request 값을 추천(보통 사용량의 상위 백분위수 기준)하고, **Updater**가 현재 request가 추천값과 크게 벌어진 Pod를 찾아 제거하며, **Admission Controller**가 Pod 재생성 시점에 새 request 값을 주입한다.
- **워크드 예제**: 배치 Pod의 request가 512Mi로 설정돼 있는데 실제 사용량이 지속적으로 900Mi~1Gi에 걸쳐 있어 OOMKilled가 반복된다면, Recommender가 1Gi를 추천하고 Update Mode가 `Auto`(또는 `Recreate`)이면 Updater가 Pod를 재시작해 새 request 1Gi를 적용한다.
- 중요한 제약: VPA는 기본적으로 실행 중인 Pod의 자원 값을 그 자리에서 바꾸지 못한다. 반드시 Pod를 재시작(퇴출→재생성)해야 새 값이 적용되므로, 상태 저장 서비스에 `Auto` 모드를 쓰면 예기치 않은 재시작이 발생할 수 있다. Update Mode `Off`는 추천값만 보여주고 적용은 하지 않는다.

### 언제 무엇을 쓰나 — 판별 원리
- 트래픽 자체가 늘고 주는 무상태 서비스(웹 API)는 **HPA**로 요청량에 맞춰 창구(Pod) 수를 조정한다. 트래픽 총량은 일정한데 Pod 하나가 필요로 하는 자원 크기를 잘못 잡은 경우(요청량은 그대로인데 메모리가 늘 부족)는 **VPA**로 request/limit 자체를 보정한다.
- HPA와 VPA를 **같은 지표(예: CPU)**로 동시에 자동 조정하면 서로 다른 신호(복제본 증가 vs 요청량 증가)가 겹쳐 반복 진동(thrashing)을 일으킬 수 있다. 그래서 같은 자원 지표에는 둘 중 하나만 Auto로 쓰고, HPA가 커스텀 메트릭(QPS 등)을 쓰고 VPA가 CPU/메모리를 보정하는 조합처럼 **역할을 지표 단위로 분리**해야 한다.
- Pod를 아무리 늘려도 그 Pod들을 배치할 노드 자체가 없으면 스케줄링이 밀린다. 이때는 Cluster Autoscaler가 노드를 추가한다 — HPA/VPA는 Pod 레벨, Cluster Autoscaler는 노드 레벨 제어라는 계층 차이가 있다.

### 비유와 흔한 오해
- **비유**: 손님 줄이 길어지면 창구를 더 여는 것이 HPA, 한 창구가 감당 못 할 복잡한 업무를 받으면 그 창구에 더 넓은 책상과 장비를 주는 것이 VPA, 매장 자체가 꽉 차면 옆 건물(노드)을 빌리는 것이 Cluster Autoscaler다.
- **오해 1**: 오토스케일링을 켜두면 무조건 안전하다 — 아니다. 임계값이 너무 예민하면 조정이 반복되며(thrashing) 오히려 서비스가 불안정해지고, 컨테이너 이미지가 크면 새 Pod가 뜨는 데 시간이 걸려(cold start) 스케일 반응이 늦다.
- **오해 2**: VPA는 HPA처럼 즉시 반영된다 — 아니다. VPA `Auto` 모드는 Pod 재시작을 수반하므로, 세션을 유지해야 하는 서비스에는 먼저 `Off` 모드로 추천값만 확인하고 수동 반영하는 것이 안전하다.

## 연결 개념
- Docker 컨테이너 - 스케일링 대상이 되는 실행 단위(Pod)의 기반
- 쿠버네티스 - HPA·VPA·Cluster Autoscaler가 동작하는 오케스트레이션 환경
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

- 개요: 오토 스케일링은 부하 지표 기반 자원 자동 조정 기술임.
- 배경: 클라우드 네이티브 서비스는 트래픽 변동이 커서 고정 용량은 장애와 비용 낭비를 만든다.
- 필요성: HPA의 Pod 수 조정과 VPA의 요청 자원 조정으로 SLO와 비용 지표를 함께 관리한다.

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

| 구분 | HPA | VPA | 선택 기준 |
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
