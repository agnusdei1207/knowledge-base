---
title: 501. XSS 유형 (Reflected, Stored, DOM-based)
date: '2026-05-08'
tags:
- studynote-software-engineering
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[726_xss_cross_site_scripting_types|XSS]] 유형 (Reflected, Stored, DOM-based)은(는) [[001_software_engineering_definition|소프트웨어 공학]]의 핵심 개념으로, 복잡한 시스템을 체계적으로 설계·관리하기 위한 원칙과 기법이다.
> 2. **가치**: 이 개념을 올바르게 적용하면 소프트웨어의 품질·[[346_maintainability_portability|유지보수성]]·재사용성이 향상되고, 개발 생산성과 팀 협업 효율이 높아진다.
> 3. **판단 포인트**: 도입 시에는 비용·복잡도·조직 성숙도를 함께 고려해야 하며, 맹목적 적용보다 프로젝트 특성에 맞는 선택적 적용이 핵심이다.

---

## Ⅰ. 개요 및 필요성

[[726_xss_cross_site_scripting_types|XSS]] 유형을 구분하면 테스트와 방어가 쉬워진다. 모두 같은 공격처럼 보여도 유입과 실행 지점이 다르다.

이 차이를 알아야 진단이 정확해진다.

- **📢 섹션 요약 비유**: 불이 났을 때 부엌, 거실, 마당 중 어디서 시작했는지 아는 것과 같다.

---

다음은 [[726_xss_cross_site_scripting_types|XSS]] 유형 (Reflected, S의 핵심 구조와 흐름을 보여주는 다이어그램이다.

```text
┌─────────────────────────────────────────────────────────────┐
│                  XSS 유형 (Reflected, S                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [입력/요구사항] ──▶ [핵심 처리 과정] ──▶ [출력/결과물]  │
│       │                    │                    │          │
│       ▼                    ▼                    ▼          │
│   요구 분석           설계·적용           품질 검증        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

이 다이어그램은 [[726_xss_cross_site_scripting_types|XSS]] 유형 (Reflected, S가 입력 요구사항을 받아 핵심 처리 과정을 거쳐 [[395_verification_process_review|검증]]된 결과물을 산출하는 흐름을 보여준다.

---

---

---

## Ⅱ. 아키텍처 및 핵심 원리

세 가지 유형은 흐름이 다르다.

```text
Reflected: 요청 -> 즉시 응답에 반영
Stored: 요청 -> 서버 저장 -> 다른 사용자에게 노출
DOM-based: 브라우저 JS -> DOM 조작으로 실행
```

| 유형 | 특징 |
|:---|:---|
| [[471_reflected_xss|Reflected XSS]] | 요청 반사 |
| [[472_stored_xss|Stored XSS]] | 서버 저장 |
| [[473_dom_xss|DOM-based XSS]] | 클라이언트 조작 |

- **📢 섹션 요약 비유**: 메아리, 메모장, 조립 장난감이 각각 다르게 작동하는 것과 같다.

---

---

---

---

## Ⅲ. 비교 및 연결

세 유형 모두 결국 출력과 실행의 문제지만, 방어 위치가 다르다.

| 구분 | Reflected | Stored | DOM-based |
|:---|:---|:---|:---|
| 흐름 | 요청-응답 | 저장-재노출 | 브라우저 내부 |
| 주된 방어 | 입력/출력 인코딩 | 저장 전 [[395_verification_process_review|검증]] | 안전한 DOM [[014_api_posix|API]] |
| 위험 | 즉시 실행 | 광범위 노출 | 클라이언트 취약 |

[[726_xss_cross_site_scripting_types|XSS]] 방어는 코드 리뷰와 [[442_test_scenario|테스트 시나리오]] 설계에도 중요하다.

- **📢 섹션 요약 비유**: 같은 도둑이라도 창문, 창고, 안방 중 어디로 들어오는지 다르다.

---

---

---

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [[568_logs_distributed_logging_elk_fluentd|로그]], 검색 결과, 댓글, URL 파라미터, 프론트엔드 렌더링을 점검한다.

점검 포인트는 다음과 같다.
1. 사용자 입력이 어디서 다시 보이는가?
2. 브라우저에서 JS가 문자열을 조립하는가?
3. 저장 데이터가 다른 사용자에게 전달되는가?

- **📢 섹션 요약 비유**: 같은 물건도 어디에 놓느냐에 따라 위험이 달라진다.

---

---

---

---

## Ⅴ. 기대효과 및 결론

[[726_xss_cross_site_scripting_types|XSS]] 유형을 구분하면 맞춤형 방어가 가능하다.

결론적으로 이 항목은 "실행 경로별 [[726_xss_cross_site_scripting_types|XSS]] [[104_classification_analysis|분류]]"다.

- **📢 섹션 요약 비유**: 병도 증상에 따라 다르게 치료해야 한다.

---

---

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[001_software_engineering_definition|소프트웨어 공학]] ([[001_software_engineering_definition|Software Engineering]]) | [[726_xss_cross_site_scripting_types|XSS]] 유형 (Reflected, Stored, DOM-based)의 상위 학문 체계이며 품질·생산성 향상의 공통 목표를 공유한다 |
| [[003_sdlc|소프트웨어 생명주기]] ([[131_sdlc_system_development_life_cycle_waterfall_agile|SDLC]], Software Development Life Cycle) | [[726_xss_cross_site_scripting_types|XSS]] 유형 (Reflected, Stored, DOM-based)은 SDLC의 특정 단계에서 핵심적으로 적용된다 |
| 품질 보증 (QA, Quality Assurance) | [[726_xss_cross_site_scripting_types|XSS]] 유형 (Reflected, Stored, DOM-based) 적용 결과는 QA 활동을 통해 [[395_verification_process_review|검증]]되고 측정된다 |
| [[020_software_configuration_management|형상 관리]] ([[167_scm_software_configuration_management|SCM]], [[020_software_configuration_management|Software Configuration Management]]) | [[726_xss_cross_site_scripting_types|XSS]] 유형 (Reflected, Stored, DOM-based)에서 생성된 산출물은 SCM을 통해 체계적으로 관리된다 |

### 📈 관련 키워드 및 발전 흐름도

```text
소프트웨어 위기 (Software Crisis) 인식
    │
    ▼
XSS 유형 (Reflected, Stored, DOM-based) 개념 정립
    │
    ▼
표준화 및 방법론 체계화 (ISO, CMMI, Agile)
    │
    ▼
클라우드 네이티브·AI 기반 확장 적용
    │
    ▼
지속적 개선 및 DevOps·MLOps 통합
```

이 흐름은 [[002_software_crisis|소프트웨어 위기]] 인식 → 체계적 방법론 개발 → 표준화 → 현대적 플랫폼 적용으로 이어지는 발전 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [[726_xss_cross_site_scripting_types|XSS]] 유형 (Reflected, Stored, DOM-based)은 레고 블록으로 성을 만들 때처럼, 규칙을 정하고 역할을 나누어 함께 작업하는 방법이에요.
2. 혼자서 막 만들면 나중에 무너지거나 고치기 어렵지만, 약속을 지키면 누구나 쉽게 고치고 더 크게 만들 수 있어요.
3. 그래서 [[001_software_engineering_definition|소프트웨어 공학]]은 프로그래머들이 좋은 프로그램을 빠르고 안전하게 만들 수 있게 도와주는 '규칙 모음집'이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 593 / 973

← **이전**: [[500_xss_defense_escaping_csp|500. 크로스 사이트 스크립팅 (XSS) 방어 - 입/출력값 인코딩, CSP(Content Security Policy) 헤더 설정]]
**다음**: [[501_xss_types|501. XSS 유형 - Reflected XSS, Stored XSS, DOM-based XSS]] →

---
