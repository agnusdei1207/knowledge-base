---
title: "디스크 접근시간 (Disk Access Time)"
date: "2026-06-30"
weight: 67
tags:
  - "exam-cspe-operating-system"
---

## Ⅰ. 정의
> 하드디스크(HDD)에서 특정 데이터에 접근하는 데 소요되는 총 시간으로, 탐색시간(Seek Time)·회전지연(Rotational Latency)·전송시간(Transfer Time)의 합으로 정의된다.

## Ⅱ. 구성요소 / 원리
- 탐색시간(Seek Time): 디스크 헤드(Head)를 목표 트랙(Track)으로 이동시키는 시간, 전체 지연의 최대 비중
- 회전지연(Rotational Latency): 목표 섹터(Sector)가 헤드 밑으로 회전해 올 때까지의 시간, 평균 1/2 회전
- 전송시간(Transfer Time): 데이터를 실제로 읽고/쓰는 시간, 데이터량 ÷ 전송률
- 평균 회전지연 = (60 / RPM) × 1000 / 2 [ms], 회전수(RPM, Revolutions Per Minute) 기준

## Ⅲ. 흐름도 / 구조
```text
요청 → [탐색: 헤드 이동] → [회전지연: 섹터 회전 대기]
         (Seek Time)         (Rotational Latency)
   → [전송: 데이터 read/write] → 완료
        (Transfer Time)
  접근시간 = Seek + Rotational + Transfer
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 디스크 I/O 성능을 정량화하여 스케줄링·설계 기준 제공 |
| 장점 | 병목 요소(Seek 비중) 식별, 성능 예측·최적화 가능 |
| 한계 | 기계적 이동에 의존해 SSD 대비 지연 큼, 부하 변동에 민감 |

## Ⅴ. 기술사적 적용
- 탐색시간 최소화를 위한 디스크 스케줄링(SSTF, SCAN 등) 적용 근거
- 회전지연 감소를 위한 고RPM 디스크·섹터 인터리빙(Interleaving) 설계
- 기계적 지연이 없는 SSD 도입으로 접근시간 구조 자체를 개선
