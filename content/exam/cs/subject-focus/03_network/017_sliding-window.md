---
title: "슬라이딩 윈도우 (Sliding Window)"
date: "2026-06-30"
weight: 17
tags:
  - "exam-cspe-network"
---

## Ⅰ. 정의
> 송신자가 ACK(Acknowledgement)를 기다리지 않고 윈도우 크기만큼의 프레임을 연속 전송하여 처리율을 높이는 흐름제어 기법.

## Ⅱ. 구성요소 / 원리
- 송신 윈도우(Send Window): 응답을 받지 않고 전송 가능한 프레임 범위
- 수신 윈도우(Receive Window): 수신·버퍼링 가능한 프레임 범위
- 윈도우 슬라이드: ACK 수신 시 윈도우 좌측 경계가 전진
- 순환 시퀀스 번호(Sequence Number): n비트로 0~2ⁿ-1 순환 사용
- 누적/선택 ACK로 GBN(Go-Back-N)·SR(Selective Repeat) 구분

## Ⅲ. 흐름도 / 구조
```text
송신측 윈도우(크기 W=4)
[1][2][3][4] 5  6      → 1~4 연속 전송
   ACK2 수신 → 윈도우 전진
 1 [2][3][4][5] 6      → 5 추가 전송 가능
처리율 ≈ W / (1+2a),  a = 전파지연/전송시간
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 정지대기(Stop-and-Wait) 비효율 개선, 회선 이용률 극대화 |
| 장점 | 다수 프레임 동시 전송으로 처리율 향상, 흐름제어 통합 |
| 한계 | 윈도우 과대 시 수신버퍼 부담, 시퀀스 번호 공간 제약 |

## Ⅴ. 기술사적 적용
- TCP(Transmission Control Protocol)의 가변 윈도우(Window Scaling)로 BDP(Bandwidth-Delay Product) 활용
- HDLC·LAPB 등 데이터링크 계층 ARQ(Automatic Repeat reQuest)와 연계
- 윈도우 크기 = 대역폭×RTT(Round Trip Time)로 산정해 고속·장거리망 최적화
