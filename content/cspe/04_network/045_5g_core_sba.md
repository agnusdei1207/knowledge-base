---
title: "5G 코어 네트워크 SBA - AMF·SMF·UPF (5G Core SBA)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 45
---

# 📖 【암기용】 개념 완전 이해

> 목적: 5G Core SBA를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 5G Core는 AMF·SMF·UPF 등 Network Function이 서비스 기반 인터페이스로 연동되는 클라우드 네이티브 코어망 구조
- **왜 필요한가**: EPC는 MME·SGW·PGW 중심의 장비 단위 구조라 slicing, MEC, API 노출, 기능 확장에 제약이 있다. 5GC는 NF를 분리해 서비스별로 조합한다.
- **핵심 직관**: EPC가 고정된 교환기 묶음이라면, SBA는 여러 마이크로서비스가 필요한 기능을 API로 호출하는 구조이다.

## 깊이 이해
- **배경·문제의식**: 5G는 eMBB·URLLC·mMTC처럼 서로 다른 요구사항을 수용해야 한다. 이를 위해 제어면 기능을 NF 단위로 쪼개고, 사용자 평면 UPF를 서비스 위치에 맞게 분산할 필요가 있다.
- **작동 원리**: UE가 등록하면 AMF가 접근·이동성을 처리하고 AUSF/UDM과 인증을 수행한다. PDU Session 요청은 SMF가 처리하며, SMF는 UPF를 선택해 N3/N6 데이터 경로를 만든다.
- **비유**: 공항에서 AMF는 입국 심사·이동 동선 안내, SMF는 탑승권과 게이트 배정, UPF는 실제 수하물 이동 컨베이어 역할을 한다.
- **구체 예시**: SBA는 Namf, Nsmf, Npcf, Nudm 같은 서비스 기반 인터페이스를 사용하고, UPF는 MEC 근처에 배치해 local breakout을 구성할 수 있다.
- **흔한 오해·주의점**: SBA는 제어면 구조이고, UPF는 사용자 평면 패킷 전달 기능이다. 모든 NF가 HTTP API만으로 데이터 패킷을 전달하는 것은 아니다.

## 연결 개념
- AMF - UE 등록, 접근, 이동성 관리
- SMF - PDU Session, IP 주소, UPF 선택, QoS Flow 제어
- UPF - 사용자 패킷 포워딩, QoS enforcement, local breakout

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 5GC SBA를 NF 명칭 나열로 끝내지 않고 AMF·SMF·UPF 역할 분리, 서비스 기반 인터페이스, 세션 흐름, 운영 지표로 답안을 구성한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 5G Core SBA는 제어면 NF가 서비스 기반 인터페이스로 기능을 제공하고, UPF가 사용자 평면을 분산 처리하는 3GPP 코어망 구조이다.
> 2. **가치**: AMF·SMF·UPF 분리로 이동성, 세션 제어, 패킷 전달을 독립 확장하고 slicing·MEC·API exposure를 지원한다.
> 3. **판단 포인트**: NF discovery, SBI 보안, UPF 위치, PDU Session 성공률, control/user plane 분리 효과를 함께 검증해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 5GC 구조 이해 확인 | AMF·SMF·UPF 역할과 N1/N2/N3/N4/N6 | NF 이름만 나열하고 흐름 누락 |
| SBA 원리 확인 | NRF discovery, 서비스 기반 인터페이스 | EPC 장비 구조와 구분 실패 |
| 운영 판단 확인 | UPF 분산, MEC, slicing, observability | 제어면·사용자 평면 혼동 |

> 요약: 이 문제는 5GC NF 역할과 SBA 호출 구조를 PDU Session 흐름으로 설명하는 답안을 요구한다.

---

## Ⅰ. 개요 및 필요성

5G Core SBA는 AMF·SMF·UPF 등 NF가 서비스 기반으로 연동되는 3GPP 5GC 구조이다. 5G SA, network slicing, MEC, private 5G는 EPC보다 세밀한 제어면 분리와 UPF 분산을 요구한다. 답안은 NF 역할과 세션 흐름을 함께 제시해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
UE -> gNB -> AMF
AMF -> AUSF/UDM/PCF/NRF
AMF -> SMF -> UPF -> Data Network
SMF -> UPF over N4
gNB -> UPF over N3
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| AMF | UE 등록, 접근 인증 연계, 이동성 관리 | N1/N2 termination |
| SMF | PDU Session 생성, IP 주소, QoS Flow, UPF 선택 | N4로 UPF 제어 |
| UPF | 사용자 패킷 포워딩, QoS 적용, N6 연결 | MEC local breakout 가능 |
| NRF/PCF/UDM | NF discovery, 정책, 가입자 데이터 제공 | SBI 기반 서비스 호출 |

> 요약: AMF는 접근·이동성, SMF는 세션 제어, UPF는 패킷 전달을 담당하며 SBI로 주변 NF와 연동한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
UE Registration -> AMF Selection -> Authentication with AUSF/UDM
-> PDU Session Request -> SMF Selection -> UPF Selection
-> N4 Rule Install -> N3/N6 User Plane Forwarding -> QoS Monitoring
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | UE가 gNB를 통해 AMF에 registration 수행 | registration success rate |
| 2 | AMF가 AUSF/UDM과 인증·가입자 정보 확인 | auth failure rate |
| 3 | SMF가 DNN·S-NSSAI 기준 PDU Session 처리 | PDU session success rate |
| 4 | SMF가 UPF를 선택하고 N4 forwarding rule 설치 | PFCP session success |
| 5 | UPF가 N3/N6 패킷 전달 및 QoS enforcement 수행 | packet loss, latency |

> 요약: 5GC는 등록, 인증, 세션 제어, UPF 규칙 설치, 사용자 평면 전달 순서로 동작한다.

---

## Ⅳ. 특징

| 구분 | EPC | 5GC SBA | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 구조 | MME·SGW·PGW 장비 중심 | AMF·SMF·UPF NF 분리 | CUPS, SBI, cloud native |
| 인터페이스 | S1/S5/S11 참조점 중심 | Namf/Nsmf/Npcf 등 서비스 호출 | OAuth2, TLS, NRF |
| 사용자 평면 | SGW/PGW 중심 | UPF 분산 배치 | MEC latency, N6 breakout |
| 운영 | APN/QCI | DNN, S-NSSAI, 5QI | slicing·QoS Flow |

> 요약: 5GC SBA는 제어면을 NF 서비스로 분리하고 UPF를 분산해 slicing과 MEC 적용 기반을 제공한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 5GC SBA | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | EPC monolithic appliance | cloud native NF, SBI | SA 전환, slicing 요구 |
| 비용/성능 | 중앙 PGW 경로 | local UPF, N6 breakout | E2E latency와 회선 비용 |
| 운영/위험 | 장비별 장애 관리 | NF별 관측성·오케스트레이션 | NF scaling, service mesh |

> 요약: 5GC SBA는 SA·slicing·MEC 요구가 있을 때 필요하며 NF 관측성과 자동화가 성공 조건이다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| SBI 장애 | NRF 조회 실패, TLS 인증서 오류 | NRF 이중화, mTLS, health check | SBI 5xx rate, NF heartbeat |
| 세션 실패 | SMF/UPF N4 규칙 불일치 | PFCP 로그 상관분석, rollback | PDU success, PFCP failure |
| UPF 병목 | local breakout 트래픽 집중 | UPF scale-out, QoS policing | UPF CPU, packet drop |

> 요약: 5GC 운영 리스크는 SBI·세션·UPF 병목이며 NF별 로그와 PM 카운터를 연결해야 한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 접속·세션 | registration/PDU success 99% 이상 | AMF/SMF PM, CDR |
| 사용자 평면 | latency, packet loss, throughput | UPF counter, probe |
| 제어면 | SBI error rate, NF discovery time | NRF/SCP 로그, tracing |

> 요약: 5GC 품질은 접속 성공률, 사용자 평면 지표, SBI 제어면 지표를 함께 보아야 한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. NF 배치: AMF/SMF는 지역 이중화, UPF는 MEC·기업망 근처에 배치해 N3/N6 경로와 E2E latency를 측정함
2. SBA 보안: SBI 구간 mTLS, OAuth2 token, NRF 접근통제를 적용하고 SBI 4xx/5xx rate를 모니터링함
3. 세션 검증: DNN·S-NSSAI·5QI별 PDU Session 성공률, PFCP N4 실패율, UPF drop counter를 대시보드화함

**결론 (2줄):**
- 기술사 판단: 5GC SBA는 SA, slicing, MEC 요구가 명확할 때 AMF·SMF·UPF 분리와 UPF 위치가 설계 핵심임
- 향후 방향: 5G-Advanced는 NWDAF, SCP, 자동 스케일링과 결합해 NF 단위 폐루프 운영으로 발전함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "5G Core SBA를 설명하시오" | registration, PDU Session, UPF forwarding 흐름 | EPC 대비 NF 분리와 SBI 비교 |
| 요구사항 명시형 | "5GC 구축 방안을 제시하시오" | NF 배치, SBI 보안, UPF 분산 절차 | 세션 실패·UPF 병목 리스크와 지표 |

> 요약: 설명형은 NF 역할과 흐름, 구축형은 배치·보안·운영 지표 중심으로 목차를 바꾼다.
