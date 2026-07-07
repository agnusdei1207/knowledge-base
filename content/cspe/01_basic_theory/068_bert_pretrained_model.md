---
title: "BERT 사전학습 모델 (BERT Pre-trained Model) [출제: 121회]"
date: "2026-07-07"
tags:
  - "cspe-basic-theory"
weight: 68
---

# 068. BERT 사전학습 모델 (BERT Pre-trained Model) [출제: 121회]

## Ⅰ. 개요

- **정의/개념**: 트랜스포머($Transformer$)의 인코더 구조를 기반으로, 방대한 비정형 말뭉치로부터 문맥의 양방향($Bidirectional$) 관계를 사전 학습($Pre$-$training$)하여 다양한 자연어 이해($NLU$) 태스크에 미세 조정($Fine$-$tuning$)이 가능한 범용 언어 모델임
- **배경/필요성**: 기존 $RNN$이나 단방향 $LM$($GPT$ 등)은 특정 시점에서 미래 정보를 보지 못하는 병목 현상($Bottleneck$)이 존재함. 이를 극복하고 단어의 다의성과 문장 간의 깊은 연관성을 파악하기 위해 마스크드 언어 모델($MLM$) 기반의 양방향 학습 체계가 고안됨

## Ⅱ. 특징 및 비교

### 1. 주요 언어 모델 아키텍처 비교

| 판단 기준 | $Word2Vec$ (정적) | $GPT$ (생성형) | $BERT$ (이해형) |
|:---|:---|:---|:---|
| **기반 아키텍처** | 룩업 테이블 (통계) | $Transformer$ $Decoder$ | $Transformer$ $Encoder$ |
| **학습 방향** | 국소적 문맥 | 단방향 ($Autoregressive$) | 양방향 ($Autoencoding$) |
| **학습 데이터 활용** | 단어 간 상관관계 | 다음 토큰 예측 | 마스킹된 토큰 복원 |
| **특화 영역** | 빠른 유사도 탐색 | 자연어 생성 ($NLG$) | 자연어 이해 ($NLU$) |

> 요약: $GPT$가 미래를 예측하는 '생성'에 특화된 반면, $BERT$는 전체 문맥을 한꺼번에 조망하는 '이해'와 '추출'에 최적화됨

### 2. $PPA$ 및 트레이드오프 ($Trade$-$offs$)
- **Performance**: $Self$-$Attention$의 연산 복잡도는 시퀀스 길이 $L$에 대해 $O(L^2 \cdot d)$이며, 양방향성으로 인해 동등 파라미터 대비 추론 정확도가 높음
- **Precision**: $MLM$을 통해 문맥 파악의 정밀도를 높였으나, 사전 학습 시의 $[MASK]$ 토큰이 실제 서비스($Inference$) 시에는 존재하지 않아 발생하는 불일치($Mismatch$)가 발생함
- **Resource**: 모델이 비대할수록($BERT$-$Large$ 등) 처리량($Throughput$)은 급감하며, 고성능 $GPU$ 메모리 자원이 대량으로 요구됨

## Ⅲ. 구성요소/구조

### 1. $BERT$ 아키텍처 인사이트 ($Architecture$ $Insight$)
- **$MLM$ ($Masked$ $Language$ $Model$)**: 전체 토큰의 $15\%$를 마스킹하고 주변 단어를 통해 이를 예측함. 이 중 $80\%$는 $[MASK]$, $10\%$는 랜덤, $10\%$는 원래 단어를 유지하여 불일치 문제를 완화함
- **$NSP$ ($Next$ $Sentence$ $Prediction$)**: 두 문장이 인접한 문장인지 판별($IsNext$ vs $NotNext$)하여 문장 레벨의 일관성($Coherence$)을 학습함
- **$Embeddings$**: $[CLS]$(문장 분류용), $[SEP]$(구분자) 토큰과 함께 $Token, Segment, Position$ 임베딩을 합산하여 트랜스포머 입력으로 사용함

### 2. 데이터 흐름 및 구성도
```text
[Input Tokens] -> [BERT Encoder Stack] -> [Output Embeddings] -> [Task Layer]
      |                   |                      |                   |
 [CLS] 토큰 포함     Self-Attention x N     문맥 반영 벡터       분류/추출 수행
```

## Ⅳ. 문제점 및 개선방안

### 1. 실무적 문제점 및 대응 전략
1. **[추론 지연 ($Inference$ $Latency$)]**: 복잡한 어텐션 연산으로 인해 실시간 고객 응대 시스템 적용 시 응답 속도 저하 발생
   - **개선방안**: 지식 증류($Distillation$) 기법을 적용한 $DistilBERT$, $TinyBERT$ 사용 및 $FP16/INT8$ 양자화($Quantization$) 적용 (확인: $Latency$ $p99$)
2. **[긴 문서 처리의 한계]**: 시퀀스 길이 $L$이 $512$ 토큰으로 제한되어 긴 법률·의료 문서 분석 시 정보 소실 발생
   - **개선방안**: $Sparse$ $Attention$을 활용한 $Longformer$, $BigBird$ 아키텍처 도입 또는 계층적 요약 후 입력 방식 적용 (확인: $Context$ $Coverage$)
3. **[도메인 불일치]**: 일반 상식 데이터로 학습된 $BERT$는 전문 용어(의학, 금융) 이해도가 낮음
   - **개선방안**: 타겟 도메인 데이터를 추가 학습($DAPT$, $TAPT$)하여 $Vocab$을 최적화한 도메인 특화 모델($BioBERT$, $FinBERT$) 활용 (확인: $F1$-$Score$)

### 2. 리얼월드 트러블슈팅 ($Real$-$world$ $Troubleshooting$)
- **상황**: 미세 조정($Fine$-$tuning$) 시 데이터셋 크기가 너무 작아 과적합($Overfitting$) 발생 및 성능 불안정
- **해결**: 학습률($Learning$ $Rate$)을 매우 작게 설정($2e$-$5$ 등)하고, $Warmup$ 단계를 충분히 두어 가중치 급변을 방지하거나 동결($Freezing$) 전략을 혼합함

## Ⅴ. 실무 적용 사례

| 적용 영역 | 적용 방식 | 확인 지표 |
|:---|:---|:---|
| **기계 독해 ($MRC$)** | 매뉴얼 원문에서 질문에 대한 정답이 포함된 텍스트 구간($Span$)의 시작/끝 위치 추출 | $EM$ ($Exact$ $Match$), $F1$ |
| **개체명 인식 ($NER$)** | 텍스트 내 인명, 지명, 조직명 등 핵심 엔티티를 양방향 문맥을 기반으로 식별 | $Precision$, $Recall$ |
| **검색 랭킹** | 검색어와 웹페이지 제목 간의 의미적 유사도를 판단하여 고도화된 리랭킹($Re$-$ranking$) 수행 | $nDCG$, $Search$ $CTR$ |

## Ⅵ. 결론

$BERT$는 자연어 처리의 패러다임을 "규칙과 통계"에서 "전이 학습($Transfer$ $Learning$)"으로 전환시킨 핵심 모델임. 비록 최근 생성 능력이 강조되는 $GPT$ 계열의 공세가 거세지만, 정교한 사실 관계 확인, 법률 검토, 지식 추출 등 '이해의 정확도'가 비즈니스 가치와 직결되는 영역에서는 여전히 가장 신뢰받는 백본 모델임. 향후 연산 효율을 높인 가벼운($Efficient$) 모델과 멀티모달 결합형 구조로 지속 진화할 전망임.
