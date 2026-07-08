---
title: "RAID 레벨 0·1·5·6·10 비교 (RAID Levels)"
date: "2026-07-08"
tags:
  - "cspe-hardware"
weight: 40
extra:
  question_no: "040"
  exam_status: "기출"
  exam_history: "125회, 131회, 136회"
---

## 미리 알고가기

- RAID는 여러 물리 디스크를 하나의 논리 볼륨처럼 묶는 구성 기술임
- 성능을 위한 striping과 안정성을 위한 mirroring과 parity가 핵심 조합 요소임
- 최적 레벨은 성능만이 아니라 rebuild 위험과 용량 효율과 장애 허용 범위를 함께 봐야 함

## Ⅰ. 개요

- **정의/개념**: RAID는 여러 디스크를 striping과 mirroring과 parity 방식으로 조합해 성능과 가용성과 용량 효율을 요구사항에 맞게 조절하는 저장장치 중복 구성 기술임
- **배경/필요성**: 단일 디스크는 장애 시 데이터 손실 위험이 크고 처리량 확장도 제한되므로, 기업 시스템은 여러 디스크를 묶어 성능과 복원력을 동시에 확보해야 함

## Ⅱ. 특징

- 같은 디스크 수라도 어떤 중복 기법을 쓰느냐에 따라 성능과 용량과 복원력이 크게 달라짐
- parity 기반 RAID는 용량 효율이 좋지만 쓰기 penalty와 rebuild 부담이 큼
- mirror 기반 RAID는 복원 단순성과 읽기 성능이 좋지만 용량 효율이 낮음
- 대용량 디스크 시대에는 정상 운용 성능보다 rebuild 구간의 위험 통제가 더 중요해짐

## Ⅲ. 종류 및 비교

| 판단 기준 | RAID 0 | RAID 1 | RAID 5 | RAID 6 | RAID 10 |
|:---|:---|:---|:---|:---|:---|
| 핵심 방식 | striping만 수행함 | mirroring만 수행함 | 분산 parity 1개를 사용함 | 분산 parity 2개를 사용함 | mirrored pair 위에 striping함 |
| 장점 | 최고 성능과 전체 용량 활용이 가능함 | 단순하고 복구가 쉬움 | 용량 효율과 읽기 성능 균형이 좋음 | 이중 장애 허용으로 안정성이 높음 | 성능과 복원력을 함께 확보하기 좋음 |
| 한계 | 장애 허용이 전혀 없음 | 용량 효율이 50% 수준임 | write penalty와 rebuild 위험이 큼 | parity 계산과 rebuild 시간이 더 큼 | 디스크 수와 비용 부담이 큼 |
| 적합 환경 | 임시 데이터와 scratch 공간 | OS 볼륨과 소규모 중요 데이터 | 파일 서버와 읽기 비중이 큰 저장소 | 대용량 아카이브와 백업 저장소 | DB와 가상화처럼 성능과 안정성이 모두 중요한 환경 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| RAID Controller | 논리 볼륨 생성과 striping과 parity 계산과 장애 감지를 수행하는 제어 중심임 |
| Member Disks | 실제 데이터와 미러와 parity를 저장하며 전체 배열의 성능과 장애 특성을 결정함 |
| Cache and Journal or BBU | write hole을 줄이고 쓰기 성능을 보완하며 전원 장애 시 미완료 쓰기를 보호함 |
| Hot Spare and Rebuild Logic | 장애 디스크를 대체하고 자동 복구를 수행해 가용성 유지 시간을 줄임 |

```text
+-------------+     +------------------+     +------------------------------+
| Host I/O    | --> | RAID Controller  | --> | Disk Members / Parity / Mirror|
+-------------+     +------------------+     +------------------------------+
                                 |
                                 v
                         +------------------+
                         | Spare / Rebuild  |
                         +------------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+     +-------------+
| I/O 요청 수신   | --> | striping 또는 mirror 배치 | --> | parity 계산 여부  | --> | 디스크 기록 수행  | --> | 장애 시 rebuild  |
+-------------+     +-------------+     +-------------+     +-------------+     +-------------+
```

1. **I/O 요청 수신**: 호스트가 읽기나 쓰기를 요청함
2. **striping 또는 mirror 배치**: 선택한 RAID 레벨에 맞춰 데이터 위치를 정함
3. **parity 계산 여부 판단**: RAID 5와 6은 parity를 생성하거나 갱신함
4. **디스크 기록 수행**: 멤버 디스크에 데이터와 parity 또는 mirror를 씀
5. **장애 시 rebuild 수행**: 고장 디스크를 spare로 교체하고 남은 정보로 복구함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 대용량 디스크에서는 RAID 5와 6의 rebuild 시간이 길어져 복구 중 추가 오류 위험이 커짐
   - 해결방안: hot spare와 proactive replacement를 적용하고 rebuild time과 unrecoverable read error exposure로 검증함
2. 문제: parity 기반 RAID는 작은 랜덤 쓰기에서 read-modify-write가 반복되어 write latency가 커질 수 있음
   - 해결방안: RAID 10 선택이나 write-back cache 최적화를 적용하고 write latency와 parity write penalty로 검증함
3. 문제: 전원 장애 중 쓰기 중단은 data와 parity 불일치인 write hole을 유발할 수 있음
   - 해결방안: journal 또는 BBU와 PLP를 적용하고 write hole incident count와 recovery consistency로 검증함

## Ⅶ. 적용 사례

- 데이터베이스 서버는 RAID 10으로 낮은 write latency와 복원력을 동시에 확보하고, transaction latency와 rebuild time로 결과를 확인함
- 기업 파일 서버는 RAID 6으로 용량 효율과 이중 장애 허용을 확보하고, usable capacity ratio와 unrecoverable read error exposure로 결과를 확인함
- 가상화 스토리지는 SSD 기반 RAID와 write-back cache를 조합해 다중 VM 부하를 수용하고, aggregate IOPS와 p99 latency로 결과를 확인함

## Ⅷ. 결론

RAID 선택의 핵심은 평상시 성능 수치보다 장애와 rebuild 구간까지 포함한 총 위험 비용을 어떤 수준으로 수용할지 결정하는 데 있음.
