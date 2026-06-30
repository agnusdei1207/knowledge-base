---
title: "HDD·SSD (Hard Disk Drive / Solid State Drive)"
date: "2026-06-30"
weight: 74
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> HDD(Hard Disk Drive)는 회전 자기 디스크에 헤드 이동으로 데이터를 읽고 쓰는 기계식 저장장치이며, SSD(Solid State Drive)는 NAND 플래시 기반 비휘발성 반도체 저장장치이다.

## Ⅱ. 구성요소 / 원리
- HDD 접근시간 = 탐색시간(Seek) + 회전지연(Latency) + 전송시간
- HDD: 플래터·헤드·스핀들(RPM), 기계적 지연 존재
- SSD: NAND 셀, FTL(Flash Translation Layer), 컨트롤러, DRAM 캐시
- SSD 특성: Erase-before-Write, 웨어레벨링(Wear Leveling), 가비지컬렉션(GC)
- FTL: 논리주소(LBA)↔물리주소 매핑, 마모 분산·블록 관리

## Ⅲ. 흐름도 / 구조
```text
HDD: [요청] -> Seek(헤드이동) -> Latency(회전) -> 전송
SSD: [요청] -> FTL(LBA→PBA) -> NAND R/W -> 컨트롤러
       └ Wear Leveling / GC / TRIM 백그라운드
```

## Ⅳ. 핵심 특징
| 구분 | HDD | SSD |
|:---|:---|:---|
| 원리 | 자기·기계식 | NAND 반도체 |
| 지연 | 탐색·회전지연(ms) | 마이크로초(μs) |
| 장점 | 대용량·저비용/GB | 고속·저전력·내충격 |
| 한계 | 충격 약함·소음 | 쓰기수명(P/E), 가격 |

## Ⅴ. 기술사적 적용
- 콜드데이터는 HDD, 핫데이터는 SSD로 계층 스토리지(Tiering)
- SSD는 NVMe·인터페이스 진화로 SATA 한계 극복
- QLC/TLC 셀, TRIM·오버프로비저닝으로 수명·성능 최적화
