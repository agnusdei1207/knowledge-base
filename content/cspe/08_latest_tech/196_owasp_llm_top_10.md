---
title: "OWASP LLM Top 10 (OWASP LLM Top 10)"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 196
---

# 📖 【암기용】 개념 완전 이해

> 목적: OWASP LLM Top 10을 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **개요**: LLM·생성형 AI 애플리케이션의 주요 보안 위험 10가지를 정리한 OWASP 보안 기준
- **왜 필요한가**: LLM 앱은 프롬프트, RAG, 에이전트, 모델 공급망, 출력 처리 등 기존 웹 보안과 다른 공격면을 가짐.
- **핵심 직관**: 생성형 AI 서비스를 만들 때 먼저 점검해야 할 AI 보안 위험 체크리스트임.

## 깊이 이해
- **배경·문제의식**: LLM은 자연어 입력을 명령처럼 처리하고 외부 데이터·도구·플러그인과 연결되며 새로운 보안 실패가 발생함.
- **작동 원리**: 2025 목록은 Prompt Injection, Sensitive Information Disclosure, Supply Chain, Data and Model Poisoning, Improper Output Handling 등으로 위험을 분류함.
- **비유**: 웹 애플리케이션에 OWASP Top 10이 있듯이, LLM 앱에는 프롬프트와 모델 공급망을 포함한 별도 안전점검표가 필요한 구조임.
- **구체 예시**: RAG 챗봇은 LLM01 프롬프트 인젝션, LLM02 민감정보 노출, LLM08 벡터·임베딩 취약점을 함께 점검해야 함.
- **흔한 오해·주의점**: 모델 자체만 점검하면 부족하다. 애플리케이션 코드, 데이터 파이프라인, 도구 권한, 운영 모니터링까지 포함해야 함.

## 연결 개념
- AI Red Teaming — Top 10 위험을 공격 시나리오로 검증
- Prompt Injection — LLM01 핵심 위험
- Improper Output Handling — LLM 출력 후단 처리 취약점

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: OWASP LLM Top 10은 LLM 애플리케이션 보안 위험을 10개 범주로 정리한 기준임.
> 2. **가치**: AI 서비스 설계·개발·운영 단계의 공통 점검표와 레드팀 기준으로 활용됨.
> 3. **판단 포인트**: 모델 단독이 아니라 RAG, 에이전트, 공급망, 출력 처리까지 범위를 잡아야 함.

## Ⅰ. 개요 및 필요성

OWASP LLM Top 10은 LLM 보안 위험 기준이다. 생성형 AI는 프롬프트와 외부 도구 연결로 기존 웹 보안 범위를 넘어선다. 개발·운영 전 단계에 AI 특화 보안 기준이 필요하다.

## Ⅱ. 구조 및 구성요소

```text
LLM App → Prompt/RAG/Agent/Model Supply Chain
  → OWASP LLM Top 10 Mapping → Control/Test
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| LLM01~04 | 프롬프트·정보노출·공급망·오염 | 핵심 공격면 |
| LLM05~07 | 출력처리·과도한 권한·시스템 프롬프트 | 앱 통제 |
| LLM08~10 | 벡터·오정보·무제한 소비 | RAG·운영 위험 |
| Control Matrix | 위험별 통제·테스트 매핑 | 레드팀 기준 |

> 요약: OWASP LLM Top 10은 LLM 앱 공격면을 10개 범주로 나누고 통제·테스트로 연결함.

## Ⅲ. 동작원리 및 흐름도

```text
AI 기능 식별 → Top 10 위험 매핑 → 통제 설계
  → 레드팀 테스트 → 운영 모니터링
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | LLM, RAG, Agent, API 기능 목록화 | 자산 식별 100% |
| 2 | OWASP LLM01~10 위험 매핑 | 위험별 owner 지정 |
| 3 | guardrail·권한·검증 통제 설계 | High risk 0건 |
| 4 | 공격 테스트·모니터링 운영 | 분기 1회 재평가 |

> 요약: OWASP LLM Top 10은 AI 기능별 위험을 매핑하고 통제·테스트·모니터링으로 관리함.

## Ⅳ. 특징

| 구분 | OWASP Web Top 10 | OWASP LLM Top 10 | 판단 포인트 |
|:---|:---|:---|:---|
| 대상 | 웹 앱 취약점 | LLM 앱·RAG·Agent | AI 특화 |
| 입력 | HTTP parameter | 프롬프트·문서·도구 호출 | 자연어 공격 |
| 공급망 | 라이브러리 중심 | 모델·데이터·플러그인 포함 | AI SBOM |
| 운영 | WAF·SAST·DAST | 레드팀·guardrail·LLMOps | 지속 평가 |

> 요약: OWASP LLM Top 10은 웹 보안에 AI 데이터·모델·프롬프트 위험을 추가한 실무 기준임.

## Ⅴ. 실무 적용 및 결론

**적용 방안 3개:**
1. 설계 검토: 신규 LLM 기능은 LLM01~10 체크리스트로 threat modeling을 수행하고 High 위험 owner 지정
2. 배포 게이트: prompt injection, sensitive disclosure, output handling 테스트 200건 이상 수행 후 High finding 0건 승인
3. 운영 관리: OWASP 범주별 탐지 로그, 사고 티켓, 완화 조치 SLA 7일 기준을 보안 대시보드에 반영

**결론 (2줄):**
- 기술사 판단: 대외 LLM 서비스는 OWASP LLM Top 10을 설계·검증·운영의 공통 기준으로 채택
- 향후 방향: OWASP LLM Top 10은 Agentic AI, AI SBOM, 자동 레드팀과 결합해 AI 보안 표준 운영체계로 확장됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "OWASP LLM Top 10을 설명하시오" | 위험 매핑→통제→테스트 흐름 | Web Top 10 대비 차이 |
| 요구사항 명시형 | "생성형 AI 보안 점검 방안을 제시하시오" | LLM01~10 체크리스트와 배포 게이트 | RAG·Agent 적용 기준 |

> 요약: 설명형은 Top 10 체계, 방안형은 위험 매핑과 배포 전 레드팀 기준을 중심으로 작성함.
