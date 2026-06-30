---
title: "SIMD (Single Instruction Multiple Data, AVX·NEON)"
date: "2026-06-30"
weight: 23
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> 하나의 명령어로 다수의 데이터를 동시에 병렬 연산하는 데이터 병렬 처리 방식으로, 인텔 AVX(Advanced Vector Extensions)와 ARM NEON이 대표적 벡터 확장이다.

## Ⅱ. 구성요소 / 원리
- 넓은 벡터 레지스터에 여러 데이터 패킹 후 동일 연산 일괄 수행
- AVX/AVX2/AVX-512: 256~512비트 벡터(x86)
- NEON: 128비트 벡터(ARM), 모바일·미디어 처리
- 플린(Flynn) 분류상 SIMD에 해당 (SISD/SIMD/MISD/MIMD)
- 컴파일러 자동 벡터화 또는 인트린식(Intrinsic)으로 활용

## Ⅲ. 흐름도 / 구조
```text
 1개 명령 ─▶ ┌ a0 a1 a2 a3 ┐
            │  +  +  +  +  │  ← 동시 연산
            └ b0 b1 b2 b3 ┘
        결과 c0 c1 c2 c3 (한 사이클 병렬)
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 멀티미디어·과학연산·AI의 데이터 병렬 가속 |
| 장점 | 처리량↑, 전력효율↑, 명령 인출 오버헤드 감소 |
| 한계 | 데이터 정렬·종속성 제약, 분기 많은 코드엔 부적합 |

## Ⅴ. 기술사적 적용
- 영상·신호처리, 행렬연산, 딥러닝 추론 가속에 활용
- GPU(SIMT), TPU/NPU 등 대규모 데이터 병렬 가속기로 확장
- AVX-512·SVE(Scalable Vector Extension) 등 가변 벡터로 진화
