---
sidebar:
  order: 78
  label: "078. AI 보안 위협 전체 구조 (AI Security Threat Landscape)"
  badge:
    text: "기출 • 85%"
    variant: note
title: "AI 보안 위협 전체 구조 (AI Security Threat Landscape)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-security"
weight: 78
extra:
  question_no: "078"
  source_status: "기출"
  source_history: "135회, 137회, 138회"
  priority: 85
  priority_note: "135•137•138회 반복된 AI 보안 위협 우산 주제임"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **인공지능 보안 위험관리(Artificial Intelligence Security Risk Management, AI Security RMF)**: 데이터 수집, 모델 학습, 배포, 추론, 에이전트 도구 연동 전 수명주기에서 발생하는 보안 위험을 체계적으로 식별, 평가, 통제하는 가버넌스 프레임워크이다.
- **모델 고유 위협(Model-specific Threat)**: 데이터 오염(Poisoning), 모델 역공학(Model Inversion), 프롬프트 인젝션, 환각(Hallucination) 오용 등 기존 애플리케이션 보안으로는 차단 불가능한 AI 고유 취약성이다.

</details>

- 정의/개념: AI 보안 위협 전체 구조는 머신러닝/생성형 AI 시스템의 파이프라인(Data, Model, Application, Agent) 전반에 걸친 공격 파생 경로와 이에 대응하는 입체적 방어 통제 프레임워크이다.
- 배경/필요성: 전통적 IT 보안(네트워크, OS, Web) 중심 통제만으로는 LLM 및 AI 에이전트 도입에 따른 데이터 유출, 모델 탈취, 비인가 외부 도구 명령 실행 위협을 막을 수 없기 때문이다.

#### 한줄 요약

- AI 파이프라인 전 생명주기(데이터, 모델, 애플리케이션, 에이전트 도구)의 위협을 가시화하고 입체적 보안 방어를 수립하는 프레임워크이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **데이터 계보(Data Lineage)**: 학습 데이터의 수집 출처, 정제 과정, 라벨링 변경 이력을 추적하여 데이터 오염을 방지하는 무결성 관리 기술이다.
- **모델 가중치(Model Weights)**: AI 모델의 지적재산권(IP) 핵심으로, 파라미터 유출 및 비인가 추출 공격(Model Extraction)의 핵심 보호 대상이다.
- **프롬프트 경계(Prompt Boundary)**: 시스템 프롬프트(System Instruction)와 사용자 입력(User Input)을 암호학적/논리적으로 격리하는 입력 검증 통제선이다.
- **검색 증강 생성 경계(Retrieval-Augmented Generation Boundary, RAG Boundary)**: 외부 벡터 DB에서 조회된 비신뢰 문서 데이터를 모델의 시스템 명령어로 오해하지 않도록 구획하는 경계이다.
- **도구 경계(Tool Boundary)**: AI 에이전트가 외부 API/DB/시스템 명령을 실행할 때 사용자의 권한 범위를 넘지 않도록 제한하는 런타임 통제선이다.
- **지속 위험 관리(Continuous Risk Management)**: 레드팀(Red Teaming) 평가와 런타임 방화벽(Guardrails) 탐지를 연계하여 위협 모델을 상시 업데이트하는 주기적 통제 체계이다.

</details>

- **데이터 계보** 관리와 **모델 가중치** 암호화를 통해 학습 자산의 무결성과 기밀성을 보존한다.
- **프롬프트 경계**, **RAG 경계**, **도구 경계**의 3중 신뢰 경계(Trust Boundary)를 수립하여 인젝션 및 비인가 명령 실행을 격리한다.
- 적대적 평가(Red Teaming)와 가드레일(Guardrails) 모니터링을 통합한 **지속 위험 관리**를 집행한다.

#### 한줄 요약

- 데이터/모델 자산 보호, 프롬프트/RAG/도구 3중 신뢰 경계 수립 및 지속적 AI 레드팀 위험 관리 체계로 구성된다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **데이터 공급망(Data Supply Chain)**: 데이터 수집, 크롤링, 라벨링, 전처리를 포함하는 데이터 유입 파이프라인 영역이다.
- **모델 공급망(Model Supply Chain)**: 오픈소스 파운데이션 모델 수용, 파인튜닝, 가중치 저장소(HuggingFace 등) 검증 영역이다.
- **적대적 평가(Adversarial Red Teaming)**: AI 모델을 대상으로 탈옥(Jailbreak), 인젝션, 민감정보 추출 공격을 가해 보안 한계를 시험하는 평가 기법이다.
- **외부 통신 통제(Egress Control)**: AI 애플리케이션 및 에이전트 모듈의 비인가 외부 C2 서버 통신 및 데이터 유출을 네트워크 수준에서 차단하는 통제이다.

</details>

```text
[AI 보안]
    |
    +-- [데이터 거버넌스]
    +-- [모델 공급망]
    +-- [응용 신뢰 경계]
    +-- [도구·권한 통제]
    `-- [평가·운영 대응]
```

선의 의미: 데이터 거버넌스, 모델 공급망, 애플리케이션 경계, 도구/권한 통제 및 운영 평가 대응을 연계한 종합 AI 보안 아키텍처이다.

| 도메인 계층 | 핵심 통제 요소 | 보호 목적 |
|:---|:---|:---|
| 데이터 거버넌스 | **데이터 공급망** 검증, **데이터 계보** 추적, PII 필터링 | 학습 데이터 오염(Poisoning) 및 개인정보 유입 방지 |
| 모델 공급망 | **모델 공급망** 가중치 서명 검증, 백도어 스캐닝, 가중치 암호화 | 악성 모델 배포 차단 및 모델 도용/추출 방지 |
| 응용 신뢰 경계 | **프롬프트 경계** 격리, **RAG 경계** 가드레일 적용 | 직접/간접 프롬프트 인젝션 및 탈옥 차단 |
| 도구·권한 통제 | **도구 경계** 런타임 샌드박싱, **외부 통신 통제** | AI 에이전트의 권한 남용 및 비인가 API 호출 방지 |
| 평가·운영 대응 | **적대적 평가** (Red Teaming), LLM WAF 모니터링 | 신종 바이패스 기법 탐지 및 상시 피드백 보정 |

#### 한줄 요약

- 데이터거버넌스, 모델공급망, 응용경계, 도구권한통제 및 적대적 평가의 5대 도메인을 연계하여 AI 시스템을 보호한다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **접근 제어 목록 기반 검색(Access Control List-based Retrieval, ACL-based Retrieval)**: RAG 벡터 검색 시 요청 사용자의 접근 권한(ACL)이 인가된 문서 조각만 벡터 스페이스에서 추출하는 통제이다.
- **승인 범위 도구 호출(Policy-bounded Tool Execution)**: AI 에이전트의 외부 액션이 사용자의 사전 인가 정책 범위를 이탈하지 못하도록 런타임에 2차 검증하는 단계이다.
- **사용자•권한 맥락 검증(User & Permission Context Verification)**: 주체 신원과 요청 작업의 인가 범위를 대조하는 단계이다.
- **ACL•출처 기반 문서 선별(ACL & Provenance-based Document Selection)**: RAG 검색 대상 문서의 권한과 무결성을 1차 검증하는 단계이다.
- **지시•비신뢰 문맥 분리(Instruction & Untrusted Context Separation)**: 사용자 프롬프트와 검색된 외부 문맥 데이터를 인젝션 방지 프레임으로 분리 구성하는 단계이다.
- **응답•도구 제안 생성(Response & Tool Candidate Generation)**: LLM이 텍스트 응답 또는 외부 API 호출 명령 인자를 도출하는 단계이다.
- **내용•권한•민감도 정책 검증(Content, Permission & Sensitivity Policy Verification)**: LLM 출력의 PII 유출, 환각, 비인가 명령 포함 여부를 최종 심사하는 단계이다.

</details>

```text
[사용자 입력·권한 맥락]
          |
          v
1. 사용자·권한 맥락 검증
          |
          v
2. ACL·출처 기반 문서 선별
          |
          v
3. 지시·비신뢰 문맥 분리
          |
          v
4. 응답·도구 제안 생성
          |
          +-- 응답만 ------> [제한된 응답]
          |
          `-- 도구 호출 제안
                    |
                    v
          5. 내용·권한·민감도 정책 검증
                    |
                    v
          [승인 범위 도구 호출]
                    |
                    `-- 도구 실행 결과
                              |
                              v
                        [제한된 응답]
```

### 동작 원리

1. **사용자•권한 맥락 검증**: 사용자 요청의 IAM 신원 및 인가 범위를 확인한다.
2. **ACL•출처 기반 문서 선별**: RAG 연동 시 사용자의 ACL 권한을 벗어나는 민감 문서는 검색 결과에서 철저히 제외한다.
3. **지시•비신뢰 문맥 분리**: 입력 프롬프트와 RAG 검색 문서를 별도 태그 영역으로 격리하여 지시 세조종(Hijacking)을 막는다.
4. **응답•도구 제안 생성**: LLM이 추론 결과를 도출하거나 외부 시스템 연동 Tool Call을 생성한다.
5. **내용•권한•민감도 정책 검증**: LLM Guardrail이 출력의 개인정보 포함 여부를 파악하고, **승인 범위 도구 호출**을 런타임 집행한다.

#### 한줄 요약

- 사용자 맥락 검증, ACL 문서 선별, 지시/문맥 분리, Guardrail 출력 심사 및 승인 범위 도구 호출로 보안 추론을 완성한다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **데이터 오염(Data Poisoning)**: 학습 데이터셋에 편향되거나 오염된 샘플을 주입하여 모델 추론 정확도를 떨어뜨리거나 백도어를 심는 공격이다.
- **백도어(Backdoor Attack)**: 특정 핑거프린트/트리거(Trigger) 입력이 들어올 때만 공격자가 지정한 악성 동작을 수행하도록 가중치를 조작하는 공격이다.
- **가중치 탈취(Weight Exfiltration)**: 배포된 AI 모델 파일이나 메모리에 직접 접근하여 가중치를 무단 복제/도용하는 위협이다.
- **인젝션(Prompt Injection)**: LLM 추론 시 악의적 텍스트를 입력하여 시스템 프롬프트를 무력화하고 인가되지 않은 조작을 유도하는 공격이다.

</details>

| 공격 대상 도메인 | 주요 위협 유형 | 대표 공격 기법 | 핵심 대응 방안 |
|:---|:---|:---|:---|
| Data Level | **데이터 오염**, **백도어** 주입 | Poisoning, Trigger 주입, Label 변조 | **데이터 계보** 검증, Sanitization, PII 필터링 |
| Model Level | **가중치 탈취**, 모델 추출, 멤버십 추론 | Model Inversion, Model Extraction | 가중치 암호화, TEE 격리, API Rate Limit |
| Application Level | Direct/Indirect **인젝션**, 탈옥 | Prompt Injection, Jailbreak | 시스템/사용자 프롬프트 격리, LLM WAF 가드레일 |
| Agent Level | 비인가 시스템 조작, C2 데이터 반출 | Tool Execution Hijacking, SSRF | 최소 권한 IAM, **승인 범위 도구 호출**, **외부 통신 통제** |

#### 한줄 요약

- Data, Model, Application, Agent의 4개 레벨로 AI 위협을 세분화하고 레벨별 맞춤형 보안 통제를 격자 적용한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **미국 국립표준기술연구소(National Institute of Standards and Technology, NIST)**: AI 보안 및 표준 규격을 제정하는 글로벌 표준화 기관이다.
- **위험관리 프레임워크(Risk Management Framework, RMF)**: 위험을 식별, 평가, 대응, 모니터링하는 표준 위험 관리 프레임워크이다.
- **NIST AI 100-1 AI RMF 1.0 (NIST Artificial Intelligence Risk Management Framework 1.0, AI 100-1)**: AI 시스템의 안전성, 신뢰성, 기밀성을 관리하기 위한 NIST 4대 핵심 기능(Govern, Map, Measure, Manage) 프레임워크이다.
- **NIST AI 600-1 생성형 AI 프로파일(NIST Generative AI Profile, AI 600-1)**: 생성형 AI 및 LLM의 특수 위협(환각, 딥페이크, 프롬프트 인젝션)에 맞춰 AI RMF 1.0을 구체화한 지침이다.
- **최소 권한(Least Privilege)**: AI 에이전트에 필요한 최소한의 API 기능 및 DB 읽기 전용 권한만 부여하는 원칙이다.
- **사람 승인(Human-in-the-loop Approval)**: 금융 이체, DB 삭제 등 고위험 에이전트 액션 실행 시 최종 인간의 서명 승인을 요구하는 통제 방식이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| AI 전사 위험 관리 프레임워크 부재 | **NIST AI 100-1 AI RMF 1.0** 준용 | Govern, Map, Measure, Manage 기반 조직적 AI 위험 거버넌스 확립 |
| 생성형 AI 및 LLM 고유 위협 대응 미비 | **NIST AI 600-1 생성형 AI 프로파일** 매핑 | LLM 환각, 프롬프트 인젝션, 딥페이크 위협의 체계적 측정 및 대응 |
| AI 에이전트의 비인가 시스템 조작 사고 | **최소 권한** 설정 및 **사람 승인** 절차 강제 | 고위험 액션의 독단적 자동 실행 차단 및 인프라 보호 |

#### 한줄 요약

- NIST AI RMF 1.0 및 AI 600-1 프로파일을 준수하여 AI 위험 거버넌스를 정립하고, Human-in-the-loop 절차를 결합한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **AI 신뢰 경계 유지(AI Trust Boundary Maintenance)**: 데이터 수집부터 LLM 추론 및 에이전트 실행까지 전체 영역에서 데이터 출처와 권한 한계를 지속 유지하는 상태이다.
- **배포•실행 차단 기준(Deployment & Execution Gate Criteria)**: 검증되지 않은 모델 배포를 막고, 위험 도구 호출 시 승인을 강제하는 보안 관문 지침이다.

</details>

- **배포•실행 차단 기준**을 적용하여 전 수명주기 동안 **AI 신뢰 경계 유지**를 원칙으로 시스템을 운영한다.

#### 한줄 요약

- NIST AI RMF 준수, 4계층(Data, Model, App, Agent) 입체 통제 및 3중 신뢰 경계 구축 중심 AI 보안 체계 구축 필수.