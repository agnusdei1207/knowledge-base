---
title: "QoS — DiffServ·IntServ (QoS DiffServ IntServ)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 89
---

# 📖 【암기용】 개념 완전 이해

> 목적: QoS, DiffServ, IntServ를 처음 봐도 패킷망에서 지연·지터·손실을 관리하는 방식을 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: QoS는 트래픽 유형별로 대역폭, 지연, 지터, 손실을 차등 관리하는 네트워크 품질 제어 체계
- **왜 필요한가**: 음성, 영상회의, 제어 트래픽은 지연과 지터에 민감하지만 파일 전송은 손실 복구가 가능하다. 같은 큐에 모두 넣으면 실시간 트래픽 품질이 흔들린다.
- **핵심 직관**: 도로의 버스전용차로처럼, 패킷에도 서비스 등급과 우선순위를 부여해 혼잡 시 처리 순서를 다르게 하는 방식이다.

## 깊이 이해
- **배경·문제의식**: IP 기본 전송은 Best Effort다. 혼잡이 생기면 모든 패킷이 비슷하게 지연·폐기되어 VoIP, 영상, 산업 제어 품질이 악화된다.
- **작동 원리**: DiffServ는 DSCP로 패킷 등급을 표시하고 라우터가 PHB(EF, AF, BE)에 따라 큐잉·스케줄링·폐기를 수행한다. IntServ는 RSVP로 플로우별 자원을 예약한다.
- **비유**: DiffServ는 택배 상자에 등급 스티커를 붙이고 물류센터가 등급별로 처리하는 방식, IntServ는 배송 전에 특정 차량 좌석을 예약하는 방식이다.
- **구체 예시**: VoIP는 DSCP EF(46)를 사용해 LLQ에 배치하고, 영상은 AF41, 일반 웹은 BE로 분류해 지연과 폐기 정책을 다르게 둔다.
- **흔한 오해·주의점**: QoS는 대역폭을 새로 만드는 기술이 아니다. 혼잡 시 어떤 패킷을 먼저 처리하고 어떤 패킷을 제한할지 결정하는 정책이다.

## 연결 개념
- 트래픽 셰이핑·폴리싱 — QoS 정책 집행 기능
- MPLS TE — 경로와 대역폭을 함께 고려하는 트래픽 엔지니어링
- ECN/WRED — 혼잡 발생 전 폐기·표시 정책

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: QoS 답안은 DSCP marking, PHB, queue scheduling, RSVP reservation, KPI 지연·지터·손실을 연결해야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: QoS는 네트워크 혼잡 상황에서 트래픽 등급별 지연, 지터, 손실, 대역폭을 정책적으로 제어하는 체계이다.
> 2. **가치**: DiffServ는 DSCP/PHB로 확장성 있는 클래스 기반 QoS를 제공하고, IntServ는 RSVP로 플로우별 자원 예약을 제공한다.
> 3. **판단 포인트**: 기업·ISP망은 DiffServ 중심, 엄격한 플로우 보장은 IntServ/RSVP-TE 또는 전용 경로와 비교해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| QoS 제어 원리 확인 | classification, marking, queuing, scheduling | 우선순위만 설명 |
| DiffServ/IntServ 비교 확인 | DSCP/PHB vs RSVP per-flow reservation | 두 모델의 확장성 차이 누락 |
| 운영 지표 판단 확인 | latency, jitter, packet loss, MOS | 대역폭 증가로만 해결한다고 설명 |

> 요약: 이 문제는 QoS 모델의 제어 위치와 확장성, 실시간 서비스 KPI를 연결하는 답안을 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 트래픽 등급별 품질 제어
- 배경: IP망은 Best Effort 전달을 기본으로 하므로 혼잡 시 음성·영상·제어 트래픽이 지연, 지터, 손실에 노출된다.
- 필요성: QoS는 DSCP, RSVP, 큐잉, 스케줄링, 폐기 정책으로 서비스별 SLA 지표를 맞춘다.

---

## Ⅱ. 구조 및 구성요소

```text
Packet Input -> Classification -> Marking
             / DiffServ: DSCP -> PHB
             / IntServ: RSVP -> Resource Reservation
-> Queueing/Scheduling -> Policing/Shaping -> Forwarding
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Classification | 트래픽 식별 | 5-tuple, VLAN CoS, application |
| Marking | QoS 등급 표시 | DSCP 6bit, EF 46, AFxy |
| PHB | 홉별 처리 동작 | EF, AF, BE |
| RSVP | 플로우별 자원 예약 | IntServ, RSVP-TE |

> 요약: QoS는 패킷을 분류·표시하고 DiffServ 또는 IntServ 모델에 따라 큐와 자원을 제어함.

---

## Ⅲ. 동작원리 및 흐름도

```text
트래픽 식별 -> DSCP/RSVP 정책 적용 -> 큐 배치
-> 스케줄링/혼잡 회피 -> shaping/policing
-> 전송 KPI 측정 -> 정책 보정
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 음성·영상·업무·백업 트래픽 분류 | ACL, NBAR, 5-tuple |
| 2 | DSCP marking 또는 RSVP reservation | DSCP trust boundary |
| 3 | LLQ, CBWFQ, WRED 적용 | queue drop, latency |
| 4 | 지연·지터·손실 측정 후 정책 조정 | p95 latency, jitter, loss |

> 요약: QoS는 분류와 표시에서 시작해 큐잉·스케줄링·혼잡 회피를 거쳐 KPI로 보정하는 폐루프임.

---

## Ⅳ. 특징

| 구분 | DiffServ | IntServ | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 제어 단위 | 클래스 기반 | 플로우 기반 | DSCP vs RSVP state |
| 확장성 | 라우터 상태 적음 | 플로우별 상태 증가 | core router state |
| 보장 방식 | PHB별 차등 처리 | 자원 예약 | EF, AF, BE / Guaranteed Service |
| 적용 | 기업망·ISP 백본 | 제한된 도메인, RSVP-TE | SLA, 관리 도메인 |

> 요약: DiffServ는 확장성, IntServ는 플로우별 보장에 강점이 있으나 상태 관리 비용이 크다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | DiffServ·IntServ QoS | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | Best Effort | DSCP/PHB 또는 RSVP | SLA 유무, 도메인 규모 |
| 비용/성능 | 단일 큐 처리 | 클래스별 큐·스케줄링 | 라우터 CPU/queue 자원 |
| 운영/위험 | 정책 단순 | trust boundary와 marking 관리 | DSCP remarking, policy drift |

> 요약: 대규모 IP망은 DiffServ를 기본으로 하고, 엄격한 경로·자원 보장은 RSVP-TE 또는 전용 경로를 검토함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| DSCP 오염 | 단말 임의 marking | trust boundary, remarking | DSCP distribution |
| 우선순위 과다 | EF 트래픽 비율 증가 | LLQ bandwidth cap | priority queue drop |
| RSVP 상태 폭증 | per-flow state 증가 | admission control, DiffServ 전환 | RSVP session count |

> 요약: QoS 리스크는 marking 신뢰, 우선순위 남용, 상태 폭증이며 정책 경계와 큐 카운터로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 음성 품질 | one-way latency 150ms 이하, jitter 30ms 이하 | IP SLA, RTP statistics |
| 손실 | voice packet loss 1% 이하 | interface/queue counter |
| 정책 준수 | DSCP별 큐 매핑 일치 | NetFlow, QoS policy map |

> 요약: 도입 평가는 지연·지터·손실과 DSCP별 큐 매핑 일치 여부로 확인해야 함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. QoS 도메인 경계에서 DSCP trust boundary를 정하고 EF 46, AF41, BE 등급을 재표시함.
2. WAN 구간은 LLQ/CBWFQ/WRED와 shaping을 조합해 음성, 영상, 업무, 백업 트래픽을 분리함.
3. 운영은 p95 latency, jitter, loss, queue drop, DSCP distribution을 주기 측정해 정책 drift를 수정함.

**결론 (2줄):**
- 기술사 판단: 대규모망은 DiffServ 중심, 폐쇄 도메인의 엄격 자원 보장은 RSVP/IntServ 또는 MPLS TE를 선택함.
- 향후 방향: QoS는 SD-WAN, 5G network slicing, intent 기반 네트워크에서 애플리케이션 SLA 정책으로 확장됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "QoS를 설명하시오" | classification -> marking -> queuing 흐름 | DiffServ와 IntServ 비교 |
| 요구사항 명시형 | "DiffServ와 IntServ를 비교하시오", "QoS 적용 방안을 제시하시오" | DSCP/RSVP 설계 절차 | 지연·지터·손실 KPI와 리스크 |

> 요약: 설명형은 QoS 처리 파이프라인, 요구사항형은 DiffServ/IntServ 선택과 SLA 지표 중심으로 목차를 전환함.
