---
title: "ATM 비동기 전송 모드 (ATM Asynchronous Transfer Mode)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 88
---

# 📖 【암기용】 개념 완전 이해

> 목적: ATM을 처음 봐도 53바이트 셀, 가상경로/가상채널, QoS 클래스의 의미를 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: 53바이트 고정 길이 셀로 음성·영상·데이터를 통합 전송하려 한 비동기식 교환 기술
- **왜 필요한가**: 가변 길이 패킷은 지연 변동이 크고, 회선교환은 데이터 burst 처리에 비경제적이다. ATM은 작은 고정 셀로 지연 예측성과 통계적 다중화를 동시에 목표로 했다.
- **핵심 직관**: 모든 화물을 같은 크기 상자(53바이트 셀)에 담아 스위치가 일정한 속도로 처리하게 만든 방식이다.

## 깊이 이해
- **배경·문제의식**: B-ISDN 시대에는 전화, 화상회의, 데이터 서비스를 하나의 광대역망에서 처리하려 했다. 서비스마다 지연, 지터, 손실 요구가 달라 QoS 클래스가 필요했다.
- **작동 원리**: ATM 셀은 5바이트 헤더와 48바이트 페이로드로 구성된다. VPI/VCI가 가상경로·가상채널을 식별하고, AAL이 상위 데이터를 셀로 분할·재조립한다.
- **비유**: 서로 다른 크기의 짐을 모두 동일 규격 컨테이너에 나누어 담고, 컨테이너 번호표로 목적지를 찾는 물류 시스템과 같다.
- **구체 예시**: AAL5는 IP 데이터 전송에 많이 쓰이며, CBR은 음성처럼 일정 대역, VBR은 영상처럼 변동 대역, ABR은 피드백 기반 데이터 전송에 사용된다.
- **흔한 오해·주의점**: ATM은 IP를 대체한 최종 인터넷 구조가 아니다. 고정 셀과 QoS 개념은 이후 MPLS, QoS, carrier Ethernet 설계에 영향을 남겼다.

## 연결 개념
- QoS DiffServ/IntServ — 서비스 등급과 자원 예약 개념
- MPLS — label switching과 가상경로 개념의 후속 구조
- SONET/SDH — ATM 전송을 수용했던 광 전송 계층

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: ATM 답안은 53 byte cell, VPI/VCI, AAL, QoS class, cell tax를 함께 써야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: ATM은 5바이트 헤더와 48바이트 페이로드로 구성된 53바이트 고정 셀 기반 비동기 전송 기술이다.
> 2. **가치**: 고정 셀 스위칭과 VPI/VCI 가상회선으로 음성·영상·데이터를 QoS 클래스별로 통합 전송한다.
> 3. **판단 포인트**: CBR/VBR/ABR/UBR 서비스 클래스, AAL 기능, cell overhead와 IP/Ethernet 대비 한계를 구분해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| ATM 구조 이해 확인 | 53 byte cell, header 5, payload 48 | 단순 패킷 교환으로 설명 |
| QoS 지원 방식 확인 | CBR, VBR, ABR, UBR, traffic contract | QoS 클래스를 누락 |
| 후속 기술 비교 확인 | MPLS, Ethernet, IP QoS와 비교 | 현재 인터넷 표준으로 과장 |

> 요약: 이 문제는 ATM의 고정 셀 교환 구조와 QoS 보장을 장점·한계까지 균형 있게 쓰는 답안을 요구한다.

---

## Ⅰ. 개요 및 필요성

ATM은 고정 길이 셀 기반 비동기 전송 모드이다.
음성·영상·데이터를 하나의 광대역망에서 처리하려면 지연, 지터, 손실 요구가 다른 트래픽을 구분해 전송해야 한다.
ATM은 53바이트 셀과 가상회선, QoS 클래스, AAL을 통해 멀티서비스 통합망을 지향했다.

---

## Ⅱ. 구조 및 구성요소

```text
Application Data -> AAL Segmentation -> ATM Cell 53 byte
                 / Header 5 byte: VPI/VCI/PTI/CLP/HEC
                 / Payload 48 byte
-> ATM Switch -> Virtual Path/Channel -> Reassembly
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| ATM Cell | 고정 길이 전송 단위 | 53 byte = header 5 + payload 48 |
| VPI/VCI | 가상경로·가상채널 식별 | label switching 유사 |
| AAL | 상위 데이터 분할·재조립 | AAL1, AAL2, AAL5 |
| QoS Class | 서비스 품질 계약 | CBR, VBR, ABR, UBR |

> 요약: ATM은 AAL이 데이터를 48바이트 단위로 나누고 VPI/VCI 기반 셀 스위칭으로 전송함.

---

## Ⅲ. 동작원리 및 흐름도

```text
서비스 요구 수신 -> QoS 클래스 선택 -> VC 설정
-> AAL segmentation -> 53 byte cell 생성
-> VPI/VCI switching -> reassembly -> 상위 계층 전달
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 트래픽 유형과 QoS 요구 분류 | PCR, SCR, MBS |
| 2 | VPI/VCI 기반 가상회선 설정 | VC table |
| 3 | AAL에서 셀 분할·헤더 삽입 | SAR error |
| 4 | ATM switch가 셀 단위 중계 | CLR, CTD, CDV |

> 요약: ATM은 서비스 계약을 기반으로 VC를 만들고, AAL 분할 후 53바이트 셀을 VPI/VCI로 교환함.

---

## Ⅳ. 특징

| 구분 | IP/Ethernet 패킷 | ATM | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 전송 단위 | 가변 길이 프레임 | 53 byte 고정 셀 | cell tax 약 9.4% |
| 교환 방식 | 주소 기반 forwarding | VPI/VCI label switching | VC table |
| QoS | Best Effort 기본 | CBR/VBR/ABR/UBR | PCR, SCR, CDV |
| 한계 | QoS 별도 설계 필요 | 셀 분할 오버헤드 | IP over ATM 복잡도 |

> 요약: ATM은 고정 셀로 지연 예측성을 확보했지만 5바이트 헤더와 셀 분할 오버헤드가 존재함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | ATM | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 회선교환 또는 IP 패킷 | VC 기반 셀 교환 | 지연·지터 보장 요구 |
| 비용/성능 | 가변 패킷 처리 | 고정 셀 하드웨어 스위칭 | cell overhead, 장비 비용 |
| 운영/위험 | IP 중심 단순화 | QoS contract 관리 | PCR/SCR 설정 정확도 |

> 요약: ATM은 멀티서비스 QoS 보장 요구에서 의미가 있으나 현대망은 MPLS, DiffServ, Carrier Ethernet으로 대체 검토함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 셀 손실 | 혼잡, CLP 폐기 | traffic policing, CAC | CLR, CLP discard |
| 지연 변동 | 스위치 큐잉 | CBR/VBR class 분리 | CDV, CTD |
| 오버헤드 증가 | 5바이트 헤더, SAR | AAL5 효율 점검 | cell tax, SAR error |

> 요약: ATM 리스크는 셀 손실, 지연 변동, 셀 분할 오버헤드이며 QoS 파라미터로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| QoS 계약 | PCR/SCR/MBS 준수 | traffic contract audit |
| 셀 품질 | CLR, CTD, CDV 임계치 이하 | ATM PM counter |
| 재조립 품질 | SAR error 0 또는 임계치 이하 | AAL statistics |

> 요약: 도입 평가는 QoS 계약 준수, 셀 손실·지연, AAL 재조립 오류로 확인해야 함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. ATM 설명 답안은 53바이트 셀, VPI/VCI, AAL, QoS class를 한 구조도에 배치함.
2. QoS 설계는 CBR/VBR/ABR/UBR별 PCR, SCR, MBS, CDV 기준을 표로 분리함.
3. 레거시 ATM망 현대화는 MPLS L2/L3VPN, Carrier Ethernet, IP QoS로 대체하면서 서비스별 지연·손실 SLA를 매핑함.

**결론 (2줄):**
- 기술사 판단: 지연·지터 보장형 멀티서비스 설명에는 ATM이 적합하나 신규 백본은 MPLS/Ethernet QoS를 우선 선택함.
- 향후 방향: ATM의 VC, label switching, QoS contract 개념은 MPLS TE와 DiffServ 설계 원리로 계승됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "ATM을 설명하시오" | QoS class -> VC -> cell switching 흐름 | 53 byte cell, AAL, VPI/VCI |
| 요구사항 명시형 | "IP와 비교하시오", "QoS 보장 방안을 제시하시오" | PCR/SCR/CDV 기반 계약 절차 | cell tax, MPLS/Ethernet 대체 기준 |

> 요약: 설명형은 셀 교환 원리, 요구사항형은 QoS 계약과 현대망 대체 기준으로 목차를 전환함.
