---
title: "CSMA/CA (Carrier Sense Multiple Access with Collision Avoidance)"
date: "2026-06-30"
weight: 30
tags:
  - "exam-cspe-network"
---

## Ⅰ. 정의
> 무선랜에서 충돌 감지가 불가능하므로, 전송 전 매체를 감지하고 대기·예약을 통해 충돌을 사전 회피하는 매체접근제어 방식.

## Ⅱ. 구성요소 / 원리
- Carrier Sense: 물리(채널)·가상(NAV) 감지로 매체 유휴 확인
- IFS(Inter-Frame Space): DIFS/SIFS 등 프레임 간 간격으로 우선순위 부여
- 랜덤 백오프(Backoff): 경쟁 윈도우 내 임의 슬롯 대기로 충돌 회피
- RTS/CTS: 전송 전 예약 교환으로 히든 터미널 문제 해소
- ACK: 충돌 미감지 환경에서 수신 확인으로 신뢰성 확보

## Ⅲ. 흐름도 / 구조
```text
매체감지 → DIFS 대기 → 랜덤 백오프(CW)
        → (옵션) RTS ─▶ 수신 ─CTS▶ 송신 (NAV 설정)
        → DATA ──▶ 수신 ──SIFS+ACK──▶ 송신
 히든터미널: A↔AP↔C, A·C 상호 미감지 → RTS/CTS로 예약
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 충돌 검출 불가한 무선 매체에서 충돌 사전 회피 |
| 장점 | 히든 터미널 완화, ACK로 신뢰성, 우선순위 제어(IFS) |
| 한계 | 백오프·RTS/CTS 오버헤드로 처리율 저하, 노출 터미널 문제 |

## Ⅴ. 기술사적 적용
- IEEE 802.11(Wi-Fi) DCF(Distributed Coordination Function)의 핵심
- 유선 CSMA/CD(충돌 감지) vs 무선 CSMA/CA(충돌 회피) 비교
- NAV 기반 가상 반송파 감지로 숨은 노드의 매체 점유 인지
