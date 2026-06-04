---
title: "248. BERT 인코더 MLM vs GPT 디코더 자동 회귀 (Autoregressive) 심화 비교"
date: "2026-04-21"
tags:
  - "studynote-data-engineering"
---


## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [BERT](/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/)(Bidirectional [Encoder](/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/) Representations from Transformers)는 양방향 문맥을 이해하는 [인코더](/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/), [GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/)([Generative Pre-trained Transformer](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/))는 왼쪽에서 오른쪽으로만 처리하는 자동 회귀(Autoregressive) [디코더](/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/)로, 설계 목적이 근본적으로 다르다.
> 2. **가치**: BERT는 [MLM](/studynote/10_ai/02_dl_architecture_new/138_mlm_learning/)([Masked Language Model](/studynote/10_ai/02_dl_architecture_new/138_mlm_learning/))과 [NSP](/studynote/10_ai/02_dl_architecture_new/139_nsp_next_sentence_prediction/)([Next Sentence Prediction](/studynote/10_ai/02_dl_architecture_new/139_nsp_next_sentence_prediction/))로 문장 이해·[분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)에 특화되고, GPT는 자동 회귀 다음 토큰 예측으로 텍스트 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)에 탁월하다.
> 3. **판단 포인트**: T5·BART는 [인코더](/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/)-[디코더](/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/) 구조를 유지해 이해와 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)을 동시에 처리하며, 현재 실무에서는 [GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/) 계열 자동 회귀 모델이 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) AI의 주류를 이룬다.

---

## Ⅰ. 개요 및 필요성

2018년은 NLP(Natural Language Processing) 혁명의 원년이다. [BERT](/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/)(Google, 2018)와 [GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/)(OpenAI, 2018)가 거의 동시에 등장하며 사전 학습-파인튜닝 패러다임을 확립했다. 두 모델은 같은 [Transformer](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) 기반이지만 어텐션 방향과 사전 학습 목표가 반대다.

| 특성 | [BERT](/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/) | [GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/) |
|:---|:---|:---|
| 구조 | [인코더](/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/)([Encoder](/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/)) | [디코더](/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/)([Decoder](/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/)) |
| 어텐션 방향 | 양방향 (Bidirectional) | [단방향](/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/) (Left-to-Right) |
| 사전 학습 목표 | [MLM](/studynote/10_ai/02_dl_architecture_new/138_mlm_learning/) + [NSP](/studynote/10_ai/02_dl_architecture_new/139_nsp_next_sentence_prediction/) | 다음 토큰 예측 |
| 강점 | 이해, [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/), [NER](/studynote/16_bigdata/05_analysis/117_ner/) | [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/), 대화, 완성 |
| 약점 | [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 불가 | 양방향 문맥 부족 |

📢 **섹션 요약 비유**: BERT는 시험 채점관이다. 문제와 답안을 동시에 보고 "이 답이 맞는지" 이해한다. GPT는 소설 작가다. 앞에서부터 순서대로 읽으면서 다음 문장을 창작한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [BERT](/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/) 아키텍처 및 사전 학습

```
BERT 입력 구성
[CLS] 나는 [MASK] 에 간다 [SEP] 공부가 재미있다 [SEP]
  ^                 ^      ^
[CLS]: 문장 전체 표현    [SEP]: 문장 구분자

어텐션 패턴 (양방향):
  나는 <--> [MASK] <--> 에 <--> 간다
  모든 토큰이 모든 토큰과 어텐션 가능
```

<strong><a href="/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/">BERT</a> 두 가지 사전 학습 목표</strong>

| 목표 | 방법 | 역할 |
|:---|:---|:---|
| [MLM](/studynote/10_ai/02_dl_architecture_new/138_mlm_learning/) ([Masked Language Model](/studynote/10_ai/02_dl_architecture_new/138_mlm_learning/)) | 15% 토큰 마스킹 후 복원 | 문맥 이해 |
| [NSP](/studynote/10_ai/02_dl_architecture_new/139_nsp_next_sentence_prediction/) ([Next Sentence Prediction](/studynote/10_ai/02_dl_architecture_new/139_nsp_next_sentence_prediction/)) | 두 문장의 연속성 예측 (IsNext/NotNext) | 문장 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 이해 |

<strong><a href="/studynote/10_ai/02_dl_architecture_new/138_mlm_learning/">MLM</a> 마스킹 <a href="/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a></strong> (15% 중):
- 80%: [MASK] 토큰으로 교체
- [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)%: 랜덤 토큰으로 교체 (노이즈 강건성)
- [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)%: 원래 토큰 유지 (표현 학습)

### [GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/) 아키텍처 및 자동 회귀 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)

```
GPT 어텐션 패턴 (인과적 마스킹):
                  미래 토큰 차단 (마스크)
나 -> 는 --------------------------------> ✗
나 -> 는 -> 학교에 -----------------------> ✗
나 -> 는 -> 학교에 -> 간다
  각 위치는 이전 위치만 볼 수 있음

자동 회귀 생성 과정:
[START] -> "나" -> "나는" -> "나는 학교에" -> "나는 학교에 간다"
  P(x_t | x_1, ..., x_{t-1}) 조건부 확률 연쇄 곱
```

<strong><a href="/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/">디코더</a> 전용 구조의 특징</strong>:
- 인과적 자기 회귀 마스킹(Causal [Self-Attention](/studynote/10_ai/02_dl_architecture_new/124_self_attention/) Masking)
- 훈련과 추론의 방향 일치
- KV 캐시([Key-Value Cache](/studynote/06_ict_convergence/04_ai_llm/291_kv_cache/))로 추론 가속

### 모델 규모 비교

```
BERT와 GPT 계열 발전
------------------------------------------------
BERT-Base  (2018): 12층, 110M 파라미터
BERT-Large (2018): 24층, 340M 파라미터
RoBERTa    (2019): BERT 개선 (더 많은 데이터, NSP 제거)

GPT-1      (2018):  12층, 117M 파라미터
GPT-2      (2019):  48층, 1.5B 파라미터  (처음엔 위험하다고 공개 지연)
GPT-3      (2020):  96층, 175B 파라미터  (퓨샷 학습 창발)
GPT-4      (2023):  비공개, ~1.8T 추정   (멀티모달)
------------------------------------------------
```

📢 **섹션 요약 비유**: BERT는 독서왕이다. 앞뒤 다 읽고 "이 단어의 의미가 뭔지" 파악한다. GPT는 즉흥 이야기꾼이다. 지금까지 말한 것만 기억하고 다음 이야기를 창작한다.

---

## Ⅲ. 비교 및 연결

### [BERT](/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/) vs [GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/) 적합 [태스크](/studynote/02_operating_system/02_process_thread/150_task/) 매핑

| [태스크](/studynote/02_operating_system/02_process_thread/150_task/) | 적합 모델 | 이유 |
|:---|:---|:---|
| 텍스트 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) | [BERT](/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/) | [CLS] 토큰으로 전체 문맥 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) |
| [개체명 인식](/studynote/16_bigdata/05_analysis/117_ner/) ([NER](/studynote/16_bigdata/05_analysis/117_ner/)) | [BERT](/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/) | 각 토큰의 양방향 문맥 필요 |
| 질문 응답 (QA) | [BERT](/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/) | 지문+질문 동시 이해 |
| 자연어 추론 (NLI) | [BERT](/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/) | 두 문장 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 양방향 비교 |
| 텍스트 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | [GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/) | 자동 회귀 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 구조 |
| 대화/챗봇 | [GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/) | 이전 발화 조건부 응답 |
| 코드 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | [GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/)/Codex | 순차적 코드 완성 |
| 번역/요약 | T5/BART | 이해+[생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 동시 필요 |

### T5 및 BART — [인코더](/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/)-[디코더](/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/) 모델

```
T5 (Text-To-Text Transfer Transformer): Google 2019
  모든 NLP 태스크를 텍스트->텍스트 변환으로 통일
  입력: "translate Korean to English: 나는 학교에 간다"
  출력: "I go to school"

  -> 분류도 텍스트 생성으로 처리
    입력: "sentiment: 오늘 정말 행복해"
    출력: "positive"

BART (Bidirectional and Auto-Regressive Transformers): Meta 2019
  사전 학습: 노이즈 제거 (문장 셔플, 토큰 삭제, 마스킹)
  인코더: BERT처럼 양방향 이해
  디코더: GPT처럼 자동 회귀 생성
  -> 요약·생성·번역에 강점
```

```
인코더-디코더 아키텍처 요약
+---------------------------------------------+
| 모델 유형     | 대표 모델 | 주요 태스크       |
+---------------------------------------------+
| 인코더 전용   | BERT      | 분류, NER, QA     |
| 디코더 전용   | GPT       | 생성, 대화        |
| 인코더-디코더 | T5, BART  | 번역, 요약, 대화  |
+---------------------------------------------+
```

📢 **섹션 요약 비유**: BERT는 의사, GPT는 소설가, T5/BART는 의사이면서 소설가다. 진단(이해)도 처방전([생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/))도 동시에 잘 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [BERT](/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/) 파인튜닝 구조 예시

```
BERT 문서 분류 파인튜닝
입력: [CLS] 이 영화는 정말 재미있었다 [SEP]
                v (12층 Transformer 인코더)
[CLS] 임베딩: [0.8, -0.3, ..., 0.5] <- 문장 전체 표현
                v
[Linear + Softmax] -> 긍정(0.9) / 부정(0.1)

파인튜닝 전략:
  1. 분류 헤드만 훈련 (BERT 동결) -> 빠름, 정확도 낮음
  2. 전체 파인튜닝 -> 느림, 정확도 높음
  3. 상위 몇 층만 파인튜닝 -> 균형
```

### [GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/) [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 활용 — [프롬프트 엔지니어링](/studynote/14_data_engineering/03_ml_dl_llm/149_prompt_engineering_cot_few_shot/)

```
시스템 프롬프트: "당신은 친절한 한국어 고객 서비스 담당자입니다."
사용자 입력:   "배송이 3일이나 늦었어요"
                      v GPT-4 자동 회귀 생성
모델 출력:     "불편을 드려서 정말 죄송합니다. 주문 번호를
               알려주시면 즉시 확인하겠습니다."

온도(Temperature):
  T=0.0 -> 결정적 (동일 프롬프트 -> 동일 출력) -> 사실 검색
  T=1.0 -> 다양성 -> 창의적 글쓰기
  T=2.0 -> 무작위 -> 비일관적 (잘 사용 안 함)
```

📢 **섹션 요약 비유**: [BERT](/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/) 파인튜닝은 전문 학위를 가진 의사에게 특정 병원의 프로토콜을 가르치는 것이고, [GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/) [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 사용은 그 의사에게 역할과 규칙을 알려주고 환자를 맡기는 것이다.

---

## Ⅴ. 기대효과 및 결론

### NLP 리더보드 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 비교 (GLUE 벤치마크)

```
GLUE 점수 (이해 태스크 기준, 100점 만점)
--------------------------------
ELMo (2018):      68.7점
BERT-Base:        79.6점  (+10.9점)
BERT-Large:       82.1점
RoBERTa:          86.4점
T5-11B:           89.3점
인간 성능:        87.1점  <- T5가 초월!
--------------------------------
```

### 기술사 시험 핵심 포인트

1. <strong><a href="/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/">BERT</a> 사전 학습</strong>: [MLM](/studynote/10_ai/02_dl_architecture_new/138_mlm_learning/)(15% 마스킹) + [NSP](/studynote/10_ai/02_dl_architecture_new/139_nsp_next_sentence_prediction/)(두 문장 연속성)
2. <strong><a href="/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/">GPT</a> 자동 회귀</strong>: 인과적 마스킹, `P(x_t|x_{<t})` [조건부 확률](/studynote/08_algorithm_stats/08_stats/132_conditional_probability/)
3. **[CLS] 토큰**: BERT에서 문장 전체 표현으로 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)에 활용
4. **T5 통일 프레임워크**: 모든 [태스크](/studynote/02_operating_system/02_process_thread/150_task/)를 텍스트->텍스트 변환
5. <strong>적합 <a href="/studynote/02_operating_system/02_process_thread/150_task/">태스크</a> 매핑</strong>: 이해 -> [BERT](/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/), [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) -> [GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/), 이해+[생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) -> T5/BART

📢 **섹션 요약 비유**: BERT와 GPT는 같은 [Transformer](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) 엔진을 가진 다른 자동차다. BERT는 주변을 360도 보는 레이더 장착 이해 차량이고, GPT는 앞만 보고 달리는 고속 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 차량이다. T5/BART는 두 기능을 모두 갖춘 SUV다.

---

### 📌 관련 개념 맵
| [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| [인코더](/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/) 모델 | [BERT](/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/) | 양방향 이해, [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) 특화 |
| 사전 학습 목표 | [MLM](/studynote/10_ai/02_dl_architecture_new/138_mlm_learning/) ([Masked Language Model](/studynote/10_ai/02_dl_architecture_new/138_mlm_learning/)) | 마스킹된 토큰 복원 |
| 보조 목표 | [NSP](/studynote/10_ai/02_dl_architecture_new/139_nsp_next_sentence_prediction/) ([Next Sentence Prediction](/studynote/10_ai/02_dl_architecture_new/139_nsp_next_sentence_prediction/)) | 두 문장 연속성 예측 |
| [디코더](/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/) 모델 | [GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/) | [단방향](/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/) 자동 회귀 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) |
| [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 방식 | 자동 회귀 (Autoregressive) | 이전 토큰 조건부 다음 토큰 예측 |
| 통합 모델 | T5 | 모든 [태스크](/studynote/02_operating_system/02_process_thread/150_task/) 텍스트->텍스트 통일 |
| 통합 모델 | BART | 노이즈 제거 사전 학습 |
| 발전 모델 | RoBERTa | [BERT](/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/) 개선 (더 많은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)) |

### 👶 어린이를 위한 3줄 비유 설명
1. BERT는 시험 문제를 풀 때 앞뒤 힌트를 모두 볼 수 있는 독자야. 빈칸 채우기를 할 때 앞 내용도, 뒤 내용도 동시에 참고할 수 있어.

### 📈 관련 키워드 및 발전 흐름도

```text
BERT (Encoder): 양방향 MLM -> 이해 · 분류 특화
GPT (Decoder): 자기회귀 -> 생성 특화
    |
    v
T5 (Enc-Dec): 모든 NLP를 Text-to-Text로 통합
    |
    v
GPT-3 -> GPT-4 -> 멀티모달 · 에이전트 시대
```
2. GPT는 이야기를 이어가는 작가야. 지금까지 쓴 내용만 보면서 다음 문장을 계속 만들어 가는데, 뒷내용은 미리 볼 수 없어.
3. T5는 만능 번역기야. 문제를 주면 어떤 종류든 답을 텍스트로 돌려주는데, [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)도 번역도 요약도 모두 "텍스트 -> 텍스트" 방식으로 통일해서 처리해.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 248 / 258

<- **이전**: [247. 파운데이션 모델 (Foundation Model) LLM 파라미터 창발성 (Emergence) 자기 지도 학습](/studynote/14_data_engineering/05_exam_keywords/247_foundation_model_llm_parameter_emergence_self_supervised/)
**다음**: [249. 인스트럭션 파인튜닝 (Instruction Fine-Tuning) PEFT LoRA 저차원 어댑터](/studynote/14_data_engineering/05_exam_keywords/249_instruction_finetuning_peft_lora_low_rank_adapter/) ->

---
