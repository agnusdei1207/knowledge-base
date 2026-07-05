---
title: "RAGAS (Retrieval Augmented Generation Assessment)"
date: "2026-07-05"
author: "Claude Opus 4.6 (Enhanced by Gemini 3.5)"
tags:
  - "cspe-08_latest_tech"
weight: 127
---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **정의** | RAG 시스템의 성능을 사람 대신 대형 언어 모델(LLM)을 이용해 자동으로, 그리고 수학적으로 채점해 주는 오픈소스 기반의 업계 표준 R... | "이 개념의 핵심" |
| **필요성** | RAG 구조를 조금만 바꿔도(청크 사이즈 변경, 임베딩 모델 교체) 답변이 확확 바뀌는데, 매번 사람이 1,000개의 질문을 읽어보고 채점... | "이 개념의 핵심" |
| **핵심 직관** | 소프트웨어 개발의 '단위 테스트(JUnit)' 같은 것 | "이 개념의 핵심" |
| **배경** | Exploding Gradients(스타트업)가 개발 및 오픈소스로 공개 | "이 개념의 핵심" |
| **작동 원리 (4대 핵심 지표 계산법)** | 1. **Faithfulness (충실성)**: RAG 답변을 문장 단위로 쪼갬 | "학습하는 기계" |
| **Answer Relevancy (답변 관련성)** | RAG가 한 답변을 보고, LLM에게 반대로 "이 답변이 나올 법한 질문을 3개 만들어봐"라고 시킴 | "이 개념의 핵심" |
| **Context Precision (문맥 정밀도)** | 검색된 문서들 중 정답이 있는 진짜 유용한 문서가 상위(1~2등)에 제대로 위치했는가? | "자동 품질 검사 라인" |

---


# 📖 【암기용】 개념 완전 이해

## 한눈에
- **정의**: RAG 시스템의 성능을 사람 대신 대형 언어 모델(LLM)을 이용해 자동으로, 그리고 수학적으로 채점해 주는 오픈소스 기반의 업계 표준 RAG 평가 프레임워크.
- **필요성**: RAG 구조를 조금만 바꿔도(청크 사이즈 변경, 임베딩 모델 교체) 답변이 확확 바뀌는데, 매번 사람이 1,000개의 질문을 읽어보고 채점할 수는 없음. 코드 돌리듯 자동화된 테스트 툴이 절대적으로 필요했음.
- **핵심 직관**: 소프트웨어 개발의 '단위 테스트(JUnit)' 같은 것. `질문`, `정답`, `RAG가 찾은 문서`, `RAG가 쓴 답변` 4가지를 프레임워크에 던져주면, "검색은 80점, 답변 충실성은 90점"이라고 상세한 건강 검진표를 출력해 줌.

## 깊이 이해
- **배경**: Exploding Gradients(스타트업)가 개발 및 오픈소스로 공개. 정답셋(Ground Truth)이 없어도 평가가 가능한 지표들(Faithfulness 등)을 제안하며, 2023년 이후 RAG 평가의 De facto(사실상 표준) 라이브러리로 자리 잡음.
- **작동 원리 (4대 핵심 지표 계산법)**:
  1. **Faithfulness (충실성)**: RAG 답변을 문장 단위로 쪼갬. 각 문장이 검색된 문서에 있는 내용인지 LLM 판사에게 O/X로 묻고, 비율을 냄 (예: 4문장 중 3문장이 진짜면 0.75점).
  2. **Answer Relevancy (답변 관련성)**: RAG가 한 답변을 보고, LLM에게 반대로 "이 답변이 나올 법한 질문을 3개 만들어봐"라고 시킴. 역으로 만든 질문들이 원래 사용자의 질문과 의미적으로 유사한지 임베딩 거리로 채점. (동문서답 걸러냄).
  3. **Context Precision (문맥 정밀도)**: 검색된 문서들 중 정답이 있는 진짜 유용한 문서가 상위(1~2등)에 제대로 위치했는가?
  4. **Context Recall (문맥 재현율)**: 실제 정답을 구성하는 데 필요한 모든 근거 정보가 빠짐없이 검색 결과에 포함되었는가?
- **비유**: RAGAS는 깐깐한 감사관. 검색팀(Vector DB)에게는 "필요한 서류 빠짐없이 챙겨왔나?(Recall), 젤 중요한 서류를 맨 위에 올렸나?(Precision)"를 따지고, 보고팀(LLM)에게는 "서류에 없는 네 뇌피셜 쓴 거 없나?(Faithfulness), 회장님 질문에 동문서답 안 했나?(Relevancy)"를 따짐.
- **흔한 오해/주의점**: RAGAS 점수가 낮다고 무조건 우리 RAG가 멍청한 건 아님. 심사위원으로 쓰는 LLM(보통 GPT-4 권장)이 GPT-3.5 같이 성능이 떨어지면 채점 자체를 엉터리로 해서 점수가 박살 남. 채점관(Judge) 모델의 성능이 가장 중요함.

## 연결 개념
- **LLM-as-a-Judge**: 인간 평가자를 대체하여 LLM을 자동 평가관으로 사용하는 패러다임. RAGAS의 근간 기술.
- **Ground Truth**: 시스템이 맞춰야 하는 '진짜 정답'. Ragas의 일부 지표(Context Recall 등)를 계산할 때 필수적임.
- **LangSmith**: LangChain에서 만든 LLMOps 플랫폼으로, Ragas 라이브러리와 연동하여 평가 점수를 대시보드에 뿌려줌.

---

# 📝 【답안용】 시험 답안 템플릿
## 핵심 인사이트 (3줄 요약)
- **본질**: LLM-as-a-Judge 방법론을 차용하여, 질문(Query), 검색 문맥(Context), 답변(Answer), 정답(Ground Truth)의 4가지 튜플(Tuple) 데이터를 기반으로 RAG 파이프라인의 검색 품질과 생성 품질을 정량적으로 산출하는 자동 평가 프레임워크.
- **가치**: Ground Truth가 부재한 상황에서도 Reference-free 평가(Faithfulness, Answer Relevancy)를 지원하여 운영 환경의 실시간 모니터링을 가능케 하며, RAG 튜닝 시 수동 평가 비용을 1/100 수준으로 낮춤.
- **판단 포인트**: 지표별 연산 시 프롬프트 호출이 다수 발생하여 API 비용이 급증할 수 있으므로, CI/CD 파이프라인 내에서 적절한 샘플링(Sampling) 적용 및 오픈소스 70B급 로컬 Judge 모델 구축(FinOps) 고려 필요.

## Ⅰ. 개요 및 필요성
- **정의**: Retrieval Augmented Generation 시스템의 구성 요소를 세분화하여, 토큰 매칭(N-gram)이 아닌 거대 언어 모델의 추론(Reasoning) 능력을 활용해 시맨틱(Semantic) 수준의 품질 메트릭을 제공하는 오픈소스 라이브러리.
- **배경**: 기존 NLP 평가지표(BLEU, ROUGE 등)는 생성형 AI의 유창함과 동의어 사용을 포착하지 못하며, 인간 평가(Human Evaluation)는 병목 현상과 높은 TCO를 유발함.
- **필요성**: RAG의 검색(Retrieval)과 생성(Generation)이라는 두 가지 이질적 워크플로를 분리(Decoupling)하여 원인 기반의 에러 분석(Root Cause Analysis) 및 MLOps 자동 배포(CI/CD) 파이프라인을 구축하기 위함.

## Ⅱ. Ragas 4대 핵심 지표 및 수학적 작동 원리
RAG 시스템의 성능을 $0 \sim 1$ 사이의 점수로 정규화하여 출력함.
| 지표 (Metrics) | 측정 대상 (평가 축) | 작동 메커니즘 (Prompting & Math) |
|:---:|:---|:---|
| **1. Faithfulness**<br>(충실성/근거기반성) | Context $\rightarrow$ Answer <br>(생성 품질, 환각 판별) | 답변을 원자적 명제(Statement)로 분리 후, 각 명제가 Context로부터 논리적 도출(Entailment)이 가능한지 LLM이 판정. <br>$Score = \frac{\text{지지되는 명제 수}}{\text{전체 명제 수}}$ |
| **2. Answer Relevancy**<br>(답변 관련성) | Question $\leftrightarrow$ Answer <br>(생성 품질, 동문서답 판별) | 답변을 보고 LLM이 역질문(Reverse Question) $N$개를 생성. 원본 질문과 역질문 간의 코사인 임베딩 거리의 평균 산출. |
| **3. Context Precision**<br>(문맥 정밀도) | Ground Truth $\leftrightarrow$ Context <br>(검색 품질, 순위 평가) | K개의 검색 문서 중 정답이 있는 유용한 문서가 상위 랭크(Top)에 위치할수록 가중치를 부여하는 $MRR$ / $nDCG$ 유사 랭킹 점수. |
| **4. Context Recall**<br>(문맥 재현율) | Ground Truth $\leftrightarrow$ Context <br>(검색 품질, 누락 평가) | Ground Truth(실제 정답)를 문장 단위로 분할하여, 각 정답 문장이 검색된 Context 내에 온전히 포함되었는지 비율 계산. |

## Ⅲ. Reference-Free 평가의 혁신성
- **기존 방식의 한계**: 전통적 평가는 무조건 사람이 작성한 정답(Ground Truth) 셋이 필요했음.
- **RAGAS의 혁신**: 4개 지표 중 **Faithfulness**와 **Answer Relevancy**는 정답(Ground Truth) 데이터 없이, 사용자의 "질문", 시스템이 찾아온 "문서", 시스템이 뱉은 "답변" 3가지만 있으면 LLM의 자가 추론으로 점수 산출이 가능함. (실제 서비스 운영 중 실시간 품질 모니터링 가능).

## Ⅳ. Ragas vs 타 평가 프레임워크 비교
| 구분 | Ragas | TruLens |
|:---:|:---|:---|
| **핵심 철학** | 역질문 생성 등 복잡한 프롬프트 엔지니어링 기반의 **수학적 점수 산출 (0~1)** | RAG Triad 개념 기반, LLM에게 0~10점 사이를 부여하게 하는 **직접적 피드백 함수** |
| **적합성** | 배치 파이프라인 평가, 실험(Experiment) 결과의 정밀한 소수점 수치 비교 | LangChain/LlamaIndex 앱 내부에 피드백 함수로 인젝트(Inject)하기 용이함 |
| **Ground Truth 필요**| 일부 지표(Recall/Precision)에 필수 | 기본 Triad 지표에는 불필요 |

## Ⅴ. 한계점 및 최적화(MLOps) 운영 전략
- **리스크 1: LLM 채점관(Judge) 자체의 성능 한계 (Bias & Error)**:
  - Ragas는 평가 로직 자체가 GPT-4 수준의 똑똑한 추론 능력을 전제로 튜닝되어 있음. 비용 절감을 위해 GPT-3.5나 로컬 작은 모델을 채점관으로 쓰면 지표가 완전히 망가짐.
  - **대응 전략**: Ragas 내부의 `Evaluator` 클래스 프롬프트를 튜닝하거나, 사내 인프라에서 Prometheus 모델(평가 특화 13B LLM)과 같은 전문 Judge 모델을 로컬에 호스팅하여 채점 정합성과 비용 문제를 동시 해결.
- **리스크 2: 높은 API 호출 및 시간 오버헤드**:
  - 1개의 QA 쌍을 4개 지표로 평가할 때 다수의 프롬프트 체인이 발생하여 시간이 오래 걸림.
  - **대응 전략**: 전체 테스트셋이 아닌, K-Means 클러스터링으로 사용자 질의 토픽을 분류한 후 토픽별 대표 샘플링 데이터(Stratified Sampling) 5~10%에 대해서만 Ragas를 비동기 병렬 실행.

## Ⅵ. 실무 적용 및 결론
- **판단 지표**: Human-LLM 상관계수(Correlation), 4대 지표(Threshold 0.85 이상 여부).
- **실무 설계**: 기업형 IT 헬프데스크 챗봇 MLOps 환경 구축. 개발팀이 BGE-M3 인코더 파인튜닝 버전을 새로 커밋(Commit)함. Github Actions에서 Ragas 라이브러리가 트리거되어, 사전에 준비된 500개의 골든 데이터셋(Golden Dataset)으로 자동 평가 수행. 기존 모델 대비 Context Recall이 0.72 $\rightarrow$ 0.89로 상승했으나, 토큰 짤림 현상으로 Faithfulness가 0.80 미만으로 떨어짐을 발견. 배포 게이트(Release Gate)에서 이를 차단(Reject)하고 슬랙 알림 발송.
- **결론**: Ragas는 'LLM을 평가하기 위해 LLM을 쓴다'는 현대 AI 공학의 역설을 가장 성공적으로 실체화한 도구이며, 감과 눈대중에 의존하던 RAG 파이프라인 개발을 데이터 기반의 엔지니어링(Data-driven Engineering) 영역으로 승격시킨 핵심 인프라임.

### 🔀 문제 유형별 목차 전환
- **Ⅱ·Ⅲ 강조 (개념/원리형)**: Answer Relevancy 측정을 위한 코사인 임베딩 추출 워크플로, Faithfulness의 명제 추출(Statement Extraction) 및 NLI Entailment 논리 수식 중심 서술.
- **Ⅴ·Ⅵ 강조 (실무/설계형)**: LangSmith, MLflow와의 로깅 인테그레이션(Integration) 방안, CI/CD 파이프라인 내에서의 Release Gate 임계치(Threshold) 설정 튜닝 전략 작성.
