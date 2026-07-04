---
title: "AI 보안 위협 전체 구조 (AI Security Threat Landscape)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 134
---

# 📖 【암기용】 개념 완전 이해

> 목적: AI 보안 위협 전체 구조를 처음 봐도 AI 생명주기별 공격면과 통제 방법을 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: AI 보안 위협 전체 구조는 데이터·모델·프롬프트·도구·운영 환경에서 발생하는 AI 특화 공격면을 생명주기별로 정리한 관점임
- **왜 필요한가**: AI 시스템은 모델 파일만 보호해서 끝나지 않음. 학습 데이터, RAG 지식베이스, 플러그인 도구, 추론 API, 로그, 사용자 피드백이 모두 공격 경로가 됨.
- **핵심 직관**: AI 서비스는 "데이터를 먹고, 모델로 판단하고, 도구로 행동"하므로 먹이·두뇌·손발을 각각 보호해야 함.

## 깊이 이해
- **배경·문제의식**: 전통 보안은 입력 검증, 인증, 취약점 패치가 중심이었으나 AI는 자연어 지시, 확률적 출력, 외부 도구 호출, 학습 데이터 오염이라는 새로운 문제를 가짐.
- **작동 원리**: 위협은 데이터 단계의 poisoning, 모델 단계의 extraction·inversion, 애플리케이션 단계의 prompt injection·sensitive information disclosure, 운영 단계의 excessive agency·unbounded consumption으로 나뉨.
- **비유**: 직원이 외부 문서와 사내 지식을 읽고 메일 발송·결제까지 대신하는 비서라고 보면, 거짓 문서·권한 과다·기밀 유출·비용 폭주를 모두 관리해야 함.
- **구체 예시**: RAG 챗봇이 공격자가 넣은 문서 지시문을 검색해 시스템 지시보다 우선 처리하면, 내부 문서 요약 대신 외부 URL로 기밀을 전송할 수 있음.
- **흔한 오해·주의점**: AI 보안은 모델 안전성만이 아님. OWASP LLM Top 10, NIST AI RMF, MITRE ATLAS를 함께 보며 기술·운영·거버넌스를 분리해야 함.

## 연결 개념
- OWASP LLM Top 10: LLM 애플리케이션 위험 분류
- MITRE ATLAS: AI 공격 전술·기법 지식베이스
- AI RMF: AI 위험 식별·측정·관리 프레임워크

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: AI 보안 위협 답안은 prompt injection 하나로 좁히지 말고 데이터·모델·앱·운영 생명주기별 통제를 제시해야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: AI Security Threat Landscape는 AI/LLM 시스템의 데이터 수집, 학습, 배포, 추론, 도구 실행 전 과정에서 발생하는 위협 구조임.
> 2. **가치**: OWASP LLM Top 10, MITRE ATLAS, NIST AI RMF를 기준으로 prompt injection, data poisoning, model extraction, excessive agency를 체계적으로 통제함.
> 3. **판단 포인트**: 모델 정확도보다 자산·공격면·권한·로그·평가 데이터를 기준으로 탐지·차단·복구 체계를 설계해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| AI 특화 위협 분류 역량 확인 | 데이터, 모델, 프롬프트, 도구, 운영 위협 | 일반 웹 보안만 나열하고 AI 고유 위협 누락 |
| 표준 프레임워크 적용 확인 | OWASP LLM Top 10, MITRE ATLAS, NIST AI RMF | prompt injection만 설명 |
| 통제 설계 판단 확인 | guardrail, 권한 최소화, red teaming, 모니터링 | "모델을 안전하게 학습" 같은 추상 문장 |

> 요약: 이 문제는 AI 생명주기별 공격면을 식별하고 표준 프레임워크와 운영 지표로 통제하는 능력을 평가함.

---

## Ⅰ. 개요 및 필요성

- 개요: AI 생명주기 공격면 분류
- 배경: 생성형 AI, RAG, AI Agent는 자연어 입력을 해석하고 외부 도구를 호출하므로 기존 웹·API 통제만으로 위험을 설명하기 어려움.
- 필요성: OWASP LLM Top 10, MITRE ATLAS, NIST AI RMF 기준으로 데이터 오염, 모델 유출, 프롬프트 조작, 비용 폭주를 분류해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Data Source -> Training / Fine-tuning -> Model Registry -> Inference API
RAG Store -> Prompt / Tool Call -> Output / Action
               +-> Guardrail / Logging / Evaluation
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Data Layer | 학습·튜닝·RAG 데이터 관리 | poisoning, embedding weakness, privacy leakage |
| Model Layer | 모델 파일·가중치·추론 API 보호 | extraction, inversion, model tampering |
| App Layer | 프롬프트·검색·출력·도구 호출 처리 | prompt injection, insecure output handling |
| Ops/Gov Layer | 권한·로그·평가·정책 운영 | red team, AI asset inventory, incident response |

> 요약: AI 보안 구조는 데이터, 모델, 애플리케이션, 운영 거버넌스가 연결된 복합 공격면으로 봐야 함.

---

## Ⅲ. 동작원리 및 흐름도

```text
Asset Inventory -> Threat Modeling -> Control Mapping
-> Prompt / Data / Model Test -> Runtime Monitor -> Incident Response
-> Feedback Update -> Risk Reassessment
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | AI 자산·데이터·도구 권한 식별 | model, dataset, vector DB, tool inventory 100% |
| 2 | 위협 모델링 및 표준 매핑 | OWASP LLM Top 10, MITRE ATLAS technique |
| 3 | 사전 평가 수행 | jailbreak, poisoning, leakage test pass rate |
| 4 | 런타임 통제 적용 | prompt filter, DLP, tool allowlist, rate limit |
| 5 | 사고 대응과 재평가 | incident ticket, abuse log, regression eval |

> 요약: AI 보안은 출시 전 red teaming과 출시 후 runtime monitoring을 연결해 위협 변화를 반복 검증함.

---

## Ⅳ. 특징

| 구분 | 기존 애플리케이션 보안 | AI 보안 위협 구조 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 입력 처리 | 정형 파라미터 검증 | 자연어 지시와 데이터 경계 혼재 | prompt injection test set 100개 이상 |
| 자산 | 코드·DB·서버 | 모델, dataset, embedding, system prompt | AI asset inventory 100% |
| 권한 | API 권한 중심 | agent tool 권한·행동 범위 | tool allowlist, human approval |
| 평가 | SAST·DAST·CVE | red teaming·eval·abuse monitoring | jailbreak success rate 1% 이하 목표 |

> 요약: AI 보안은 입력 검증보다 지시 해석, 데이터 출처, 도구 권한, 평가 데이터 운영이 핵심 차이임.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 모델 API 보안 단독 | 생명주기 기반 AI threat landscape | RAG·agent·fine-tuning 포함 시 필수 |
| 비용/성능 | 출시 후 로그 대응 | 사전 red team+런타임 guardrail | 고객 데이터 처리 AI는 사전 평가 필수 |
| 운영/위험 | 일반 SOC 룰 | AI abuse pattern, prompt log, tool audit | 개인정보·결제·메일 tool 권한 보유 시 |

> 요약: AI 기능이 외부 도구나 민감 데이터와 연결되면 일반 API 보안보다 생명주기 기반 위협 관리가 우선됨.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 데이터 오염 | 공개 데이터·RAG 문서 조작 | source trust, content signing, corpus review | poisoned document detect rate |
| 기밀 유출 | prompt injection, over-retrieval, log 노출 | DLP, permission filtering, output policy | sensitive output incident 월 0건 |
| 권한 남용 | agent tool 권한 과다 | least privilege, approval gate, sandbox | high-risk tool auto-execute 0건 |

> 요약: AI 보안 리스크는 데이터 신뢰, 출력 통제, 도구 권한을 분리해 지표로 관리해야 함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 위협 커버리지 | OWASP LLM Top 10 항목별 통제 1개 이상 | control matrix, architecture review |
| 평가 품질 | prompt attack dataset 100개 이상, 재현율 기록 | red team eval, regression test |
| 운영 탐지 | 이상 prompt·tool call 5분 내 알림 | SIEM, LLM gateway, audit log |

> 요약: 도입 후 성공 기준은 위협 커버리지, 평가 데이터 규모, 런타임 탐지 시간으로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 거버넌스: AI asset inventory, data classification, model card, risk register를 구축하고 OWASP LLM Top 10 기반 통제 매트릭스 작성.
2. 기술 통제: prompt firewall, retrieval permission filtering, output DLP, tool allowlist, rate limit, sandbox execution을 AI gateway에 적용.
3. 운영 통제: jailbreak·prompt injection 100개 이상 회귀 테스트, MITRE ATLAS 기반 red team, prompt/tool audit log SIEM 연계 구성.

**결론 (2줄):**
- 기술사 판단: 단순 Q&A 챗봇은 prompt·output 통제를 우선하고, agent형 AI는 권한 최소화·human approval·sandbox를 필수 조건으로 둠.
- 향후 방향: AI SBOM, model provenance, continuous red teaming, agent runtime policy가 결합되어 AI 보안 운영 표준으로 전개됨.

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "AI 보안 위협을 설명하시오", "LLM 보안을 기술하시오" | 데이터·모델·앱·운영 단계별 위협 흐름 | 기존 보안과 AI 보안 차이 |
| 요구사항 명시형 | "대응 방안을 제시하시오", "설계하시오", "위험을 분석하시오" | threat modeling, red team, runtime monitor | 통제 우선순위, 지표, 사고 대응 |

> 요약: 설명형은 전체 위협 지형을 넓게 쓰고, 방안형은 AI gateway·권한·평가·모니터링 중심으로 답안을 전환함.
