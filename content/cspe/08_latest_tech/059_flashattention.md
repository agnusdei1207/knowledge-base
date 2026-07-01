---
title: "FlashAttention"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 59
---

# 📖 【암기용】 개념 완전 이해

> 목적: FlashAttention을 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **개요**: Attention 행렬 전체를 HBM에 저장하지 않고 SRAM 타일 단위로 계산해 메모리 I/O를 줄이는 정확한 Attention 알고리즘
- **왜 필요한가**: Self-Attention은 N×N 점수 행렬을 만들어 긴 문맥에서 GPU 메모리 대역폭 병목이 발생함.
- **핵심 직관**: 큰 표를 통째로 복사하지 않고, 작은 창으로 나눠 읽고 계산한 뒤 필요한 결과만 저장하는 방식임.

## 깊이 이해
- **배경·문제의식**: 기존 Attention은 QKᵀ score와 Softmax 결과를 HBM에 저장했다가 다시 읽음. 긴 시퀀스에서는 연산보다 메모리 왕복이 병목임.
- **작동 원리**: Q·K·V를 block tile로 나누고, GPU SRAM에서 부분 Attention을 계산함. Online Softmax로 수치 안정성을 유지하면서 최종 출력만 HBM에 기록함.
- **비유**: 전체 엑셀 파일을 매번 저장하지 않고, 화면에 보이는 범위만 계산해 최종 합계만 기록하는 것과 같음.
- **구체 예시**: 4K~32K context 학습·추론에서 attention memory를 줄이고 throughput을 높이는 표준 커널로 사용됨.
- **흔한 오해·주의점**: FlashAttention은 근사 Attention이 아님. 같은 Attention 결과를 메모리 접근 패턴만 바꿔 계산함.

## 연결 개념
- Scaled Dot-Product Attention — FlashAttention이 최적화하는 대상
- Long Context LLM — 긴 문맥에서 효과가 커짐
- GPU Memory Hierarchy — HBM/SRAM 접근 비용 차이


# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: FlashAttention은 Attention을 타일 단위로 계산해 HBM read/write를 줄이는 IO-aware exact attention임.
> 2. **가치**: N×N attention matrix 저장을 회피해 긴 문맥 학습·추론의 메모리 병목을 완화함.
> 3. **판단 포인트**: 시퀀스 길이, GPU SRAM 크기, causal mask, 커널 지원 여부가 적용 기준임.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| Attention 메모리 병목 해결 이해 | HBM/SRAM 계층 구분, tiling·online softmax 원리, exact attention 유지 | 근사(approximate) Attention이 아님을 명시, GPU 아키텍처별 커널 의존성 언급 |

> 요약: FlashAttention은 정확한 Attention 결과를 유지하면서 HBM I/O를 SRAM tiling으로 줄이는 알고리즘이며, 근사가 아닌 exact임을 반드시 짚어야 함.

---

## Ⅰ. 개요 및 필요성

- 정의: Attention 행렬을 SRAM 타일 단위로 계산해 HBM I/O를 줄이는 IO-aware exact attention 알고리즘
- 배경: Transformer의 N×N score 행렬 저장·재로드가 HBM 대역폭 병목을 야기함
- 필요성: tiling과 online softmax로 중간 행렬 저장 없이 동일 결과를 산출, 장문맥 학습·추론 처리량 향상


## Ⅱ. 구조 및 구성요소

```text
Q/K/V Blocks -> SRAM Tile Compute -> Online Softmax -> Output Block
  -> HBM에는 최종 Output만 기록 (중간 N×N score 저장 회피)
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Tiling | Q/K/V를 block으로 분할 | SRAM 적재 가능 크기 |
| SRAM Compute | block 단위 Attention 계산 | HBM 왕복 감소 |
| Online Softmax | 전체 Softmax를 streaming 계산 | 수치 안정성 유지 |
| Fused Kernel | matmul·softmax·dropout 결합 | kernel launch 감소 |

> 요약: FlashAttention은 tiling과 fused kernel로 Attention 중간 행렬 저장을 피하고 최종 출력만 기록함.


## Ⅲ. 동작원리 및 흐름도

```text
Q/K/V 로드 -> 타일 분할 -> SRAM에서 QKᵀ 계산
    -> online softmax 갱신 -> V 가중합 -> output block 저장
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | Q/K/V를 tile 단위로 HBM에서 SRAM으로 로드 | block size, SRAM fit |
| 2 | tile별 QKᵀ와 causal mask 계산 | mask 정확성 |
| 3 | online softmax로 누적 정규화 | numerical stability |
| 4 | V 가중합 후 output만 HBM 저장 | memory footprint, tokens/s |

> 요약: Attention score 전체를 저장하지 않고 타일별 누적 계산으로 같은 결과를 산출함.


## Ⅳ. 특징

| 구분 | 표준 Attention | FlashAttention | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 중간 저장 | N×N score 저장 | score 저장 회피 | memory O(N²) 완화 |
| 병목 | HBM read/write | SRAM tile compute | IO-aware |
| 정확도 | exact | exact | 근사 아님 |
| 적용 | 일반 커널 | GPU별 최적 커널 필요 | CUDA/ROCm 지원 확인 |

> 요약: FlashAttention은 Attention 결과를 바꾸지 않고 메모리 I/O를 줄여 긴 시퀀스 처리량을 높임.


## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 표준 Attention | FlashAttention | 선택 기준 |
|:---|:---|:---|:---|
| 중간 저장 | N×N score HBM 저장 | score 저장 회피(SRAM only) | 시퀀스 길이 4K 이상 여부 |
| 병목 | HBM read/write bandwidth | SRAM compute bound | GPU SRAM 크기 |
| 정확도 | exact | exact (동일) | 근사 아님 |

> 요약: 4K 이상 시퀀스에서 FlashAttention은 HBM I/O를 줄여 처리량을 높이며, 정확도 손실이 없음.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| GPU 커널 미지원 | 아키텍처별 CUDA/ROCm 커널 의존 | A100/H100/MI300 호환 매트릭스 확인, fallback 경로 설정 | 커널 로드 성공 여부 |
| Causal Mask 오류 | mask 적용 누락 시 미래 토큰 참조 | 단위 테스트로 causal 결과 검증 | 생성 품질·perplexity 비교 |
| Mixed Precision 회귀 | FP16/BF16 전환 시 수치 불안정 | perplexity 회귀 테스트, BF16 우선 적용 | perplexity 변화 0.5% 이내 |

> 요약: 커널 호환·mask 정확성·precision 세 리스크를 사전 검증과 fallback으로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| Peak Memory | 표준 대비 40~60% 절감 | torch.cuda.max_memory_allocated |
| tokens/s | 표준 대비 1.5~2배 향상 | 벤치마크(4K/16K/32K context) |
| 정확도 | perplexity 변화 0.1% 이내 | 검증 데이터셋 평가 |

> 요약: peak memory·tokens/s·perplexity 세 지표로 FlashAttention 적용 효과를 정량 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 4K 이상 context 학습·추론에서 FlashAttention 커널을 활성화하고 peak memory와 tokens/s를 비교
2. causal mask, dropout, mixed precision(FP16/BF16) 설정별 정확도 회귀를 perplexity로 확인
3. GPU 아키텍처별(A100/H100/MI300) 지원 커널과 fallback 여부를 배포 체크리스트에 포함

**결론 (2줄):**
- 기술사 판단: 긴 문맥 Transformer는 FlashAttention 적용을 기본값으로 두고, 미지원 GPU에서는 context 길이와 batch를 제한함.
- 향후 방향: FlashAttention 계열은 PagedAttention·sequence parallelism과 결합해 장문맥 LLM 런타임을 구성함.


### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | 설명하시오, 기술하시오 | tile·online softmax 계산 흐름 | 표준 Attention 대비 IO |
| 요구사항 명시형 | 최적화하시오, 비교하시오 | 커널 적용·검증 절차 | 메모리·tokens/s·정확도 기준 |

> 요약: 설명형은 IO-aware 알고리즘, 최적화형은 GPU 커널 적용과 회귀 검증 중심으로 목차를 전환함.
