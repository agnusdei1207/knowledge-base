---
title: "4-bit Quantization"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 78
---

# 📖 【암기용】 개념 완전 이해

> 목적: 4-bit Quantization을 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **개요**: 모델 가중치를 4-bit 수준으로 표현해 LLM 메모리 사용량을 크게 줄이는 양자화 기법
- **왜 필요한가**: 7B~70B LLM은 FP16 가중치가 수십GB~수백GB라 단일 GPU·PC·엣지 배포가 어렵다.
- **핵심 직관**: 모델의 숫자를 16단계 눈금으로 압축해 메모리를 줄이고, 중요한 값은 보정 기법으로 보존하는 방식임.

## 깊이 이해
- **배경·문제의식**: LLM 서빙은 weight와 KV Cache가 GPU 메모리를 차지함. 4-bit weight-only quantization은 가중치 메모리를 FP16 대비 약 75% 줄여 큰 모델을 작은 장치에 올림.
- **작동 원리**: 그룹 단위로 scale을 계산하고 4-bit 코드로 weight를 저장함. 추론 시 dequantization 후 matmul을 수행하거나 4-bit 전용 kernel을 사용함.
- **비유**: 큰 지도를 접어 휴대용 지도로 만들되, 주요 도로와 랜드마크는 잘 보이게 남기는 것과 같음.
- **구체 예시**: 13B FP16 모델은 약 26GB가 필요하지만 4-bit 적용 시 약 7~10GB 수준으로 단일 GPU 배포 가능성이 생김.
- **흔한 오해·주의점**: activation까지 무리하게 4-bit로 낮추면 정확도 하락이 커질 수 있음. LLM은 weight-only 4-bit가 실무 적용이 많음.

## 연결 개념
- GPTQ — Hessian 기반 4-bit 양자화
- AWQ — activation-aware weight quantization
- QLoRA — 4-bit 기반 파라미터 효율 튜닝

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 4-bit Quantization은 LLM 가중치를 4-bit로 저장해 GPU 메모리와 대역폭을 줄이는 압축 기법임.
> 2. **가치**: 7B~70B 모델을 더 적은 GPU 메모리로 서빙·튜닝 가능하게 함.
> 3. **판단 포인트**: group size, scale, weight-only 여부, kernel 지원, perplexity·업무 정확도 회귀를 검증해야 함.

## Ⅰ. 개요 및 필요성

4-bit Quantization은 LLM 가중치 초저비트 압축 기법임. 대형 모델의 GPU 메모리 병목을 완화해 단일 GPU, AI PC, 저비용 서빙 환경에서 모델 실행 가능성을 높임.

## Ⅱ. 구조 및 구성요소

```text
FP16 Weights → Grouping → Scale 계산 → 4-bit 저장
      → Dequant/4-bit Kernel → LLM Inference → Evaluation
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Group-wise Scale | weight 그룹별 범위 보정 | group size 32~128 |
| 4-bit Code | 16단계 값 저장 | NF4/INT4 등 |
| Dequantization | 연산 전 실수 복원 | kernel 효율 중요 |
| Evaluation | 품질 회귀 측정 | perplexity, MMLU |

> 요약: 4-bit 양자화는 그룹별 scale로 오차를 보정하면서 weight 저장 비용을 FP16 대비 약 25% 수준으로 낮춤.

## Ⅲ. 동작원리 및 흐름도

```text
모델 로드 → weight 그룹화 → 4-bit 코드 변환
    → 추론 kernel 적용 → 정확도·메모리·지연 측정
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | layer별 weight 분포 분석 | outlier 비율 |
| 2 | group size와 scale 산정 | group 32/64/128 |
| 3 | 4-bit 변환·kernel 적용 | VRAM, tokens/s |
| 4 | 회귀 평가 | perplexity 증가, MMLU 하락 |

> 요약: 4-bit 적용은 그룹 단위 보정과 kernel 지원을 결합해 메모리 절감과 정확도 보존의 균형점을 찾음.

## Ⅳ. 특징

| 구분 | INT8 | 4-bit | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 메모리 | FP16 대비 약 50% | FP16 대비 약 25% | 13B: 26GB→7~10GB |
| 정확도 | 회귀 작음 | 회귀 위험 증가 | GPTQ/AWQ 보정 필요 |
| 적용 | 범용 | LLM weight 중심 | activation 주의 |
| 하드웨어 | 지원 넓음 | kernel 의존 큼 | vLLM/TensorRT 확인 |

> 요약: 4-bit는 LLM 메모리 절감 폭이 크지만, 정확도 회귀와 kernel 지원성 검증이 INT8보다 중요함.

## Ⅴ. 실무 적용 및 결론

**적용 방안 3개:**
1. 7B~13B 사내 SLM은 AWQ/GPTQ 4-bit로 변환하고 MMLU·사내 QA 하락 2%p 이내 기준 검증
2. 장문 LLM 서빙은 weight 4-bit와 KV cache INT8을 분리 적용해 VRAM과 TPOT를 동시에 측정
3. 중요 업무는 layer별 mixed precision을 적용해 outlier layer는 FP16/INT8로 유지

**결론 (2줄):**
- 기술사 판단: VRAM 병목이 크고 정확도 허용폭 1~3%p가 있으면 4-bit, 정확도 민감 업무는 INT8/FP16을 선택함.
- 향후 방향: 4-bit는 SLM, QLoRA, 개인 장치 LLM 실행의 핵심 최적화로 확산됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | 설명하시오, 기술하시오 | group scale·kernel 적용 흐름 | INT8 대비 특징 |
| 요구사항 명시형 | 최적화 방안을 제시하시오 | AWQ/GPTQ·mixed precision 절차 | VRAM·정확도·kernel 기준 |

> 요약: 설명형은 4-bit 변환 원리, 최적화형은 LLM 메모리 병목과 정확도 회귀 기준으로 목차를 전환함.
