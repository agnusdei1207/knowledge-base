---
title: "RAID (Redundant Array of Independent Disks)"
date: "2026-06-30"
weight: 75
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> RAID(Redundant Array of Independent Disks)는 다수의 디스크를 묶어 스트라이핑·미러링·패리티 기법으로 성능과 가용성을 동시에 확보하는 저장 구성 기술이다.

## Ⅱ. 구성요소 / 원리
- 스트라이핑(Striping): 데이터 분산 저장으로 병렬 I/O 성능 향상
- 미러링(Mirroring): 동일 데이터 복제로 가용성 확보
- 패리티(Parity): XOR 연산 기반 오류 복구 정보
- 구현: 하드웨어 RAID(컨트롤러), 소프트웨어 RAID(OS/mdadm)

## Ⅲ. 흐름도 / 구조
```text
RAID 5: [D1][D2][D3][P]   (패리티 분산)
   write -> 데이터 분산 + 패리티(XOR) 갱신
   fail  -> 패리티+생존디스크로 재구성(Rebuild)
RAID 10: (mirror)+(stripe) 결합
```

## Ⅳ. 핵심 특징
| 레벨 | 방식 | 최소 디스크 | 내결함성 | 특징 |
|:---|:---|:---|:---|:---|
| 0 | 스트라이핑 | 2 | 없음 | 최고 성능, 용량 100% |
| 1 | 미러링 | 2 | 1개 | 안정성↑, 용량 50% |
| 5 | 분산 패리티 | 3 | 1개 | 성능·용량·안정 균형 |
| 6 | 이중 패리티 | 4 | 2개 | 대용량 안정성↑ |
| 10 | 1+0 결합 | 4 | 그룹당 1 | 고성능+고가용 |

## Ⅴ. 기술사적 적용
- 대용량 NL-SAS 환경은 재구성 시간 문제로 RAID 6 권장
- SSD 어레이는 RAID 5/10, 분산 스토리지는 Erasure Coding으로 대체
- 핫스페어·스크러빙으로 무중단 복구 및 무결성 보장
