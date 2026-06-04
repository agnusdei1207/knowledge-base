---
title: "384. 토크나이저 BPE (Byte Pair Encoding)"
date: "2026-05-09"
tags:
  - "studynote-ai"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: BPE ([Byte Pair Encoding](/studynote/06_ict_convergence/05_data_science/378_bpe_byte_pair_encoding/), [바이트](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) 쌍 인코딩)는 가장 빈도 높은 문자 쌍을 반복적으로 병합해 서브워드 (Subword) 어휘집을 구성하며, 어휘 크기와 OOV (Out-Of-Vocabulary) 사이의 균형을 최적화한다.
> 2. **가치**: 단어 단위 토크나이저의 OOV 문제와 문자 단위의 과도한 시퀀스 길이 문제를 동시에 해결하며, [GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/)-2, RoBERTa, LLaMA 등 현대 LLM의 표준 토크나이저다.
> 3. **판단 포인트**: 어휘 크기(Vocab Size)는 BPE의 병합 횟수로 결정되며, 클수록 OOV가 줄고 시퀀스가 짧아지지만 [임베딩](/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) 메모리와 학습 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 더 필요하다.

---

## Ⅰ. 개요 및 필요성

자연어 처리에서 토크나이저는 원시 텍스트를 모델이 처리할 수 있는 토큰 시퀀스로 변환한다. 토크나이저 단위 선택은 모델 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 효율에 직접 영향을 미친다.

| 방식 | 단위 | OOV | 시퀀스 길이 | 어휘 크기 |
|:---|:---|:---|:---|:---|
| 단어([Word](/studynote/01_computer_architecture/02_data_representation_arithmetic/075_word/)) | 단어 | 심각 | 짧음 | 수십만 |
| 문자(Char) | 문자 | 없음 | 매우 긺 | ~100 |
| 서브워드(BPE) | 서브워드 | 거의 없음 | 중간 | 수만 |

BPE는 원래 [데이터 압축](/studynote/08_algorithm_stats/09_info_theory/159_compression/) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이었으나, Sennrich et al. (2016)이 NMT (Neural Machine Translation)에 도입했다.

```text
+----------------------------------------------+
| Background Problem -> Need -> Adoption Value   |
+----------------------------------------------+
| Existing limitation | Operational pressure   |
| New requirement     | Design decision point  |
+----------------------------------------------+
```

- **📢 섹션 요약 비유**: BPE는 "자주 등장하는 레고 블록 조합을 새로운 블록으로 묶어 보관하는 것"이다. 자주 쓰는 단어 조각은 하나의 토큰으로 만들어 효율화한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### BPE 학습 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)

```
1. 초기화: 모든 단어를 문자 단위로 분리 + 단어 끝 표시 </w>
   "low"  -> l o w </w>
   "lower"-> l o w e r </w>
   "newer"-> n e w e r </w>

2. 빈도 계산: 인접 문자 쌍의 등장 빈도 계산
   (l,o): 3회,  (o,w): 3회,  (e,r): 2회, ...

3. 가장 빈도 높은 쌍 병합:
   병합 1: (l,o) -> "lo"
   병합 2: (lo,w) -> "low"
   병합 3: (e,r) -> "er"
   ...

4. 목표 어휘 크기에 도달할 때까지 반복
```

```
+------------------------------------------------------+
|  초기:  l o w </w>  /  l o w e r </w>                |
|  병합1: lo w </w>   /  lo w e r </w>   (+lo)         |
|  병합2: low </w>    /  low e r </w>    (+low)         |
|  병합3: low </w>    /  low er </w>     (+er)          |
|  결과 어휘: {l, o, w, e, r, </w>, lo, low, er, ...}  |
+------------------------------------------------------+
```

### BPE 인코딩 (적용)

학습된 병합 규칙을 우선순위대로 새 텍스트에 적용:
```
"lowest" -> l o w e s t -> lo w e s t -> low e s t -> low es t -> low est
```
-> OOV 단어도 알려진 서브워드로 분해 가능

### [GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/)-2 [Byte](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/)-level BPE

[UTF-8](/studynote/01_computer_architecture/02_data_representation_arithmetic/105_utf8/) [바이트](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/)를 기본 어휘로 사용 -> 모든 [유니코드](/studynote/01_computer_architecture/02_data_representation_arithmetic/104_unicode/) 문자 처리 가능, OOV 완전 제거

| 요소 | 역할 |
|:---|:---|
| 입력 표현 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 토큰·벡터·[특성 맵](/studynote/10_ai/01_ai_basics/099_feature_map_activation_map_cnn_output/)으로 바꾸는 전처리 계층이다. |
| 모델 구조 | 정보를 축적·선택·[생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하는 핵심 계산 흐름을 담당한다. |
| 경량화 | 배포 환경에 맞춰 메모리와 연산량을 조정한다. |
| 응용 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) | 검색, [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/), 추천, 제어 등 실제 문제 해결 단계로 이어진다. |

- **📢 섹션 요약 비유**: BPE 병합은 자주 같이 오는 친구를 "단짝"으로 묶어 새 이름을 주는 것이다. 수천 번 반복하면 자주 쓰는 단어 조각들이 모두 이름을 갖게 된다.

---

## Ⅲ. 비교 및 연결

| 토크나이저 | [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 결합 기준 | 사용 모델 |
|:---|:---|:---|:---|
| BPE | 빈도 기반 병합 | 문자 쌍 빈도 | [GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/)-2, RoBERTa, LLaMA |
| WordPiece | 우도 기반 병합 | 언어 모델 우도 증가량 | [BERT](/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/), DistilBERT |
| SentencePiece | BPE/Unigram | 직접 [바이트](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) 처리 | T5, LLaMA (내부) |
| Unigram LM | [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) 기반 제거 | 우도 감소 최소 | AlBERT |

- **📢 섹션 요약 비유**: BPE는 "가장 인기 있는 쌍부터 묶는 합산 방식", WordPiece는 "묶었을 때 언어 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/)이 가장 올라가는 쌍부터 묶는 성과 방식"이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**어휘 크기 선택**:
- 영어 [LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/): 32k ~ 100k ([GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/)-4: ~100k, LLaMA: 32k)
- 다국어 모델: 언어 수에 비례해 어휘 확장 필요
- 한국어: 자소 분리 + BPE 조합으로 한글 형태소 특성 반영

**토큰 길이와 비용**: 더 짧은 토큰 시퀀스 = 더 적은 컴퓨팅 비용
- "unhappiness" -> [BERT](/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/): ["un", "##happy", "##ness"] (3토큰)
- [GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/)-2: ["un", "h", "app", "iness"] (4토큰 경우도 있음)

기술사 포인트: BPE [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 3단계([초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)화->병합->적용)와 OOV 해결 원리를 명확히 설명.

- **📢 섹션 요약 비유**: 어휘 크기 선택은 "사전의 두께"다. 두꺼우면 표현력이 좋지만 외워야 할 단어가 많고, 얇으면 가볍지만 알 수 없는 단어가 늘어난다.

---

## Ⅴ. 기대효과 및 결론

BPE는 단순한 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)으로 단어 단위 vs 문자 단위의 딜레마를 해결한 실용적 발명이다. [Byte](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/)-level BPE는 OOV를 완전히 제거하며 다국어, 코드, 이모지까지 처리 가능한 범용 토크나이저로 진화했다. 현대 LLM의 토크나이저 설계는 BPE를 기반으로 계속 발전하고 있다.

- **📢 섹션 요약 비유**: BPE는 모든 언어의 "공통 레고 블록"을 찾아내는 것이다. 어떤 언어든 기본 블록으로 분해하면 모델이 처리할 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| BPE | 빈도 병합, 서브워드 / 현대 표준 토크나이저 |
| OOV | Out-Of-Vocabulary / 서브워드로 해결 |
| 어휘 크기 | Vocab Size, 병합 횟수 / 시퀀스 길이 vs 표현력 |
| WordPiece | [BERT](/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/), 우도 기반 / BPE 변형 |
| SentencePiece | T5, 언어 독립적 / BPE의 다국어 확장 |
| [Byte](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/)-level BPE | [GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/)-2, OOV 없음 / [바이트](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) 단위 BPE |

### 📈 관련 키워드 및 발전 흐름도

```text
[입력 표현·특징 추출] -> [토크나이저 BPE (Byte Pair Encoding)] -> [경량화·멀티모달·서비스 적용]
```

### 👶 어린이를 위한 3줄 비유 설명

1. BPE는 자주 같이 오는 글자들을 묶어서 새 이름을 주는 거야. "ab"가 자주 나오면 "ab"라는 새 토큰을 만들어.
2. 이렇게 계속 묶다 보면 자주 쓰는 단어는 하나의 토큰이 되고, 드문 단어는 작은 조각들로 나뉘어.
3. 덕분에 "처음 본 단어"도 이미 알고 있는 조각들로 분해해서 이해할 수 있어!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 384 / 420

<- **이전**: [383. LLM 자기 회귀 (Auto-Regressive) 언어 모델 우도 수식](/studynote/10_ai/05_data_science_ml/383_llm_autoregressive_math/)
**다음**: [385. WordPiece / SentencePiece 토크나이징 비교 (Wordpiece Sentencepiece)](/studynote/10_ai/05_data_science_ml/385_wordpiece_sentencepiece/) ->

---
