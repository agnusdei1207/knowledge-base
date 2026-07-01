---
title: "5G 특화망·로컬 5G (Private 5G Local 5G)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 48
---

# 📖 【암기용】 개념 완전 이해

> 목적: 5G 특화망·로컬 5G를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 기업·기관이 특정 지역에서 전용 주파수 또는 사업자 협력을 통해 구축하는 5G 기반 사설 무선망
- **왜 필요한가**: 공장, 항만, 병원, 캠퍼스는 Wi-Fi보다 예측 가능한 QoS, 이동성, 단말 인증, 전용 데이터 경로가 필요하다. 공용망만으로는 현장 SLA와 데이터 경계 요구를 모두 맞추기 어렵다.
- **핵심 직관**: 공용 도로가 아니라 공장 안 전용 도로를 만들고, 차량 통행 규칙과 관제실을 현장 요구에 맞게 운영하는 방식이다.

## 깊이 이해
- **배경·문제의식**: 산업 자동화와 로봇·AGV·비전 검사 시스템은 이동 중 끊김, 업링크 영상, 현장 데이터 보관 요구가 있다. 5G 특화망은 전용 gNB, local 5GC, MEC를 배치해 현장 내 데이터 경로를 짧게 만든다.
- **작동 원리**: 단말은 사설 PLMN 또는 SNPN에 접속하고, 로컬 AMF/SMF/UPF가 인증·세션을 처리한다. UPF는 공장 MEC나 내부망으로 local breakout을 수행한다.
- **비유**: 회사 내부망 Wi-Fi가 사무실 무선 LAN이라면, private 5G는 인증·우선순위·커버리지·이동성을 갖춘 산업용 무선 교통망이다.
- **구체 예시**: 스마트팩토리 AGV는 5QI, local UPF, MEC 제어 서버를 통해 현장 내 지연시간과 패킷 손실을 측정하며 운영한다.
- **흔한 오해·주의점**: Private 5G가 Wi-Fi를 모두 대체하는 것은 아니다. 고정형 고속 데이터는 Wi-Fi 6/7, 이동·QoS·전용 경로는 private 5G로 역할을 나눈다.

## 연결 개념
- SNPN/PNI-NPN - 3GPP Non-Public Network 구축 형태
- MEC - 현장 내 애플리케이션 처리
- 5G Network Slicing - 공용망 기반 기업 전용 논리망 구성

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 특화망을 전용망 홍보어로 쓰지 않고 SNPN/PNI-NPN, spectrum, local 5GC/UPF, MEC, SLA, 보안 운영을 기준으로 답안을 구성한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 5G 특화망·로컬 5G는 특정 구역에서 기업 전용 5G 무선·코어·엣지를 구성하는 Non-Public Network이다.
> 2. **가치**: 현장 데이터 경계, 이동성, QoS, local breakout, 단말 인증을 기업 SLA에 맞춰 제어한다.
> 3. **판단 포인트**: 주파수 확보, SNPN/PNI-NPN 선택, local UPF 위치, Wi-Fi 공존, 운영 인력과 장애 대응 절차를 평가해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| private 5G 구조 이해 확인 | gNB, local 5GC, UPF, MEC, NPN | 공용 5G 요금제와 혼동 |
| 산업 적용 판단 확인 | 제조·항만·병원 SLA와 데이터 경계 | Wi-Fi 대비 무조건 우위로 단정 |
| 구축 리스크 확인 | 주파수, 단말, 운영, 보안, 장애 대응 | 주파수 규제와 운용 책임 누락 |

> 요약: 이 문제는 private 5G의 기술 구성과 산업 현장 적용 조건을 균형 있게 제시하는 답안을 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 특정 구역 전용 5G 사설망
- 배경: 공용망은 공장, 항만, 캠퍼스의 데이터 경계와 현장 지연 요구를 모두 보장하기 어려움
- 필요성: local 5GC, MEC, 전용 주파수로 QoS, 이동성, 현장 데이터 처리를 통제

---

## Ⅱ. 구조 및 구성요소

```text
Industrial UE/Robot/Camera -> Private gNB -> Local 5GC
Local 5GC -> AMF/SMF -> Local UPF -> MEC/Application
Private 5G
  / SNPN standalone
  / PNI-NPN with operator integration
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Private gNB | 현장 5G 무선 커버리지 제공 | 실내 음영, handover 설계 |
| Local 5GC | 인증·이동성·세션 처리 | AMF/SMF/UPF 소형화 배치 |
| Local UPF/MEC | 현장 데이터 경로 단축 | 내부망 local breakout |
| NPN 운영체계 | 단말·주파수·장애 관리 | SNPN 또는 PNI-NPN 선택 |

> 요약: private 5G는 현장 gNB, local 5GC, UPF/MEC, 운영체계를 결합해 기업 전용 무선망을 구성한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
업무 SLA 정의 -> 주파수/구축모델 선택 -> RF 설계
-> gNB/5GC/UPF 구축 -> 단말 인증 -> MEC 연동
-> KPI 측정 -> 운영 정책 조정
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | AGV·카메라·센서별 SLA 정의 | latency, packet loss, uplink Mbps |
| 2 | SNPN/PNI-NPN과 주파수 사용 방식 결정 | 규제 적합성, 사업자 연동 |
| 3 | RF survey와 gNB 배치 설계 | RSRP, SINR, handover area |
| 4 | local 5GC, UPF, MEC 애플리케이션 연동 | PDU success, E2E latency |
| 5 | 운영 모니터링과 장애 대응 절차 수립 | MTTR, SLA violation |

> 요약: private 5G는 업무 SLA에서 시작해 주파수·RF·코어·MEC·운영 절차를 순서대로 검증한다.

---

## Ⅳ. 특징

| 구분 | Wi-Fi/공용망 | Private 5G | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 접속 제어 | SSID/공용망 가입자 | SIM/eSIM, 5G AKA | 단말 인증·권한 |
| 이동성 | AP roaming 중심 | gNB handover | AGV 이동 경로 |
| 데이터 경로 | 인터넷/기업 LAN | local UPF/MEC | E2E latency, data boundary |
| 운영 책임 | IT LAN 또는 통신사 | 기업+통신/장비사 역할 분담 | NOC, 장애 MTTR |

> 요약: private 5G는 이동성·QoS·현장 데이터 경로가 필요한 산업 업무에 적합하며 Wi-Fi와 역할을 분담한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | Private 5G | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | Wi-Fi 6/7, 공용 5G | 전용 gNB, local 5GC, MEC | 이동성, QoS, 데이터 경계 |
| 비용/성능 | AP 중심 투자 | 주파수·코어·운영 투자 | SLA 위반 비용과 생산 중단 영향 |
| 운영/위험 | LAN 운영 | 통신망 운영 절차 필요 | RF 엔지니어링, 단말 인증 |

> 요약: 단순 인터넷 접속은 Wi-Fi, 생산제어·이동체·현장 데이터 경계는 private 5G를 선택한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 커버리지 음영 | 금속 설비·차폐 구조 | RF survey, small cell 추가 | RSRP, SINR, handover fail |
| 운영 역량 부족 | 5GC·RF 장애 대응 경험 부족 | managed service, NOC runbook | MTTR, alarm 처리시간 |
| 단말 생태계 제약 | 산업 단말 band·SIM 지원 부족 | 인증 단말 목록, PoC 검증 | device attach success |

> 요약: private 5G 리스크는 RF 환경, 운영 역량, 단말 호환성이며 현장 PoC 지표로 조기 확인해야 한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 무선 품질 | RSRP/SINR, handover fail 목표 | site survey, drive/walk test |
| 서비스 SLA | E2E latency, packet loss, uplink Mbps | MEC probe, app log |
| 운영 품질 | MTTR, attach/PDU success 99% 이상 | NOC ticket, 5GC PM |

> 요약: 도입 효과는 무선 커버리지, 애플리케이션 SLA, 운영 복구 지표를 함께 측정해야 한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. PoC: AGV 10대, 카메라 20대 등 대표 업무를 선정하고 latency, packet loss, uplink Mbps 목표를 사전 정의함
2. 아키텍처: SNPN 또는 PNI-NPN을 선택하고 local UPF와 MEC를 생산망 DMZ에 배치해 데이터 경계를 검증함
3. 운영: SIM/eSIM lifecycle, gNB 장애, 5GC 장애, RF 간섭 대응 runbook과 MTTR 목표를 수립함

**결론 (2줄):**
- 기술사 판단: private 5G는 이동성·QoS·데이터 경계 요구가 명확할 때 선택하고, 일반 사무망은 Wi-Fi와 병행 설계함
- 향후 방향: RedCap, 5G LAN, slicing, MEC 통합으로 산업 단말 비용과 운영 자동화 범위가 개선되는 추세임

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "5G 특화망을 설명하시오" | gNB, local 5GC, UPF, MEC 구축 흐름 | Wi-Fi·공용망 대비 특징 |
| 요구사항 명시형 | "스마트팩토리 적용 방안을 제시하시오" | SLA 정의, RF 설계, PoC 절차 | 운영·단말·주파수 리스크 |

> 요약: 설명형은 NPN 구조, 방안형은 현장 SLA와 운영 책임 중심으로 목차를 전환한다.
