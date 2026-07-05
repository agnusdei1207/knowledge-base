---
title: "사내망 RAG (Private RAG)"
date: "2026-07-05"
author: "Claude Opus 4.6 (Enhanced by Gemini 3.5)"
tags:
  - "cspe-08_latest_tech"
weight: 137
---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **핵심 직관** | 인트라넷. 우리 집 거실에서만 돌아가는 개인용 컴퓨터 | "핵심 기술 요소" |
| **배경** | 초기 LLM 시장은 초거대 파라미터가 필요한 SaaS 중심이었음 | "소프트웨어 구독" |
| **구체 예시** | 한국군(국방부)에서 작전 교범 파일(비밀 문서)을 검색하는 챗봇을 만듦 | "핵심 기술 요소" |
| **sLLM (Small LLM) / 오픈소스 모델** | Private RAG 구축의 핵심 심장 | "핵심 기술 요소" |
| **vLLM / TGI (추론 최적화)** | 사내 GPU의 한정된 자원을 쥐어짜서 빠르게 답변을 뱉어내게 만드는 런타임 엔진 | "그래픽 전문 두뇌" |
| **Data Sovereignty (데이터 주권)** | 데이터가 해외 서버에 저장되지 않고 자국/자사 내에 머물러야 한다는 컴플라이언스 원칙 | "핵심 기술 요소" |
| **모델 경량화 (Quantization)** | - 70B 모델을 그대로 올리면 GPU 메모리(VRAM) 수백 GB가 필요함 | "그래픽 전문 두뇌" |

---


# 📖 【암기용】 개념 완전 이해

## 한눈에
- **정의**: 외부 인터넷과 완전히 단절된 사내 폐쇄망(On-Premise) 또는 논리적으로 격리된 프라이빗 클라우드(VPC) 내부에 LLM 모델부터 Vector DB까지 모든 컴포넌트를 구축하여 구동하는 RAG 아키텍처.
- **필요성**: OpenAI(ChatGPT)나 Anthropic의 API를 쓰면 성능은 좋지만, 사내 기밀문서나 고객의 개인정보(PII)가 외부 서버로 넘어가기 때문에 국방, 금융, 공공기관에서는 법적으로/보안상 절대 사용할 수 없음.
- **핵심 직관**: 인트라넷. 우리 집 거실에서만 돌아가는 개인용 컴퓨터. 외부로 데이터가 1바이트도 나가지 않아 해킹이나 데이터 유출 걱정 없이 마음껏 기밀문서를 먹여서 학습시키고 검색할 수 있음.

## 깊이 이해
- **배경**: 초기 LLM 시장은 초거대 파라미터가 필요한 SaaS 중심이었음. 그러나 Llama 3, Mistral, EEVE(한국어) 등 오픈소스 sLLM(소형 LLM)의 눈부신 발전과 vLLM 등 추론 최적화 프레임워크의 등장으로, 기업이 자체 GPU 서버 1~2대만으로도 충분히 고성능의 RAG를 돌릴 수 있는 환경이 조성됨.
- **작동 원리 (API 호출 통제)**:
  1. (기존 SaaS RAG): 텍스트 $\rightarrow$ (인터넷) $\rightarrow$ OpenAI 임베딩 API $\rightarrow$ Vector DB $\rightarrow$ (인터넷) $\rightarrow$ OpenAI GPT-4 API $\rightarrow$ 답변
  2. (Private RAG): 텍스트 $\rightarrow$ **사내 허깅페이스 임베딩 모델** $\rightarrow$ 사내 Milvus DB $\rightarrow$ **사내 GPU 서버의 오픈소스 LLM** $\rightarrow$ 답변. (전 구간 오프라인).
- **구체 예시**: 한국군(국방부)에서 작전 교범 파일(비밀 문서)을 검색하는 챗봇을 만듦. 국방망은 인터넷이 끊겨 있으므로 ChatGPT 불가. 사내 데이터센터에 GPU 서버를 사고, Llama 3를 양자화(Quantization)하여 올린 뒤 Private RAG를 구축함.
- **흔한 오해/주의점**: "Private RAG 구축하면 무조건 안전하니까 보안 필터 안 걸어도 되지?" $\rightarrow$ 아님! '외부'로 안 새어나갈 뿐이지, '내부' 직원들끼리의 권한 통제(Permission-aware)는 여전히 필수임. 사원이 사장님 연봉 문서를 보면 안 됨.

## 연결 개념
- **sLLM (Small LLM) / 오픈소스 모델**: Private RAG 구축의 핵심 심장. 파라미터 수가 7B ~ 70B 수준으로 단일 GPU 서버에 올라가는 모델.
- **vLLM / TGI (추론 최적화)**: 사내 GPU의 한정된 자원을 쥐어짜서 빠르게 답변을 뱉어내게 만드는 런타임 엔진.
- **Data Sovereignty (데이터 주권)**: 데이터가 해외 서버에 저장되지 않고 자국/자사 내에 머물러야 한다는 컴플라이언스 원칙.

---

# 📝 【답안용】 시험 답안 템플릿
## 핵심 인사이트 (3줄 요약)
- **본질**: 퍼블릭 클라우드 LLM API의 의존성을 배제하고, 기업의 온프레미스(On-premise) 망분리 환경 또는 전용 VPC 내에 오픈소스 LLM, 로컬 임베딩 모델, Vector DB를 내재화(Internalize)하여 구축한 RAG 아키텍처.
- **가치**: 고객 개인식별정보(PII) 및 기업 극비 영업자산(Trade Secret)의 외부 반출을 물리적/논리적으로 원천 차단하여 완전한 데이터 주권(Data Sovereignty)과 규제 준수(Compliance)를 확보함.
- **판단 포인트**: 클라우드 API 대비 모델 파라미터 크기 한계로 인한 성능 저하(환각 증가)와 초기 GPU 인프라 구축 비용(CAPEX) 발생의 트레이드오프를 극복하기 위해, PEFT(파인튜닝) 기반 도메인 지식 주입 및 추론 최적화(vLLM, 양자화) 기술 역량이 필수적임.

## Ⅰ. 개요 및 필요성
- **정의**: 데이터 수집, 청킹, 임베딩 벡터화, 의미론적 검색, 텍스트 생성에 이르는 RAG의 전(全) 생애주기 파이프라인이 외부망 통신 없이 기업 통제하의 격리된 네트워크에서 수행되는 시스템.
- **배경**: OpenAI API 등 퍼블릭 SaaS 모델은 사용자의 프롬프트와 검색된 Context가 서비스 제공자의 로그에 남거나 훈련 데이터로 유용될 수 있는 치명적 보안 리스크(Data Breach)가 존재함.
- **필요성**: 금융보안원 가이드라인, 공공 망분리 규제, 국방부 보안 규정 등 최고 수준의 기밀성을 요구하는 Mission-critical 도메인에서 생성형 AI 기술을 합법적이고 안전하게 도입하기 위함.

## Ⅱ. Private RAG의 핵심 컴포넌트 내재화 (Internalization)
SaaS 의존 컴포넌트들을 모두 오픈소스 및 로컬 생태계로 대체함.
| 컴포넌트 | Public SaaS RAG | Private RAG (망분리 환경) | 핵심 도입 기술 및 프레임워크 |
|:---:|:---|:---|:---|
| **임베딩 (Embedding)** | OpenAI `text-embedding-3` | **로컬/사내 임베딩 모델** | BGE-m3, KR-SBERT 등 오픈소스 한국어 임베딩 모델 (HuggingFace 호스팅) |
| **저장소 (Vector DB)** | Pinecone (SaaS) | **설치형 Vector DB** | Milvus, Qdrant, pgvector (사내 온프레미스 서버 또는 VM 인스턴스) |
| **추론 (Generation)** | GPT-4o, Claude 3.5 | **로컬 sLLM 기반 추론 서버** | Llama 3 (8B/70B), EEVE-10.8B + **추론 엔진(vLLM, TGI, Ollama)** |
| **인프라 환경** | Public Internet | **Air-gapped / VPC** | 물리적 망분리 인프라, 전용 HSM(키 관리), 사내 SSO 연동 |

## Ⅲ. Private 구축의 기술적 난제와 해결 방안 (Optimization)
로컬 인프라는 GPU 자원이 한정되어 있으므로 '가벼우면서도 똑똑하게' 만드는 최적화가 필수적임.
1. **모델 경량화 (Quantization)**:
   - 70B 모델을 그대로 올리면 GPU 메모리(VRAM) 수백 GB가 필요함. 이를 해결하기 위해 FP16(16비트) 모델의 가중치를 INT8 또는 INT4(4비트)로 압축하는 **AWQ/GPTQ** 양자화 기법을 적용하여 메모리 사용량을 1/4 수준으로 절감.
2. **추론 속도 극대화 (vLLM & PagedAttention)**:
   - 다수의 사내 직원이 동시에 질문할 경우 GPU 메모리 병목으로 서버가 터지는 현상 방지. **PagedAttention** 메모리 페이징 기술을 탑재한 `vLLM`을 적용하여 처리량(Throughput)을 수십 배 향상.
3. **도메인 특화 성능 향상 (PEFT & LoRA)**:
   - 오픈소스 sLLM은 GPT-4보다 기본 상식이 부족함. 부족한 성능을 메우기 위해 사내 특화 용어 및 규정 데이터셋으로 가벼운 **LoRA 미세조정(Fine-Tuning)**을 수행하여 해당 도메인에서의 답변 정확도를 극대화.

## Ⅳ. 보안성 검토: Private RAG의 보안 아키텍처
- **Data in Transit (전송 중 보호)**: 모든 내부 API 통신(Retriever $\leftrightarrow$ LLM 서버) 구간을 mTLS(상호 인증 TLS)로 암호화.
- **Data at Rest (저장 데이터 보호)**: Vector DB에 적재된 임베딩 벡터 및 메타데이터, LLM의 가중치 파일을 사내 KMS(Key Management System)를 통한 AES-256 암호화 적용.
- **Logging & Auditing**: 허용된 사내망 밖으로 나가는 Outbound Traffic을 방화벽단에서 전면 차단하고, LLM의 프롬프트 입출력 내역은 전량 SIEM(통합보안관제)으로 포워딩.

## Ⅴ. 실무 적용 및 결론
- **판단 지표**: TCO(총 소유 비용, 3년 단위 CAPEX/OPEX 비교), 보안 컴플라이언스(ISMS) 위반 건수 0건, P95 응답 지연 시간(Latency < 3sec).
- **실무 설계**: 국내 A생명보험사 고객 약관 QA 챗봇 시스템. 금융망분리 가이드라인에 따라 외부 SaaS 접근 전면 불가 상태. 온프레미스 망 내에 NVIDIA A100 GPU 서버 2대를 증설. 한국어 특화 `EEVE-Korean-10.8B` 오픈소스 모델을 도입하고, vLLM을 활용해 서빙 인프라 구축. 검색 엔진으로는 설치형 Elasticsearch(BM25)와 FAISS 기반 하이브리드 검색 적용. 배포 전 Red-teaming(모의 해킹)을 통해 사내 데이터 밖으로의 정보 유출이 구조적으로 불가능함을 증명 후 상용화 오픈 완료.
- **결론**: Private RAG는 단순히 '모델을 내부에 설치했다'는 인프라적 개념을 넘어, 오픈소스 생태계의 민주화(Democratization)와 추론 최적화 기술의 발전이 맞물려 탄생한, 엔터프라이즈 AI의 가장 현실적이고 주권적인(Sovereign) 진화 형태이다.

### 🔀 문제 유형별 목차 전환
- **Ⅱ·Ⅲ 강조 (개념/원리형)**: sLLM 서빙을 위한 vLLM의 PagedAttention 메모리 관리 메커니즘과 AWQ/GPTQ 양자화 모델 적용 시 발생하는 성능(Perplexity)과 메모리 간의 트레이드오프 수리적 분석.
- **Ⅴ·Ⅵ 강조 (실무/설계형)**: 퍼블릭 SaaS 모델(GPT-4 API)과 Private sLLM 구축 모델 간의 3년 TCO(Total Cost of Ownership) 기반 BEP(손익분기점) 교차점 분석 및 망분리 규제(금융/공공) 환경 하의 보안 참조 아키텍처 다이어그램 제시.
