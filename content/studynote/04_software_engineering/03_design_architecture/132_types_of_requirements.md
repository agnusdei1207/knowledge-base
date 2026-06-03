---
title: 132. 요구사항 유형 (기능·비기능·제약사항) - FR·NFR·Constraints 분류
date: '2026-04-19'
tags:
- studynote-software-engineering
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 요구사항은 **기능 요구사항(FR, 시스템이 해야 하는 것)**·**[[133_non_functional_requirements|비기능 요구사항]]([[133_non_functional_requirements|NFR]], [[282_performance_tactics|성능]]·보안·[[452_availability|가용성]] 등 품질 [[082_attribute_types_er_model|속성]])**·**제약사항(Constraints, 기술·법적 제한)**의 3가지로 분류된다.
> 2. **가치**: FR만 정의하면 "로그인은 되는데 3초 걸리고 해킹에 취약한" 시스템이 되며, NFR이 **시스템의 품질 수준**을 결정한다. 기술사 시험에서 [[133_non_functional_requirements|NFR]] 누락이 가장 흔한 감점 포인트이다.
> 3. **판단 포인트**: NFR은 ISO 25010 품질 모델(기능성·[[642_reliability_mtbf_mttr_mttf_availability|신뢰성]]·[[286_usability_tactics|사용성]]·효율성·[[346_maintainability_portability|유지보수성]]·이식성·보안·[[344_compatibility_usability|호환성]])로 체계적으로 도출하며, **측정 가능한 수치**로 명세해야 한다.

---

## Ⅰ. 개요 및 필요성

```text
FR:  "사용자는 이메일로 로그인할 수 있다"
NFR: "로그인 응답 시간은 2초 이내이다" (성능)
     "99.9% 가용성을 보장한다" (가용성)
     "OWASP Top 10 대응" (보안)
Constraints: "Java 17 사용", "GDPR 준수"
```

- **📢 섹션 요약 비유**: FR은 "차가 달린다(기능)", NFR은 "200km/h·연비 15km/L(품질)", 제약은 "경유만 사용(제한)"이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 유형 | 질문 | 예 |
|:---|:---|:---|
| **FR** | What? | 로그인, 결제, 검색 |
| **[[133_non_functional_requirements|NFR]]** | How well? | 응답 2초, 가용 99.9% |
| **Constraints** | What limits? | Java, AWS, [[791_gdpr_eu|GDPR]] |

---

## Ⅲ~Ⅴ. 결론

NFR은 **아키텍처를 결정하는 핵심 동인([[319_architecture|Architecture]] Driver)**이며, 측정 가능한 수치로 명세하지 않으면 검증이 불가능하다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **FR** | 기능 요구사항 (What) |
| **[[133_non_functional_requirements|NFR]]** | [[133_non_functional_requirements|비기능 요구사항]] (How well) |
| **ISO 25010** | 품질 모델 (8대 특성) |
| **QAW** | 품질 [[082_attribute_types_er_model|속성]] 워크숍 |
| **[[229_atam_architecture_trade_off_analysis_method|ATAM]]** | 아키텍처 트레이드오프 분석 |

### 📈 관련 키워드 및 발전 흐름도

```text
[비공식 요구 (기능만)] → [IEEE 830 (FR+NFR 분리)]
    → [ISO 25010 품질 모델 (2011)]
    → [QAW·ATAM (아키텍처 관점 NFR)]
    → [현재: AI NFR 자동 도출 — 요구사항에서 품질 속성 추출]
```

### 👶 어린이를 위한 3줄 비유 설명
1. FR은 "차가 **달린다**"(기능), NFR은 "**얼마나 빨리**, 얼마나 안전하게"(품질)예요.
2. "달리기만 하면 돼"라고 하면 **느리고 위험한** 차가 만들어져요.
3. "200km/h, 에어백 10개"처럼 **숫자로 정확히** 적어야 좋은 차가 나와요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 132 / 973

← **이전**: [[131_requirements_engineering|131. 요구사항 공학 (Requirements Engineering) - 체계적 요구 수집·분석·관리]]
**다음**: [[133_non_functional_requirements|133. 비기능 요구사항 (NFR) - 시스템 품질 속성 정의]] →

---
