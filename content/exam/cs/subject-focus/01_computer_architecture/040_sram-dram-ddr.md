---
title: "SRAM·DRAM·DDR (Static/Dynamic RAM, Double Data Rate)"
date: "2026-06-30"
weight: 40
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> SRAM(Static RAM)은 플립플롭 기반 고속 휘발성 메모리, DRAM(Dynamic RAM)은 커패시터 기반 대용량 휘발성 메모리, DDR(Double Data Rate)은 클럭 양 에지에서 전송하는 DRAM 인터페이스 규격.

## Ⅱ. 구성요소 / 원리
- SRAM: 셀당 6트랜지스터(6T), 리프레시 불필요, 고속·고가 → 캐시용
- DRAM: 셀당 1T1C(트랜지스터+커패시터), 전하 누설로 주기적 리프레시 필요 → 주기억용
- DDR: 클럭 상승·하강 에지 모두 사용해 1클럭당 2전송(SDR 대비 2배)
- 세대: DDR2/3/4/5로 프리패치 폭·대역폭 증가, 전압 강하

## Ⅲ. 흐름도 / 구조
```text
SRAM(6T)  : 빠름·소용량·비휘발 아님 → L1/L2/L3 Cache
DRAM(1T1C): 느림·대용량 + Refresh → Main Memory
DDR clock : ─┐_┌─┐_┌─  ↑하강↑상승 모두 전송 = 2배 대역폭
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 속도(SRAM)·용량(DRAM)·대역폭(DDR) 요구 분담 |
| 장점 | SRAM 무리프레시 고속, DRAM 고집적 저가, DDR 대역폭 2배 |
| 한계 | SRAM 고가·저집적, DRAM 리프레시 전력·지연, DDR 신호 무결성 |

## Ⅴ. 기술사적 적용
- 비교: 캐시=SRAM, 메인메모리=DDR DRAM 역할 분담
- 실무: LPDDR(모바일 저전력), GDDR(그래픽), HBM(적층 광대역)
- 최신: DDR5 on-die ECC, CXL 메모리 확장, PIM(Processing-In-Memory)
