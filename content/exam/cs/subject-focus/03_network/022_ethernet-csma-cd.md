---
title: "이더넷·CSMA/CD (Ethernet/CSMA-CD)"
date: "2026-06-30"
weight: 22
tags:
  - "exam-cspe-network"
---

## Ⅰ. 정의
> 공유 매체에서 전송 전 반송파를 감지(Carrier Sense)하고, 충돌 발생 시 이를 감지(Collision Detection)해 재전송하는 이더넷의 매체접근제어(MAC) 방식.

## Ⅱ. 구성요소 / 원리
- Carrier Sense: 전송 전 매체 사용 여부 감지
- Multiple Access: 다수 노드가 매체 공유
- Collision Detection: 전송 중 충돌 신호 감지
- 1-persistent: 매체 유휴 시 즉시 전송
- 백오프(Binary Exponential Backoff): 충돌 시 무작위 대기 후 재전송

## Ⅲ. 흐름도 / 구조
```text
전송준비 → 매체감지(Carrier Sense)
 ├ busy → 계속 감지(1-persistent)
 └ idle → 전송 시작
        충돌? → Jam신호 송출 → 백오프(2ⁿ 슬롯 랜덤) → 재시도
        무충돌 → 전송 완료
 16회 충돌 → 폐기(과부하)
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 공유 반이중 매체에서 충돌을 줄여 매체 공정 분배 |
| 장점 | 구조 단순·저비용, 비결정적 분산 제어 |
| 한계 | 부하 증가 시 충돌·지연 급증, 거리/속도 제약(최소프레임 64B) |

## Ⅴ. 기술사적 적용
- 전이중 스위치 환경에선 충돌이 없어 CSMA/CD 사실상 비활성화
- 무선랜은 충돌감지 불가로 CSMA/CA(Collision Avoidance) 채택
- 최소 프레임 길이·슬롯타임은 충돌 검출 보장 위한 설계 근거
