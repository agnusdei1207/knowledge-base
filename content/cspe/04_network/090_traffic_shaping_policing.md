---
title: "트래픽 셰이핑·폴리싱 (Traffic Shaping Policing)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 90
---

# 📖 【암기용】 개념 완전 이해

> 목적: 트래픽 셰이핑과 폴리싱을 처음 봐도 속도 제한의 위치와 동작 차이를 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: 셰이핑은 트래픽을 버퍼에 보관해 송신 속도를 매끄럽게 만들고, 폴리싱은 계약 초과 패킷을 즉시 폐기·재표시하는 QoS 집행 기술
- **왜 필요한가**: WAN 회선은 CIR, PIR, SLA 같은 계약 속도를 가진다. 애플리케이션 burst가 회선보다 크면 큐 손실, 지연, 제공망 폐기가 발생한다.
- **핵심 직관**: 셰이핑은 줄을 세워 천천히 내보내는 방식이고, 폴리싱은 입구에서 규정 초과 차량을 바로 돌려보내는 방식이다.

## 깊이 이해
- **배경·문제의식**: 라우터가 LAN 속도(1/10GbE)로 WAN(100Mbps) 회선에 트래픽을 밀어 넣으면 제공망에서 무작위 폐기가 생긴다. 실시간 트래픽은 지연·지터 정책과 함께 속도 제어가 필요하다.
- **작동 원리**: token bucket은 일정 속도로 토큰을 채우고 패킷 크기만큼 토큰을 소비한다. 셰이핑은 토큰 부족 시 큐에 보관하고, 폴리싱은 discard 또는 remarking을 수행한다.
- **비유**: 수도꼭지 물을 양동이에 모아 일정하게 흘려보내면 셰이핑, 계량기 한도를 넘는 즉시 차단하면 폴리싱이다.
- **구체 예시**: CIR 100Mbps, CBS 12.5MB로 설정하면 평균 100Mbps를 유지하면서 짧은 burst를 토큰 용량만큼 허용한다.
- **흔한 오해·주의점**: 셰이핑은 손실을 줄일 수 있지만 큐 지연을 만든다. 폴리싱은 지연을 만들지 않지만 초과 패킷 손실 또는 DSCP remarking을 발생시킨다.

## 연결 개념
- QoS DiffServ/IntServ — 분류·표시 후 속도 집행
- Token Bucket — CIR/PIR/CBS/EBS 계산 모델
- WRED/Queueing — 혼잡 회피와 큐 관리 기능

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 셰이핑·폴리싱은 둘 다 rate limiting이지만 buffer 여부, 초과 패킷 처리, 적용 위치, 지연·손실 영향이 다름.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 트래픽 셰이핑과 폴리싱은 token bucket 기반으로 트래픽을 계약 속도(CIR/PIR) 안에 맞추는 QoS 집행 기능이다.
> 2. **가치**: 셰이핑은 큐잉으로 burst를 평탄화하고, 폴리싱은 초과 트래픽을 drop 또는 remark해 제공망 SLA를 보호한다.
> 3. **판단 포인트**: egress WAN은 shaping, ingress trust boundary는 policing을 우선 검토하고 지연·손실 영향을 분리해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| QoS 집행 기능 이해 확인 | token bucket, CIR, PIR, CBS, EBS | 둘을 동일 속도 제한으로 처리 |
| 동작 차이 비교 확인 | shaping은 buffer, policing은 drop/remark | 지연과 손실 영향 누락 |
| 적용 위치 판단 확인 | egress WAN vs ingress edge | 제공망 폐기와 LAN burst 관계 누락 |

> 요약: 이 문제는 속도 제한 기능의 동작 차이를 지연·손실·적용 위치 기준으로 비교하는 답안을 요구한다.

---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **트래픽 셰이핑·폴리싱** | 트래픽 셰이핑·폴리싱 (Traffic Shaping Policing)의 핵심 개념 | "이 주제의 본질" |
| **프로토콜** | 통신 규칙의 표준화된 집합 | "공용 언어" |
| **패킷** | 네트워크를 통해 전송되는 데이터의 단위 | "택배 상자" |

---

## Ⅰ. 개요 및 필요성

- 개요: QoS 속도 집행 기술
- 배경: LAN과 WAN 속도 차이, 클라우드 회선 계약, 실시간 트래픽 보호 요구로 트래픽을 CIR/PIR 범위 안에서 제어해야 한다.
- 필요성: 셰이핑은 초과 트래픽을 큐에 보관하고 폴리싱은 초과 트래픽을 폐기하거나 DSCP를 재표시한다.

---

## Ⅱ. 구조 및 구성요소

```text
Packet Input -> Classification -> Token Bucket
              / Shaping: queue -> scheduled output
              / Policing: drop or remark
-> CIR/PIR Enforcement -> Interface Forwarding
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Token Bucket | 토큰 축적·소비 모델 | CIR, PIR, CBS, EBS |
| Shaper Queue | 초과 트래픽 임시 보관 | egress 지연 증가 |
| Policer Action | 초과 패킷 처리 | drop, remark, transmit |
| Scheduler | 큐별 송신 순서 제어 | LLQ, CBWFQ 연계 |

> 요약: 두 기능은 token bucket을 공유하지만 셰이핑은 큐잉, 폴리싱은 즉시 조치가 구조적 차이임.

---

## Ⅲ. 동작원리 및 흐름도

```text
패킷 도착 -> 패킷 크기만큼 토큰 확인
-> 토큰 충분: 전송
-> 토큰 부족
   / shaping: 큐 저장 후 송신
   / policing: drop 또는 DSCP remark
-> KPI 측정
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 트래픽 클래스와 계약 속도 확인 | CIR, PIR, CBS, EBS |
| 2 | 패킷 크기별 토큰 차감 | token bucket state |
| 3 | 셰이핑은 큐에 저장 후 속도 맞춤 | queue depth, delay |
| 4 | 폴리싱은 초과 패킷 폐기·재표시 | drop count, remark count |

> 요약: token bucket 결과에 따라 셰이핑은 시간 지연으로 조절하고 폴리싱은 손실·표시 변경으로 집행함.

---

## Ⅳ. 특징

| 구분 | 트래픽 셰이핑 | 트래픽 폴리싱 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 초과 처리 | 큐 보관 후 전송 | drop 또는 remark | buffer 여부 |
| 지연 영향 | 큐 지연 증가 | 추가 큐 지연 없음 | p95 latency |
| 손실 영향 | 큐 overflow 시 손실 | 초과 즉시 손실 가능 | drop count |
| 적용 위치 | egress WAN, provider edge 전 | ingress edge, trust boundary | CIR/PIR 준수 |

> 요약: 셰이핑은 손실을 줄이는 대신 지연을 만들고, 폴리싱은 지연을 만들지 않지만 초과 손실을 발생시킴.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 셰이핑·폴리싱 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 무제어 Best Effort | token bucket rate control | 계약 회선, QoS 도메인 |
| 비용/성능 | 제공망 임의 폐기 | CIR/PIR 준수 | SLA penalty, burst 특성 |
| 운영/위험 | 정책 단순 | 큐·토큰 파라미터 필요 | 지연 허용, 손실 허용 |

> 요약: 지연 허용 가능하고 손실 최소화가 목표면 셰이핑, 경계 보호와 초과 억제가 목표면 폴리싱을 선택함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 큐 지연 증가 | shaping buffer 과대 | queue limit, LLQ 분리 | p95 latency, jitter |
| 초과 폐기 증가 | policing rate 낮음 | CIR/PIR 재산정, remarking | policer drop % |
| 토큰 파라미터 오류 | CBS/EBS 과소·과대 | BDP 기반 burst 계산 | burst loss, queue depth |

> 요약: 주요 리스크는 큐 지연, 초과 폐기, 토큰 파라미터 오류이며 지연·손실·큐 깊이로 검증함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 계약 준수 | 평균 전송률 CIR 이하, burst PIR 이하 | interface rate, NetFlow |
| 손실 | policer drop 임계치 이하 | QoS counter |
| 지연·지터 | 음성 150ms/30ms 기준 충족 | IP SLA, RTP stats |

> 요약: 도입 평가는 계약 속도 준수, drop count, 지연·지터를 클래스별로 측정해야 함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. WAN egress에는 CIR보다 5~10% 낮은 shaping rate를 적용해 제공망 policer 폐기를 줄임.
2. 인터넷·클라우드 ingress 경계에는 DSCP trust 정책과 policing을 적용해 임의 marking과 초과 트래픽을 통제함.
3. token bucket 파라미터는 CIR/PIR, RTT, MTU, BDP를 기준으로 CBS/EBS를 산정하고 QoS counter로 보정함.

**결론 (2줄):**
- 기술사 판단: 회선 계약 준수와 손실 완화가 목표면 egress shaping, 경계 보호와 남용 억제가 목표면 ingress policing을 선택함.
- 향후 방향: 셰이핑·폴리싱은 SD-WAN, cloud interconnect, 5G slice SLA에서 애플리케이션 정책 기반 rate control로 확장됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "트래픽 셰이핑과 폴리싱을 설명하시오" | token bucket, 큐잉, drop/remark 흐름 | 지연·손실·적용 위치 비교 |
| 요구사항 명시형 | "차이를 비교하시오", "QoS 적용 방안을 제시하시오" | CIR/PIR/CBS/EBS 산정 절차 | WAN egress와 ingress edge 선택 기준 |

> 요약: 설명형은 token bucket 동작, 요구사항형은 적용 위치와 SLA 지표 중심으로 목차를 전환함.
