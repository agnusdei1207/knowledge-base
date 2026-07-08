---
title: "DDR SDRAM·갱신 방식 (DDR SDRAM Refresh)"
date: "2026-07-08"
tags:
  - "cspe-hardware"
weight: 29
extra:
  question_no: "029"
  exam_status: "기출"
  exam_history: "129회"
---

## 미리 알고가기

- DDR은 클록의 상승과 하강 에지 모두에서 데이터를 전송하는 방식임
- SDRAM은 클록에 동기화되어 동작하는 DRAM이며 bank 구조와 row buffer를 가짐
- refresh는 커패시터 전하 누설로 인한 데이터 손실을 막기 위해 필수임

## Ⅰ. 개요

- **정의/개념**: DDR SDRAM은 동기식 DRAM에 double data rate 전송 방식을 적용해 같은 기본 클록에서 더 높은 대역폭을 내는 메모리이고, refresh는 저장 전하를 주기적으로 복원해 데이터 무결성을 유지하는 제어 메커니즘임
- **배경/필요성**: CPU와 가속기의 처리량이 커질수록 메모리 대역폭 요구도 급증하지만 DRAM 셀은 누설 특성을 피할 수 없으므로, 고속 전송과 데이터 보존을 동시에 만족하는 정교한 제어가 필요함

## Ⅱ. 특징

- 양 에지 전송과 prefetch 구조로 기본 클록 대비 높은 실효 대역폭을 제공함
- bank와 row buffer를 활용해 병렬성을 키우지만 접근 패턴에 따라 충돌 지연이 생길 수 있음
- refresh는 필수라서 용량과 온도가 높아질수록 성능 손실과 전력 부담이 증가함
- 성능 최적화는 순수 전송률보다 refresh 스케줄과 bank 활용 효율에 크게 좌우됨

## Ⅲ. 종류 및 비교

| 판단 기준 | Auto Refresh | Per-Bank Refresh | Self Refresh |
|:---|:---|:---|:---|
| 동작 방식 | 컨트롤러가 전체 칩 기준으로 주기적 갱신 명령을 보냄 | 특정 bank만 선택적으로 갱신해 나머지 bank 접근을 유지함 | 저전력 상태에서 DRAM 내부 로직이 스스로 갱신함 |
| 강점 | 구현이 단순하고 표준 호환성이 높음 | 성능 손실을 분산해 병렬성을 높임 | 대기 전력을 크게 줄일 수 있음 |
| 한계 | refresh 동안 접근 차단이 커짐 | 제어 로직이 복잡해짐 | 모드 전환 지연과 성능 제한이 있음 |
| 적합 환경 | 일반 서버와 표준 메모리 경로 | 고성능 서버와 대역폭 민감 워크로드 | 모바일과 절전 중심 장치 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| DDR Channel and Clock | 명령과 데이터 전송을 동기화하며 양 에지에서 데이터를 주고받아 대역폭을 높임 |
| Bank and Row Buffer | 여러 bank를 병렬 운용하고 열린 row를 재사용해 access locality를 활용함 |
| Memory Controller | 읽기·쓰기와 refresh 명령을 함께 스케줄링해 충돌과 공백 시간을 조정함 |
| Refresh Scheduler | 모든 row가 보존 시간 내에 갱신되도록 타이밍과 대상 bank를 결정함 |

```text
+----------------+     +------------------+     +------------------+
| Memory Request | --> | Memory Controller| --> | Bank / Row Buffer|
+----------------+     +------------------+     +------------------+
                                |
                                v
                        +------------------+
                        | Refresh Scheduler|
                        +------------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+     +-------------+
| 접근 요청 수신  | --> | bank 상태 확인   | --> | read/write 또는 refresh | --> | 데이터 전송      | --> | 다음 주기 예약   |
+-------------+     +-------------+     +-------------+     +-------------+     +-------------+
```

1. **접근 요청 수신**: 컨트롤러가 CPU나 DMA의 메모리 요청을 받음
2. **bank 상태 확인**: 대상 row와 bank 점유 상태를 판단함
3. **read/write 또는 refresh 수행**: 우선순위와 타이밍 규칙에 맞게 명령을 배치함
4. **데이터 전송**: DDR 방식으로 양 에지에서 데이터를 송수신함
5. **다음 주기 예약**: 다음 refresh 시점과 bank 사용 순서를 다시 계산함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 메모리 용량이 커질수록 refresh에 소모되는 시간이 늘어나 실제 접근 가능한 대역폭이 감소함
   - 해결방안: per-bank refresh와 fine granularity refresh를 적용하고 refresh penalty와 effective bandwidth로 검증함
2. 문제: 특정 row를 반복 활성화하면 인접 셀 간섭으로 RowHammer 위험이 커질 수 있음
   - 해결방안: TRR과 ECC와 access throttling을 적용하고 row activation rate와 corrected error count로 검증함
3. 문제: 온도 상승은 전하 누설을 빠르게 만들어 보존 주기와 전력 비용을 동시에 악화시킴
   - 해결방안: temperature-compensated self refresh와 열 제어를 연동하고 refresh power와 thermal margin으로 검증함

## Ⅶ. 적용 사례

- DDR5 서버 메모리는 per-bank refresh를 활용해 대역폭 손실을 줄이고 확인 지표는 effective bandwidth와 refresh penalty임
- LPDDR 모바일 기기는 self refresh와 partial array 제어를 사용해 대기 전력을 낮추고 확인 지표는 standby power와 resume latency임
- 데이터센터 운영은 메모리 온도와 refresh 정책을 함께 관리해 안정성을 유지하고 확인 지표는 thermal margin과 corrected error count임

## Ⅷ. 결론

DDR SDRAM의 경쟁력은 전송률 숫자보다도 refresh라는 물리 제약을 얼마나 영리하게 숨기면서 유효 대역폭을 지켜내는지에 달려 있음.
