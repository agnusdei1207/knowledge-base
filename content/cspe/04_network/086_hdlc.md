---
title: "HDLC 프레임 구조·동작 모드 (HDLC)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 86
---

# 📖 【암기용】 개념 완전 이해

> 목적: HDLC를 처음 봐도 비트 지향 데이터링크 프로토콜의 프레임 구조와 동작 모드를 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: 점대점·다중점 링크에서 프레임 단위 전송, 오류검출, 흐름제어를 수행하는 비트 지향 데이터링크 프로토콜
- **왜 필요한가**: 물리 회선은 비트열만 전달하므로 프레임 경계, 주소, 제어, 오류검출 규칙이 필요하다. HDLC는 flag 0x7E와 FCS로 프레임을 식별·검증한다.
- **핵심 직관**: 비트열에 시작/끝 표시와 검사값을 붙여, 수신자가 "어디부터 어디까지가 한 통신 단위인지" 알게 하는 약속이다.

## 깊이 이해
- **배경·문제의식**: 문자 지향 프로토콜은 특정 문자 집합과 제어문자에 의존했다. HDLC는 비트 지향 방식으로 투명성을 높이고 다양한 회선 구성에 적용되도록 설계됐다.
- **작동 원리**: 프레임은 Flag, Address, Control, Information, FCS, Flag로 구성된다. 데이터 안에 flag 패턴이 나타나면 bit stuffing으로 5개의 연속 1 뒤에 0을 삽입한다.
- **비유**: 택배 상자 양끝에 봉인 테이프를 붙이고 운송장·검수 체크섬을 넣어, 중간 내용이 무엇이든 상자를 구분하는 것과 같다.
- **구체 예시**: HDLC flag는 01111110(0x7E)이며, FCS는 CRC-16 또는 CRC-32 기반으로 오류를 검출한다.
- **흔한 오해·주의점**: HDLC는 라우팅 프로토콜이 아니다. OSI 2계층에서 프레임 경계와 링크 제어를 담당한다.

## 연결 개념
- PPP — HDLC류 framing을 활용한 점대점 링크 프로토콜
- LAPB/LAPD — X.25, ISDN에서 파생된 HDLC 계열
- CRC/FCS — 프레임 오류검출 메커니즘

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: HDLC 답안은 flag 0x7E, bit stuffing, I/S/U frame, NRM/ARM/ABM 모드를 연결해 써야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: HDLC는 비트 지향 프레임 구조로 링크 계층에서 프레임 동기, 오류검출, 흐름제어, 링크 관리를 수행하는 프로토콜이다.
> 2. **가치**: flag 0x7E, bit stuffing, FCS로 데이터 투명성과 프레임 경계 식별을 제공한다.
> 3. **판단 포인트**: I-frame/S-frame/U-frame의 역할과 NRM/ARM/ABM 동작 모드 차이를 구분해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 데이터링크 계층 framing 이해 확인 | Flag, Address, Control, Information, FCS | 프레임 필드 순서 누락 |
| 비트 지향 투명성 확인 | 0x7E, bit stuffing, CRC | 문자 지향 프로토콜로 설명 |
| 동작 모드 판단 확인 | NRM, ARM, ABM과 I/S/U frame | 라우팅·전송계층 기능으로 오해 |

> 요약: 이 문제는 HDLC 프레임 구조와 링크 제어 모드를 필드·프레임 유형·동작 모드로 정리하는 답안을 요구한다.

---

## Ⅰ. 개요 및 필요성

HDLC는 비트 지향 데이터링크 제어 프로토콜이다.
물리 회선은 연속 비트열만 전달하므로 송수신 노드는 프레임 경계, 오류검출, 재전송, 흐름제어 규칙이 필요하다.
HDLC는 0x7E flag와 FCS, I/S/U 프레임을 통해 점대점·다중점 회선의 링크 제어 기준을 제공한다.

---

## Ⅱ. 구조 및 구성요소

```text
Flag 0x7E -> Address -> Control -> Information -> FCS -> Flag 0x7E
           / I-frame: user data
           / S-frame: flow/error control
           / U-frame: link management
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Flag | 프레임 시작·종료 표시 | 01111110, 0x7E |
| Address | station 식별 | multipoint 회선에서 사용 |
| Control | 프레임 유형·순서 제어 | I/S/U frame, N(S), N(R) |
| FCS | 오류검출 | CRC-16 또는 CRC-32 |

> 요약: HDLC 프레임은 flag로 경계를 잡고 control 필드와 FCS로 링크 제어와 오류검출을 수행함.

---

## Ⅲ. 동작원리 및 흐름도

```text
링크 설정 -> 프레임 생성 -> bit stuffing 적용
-> flag 0x7E로 송신 -> 수신 bit unstuffing
-> FCS 검증 -> ACK/재전송 또는 링크 관리
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | U-frame으로 링크 설정 | SABM, UA |
| 2 | I-frame에 데이터와 순서번호 삽입 | N(S), N(R) |
| 3 | 5개 연속 1 뒤 0 삽입 | bit stuffing rule |
| 4 | FCS 오류검출 후 S-frame 제어 | RR, RNR, REJ |

> 요약: HDLC는 링크 설정 후 I-frame 데이터 전송, bit stuffing, FCS 검증, S-frame 제어의 순서로 동작함.

---

## Ⅳ. 특징

| 구분 | 문자 지향 방식 | HDLC | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 프레임 경계 | 제어문자 의존 | flag 0x7E | 01111110 |
| 데이터 투명성 | escape 문자 사용 | bit stuffing | 5연속 1 뒤 0 삽입 |
| 제어 기능 | 제한적 제어 | I/S/U frame | RR, RNR, REJ, SABM |
| 오류검출 | 단순 검사 가능 | FCS CRC | CRC-16/CRC-32 |

> 요약: HDLC는 비트 지향 framing과 CRC 기반 FCS로 링크 계층 신뢰 제어를 표준화한 방식임.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | HDLC | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 문자 지향 BSC | 비트 지향 flag/FCS | 투명성, 회선 종류 |
| 비용/성능 | 단순 제어 | sequence 기반 흐름제어 | 오류율, 재전송 요구 |
| 운영/위험 | 구현 단순 | 모드와 상태 관리 필요 | NRM/ARM/ABM 운용 |

> 요약: 회선 오류검출과 링크 제어가 필요한 전용 링크는 HDLC 계열, IP 점대점 접속은 PPP와 비교함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 프레임 경계 오류 | flag 패턴 손상 | bit stuffing, FCS 검사 | frame abort count |
| 순서 제어 오류 | N(S)/N(R) 불일치 | window 초기화, REJ 처리 | retransmission count |
| 모드 불일치 | NRM/ABM 설정 차이 | 링크 협상값 점검 | SABM/UA success rate |

> 요약: HDLC 운영 리스크는 framing, 순서번호, 모드 협상이며 링크 카운터로 추적함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 오류율 | FCS error 임계치 이하 | interface counter |
| 링크 제어 | REJ/RNR 빈도 감소 | protocol trace |
| 프레임 투명성 | stuffing/unstuffing 오류 0 | packet analyzer |

> 요약: 도입 평가는 FCS error, 재전송, link control frame 상태로 확인해야 함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 답안 작성 시 HDLC 프레임을 Flag -> Address -> Control -> Information -> FCS -> Flag 순서로 먼저 제시함.
2. 제어 프레임은 I-frame 데이터, S-frame RR/RNR/REJ, U-frame SABM/UA로 역할을 분리함.
3. 링크 장애 분석은 FCS error, frame abort, retransmission count, mode negotiation trace를 함께 확인함.

**결론 (2줄):**
- 기술사 판단: 비트 지향 링크 제어 설명 문제는 HDLC를 기준으로 쓰고, IP 점대점 연결 문제는 PPP와의 차이를 함께 제시함.
- 향후 방향: HDLC 원리는 PPP, LAPB, LAPD 등 파생 프로토콜의 framing과 오류검출 이해 기반으로 유지됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "HDLC를 설명하시오" | 프레임 생성, stuffing, FCS 검증 흐름 | 필드 구조와 I/S/U frame |
| 요구사항 명시형 | "프레임 구조를 기술하시오", "동작 모드를 비교하시오" | control field와 모드 전환 | NRM/ARM/ABM, 오류·흐름제어 |

> 요약: 설명형은 전체 링크 제어, 요구사항형은 필드 구조와 동작 모드 비교 중심으로 목차를 전환함.
