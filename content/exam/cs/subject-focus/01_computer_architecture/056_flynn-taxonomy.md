---
title: "플린의 분류법 (Flynn's Taxonomy: SISD·SIMD·MISD·MIMD)"
date: "2026-06-30"
weight: 56
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> 명령어 스트림(Instruction Stream)과 데이터 스트림(Data Stream)의 다중성(단일/다중)을 기준으로 컴퓨터 구조를 4가지로 분류한 병렬처리 분류 체계.

## Ⅱ. 구성요소 / 원리
- SISD(Single Instruction Single Data): 단일 명령·단일 데이터, 전통적 폰노이만 구조
- SIMD(Single Instruction Multiple Data): 하나의 명령으로 다수 데이터 동시 처리(벡터·GPU)
- MISD(Multiple Instruction Single Data): 다수 명령이 단일 데이터 처리(이론적·결함허용 파이프라인)
- MIMD(Multiple Instruction Multiple Data): 다수 명령·다수 데이터, 멀티코어·클러스터

## Ⅲ. 흐름도 / 구조
```text
            Instruction Stream
            Single        Multiple
Data  S  | SISD(CPU)  | MISD(희소)  |
Stream M | SIMD(GPU)  | MIMD(멀티코어)|
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 병렬성 유형을 명령/데이터 다중성으로 체계적 분류 |
| 장점 | 단순·직관적, 아키텍처 비교 기준 제공 |
| 한계 | 현대 혼합형(GPGPU·SIMT) 표현에 한계, MISD 실사례 희소 |

## Ⅴ. 기술사적 적용
- SIMD → 벡터 프로세서·GPU·AVX 명령어 확장의 이론적 기반
- MIMD → SMP·NUMA·클러스터 등 다중처리 시스템 분류 근거
- SIMT(NVIDIA)는 SIMD+MIMD 혼합으로 분류 한계 보완
