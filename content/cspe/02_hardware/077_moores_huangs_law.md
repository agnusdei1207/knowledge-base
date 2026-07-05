---
title: 무어의 법칙 및 황의 법칙 (Moores Law and Huangs Law)
date: 2026-07-05
tags: [cspe-hardware]
weight: 77
---

## Ⅰ. 개요
- 정의: 반도체 집적도와 연산 성능의 지수적 성장을 설명하는 경험 법칙
- 배경: 물리적 미세화 한계(Moore)와 AI 특화 가속기(Huang) 중심의 패러다임 전환
- 출제 의도: 하드웨어 진화의 역사적 흐름 및 AI 시대의 새로운 성능 지표 이해

## Ⅱ. 구성요소
- ASCII 구조도
  [ Moore's Law ]       [ Huang's Law ]
  - Target: Transistors - Target: AI Performance
  - Scale: Density     - Scale: Architecture + SW
  - Period: 18~24 mon  - Period: < 12 mon (doubling)

- 구성요소 표
| 구성요소 | 설명 | 비유 |
| :--- | :--- | :--- |
| Moore's Law | 반도체 집적도가 2년마다 2배 증가한다는 법칙 | 도시 인구 밀집도 |
| Huang's Law | AI 추론 성능이 매년 2배 이상 향상된다는 법칙 | 배달 처리 속도 |
| Dennard Scaling | 크기가 줄면 전력 밀도가 유지된다는 법칙 (붕괴됨) | 소형화의 마법 |

- > 요약: 무어는 물리적 집적을, 황은 아키텍처와 소프트웨어의 최적화 강조

## Ⅲ. 절차
- ASCII 흐름도
  [Node Scaling] -> [Density Up] -> [Architecture Opt] -> [Perf Doubling]

1. 미세 공정 적용: 선폭 축소를 통한 동일 면적 내 소자 수 증대(Moore)
2. 도메인 특화: 범용 CPU 대신 병렬 처리에 최적화된 GPU/NPU 설계
3. 스택 최적화: 하드웨어 가속기와 라이브러리(CUDA 등)의 밀결합
4. 성능 실측: AI 모델(LLM 등) 학습/추론 속도를 통한 가속 증명(Huang)

- > 요약: 물리적 한계를 구조적 혁신과 소프트웨어 기술로 보완하며 성장

## Ⅳ. 문제점
- 물리적 한계: 원자 단위 미세화 시 발생하는 터널링 및 발열 문제 (Post-Moore)
- 경제성 저하: 공정 전환 비용이 기하급수적으로 상승하여 무어의 법칙 비용 효율 하락

## Ⅴ. 개선방안
- More than Moore: 칩렛, 3D 적층 등 패키징 기술을 통한 집적도 향상
- 알고리즘 혁신: 저정밀도 연산(FP8, INT4) 도입을 통한 실질 연산량 극대화

## Ⅵ. 전망
- 로드맵: AI 네이티브 하드웨어로의 전격 전환 및 전력 효율(Perf/Watt) 경쟁 가속
- CSF: 단순 공정 미세화를 넘어선 풀스택(칩-시스템-SW) 최적화 역량 확보
