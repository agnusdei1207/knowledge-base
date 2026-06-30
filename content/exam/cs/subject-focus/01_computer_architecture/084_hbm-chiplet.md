---
title: "HBM·칩렛 (High Bandwidth Memory / Chiplet)"
date: "2026-06-30"
weight: 84
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> HBM(High Bandwidth Memory)은 DRAM 다이를 TSV로 수직 적층해 초고대역폭을 제공하는 메모리이며, 칩렛(Chiplet)은 큰 단일 칩 대신 여러 소형 다이를 패키지에 통합하는 모듈형 설계 기법이다.

## Ⅱ. 구성요소 / 원리
- HBM: DRAM 적층 + TSV(Through-Silicon Via) + 인터포저로 GPU 근접 배치
- 광폭 버스(1024비트 이상)로 GDDR 대비 대역폭·전력효율 우수
- 칩렛: 기능별 다이 분할, 인터포저/실리콘 브리지로 연결
- 패키징: 2.5D(인터포저), 3D 적층, UCIe 다이간 표준 인터페이스

## Ⅲ. 흐름도 / 구조
```text
HBM:  [DRAM die]┐
      [DRAM die]┤ TSV 수직적층
      [Logic   ]┘─인터포저─[GPU/가속기]
칩렛: [CPU die][IO die][GPU die] ─ 인터포저/UCIe 통합
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 대역폭 확보(HBM) / 수율·확장성(칩렛) |
| 장점 | 초고대역폭·저전력, 모듈화·수율 향상·비용 절감 |
| 한계 | 고가, 발열·패키징 복잡, 다이간 지연 |

## Ⅴ. 기술사적 적용
- AI 가속기·GPU의 메모리월 완화 핵심
- 칩렛+HBM으로 거대 SoC를 모듈 조합 구현
- UCIe 표준으로 이종 다이(Heterogeneous) 통합 가속
