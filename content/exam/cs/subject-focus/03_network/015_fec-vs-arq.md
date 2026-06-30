---
title: "FEC vs ARQ (Forward Error Correction vs Automatic Repeat reQuest)"
date: "2026-06-30"
weight: 15
tags:
  - "exam-cspe-network"
---

## Ⅰ. 정의
> 오류 제어의 두 축으로, FEC는 송신측이 정정 부호를 부가해 수신측이 재전송 없이 오류를 정정하는 방식이고, ARQ는 오류 검출 시 재전송을 요청하는 방식이다.

## Ⅱ. 구성요소 / 원리
- FEC(Forward Error Correction): 중복 부호(해밍·RS·터보·LDPC)로 수신측 자체 정정, 단방향 전송
- ARQ(Automatic Repeat reQuest): 검출(CRC)+ACK/NAK+재전송, 양방향 채널·타이머 필요
- 트레이드오프: FEC는 대역폭 오버헤드 상시 발생하나 지연 일정, ARQ는 오류 시에만 비용·지연 변동
- HARQ(Hybrid ARQ): FEC+ARQ 결합, 1차 FEC 정정 실패 시 재전송, 패리티 누적(Chase/IR)
- 채널 특성에 따라 선택: 고지연·단방향→FEC, 저지연 양방향→ARQ, 무선→HARQ

## Ⅲ. 흐름도 / 구조
```text
 FEC : 송신[데이터+정정부호] → 수신[오류 자체 정정]   (재전송 없음)
 ARQ : 송신[데이터+CRC] → 수신[오류검출] → NAK → 재전송
 HARQ: 송신[데이터+FEC] → 정정실패시 NAK → 추가 패리티 재전송→합성정정
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 채널 오류를 정정(FEC) 또는 재전송(ARQ)하여 신뢰성 확보 |
| 장점 | FEC는 지연 일정·단방향 가능, ARQ는 오류 없을 때 오버헤드 최소 |
| 한계 | FEC는 상시 대역폭 소모·정정능력 초과 시 실패, ARQ는 재전송 지연·역방향 채널 필요 |

## Ⅴ. 기술사적 적용
- LTE/5G는 HARQ로 무선 오류를 빠르게 복구하며 재전송 지연 최소화
- 위성·방송 등 단방향/고지연 링크는 FEC(LDPC/RS) 중심 설계
- TCP는 ARQ 기반 재전송으로 신뢰성 보장, 실시간 미디어는 FEC 병행
