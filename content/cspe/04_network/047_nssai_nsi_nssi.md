---
title: "NSSAI·NSI·NSSI (NSSAI NSI NSSI)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 47
---

# 📖 【암기용】 개념 완전 이해

> 목적: NSSAI·NSI·NSSI를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: NSSAI는 단말이 사용할 slice 목록, NSI는 전체 네트워크 슬라이스 인스턴스, NSSI는 RAN·Core·Transport별 하위 slice 인스턴스
- **왜 필요한가**: 슬라이싱은 이름만으로 운영할 수 없다. 단말 요청, 전체 slice 인스턴스, 도메인별 하위 인스턴스를 구분해야 생성·선택·장애 분석이 가능하다.
- **핵심 직관**: NSSAI는 주문서, NSI는 완성된 코스 요리, NSSI는 주방·홀·배달 팀별 담당 파트이다.

## 깊이 이해
- **배경·문제의식**: 5G slicing은 사용자별 요청과 운영자별 인프라 구성이 분리된다. 단말은 S-NSSAI 목록을 요청하지만, 실제 제공은 NSI와 도메인별 NSSI 조합으로 이루어진다.
- **작동 원리**: UE는 Requested NSSAI를 보낸다. AMF와 NSSF는 가입자·위치·정책을 확인해 Allowed NSSAI를 정하고, 해당 S-NSSAI에 맞는 NSI를 선택한다. NSI는 RAN NSSI, CN NSSI, TN NSSI로 구성될 수 있다.
- **비유**: 고객은 메뉴 번호를 주문하지만, 식당 운영자는 주방 조리 라인, 서빙 라인, 배달 라인을 조합해 주문을 수행한다.
- **구체 예시**: S-NSSAI는 SST와 SD로 구성된다. SST 1은 eMBB, SST 2는 URLLC, SST 3은 MIoT 계열로 사용되며 SD는 세부 구분에 쓰인다.
- **흔한 오해·주의점**: NSSAI와 NSI는 같은 것이 아니다. NSSAI는 식별자 목록이고, NSI는 실제 운영되는 slice 인스턴스이다.

## 연결 개념
- S-NSSAI - 단일 slice 식별자, SST + SD
- NSSF - Allowed NSSAI와 NSI 선택을 지원
- NSMF/NSSMF - NSI와 NSSI 생명주기 관리

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: NSSAI·NSI·NSSI를 용어 암기로 쓰지 않고 단말 요청, slice 선택, 인스턴스 구성, 도메인별 운영 책임으로 연결한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: NSSAI는 S-NSSAI 목록, NSI는 end-to-end network slice instance, NSSI는 RAN/CN/TN 등 하위 도메인 slice instance이다.
> 2. **가치**: 단말의 slice 요청과 운영자의 실제 인프라 인스턴스를 분리해 selection, orchestration, assurance를 수행한다.
> 3. **판단 포인트**: Requested/Allowed/Configured NSSAI, S-NSSAI, NSI-NSSI 매핑, NSSF/NSMF/NSSMF 역할을 구분해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| slicing 식별 체계 이해 확인 | NSSAI, S-NSSAI, NSI, NSSI 계층 | NSSAI와 NSI를 동일 용어로 처리 |
| 5GC 절차 이해 확인 | UE 요청, AMF/NSSF 선택, SMF 세션 | NSSF 역할 누락 |
| 운영·장애 분석 판단 확인 | NSI와 RAN/CN/TN NSSI 매핑 | 도메인별 SLA 지표 누락 |

> 요약: 이 문제는 slice 식별자와 실제 인스턴스 계층을 구분하는 정확한 용어 운용이 핵심이다.

---

## Ⅰ. 개요 및 필요성

NSSAI·NSI·NSSI는 5G 네트워크 슬라이스를 식별·선택·운영하기 위한 계층적 개념이다. 단말은 NSSAI로 slice를 요청하고, 사업자는 NSI와 NSSI로 실제 자원을 구성한다. 답안은 식별자와 인스턴스의 차이를 먼저 고정해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
UE -> Requested NSSAI -> AMF -> NSSF
NSSF -> Allowed NSSAI -> NSI Selection
NSI
  / RAN NSSI
  / Core NSSI
  / Transport NSSI
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| NSSAI | S-NSSAI 목록 | Configured, Requested, Allowed NSSAI로 구분 |
| S-NSSAI | 단일 slice 식별자 | SST + SD 구조 |
| NSI | end-to-end slice instance | 서비스별 SLA와 연결 |
| NSSI | 도메인별 하위 slice instance | RAN, CN, TN resource mapping |

> 요약: NSSAI는 요청·허용 목록, NSI는 전체 slice 인스턴스, NSSI는 도메인별 구성 단위이다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Configured NSSAI 저장 -> UE Requested NSSAI 전송 -> AMF 수신
-> NSSF 조회 -> Allowed NSSAI 결정 -> NSI 선택
-> SMF/UPF와 NSSI 매핑 -> SLA assurance
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 단말에 Configured NSSAI 저장 | USIM/UE policy 일관성 |
| 2 | Registration 시 Requested NSSAI 전달 | AMF log, reject cause |
| 3 | AMF가 NSSF에 slice selection 요청 | NSSF response time |
| 4 | Allowed NSSAI와 NSI를 결정 | S-NSSAI 정책 매핑 |
| 5 | NSI를 RAN/CN/TN NSSI와 연결해 운영 | SLA violation, domain KPI |

> 요약: NSSAI 처리 흐름은 단말 요청에서 NSSF 선택, NSI/NSSI 매핑, SLA 검증으로 이어진다.

---

## Ⅳ. 특징

| 구분 | NSSAI | NSI | NSSI |
|:---|:---|:---|:---|
| 성격 | 식별자 목록 | end-to-end 인스턴스 | 도메인별 하위 인스턴스 |
| 위치 | UE·AMF·NSSF 절차 | NSMF 관리 대상 | NSSMF 관리 대상 |
| 구성 | S-NSSAI 1개 이상 | RAN/CN/TN NSSI 조합 | RAN, Core, Transport |
| 수치·판단 | SST 1/2/3, SD 24-bit | SLA 단위 | domain KPI 단위 |

> 요약: NSSAI는 선택을 위한 목록, NSI는 서비스 제공 단위, NSSI는 인프라 도메인 운영 단위이다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | NSSAI·NSI·NSSI | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | APN/DNN 중심 구분 | S-NSSAI와 NSI 계층 구분 | 서비스별 SLA와 다중 도메인 관리 |
| 비용/성능 | 단일 QoS 정책 | slice별 인스턴스·자원 매핑 | 격리 수준과 자원 예약 비용 |
| 운영/위험 | 장비별 관리 | NSMF/NSSMF orchestration | lifecycle 자동화와 장애 범위 |

> 요약: 다중 slice 운영에서는 NSSAI·NSI·NSSI를 분리해야 고객 요청과 도메인 장애를 정확히 연결할 수 있다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| slice 접속 실패 | Requested NSSAI와 가입자 정책 불일치 | UDM/PCF/NSSF 정책 검증 | reject cause, attach fail |
| SLA 원인 추적 실패 | NSI와 NSSI 매핑 누락 | topology inventory, correlation ID | MTTR, alarm correlation |
| 자원 경합 | NSSI 공유 자원 과다 | quota, admission control | PRB usage, UPF load |

> 요약: 식별·매핑 오류가 주요 리스크이며 reject cause와 도메인 KPI를 함께 추적해야 한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 정책 일관성 | S-NSSAI, DNN, 5QI 매핑 100% 검증 | 정책 카탈로그, CI 검사 |
| 접속 품질 | slice registration/PDU success 99% 이상 | AMF/SMF/NSSF 로그 |
| 도메인 SLA | RAN/CN/TN KPI 목표 충족 | NSMF/NSSMF dashboard |

> 요약: NSSAI·NSI·NSSI 운영 평가는 정책 일관성, 접속 성공률, 도메인별 SLA 달성률로 수행한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 설계: 서비스 카탈로그별 S-NSSAI(SST/SD), DNN, 5QI, 가입자 그룹을 정책 테이블로 관리함
2. 구축: NSSF, AMF, SMF, NSMF/NSSMF 간 NSI·NSSI 매핑 정보를 inventory와 동기화함
3. 운영: slice reject cause, NSSF latency, NSI별 SLA, NSSI별 자원 사용률을 상관 분석함

**결론 (2줄):**
- 기술사 판단: NSSAI는 요청 식별, NSI는 서비스 인스턴스, NSSI는 도메인 자원 단위로 구분해 써야 감점이 없음
- 향후 방향: slicing 자동화는 NSI/NSSI inventory와 NWDAF 기반 assurance의 연동 범위를 확대하는 방향임

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "NSSAI, NSI, NSSI를 설명하시오" | UE 요청에서 NSSF 선택까지 흐름 | 세 용어의 계층·역할 비교 |
| 요구사항 명시형 | "slice 운영 방안을 제시하시오" | 정책 카탈로그와 NSI/NSSI 매핑 절차 | 접속 실패·SLA 추적 리스크 |

> 요약: 설명형은 용어 계층, 운영형은 정책·인벤토리·SLA 상관분석 중심으로 답안을 전환한다.
