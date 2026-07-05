---
title: "권한인지 RAG (Permission-aware RAG)"
date: "2026-07-05"
author: "Claude Opus 4.6 (Enhanced by Gemini 3.5)"
tags:
  - "cspe-08_latest_tech"
weight: 136
---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **권한인지 RAG** | 권한인지 RAG (Permission-aware RAG)의 핵심 개념 | 이 주제의 본질 |

---

# 📖 【암기용】 개념 완전 이해

## 한눈에
- **정의**: 검색증강생성(RAG) 파이프라인에서 벡터 검색을 수행할 때, 사용자의 신분(직급, 부서, 프로젝트)에 따라 "읽을 권한이 있는 문서(ACL)만 검색되도록" 필터링을 강제하는 보안 아키텍처.
- **필요성**: RAG가 대유행하면서 사내 모든 문서를 Vector DB에 쏟아부었는데, 인턴 사원이 "우리 회사 연봉 테이블 알려줘"라고 치면 대표이사 연봉 문서까지 찾아와 답변해버리는 끔찍한 정보 유출(Data Breach) 사태를 막기 위함.
- **핵심 직관**: 출입증 기반 서고 출입. 도서관 사서(AI)에게 책을 찾아달라고 할 때, 사서는 내 사원증(Token)을 먼저 확인하고, 내가 들어갈 수 있는 열람실(Permission)에 있는 책만 뒤져서 답변해 줌.

## 깊이 이해
- **배경**: 초기 오픈소스 RAG 프레임워크(LangChain 등)는 오직 "질문과 의미가 비슷한가?(Cosine Similarity)"만 따졌음. 그러나 엔터프라이즈 환경에서는 '의미'보다 **'보안(Security)'**이 1순위임. Vector DB 벤더(Milvus, Qdrant 등)들이 앞다퉈 메타데이터 필터링 기능을 탑재하며 기술이 성숙함.
- **작동 원리 (Pre-filtering 방식 기준)**:
  1. **인제스천(Ingestion)**: PDF 문서를 Chunk로 쪼갤 때, 사내 그룹웨어(AD)와 연동하여 문서의 소유자 권한(`allowed_roles: ["HR", "C-Level"]`)을 메타데이터로 함께 저장함.
  2. **쿼리(Querying)**: 사용자가 질문할 때, 세션의 JWT 토큰에서 사용자 Role(`role: "Intern"`)을 추출함.
  3. **권한 필터링(Filtering)**: Vector DB가 유사도를 계산하기 직전, `allowed_roles`에 "Intern"이 없는 문서는 검색 대상에서 아예 누락(Drop)시킴.
  4. **생성(Generation)**: 권한이 있는 안전한 문서들로만 Context가 구성되어 LLM에 전달됨.
- **구체 예시**: 병원 의료 기록 RAG. 간호사가 "A환자 병력 요약해 줘"라고 하면, 간호사 권한(간호 기록) 내의 문서만 참고해 요약함. 의사가 동일한 질문을 하면, 의사 권한(진단서, 처방전, 간호 기록 모두 포함)을 바탕으로 훨씬 깊은 전문적인 요약을 제공함.
- **흔한 오해/주의점**: "일단 다 검색해서 LLM한테 주고, 마지막에 마스킹(Post-filtering)하면 되지 않나?" $\rightarrow$ 절대 안 됨! LLM은 똑똑해서 문맥을 읽고 숨겨진 내용을 유추(환각)해버릴 수 있고, 프롬프트 인젝션 공격에 뚫리면 뱉어버림. 무조건 검색하기 전에 쳐내는 **사전 필터링(Pre-filtering)**이 정석임.

## 연결 개념
- **RBAC / ABAC**: 역할 기반, 속성 기반 접근 통제. 이 정책들이 Vector DB 메타데이터에 매핑됨.
- **Vector DB Metadata Filtering**: 임베딩 벡터 옆에 달린 JSON 속성값을 이용해 검색 범위를 좁히는 기술.
- **Enterprise RAG**: 권한인지 RAG는 엔터프라이즈 RAG가 되기 위한 가장 크고 중요한 필수 조건임.

---

# 📝 【답안용】 시험 답안 템플릿
## 핵심 인사이트 (3줄 요약)
- **본질**: RAG의 정보 검색(Information Retrieval) 계층에 기업의 IAM(Identity and Access Management) 기반 접근 통제 목록(ACL) 정책을 메타데이터 속성으로 주입하여, 권한이 부여된 지식 객체만 언어 모델의 문맥으로 승급시키는 보안 아키텍처.
- **가치**: 대규모 내부망 데이터 레이크(Data Lake)를 LLM과 연동할 때 발생하는 치명적인 내부자 권한 상승(Privilege Escalation) 및 수평적 정보 탈취 리스크를 원천 차단하여 Zero Trust AI 환경을 구현함.
- **판단 포인트**: 사후(Post)가 아닌 사전 필터링(Pre-filtering) 전략 채택, IAM과의 실시간 메타데이터 동기화(CDC), 그리고 권한 우회 시도를 모니터링하는 감사 로그(Audit Trail) 아키텍처 설계가 보안 컴플라이언스 만족의 핵심임.

## Ⅰ. 개요 및 필요성
- **정의**: 검색증강생성 아키텍처에서 사용자(User Entity)의 인가(Authorization) 컨텍스트를 Vector Search 쿼리에 동적으로 결합하여, 허용된 지식(Allowed Knowledge) 내에서만 의미론적 검색 및 생성을 수행하는 기술.
- **배경**: 시맨틱 검색(Semantic Search)은 텍스트의 코사인 유사도에만 의존하므로, 기존 IT 시스템의 디렉토리/테이블 단위 물리적 망분리 및 접근 제어 메커니즘을 무력화하는 보안 사각지대를 발생시킴.
- **필요성**: PII(개인식별정보), 임원 기밀, 부서별 영업 비밀 등을 다루는 Enterprise AI 환경에서, 정보 자산의 기밀성(Confidentiality)을 훼손하지 않고 전사적 검색 경험을 제공하기 위한 필수 방어선임.

## Ⅱ. 권한 인지 아키텍처 매커니즘 (IAM 연동 기반)
Vector DB의 메타데이터 필터링(Metadata Filtering) 기능을 활용한 동적 쿼리 조합.
1. **ACL Metadata Ingestion (권한 색인화)**:
   - 문서 파싱 및 Chunking 시, 사내 Active Directory(AD)의 그룹/권한 정보를 매핑.
   - Vector DB 저장 구조: `{ vector: [0.12, 0.5...], metadata: {"doc_id": "1", "acl_groups": ["HR_Admin", "C_level"]} }`
2. **Context-aware Query Construction (쿼리 재구성)**:
   - 사용자가 시스템 로그인 시 발급받은 JWT/SAML 토큰에서 Role Claim을 추출.
   - 자연어 쿼리("인사평가 기준은?") $\rightarrow$ Vector 쿼리 변환 시 필터 조건(`WHERE "HR_Admin" IN acl_groups`)을 강제 삽입.
3. **Pre-filtering & Retrieval (사전 필터링)**:
   - Vector DB의 검색 엔진 구조(HNSW 등)에서 인덱스 순회 전/중간 단계에 필터를 적용하여 인가되지 않은 벡터를 배제함.

## Ⅲ. 필터링 전략 비교: Pre-filtering vs Post-filtering
보안과 성능(Recall) 간의 트레이드오프 관점.
| 구분 | Pre-filtering (사전 필터링) [권장] | Post-filtering (사후 필터링) [지양] |
|:---:|:---|:---|
| **동작 방식** | 코사인 유사도 연산 **전에** 메타데이터 필터를 먼저 걸어 대상 모집단을 축소함. | 코사인 유사도로 Top-K(예: 10개)를 뽑은 **후**, 권한 없는 문서를 버림. |
| **보안 무결성**| 절대적인 권한 통제 보장 (Zero Leakage). | 권한 없는 문서가 LLM에 넘어갈 잠재적 위험 잔존. |
| **성능(Recall)** | 모집단 축소로 HNSW 그래프 탐색 시 노드 고립(Recall Drop) 현상 발생 가능. | Top-10 중 8개가 권한 미달로 버려지면, LLM에 2개만 전달되어 답변 불능 사태 발생. |
| **대응책** | 필터 적용 후 시맨틱 탐색을 수행하는 최신 Vector DB(Milvus, Pinecone) 기능 활용. | Top-K를 극단적으로 크게(예: 100) 잡아 보완. |

## Ⅳ. 고도화: 동적 권한 동기화 및 보안 감사 (Audit)
사내 권한은 수시로 변경되므로 지속적 동기화가 생명임.
1. **CDC 기반 실시간 권한 동기화 (Event-driven Sync)**:
   - 그룹웨어에서 직원이 퇴사하거나 부서가 이동될 때, Kafka 등 메시지 큐를 통해 이벤트를 수신하고 즉각적으로 Vector DB의 메타데이터를 업데이트(Upsert)하는 파이프라인 구축.
2. **보안 감사 추적성 (Audit Trail)**:
   - 질의(Query) $\rightarrow$ 검색된 Doc ID $\rightarrow$ 사용자 권한 토큰 $\rightarrow$ 거절된 Doc ID 이력을 WORM(Write-Once-Read-Many) 스토리지에 적재하여, 추후 정보 유출 사고 시 포렌식 자료로 활용.

## Ⅴ. 실무 적용 및 결론
- **판단 지표**: False Positive Rate (미인가자에게 정보 제공된 비율 - **0% 필수**), ACL 동기화 지연 시간(SLA: 5분 이내).
- **실무 설계**: A증권사 컴플라이언스 위반 탐지 및 규정 안내 챗봇. 금융망 특성상 정보 격벽(Chinese Wall)이 존재하여, IB 부서와 리서치 부서의 정보가 섞이면 안 됨. LlamaIndex의 `VectorStoreQueryMode.DEFAULT`에 `MetadataFilters` 모듈을 결합하여 RBAC 적용. 사용자의 부서 코드를 SAML 토큰에서 추출해 Vector DB(Qdrant)의 payload에 `부서_ID` 매칭 필터를 강제로 끼워 넣음. 그 결과 부서 간 정보 교차 유출 건수 0건 달성 및 금감원 보안 심사 무결점 통과.
- **결론**: 권한인지 RAG는 AI의 지능(Intelligence)에 조직의 위계(Hierarchy)와 보안 규칙을 이식하는 수술이며, 이는 기술적 선택이 아니라 엔터프라이즈 AI 서비스 상용화를 위한 최소한의 법적/윤리적 입장권(Ticket)이다.

### 🔀 문제 유형별 목차 전환
- **Ⅱ·Ⅲ 강조 (개념/원리형)**: HNSW 알고리즘 내에서 Pre-filtering 수행 시 발생하는 노드 고립(Disconnected Graph) 문제와 이를 해결하기 위한 Vector DB 벤더들의 내부 파이프라인 최적화 기술 비교 중심 서술.
- **Ⅴ·Ⅵ 강조 (실무/설계형)**: ABAC(Attribute-Based Access Control)를 적용한 세밀한(Fine-grained) 청크 단위 필터링 설계, IAM/SSO(OIDC, SAML) 아키텍처와의 런타임 토큰 연동 아키텍처 다이어그램 제시.
