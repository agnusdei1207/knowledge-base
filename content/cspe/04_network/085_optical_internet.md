---
title: "광 인터넷 (Optical Internet)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 85
---

# 📖 【암기용】 개념 완전 이해

> 목적: 광 인터넷을 처음 봐도 IP 계층과 광 전송 계층이 어떻게 결합되는지 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: IP 트래픽을 광 파장·광 경로 단위로 직접 운반해 대용량 백본을 구성하는 네트워크 구조
- **왜 필요한가**: 클라우드, CDN, AI 데이터센터는 수백 Gbps~Tbps 트래픽을 만든다. 전기 스위칭만으로는 전력, 지연, 포트 비용이 커진다.
- **핵심 직관**: 패킷 고속도로 아래에 파장 단위 전용 차선을 깔아, 큰 흐름은 광 경로로 바로 보내는 구조이다.

## 깊이 이해
- **배경·문제의식**: 전통 인터넷은 IP/MPLS 라우터와 SDH/SONET 전송망이 계층적으로 분리됐다. 트래픽 폭증은 라우터 hop 수, 전기 변환, 전력 소모를 증가시켰다.
- **작동 원리**: IP/MPLS 라우터가 광 전송망(OTN, DWDM, ROADM)과 연동해 lightpath를 설정한다. GMPLS 또는 SDN 컨트롤러가 패킷 경로와 광 경로를 함께 제어한다.
- **비유**: 일반 차량은 교차로를 지나가지만, 물동량이 큰 노선은 도시 간 직통 철도를 놓아 중간 환승을 줄이는 것과 같다.
- **구체 예시**: 데이터센터 간 DCI는 400ZR coherent optics와 DWDM을 사용해 100km급 metro 구간에서 400GbE를 파장 단위로 운반한다.
- **흔한 오해·주의점**: 광 인터넷은 모든 패킷을 광으로 스위칭한다는 뜻이 아니다. 세밀한 패킷 제어는 IP 계층, 대용량 운반은 광 계층이 맡는다.

## 연결 개념
- WDM/DWDM — 광 파장 단위 용량 제공
- GMPLS/SDN — 패킷 계층과 광 계층 제어 연동
- OTN — 광 전송망에서 클라이언트 신호 보호와 OAM 제공

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 광 인터넷은 광섬유 속도 이야기가 아니라 IP/MPLS, OTN, DWDM, ROADM 제어 연동과 KPI를 쓰는 문제임.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 광 인터넷은 IP 패킷 트래픽을 광 파장(lightpath) 단위 전송망과 연동해 운반하는 고용량 인터넷 백본 구조이다.
> 2. **가치**: 라우터 hop과 O/E/O 변환을 줄이고 100G/400G/800G 광 채널로 metro/core 트래픽을 처리한다.
> 3. **판단 포인트**: IP-optical integration, OTN OAM, ROADM, coherent optics, 장애 복구 정책을 함께 설계해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 광 기반 인터넷 구조 이해 확인 | IP/MPLS + OTN + DWDM + ROADM | 광섬유 전송 속도만 설명 |
| 계층 통합 판단 확인 | packet switching과 optical switching 역할 분담 | 패킷망과 전송망 경계 누락 |
| 운영 지표 확인 | lightpath, OSNR, BER, restoration time | 용량 확장만 쓰고 장애·OAM 누락 |

> 요약: 이 문제는 IP 계층의 경로 제어와 광 계층의 대용량 전송을 통합 관점으로 쓰는 답안을 요구한다.

---

## Ⅰ. 개요 및 필요성

광 인터넷은 IP 트래픽을 광 전송망과 연동해 운반하는 구조이다.
클라우드, CDN, AI 학습 트래픽은 100G/400G 포트와 Tbps 백본을 요구하며, 전기 라우터 hop 증가는 지연과 전력 소모를 키운다.
광 인터넷은 DWDM 파장, OTN, ROADM, SDN 제어를 결합해 대용량·장거리 인터넷 백본을 구성한다.

---

## Ⅱ. 구조 및 구성요소

```text
IP/MPLS Router -> Optical Transponder -> OTN Mapping
               / DWDM Wavelength
               / ROADM Lightpath
               / SDN/GMPLS Control
-> Optical Core -> Remote Router
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| IP/MPLS 라우터 | 패킷 경로 제어 | BGP, IS-IS, RSVP-TE/SR |
| OTN | 클라이언트 신호 매핑·OAM | ODUk, FEC, 보호 |
| DWDM/ROADM | 파장 전송·분기 | 100G/400G lightpath |
| SDN/GMPLS | 패킷-광 경로 통합 제어 | multi-layer PCE |

> 요약: 광 인터넷은 IP 라우팅과 OTN/DWDM 광 경로를 제어 평면에서 연동하는 다계층 구조임.

---

## Ⅲ. 동작원리 및 흐름도

```text
트래픽 수요 분석 -> IP 경로 계산 -> Lightpath 설정
-> OTN 매핑/FEC -> DWDM 전송
-> ROADM 경유 -> 수신 라우터 전달 -> KPI 피드백
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | IP 트래픽 매트릭스 분석 | peak Gbps, flow demand |
| 2 | lightpath 후보와 라우팅 계산 | path diversity, SRLG |
| 3 | OTN/DWDM 채널 설정 | OSNR, pre-FEC BER |
| 4 | 장애 시 packet reroute 또는 optical restoration | restoration time, packet loss |

> 요약: 광 인터넷은 트래픽 수요에 따라 광 경로를 설정하고, 장애 시 IP와 광 계층 복구 정책을 조합함.

---

## Ⅳ. 특징

| 구분 | 전통 IP over SDH | 광 인터넷 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 계층 구조 | IP/MPLS와 전송망 분리 | IP-optical 통합 제어 | multi-layer PCE |
| 용량 | STM/OC 계위 중심 | 100G/400G/800G wavelength | coherent optics |
| 지연 | 다중 O/E/O, 라우터 hop | lightpath 직결 | hop count 감소 |
| 운용 | 계층별 수동 조정 | SDN/GMPLS 자동 경로 | restoration time |

> 요약: 광 인터넷은 패킷 제어 유연성과 광 전송 용량을 결합하지만 계층 간 장애 책임과 복구 정책을 명확히 해야 함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 광 인터넷 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 라우터 중심 증설 | router + optical lightpath | 트래픽 매트릭스, hop 수 |
| 비용/전력 | 모든 흐름 라우터 처리 | 대용량 흐름 광 우회 | W/Gbps, port cost |
| 운영/위험 | 계층별 독립 운용 | multi-layer orchestration | SRLG, OAM 연동 |

> 요약: 대용량 장거리 흐름은 광 경로 우회, 미세 트래픽은 IP 라우팅으로 처리하는 하이브리드가 적합함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 계층 복구 충돌 | IP reroute와 optical restoration 동시 작동 | hold-off timer, policy 분리 | flap count, convergence time |
| 광 품질 저하 | OSNR 부족, 분산 | FEC, power equalization | pre-FEC BER, Q-factor |
| 경로 단일점 | SRLG 미반영 | fiber route diversity | shared risk group audit |

> 요약: 광 인터넷 리스크는 계층 복구 충돌, 광 품질, SRLG이며 설계 단계에서 정책과 물리 경로를 함께 검증해야 함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 용량 | 100G/400G 채널 사용률 60~80% | router/OTN PM |
| 품질 | post-FEC BER 10^-15 이하 | transponder counter |
| 복구 | 서비스 등급별 50ms~수초 | 장애 주입 시험 |

> 요약: 도입 평가는 채널 사용률, BER, 복구 시간을 계층별로 분리 측정해야 함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. metro/core 구간 트래픽 매트릭스를 분석해 100G/400G lightpath 후보와 라우터 우회 구간을 선정함.
2. IP/MPLS SR-TE와 ROADM/OTN 제어를 PCE 또는 SDN 컨트롤러로 연동하고 SRLG 기반 경로 다양성을 적용함.
3. 운영 KPI는 OSNR, pre-FEC BER, 라우터 인터페이스 사용률, 복구 시간을 공통 대시보드로 통합함.

**결론 (2줄):**
- 기술사 판단: 장거리 대용량 elephant flow가 많으면 광 인터넷 구조, 변동성 높은 세부 트래픽은 IP/MPLS 중심 구조를 선택함.
- 향후 방향: 400ZR/800ZR, coherent pluggable, IP-optical SDN으로 라우터와 광 전송망 경계가 더 가까워짐.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "광 인터넷을 설명하시오" | IP 경로 -> lightpath -> OTN/DWDM 흐름 | 전통 IP over SDH와 차이 |
| 요구사항 명시형 | "백본 구축 방안을 제시하시오", "운영 방안을 논하시오" | multi-layer path, SRLG, 복구 정책 | 용량·품질·복구 KPI |

> 요약: 설명형은 계층 구조, 요구사항형은 IP-optical 통합 설계와 운영 KPI로 목차를 전환함.
