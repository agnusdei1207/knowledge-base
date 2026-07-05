---
title: "5G SLA 보장 슬라이싱 (5G SLA Slicing)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 96
---

# 📖 【암기용】 개념 완전 이해

> 목적: 5G SLA 보장 슬라이싱을 서비스 계약 지표를 슬라이스 자원과 정책으로 구현하는 체계로 이해하게 만든다.

## 한눈에
- **개요**: 5G 슬라이스별 지연·대역폭·가용성·손실률 SLA를 보장하는 운영 방식
- **왜 필요한가**: 원격제어, 스마트팩토리, 재난망은 일반 모바일 인터넷과 다른 SLA를 요구한다.
- **핵심 직관**: 같은 전력망을 쓰지만 병원, 공장, 가정에 다른 우선순위와 예비 용량을 배정하는 것과 같다.

## 깊이 이해
- **배경·문제의식**: 5G는 eMBB, URLLC, mMTC를 한 인프라에서 제공한다. SLA를 계약했으면 무선 구간, 전송망, 5G Core, MEC 중 어디에서 병목이 생겨도 지표를 측정하고 조치해야 한다.
- **작동 원리**: S-NSSAI로 슬라이스를 식별하고 5QI, ARP, GBR, AMBR, UPF selection, MEC placement를 조합해 SLA 목표를 만족시킨다. closed-loop assurance가 지표 초과 시 자원 재배치나 경로 변경을 수행한다.
- **비유**: 식당 예약에서 VIP룸, 전용 직원, 제한된 좌석을 미리 확보하고 대기시간을 SLA로 관리하는 방식이다.
- **구체 예시**: 원격제어 슬라이스는 p95 latency 10ms 이하, availability 99.99%, packet loss 0.001% 이하를 목표로 MEC 근접 배치와 GBR QoS flow를 사용한다.
- **흔한 오해·주의점**: SLA는 슬라이스 이름만으로 보장되지 않는다. 측정 지점, 위반 판정 기간, penalty, degradation policy가 계약에 포함되어야 한다.

## 연결 개념
- Network Slice Resource Management — SLA를 자원 배정으로 구현
- 5QI/QoS Flow — 사용자 트래픽별 우선순위와 보장률
- MEC — 지연 SLA 달성을 위한 compute 위치

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 5G SLA slicing 출제 시 계약 지표, QoS 정책, assurance loop, 위반 대응을 압축 답안으로 제시한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 5G SLA Slicing은 S-NSSAI별 latency, throughput, availability, packet loss 목표를 QoS·자원·관측 체계로 보장하는 기술이다.
> 2. **가치**: 산업 서비스별 계약 품질을 RAN, transport, core, MEC까지 end-to-end로 측정하고 통제한다.
> 3. **판단 포인트**: SLA 지표 정의, 5QI/GBR 설정, admission control, closed-loop assurance, penalty 기준을 함께 설계한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 5G QoS와 SLA 연결 확인 | S-NSSAI, 5QI, GBR, ARP, UPF, MEC | 슬라이스 생성만 설명 |
| 보장 메커니즘 이해 확인 | admission, resource reservation, assurance loop | 측정·검증 지표 누락 |
| 운영·계약 판단 확인 | SLA 위반 기준, 보고, penalty, degradation | 가용성·손실률 없이 지연만 서술 |

> 요약: 이 문제는 5G 슬라이스를 계약 품질 보장 체계로 설계하는지를 확인한다.

---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **5G SLA 보장 슬라이싱** | 5G SLA 보장 슬라이싱 (5G SLA Slicing)의 핵심 개념 | "이 주제의 본질" |
| **프로토콜** | 통신 규칙의 표준화된 집합 | "공용 언어" |
| **패킷** | 네트워크를 통해 전송되는 데이터의 단위 | "택배 상자" |

---

## Ⅰ. 개요 및 필요성

- 개요: 슬라이스별 SLA 보장 구조
- 배경: 산업용 5G는 지연, 손실, 가용성, 단말 수 요구가 일반 인터넷 접속과 다르다.
- 필요성: 5G SLA Slicing은 QoS flow, 자원 예약, 관측, 위반 대응을 통합해 슬라이스별 계약 지표를 관리한다.

---

## Ⅱ. 구조 및 구성요소

```text
SLA Contract -> S-NSSAI -> 5QI/GBR/ARP Policy
             -> RAN / Transport / UPF / MEC Resource
             -> SLA Probe -> Assurance Loop -> Report/Penalty
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| SLA 지표 | 지연·손실·가용성·처리량 목표 | p95, p99, monthly uptime |
| QoS 정책 | 5QI, GBR, ARP, AMBR 설정 | QoS Flow Identifier 사용 |
| 자원 도메인 | RAN, transport, UPF, MEC 자원 보장 | PRB, bandwidth, CPU |
| Assurance | 측정·분석·조치 자동화 | closed-loop control |

> 요약: 5G SLA slicing은 계약 지표를 QoS 정책과 E2E 자원 보장 구조로 변환한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
SLA 요구 수신 -> slice/QoS 정책 생성 -> 자원 승인
-> 트래픽 처리 -> SLA 측정 -> 위반 감지 -> 자원 조정/보고
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | SLA에서 latency, availability, loss, throughput 추출 | 지표·기간 명시 |
| 2 | S-NSSAI와 5QI/GBR/ARP 매핑 | QoS flow 설정 |
| 3 | RAN PRB, transport path, UPF/MEC 자원 예약 | admission 통과 |
| 4 | probe와 telemetry로 SLA 측정 | p95 latency, loss % |
| 5 | 위반 시 scale-out, 경로 변경, 보고 수행 | SLA 위반 시간 기록 |

> 요약: SLA slicing은 계약 해석, 정책 매핑, 자원 예약, 측정, 위반 조치의 반복 구조다.

---

## Ⅳ. 특징

| 구분 | 기존/대안 | 5G SLA Slicing | 수치 컬럼 |
|:---|:---|:---|:---|
| 품질 제공 | best-effort APN | S-NSSAI별 계약 품질 | latency 10ms |
| QoS 제어 | 단일 우선순위 | 5QI, GBR, ARP | packet loss 0.001% |
| 측정 범위 | 장비별 KPI | RAN~MEC E2E SLA | availability 99.99% |
| 운영 방식 | 장애 후 대응 | closed-loop assurance | 위반 5분 내 조치 |

> 요약: 5G SLA slicing은 품질 목표를 계약·정책·측정·조치로 연결한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 서비스 모델 | 일반 모바일 데이터 | 산업별 SLA slice | 공장·의료·재난망 요구 |
| 품질 보장 | QoS class만 설정 | SLA+assurance loop | penalty 계약 존재 |
| 자원 배정 | 통계적 공유 | admission+reservation | URLLC·GBR 트래픽 |

> 요약: SLA slicing은 계약 위반 비용이 존재하고 지표 측정이 가능한 서비스에 적용한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| SLA 미달 | 과다 수용, 무선 혼잡 | admission control, PRB reservation | p95 latency, PRB usage |
| 측정 분쟁 | 측정 위치·기간 불명확 | probe 위치, 산정 주기 계약화 | SLA report 일치율 |
| 자원 낭비 | 과도한 예약 | dynamic scaling, quota | reserved vs used ratio |

> 요약: SLA slicing은 과다 수용, 측정 분쟁, 예약 과잉을 계약과 지표로 통제해야 한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 지연·손실 | p95 latency 10ms 이하, loss 0.001% 이하 | active probe, UPF telemetry |
| 가용성 | monthly availability 99.99% | SLA report, incident log |
| 자원 효율 | reserved vs used 60~85% | orchestrator metric |

> 요약: SLA 달성은 지연·손실·가용성·예약 사용률을 함께 측정해야 신뢰할 수 있다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. SLA 계약서에 p95 latency, packet loss %, availability, 측정 위치, 산정 기간, penalty를 명시
2. S-NSSAI별 5QI, GBR, ARP, UPF selection, MEC placement 정책을 표준 템플릿화
3. telemetry와 active probe를 closed-loop assurance에 연결해 위반 5분 내 scale-out·경로 변경 수행

**결론 (2줄):**
- 기술사 판단: URLLC·산업 제어처럼 위반 비용이 큰 서비스는 SLA slicing으로 자원 예약과 측정 기준을 계약화해야 함
- 향후 방향: intent 기반 SLA 입력과 AI assurance로 슬라이스 자원 조정을 자동화하는 방향

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "설명하시오", "기술하시오" | SLA 요구를 QoS·자원으로 변환 | best-effort 대비 계약 보장 |
| 요구사항 명시형 | "비교하시오", "방안을 제시하시오", "설계하시오" | 측정 위치·위반 조치·assurance 설계 | SLA 미달·분쟁·예약 과잉 대응 |

> 요약: 포괄형은 SLA slicing 구조, 요구사항 명시형은 계약 지표와 운영 보장 방안을 중심으로 답안을 구성한다.
