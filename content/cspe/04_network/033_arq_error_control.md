---
title: "오류 제어 — ARQ·Go-Back-N·SR (ARQ Error Control)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 33
---

# 📖 【암기용】 개념 완전 이해

> 목적: ARQ 오류 제어를 손실 검출과 재전송 전략 관점에서 이해하게 만든다. 시험 답안 양식이 아니라, Stop-and-Wait, Go-Back-N, Selective Repeat 차이를 잡기 위한 설명이다.

## 한눈에
- **개요**: ARQ는 오류나 손실이 검출된 프레임을 ACK/NAK와 timeout으로 재전송하는 오류 제어 방식
- **왜 필요한가**: 무선·장거리·혼잡 링크에서는 비트 오류와 패킷 손실이 발생하므로 수신자가 받은 데이터의 순서와 무결성을 맞춰야 함.
- **핵심 직관**: 택배 상자를 번호대로 보내고, 못 받은 상자 번호를 확인해 다시 보내는 절차임.

## 깊이 이해
- **배경·문제의식**: 링크는 CRC로 오류를 검출할 수 있지만, 오류 프레임을 어떻게 회복할지는 별도 제어가 필요함. ARQ는 수신 확인과 타이머로 손실을 복구함.
- **작동 원리**: 송신자는 순서번호를 붙여 프레임을 보내고 ACK를 기다림. ACK가 오지 않거나 NAK가 오면 재전송함. Go-Back-N은 오류 이후 프레임을 묶어 재전송하고, Selective Repeat는 손실 프레임만 다시 보냄.
- **비유**: 선생님이 1~10번 시험지를 나눠주고 학생이 4번을 못 받았다고 말하면, Go-Back-N은 4~10번을 다시 주고 SR은 4번만 다시 줌.
- **구체 예시**: 윈도우 크기 4에서 3번 프레임 손실 시 Go-Back-N은 3,4,5,6 재전송 가능, SR은 3번만 재전송함.
- **흔한 오해·주의점**: ARQ는 오류 검출 자체가 아니라 검출 후 회복 방식임. CRC, checksum은 검출이고 ARQ는 재전송 제어임.

## 연결 개념
- Sliding Window: 여러 프레임을 연속 전송하는 기반
- TCP 재전송: ACK, timeout, selective acknowledgment와 연결
- FEC: 재전송 없이 중복 정보로 복구하는 대안

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: ARQ는 방식 명칭보다 윈도우, 순서번호, 재전송 범위, 버퍼 요구량, 링크 특성별 선택 기준을 제시해야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: ARQ (Automatic Repeat reQuest)는 오류 검출 후 ACK/NAK·timeout·순서번호로 손실 프레임을 재전송하는 오류 제어 방식이다.
> 2. **가치**: Stop-and-Wait, Go-Back-N, Selective Repeat는 처리량과 버퍼 비용을 서로 다르게 배분한다.
> 3. **판단 포인트**: RTT, BER, 윈도우 크기, 수신 버퍼, 순서번호 공간을 기준으로 방식을 선택해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 오류 제어 원리 확인 | ACK/NAK, timeout, 순서번호, 재전송 | CRC와 ARQ를 같은 기능으로 설명 |
| 방식별 차이 이해 확인 | Stop-and-Wait, Go-Back-N, Selective Repeat 비교 | Go-Back-N과 SR 재전송 범위 혼동 |
| 링크 특성별 선택 역량 확인 | RTT, BER, 윈도우 크기, 버퍼 요구량 | 고손실 무선에서 Go-Back-N만 권장 |

> 요약: ARQ 문제는 오류 검출 이후 어떤 프레임을 언제 다시 보낼지 결정하는 제어 문제임.

---

## Ⅰ. 개요 및 필요성

ARQ는 오류 프레임을 자동 재전송하는 오류 제어 기법이다. 링크 계층과 전송 계층은 CRC·checksum으로 오류를 감지하고, ACK/NAK·timeout으로 손실을 복구한다. RTT가 크거나 오류율이 높은 환경에서는 재전송 범위와 버퍼 요구량이 처리량을 좌우한다.

---

## Ⅱ. 구조 및 구성요소

```text
Sender Window -> Frame Seq No -> Receiver Check -> ACK/NAK
          / Timer
          / Retransmission Buffer
          / Receiver Reorder Buffer
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| 순서번호 | 프레임 중복·순서 식별 | SR은 순서번호 공간 2W 이상 필요 |
| ACK/NAK | 정상 수신 또는 오류 통지 | 누적 ACK 또는 개별 ACK |
| Timer | ACK 미수신 시 timeout 발생 | RTT 추정과 RTO 설정 필요 |
| 송수신 버퍼 | 재전송·재정렬 프레임 보관 | SR은 수신 버퍼 요구량 증가 |

> 요약: ARQ는 순서번호, 확인응답, 타이머, 버퍼를 조합해 오류 프레임의 재전송 범위를 통제함.

---

## Ⅲ. 동작원리 및 흐름도

```text
Frame 송신 -> CRC/Checksum 확인 -> ACK 수신
-> 정상: window 이동
-> 오류/timeout: 방식별 재전송 -> 순서 복구
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 송신자가 순서번호와 CRC 포함 프레임 전송 | seq no wrap 확인 |
| 2 | 수신자가 오류 검출 후 ACK/NAK 생성 | CRC error count |
| 3 | 송신자가 timeout 또는 NAK 확인 | RTO, duplicate ACK |
| 4 | Go-Back-N 또는 SR 규칙으로 재전송 | retransmission count |
| 5 | 수신자가 순서 정렬 후 상위 계층 전달 | out-of-order buffer |

> 요약: ARQ 흐름은 오류 검출, 확인응답, timeout 판단, 방식별 재전송, 순서 복구 순서로 진행됨.

---

## Ⅳ. 특징

| 구분 | Go-Back-N | Selective Repeat | 수치·표준 포인트 |
|:---|:---|:---|:---|
| 재전송 범위 | 오류 프레임 이후 모두 | 오류 프레임만 | SR 재전송량 최소 |
| 수신 버퍼 | 순서 밖 프레임 폐기 가능 | 순서 밖 프레임 저장 | SR 버퍼 W개 필요 |
| 순서번호 | W+1 이상 | 2W 이상 | 모호성 방지 |
| 적용 조건 | 낮은 BER, 구현 단순 | 높은 BER, 긴 RTT | 위성·무선 링크 |

> 요약: Go-Back-N은 구현 비용을 줄이고, SR은 버퍼와 순서번호 비용을 사용해 재전송량을 줄임.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | ARQ 방식 | 선택 기준 |
|:---|:---|:---|:---|
| 짧은 RTT | Stop-and-Wait 가능 | 단순 구현 | RTT 1ms 이하, 낮은 처리량 |
| 긴 RTT | Go-Back-N/SR | window 기반 연속 전송 | bandwidth-delay product 반영 |
| 높은 BER | FEC 병행 | SR 또는 Hybrid ARQ | 재전송 지연 허용 여부 |

> 요약: 링크 RTT와 오류율이 커질수록 Stop-and-Wait에서 SR·Hybrid ARQ로 전환해야 함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 재전송 폭증 | BER 상승, timeout 오판 | RTO 튜닝, SR 적용 | retransmission ratio |
| 순서번호 모호성 | 번호 공간 부족 | SR은 sequence space 2W 이상 | duplicate accept count |
| 버퍼 고갈 | out-of-order 프레임 누적 | receive window 제한, drop policy | reorder buffer usage |

> 요약: ARQ 리스크는 재전송량, 순서번호 모호성, 버퍼 고갈이며 윈도우와 RTO로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 재전송률 | 전체 프레임의 1~3% 이하 | link counter |
| RTO 정확도 | spurious timeout 0.5% 이하 | ACK trace |
| 처리량 | BDP 대비 window utilization 80% 이상 | throughput test |

> 요약: ARQ 효과는 재전송률, timeout 오판, 윈도우 활용률로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수):**
1. 저오류 유선 링크: Go-Back-N 또는 TCP 누적 ACK 구조로 구현 복잡도와 버퍼 사용량 절감
2. 고손실 무선 링크: SR 또는 SACK 적용, 수신 버퍼 W개와 순서번호 2W 이상 확보
3. 장거리 링크: BDP 기반 window size 산정, RTO는 RTT 평균·분산 기반으로 동적 계산

**결론 (2줄):**
- 기술사 판단: RTT·BER이 낮으면 Go-Back-N, 손실률과 지연이 크면 SR 또는 FEC 병행을 선택함
- 향후 방향: 5G·위성·QUIC 환경에서는 ARQ와 FEC를 결합한 지연 예산 기반 오류 제어가 확대됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "ARQ 오류 제어를 설명하시오" | ACK/NAK, timeout, 재전송 흐름 | Stop-and-Wait, GBN, SR 차이 |
| 요구사항 명시형 | "Go-Back-N과 SR을 비교하시오" | 손실 시 재전송 절차 | 버퍼·순서번호·링크 조건 선택 기준 |

> 요약: 설명형은 원리 중심, 비교형은 재전송 범위와 버퍼 요구량 중심으로 답안을 전환함.
