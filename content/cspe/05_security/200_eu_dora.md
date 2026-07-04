---
title: "EU DORA 디지털 운영 복원력 (EU DORA)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 200
---

# 📖 【암기용】 개념 완전 이해

> 목적: EU DORA를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: EU 금융권의 ICT 위험관리, 사고보고, 복원력 시험, 제3자 위험을 통합 규율하는 디지털 운영 복원력 규정
- **왜 필요한가**: 금융 서비스는 클라우드, 코어뱅킹, 결제망, 외부 ICT 공급자에 의존한다. 한 공급자 장애가 여러 금융기관 업무 중단으로 번질 수 있어 EU가 공통 규칙을 적용함.
- **핵심 직관**: 은행이 금고만 튼튼하게 만드는 것이 아니라 전산센터, 클라우드, 협력사, 사고보고, 모의훈련까지 같은 감독 기준으로 관리하게 하는 규정임.

## 깊이 이해
- **배경·문제의식**: 기존 금융 규제는 ICT 운영 장애와 공급망 집중 위험을 국가별로 다르게 다뤘다. DORA는 Regulation (EU) 2022/2554로 2025년 1월 17일부터 적용되어 EU 회원국에 직접 효력을 가짐.
- **작동 원리**: 적용 대상 금융기관은 ICT risk management, incident reporting, digital operational resilience testing, ICT third-party risk management, information sharing을 갖춰야 함. EIOPA는 20개 금융 entity 유형과 ICT third-party service provider를 범위로 설명함.
- **비유**: 항공사가 비행기 정비, 관제 통신, 협력 정비사, 사고 보고, 비상 훈련을 한 규정으로 관리하는 것과 유사함.
- **구체 예시**: EU에 서비스를 제공하는 은행이 클라우드 장애로 결제 서비스가 중단되면 major ICT-related incident 분류, 감독기관 보고, 복구 절차, 공급자 계약 검토, 사후 개선을 수행해야 함.
- **흔한 오해·주의점**: DORA는 보안 제품 도입 규정이 아님. 이사회 책임, 중요 기능, ICT 자산·공급자 register, TLPT, 계약 조항, 감독 보고까지 포함한 운영 복원력 체계임.

## 연결 개념
- NIS2 - EU 전 산업 사이버보안 지침, 금융권은 DORA가 특화 규정 역할
- TLPT - 위협 주도 침투 테스트로 복원력 시험 수행
- ICT Third-Party Risk - 클라우드·SaaS 등 중요 공급자 계약과 집중 위험 관리

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: DORA 답안은 적용일 2025-01-17, Regulation (EU) 2022/2554, 5대 축, ICT 제3자 위험, TLPT, incident reporting을 반드시 써야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: DORA는 EU 금융부문의 ICT 장애·사이버공격·제3자 의존을 운영 복원력 관점에서 통합 규율하는 법규임.
> 2. **가치**: ICT risk, incident, testing, third-party, information sharing을 단일 체계로 묶어 금융 서비스 중단과 전이 위험을 감독함.
> 3. **판단 포인트**: Article 5~16, 17~23, 24~27, 28~44, 45 범위와 적용일 2025-01-17, 적용 대상 20개 entity 유형을 제시해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| EU 금융 보안 규제 이해 확인 | Regulation (EU) 2022/2554, 2025-01-17 적용, 직접 적용 | GDPR·NIS2와 혼동 |
| 운영 복원력 구조 확인 | ICT risk, incident, testing, third-party, sharing 5대 축 | 단순 보안 인증제도로 설명 |
| 실무 대응 판단 확인 | register of information, major incident report, TLPT, 계약 조항 | 제3자 공급자 감독과 계약 조항 누락 |

> 요약: 이 문제는 DORA를 기술 보안이 아니라 금융 ICT 운영 복원력과 감독 보고 체계로 쓰는지 확인함.

---

## Ⅰ. 개요 및 필요성

- 개요: EU 금융 ICT 복원력 규정
- 배경: 클라우드 집중, 결제 장애, 사이버공격은 단일 금융기관 장애를 시장·고객·제3자 서비스로 전이시킬 수 있다.
- 필요성: Regulation (EU) 2022/2554 DORA 기준으로 ICT 위험관리, 중대사고 보고, 복원력 시험, 제3자 감독을 통합한다.

---

## Ⅱ. 구조 및 구성요소

```text
Financial Entity -> ICT Risk Framework -> Incident Reporting
  / Resilience Testing/TLPT -> ICT Third-Party Risk
  / Information Sharing -> Competent Authority/Oversight
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| ICT Risk Management | Article 5~16, governance와 보호·탐지·복구 체계 | 이사회 책임, ICT 자산 식별 |
| Incident Reporting | Article 17~23, major ICT incident 분류·보고 | 감독기관 통보, 표준 template |
| Resilience Testing | Article 24~27, 기본 시험과 TLPT | 중요 기관은 threat-led test |
| Third-Party Risk | Article 28~44, ICT 공급자 계약·감독 | register of information, critical provider |
| Information Sharing | Article 45, 사이버 위협 정보 공유 | 신뢰 커뮤니티와 기밀성 조건 |

> 요약: DORA는 ICT 위험관리, 사고보고, 복원력 시험, 제3자 위험, 정보공유를 하나의 감독 체계로 묶음.

---

## Ⅲ. 동작원리 및 흐름도

```text
적용 대상 확인 -> ICT 자산/중요 기능 식별 -> 위험관리 체계 수립
-> 사고 분류/보고 -> 복원력 시험/TLPT -> 공급자 계약·register 관리
-> 감독 대응과 개선
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | Article 2 적용 대상과 중요 기능 확인 | 금융 entity 유형, critical function list |
| 2 | ICT risk framework와 자산·의존성 식별 | ICT asset inventory 100% |
| 3 | major ICT incident 분류와 보고 절차 구축 | reporting template, escalation time |
| 4 | resilience test와 TLPT 계획 수행 | 연 1회 시험, TLPT 대상 별도 관리 |
| 5 | ICT third-party register와 계약 조항 관리 | register completeness 100% |

> 요약: DORA 대응은 적용 범위 확인에서 시작해 위험관리, 사고보고, 시험, 제3자 계약, 감독 대응으로 순환함.

---

## Ⅳ. 특징

| 구분 | 기존 금융 ICT 관리 | DORA 기반 복원력 | 수치·법규 포인트 |
|:---|:---|:---|:---|
| 법적 성격 | 국가별 규제·가이드 혼재 | EU Regulation 직접 적용 | 2025-01-17 적용 |
| 범위 | 기관 내부 보안 중심 | 금융기관 20개 유형과 ICT third-party | Article 2, 28~44 |
| 시험 | 취약점 점검·DR drill | resilience testing, TLPT | Article 24~27 |
| 보고 | 기관별 사고 보고 | major ICT incident 표준 보고 | Article 17~23 |

> 요약: DORA는 금융 ICT를 내부 보안에서 공급망·시험·보고까지 확장한 법적 복원력 프레임워크임.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 규제 비교 | NIS2 일반 사이버보안 | DORA 금융 ICT 복원력 특화 | EU 금융 entity 또는 ICT 공급자 |
| 운영 범위 | 보안 통제 중심 | 장애·복구·보고·공급자 계약 포함 | 중요 기능 중단 영향 존재 |
| 시험 수준 | 취약점 진단 | TLPT와 복원력 시험 | 감독기관 요구 또는 중요 기관 |

> 요약: EU 금융기관과 중요 ICT 공급자는 NIS2 일반 요건보다 DORA의 금융 특화 운영 복원력 요건을 우선 검토해야 함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 적용 범위 누락 | EU 고객·지점·서비스 범위 미식별 | Article 2 scope assessment | scope exception 0건 |
| 보고 지연 | major incident 분류 기준 미정 | classification matrix, escalation drill | reporting SLA 준수율 100% |
| 제3자 집중 | 핵심 클라우드·SaaS 의존 | exit plan, subcontracting review | critical provider register 100% |
| 시험 형식화 | TLPT와 복구훈련 미흡 | scenario-based test, AAR, remediation | finding closure 90일 이내 |

> 요약: DORA 리스크는 범위 누락, 보고 지연, 제3자 집중, 형식적 시험이며 register와 drill로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 거버넌스 | ICT risk framework 승인 100% | 이사회 의사록, policy review |
| 사고 대응 | major incident 분류·보고 SLA 100% | incident register, report evidence |
| 제3자·시험 | register completeness 100%, TLPT finding 90일 내 조치 | RoI, TLPT report, remediation tracker |

> 요약: DORA 준수 여부는 이사회 승인, 사고보고 증적, 제3자 register, TLPT 개선 완료율로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 범위 진단: EU 금융 entity 여부, ICT 서비스 제공 범위, critical or important function을 Article 2와 계약 기준으로 식별함.
2. 운영 체계 구축: Article 5~16 위험관리, Article 17~23 사고보고, Article 24~27 시험, Article 28~44 제3자 register를 정책·절차·증적으로 연결함.
3. 검증과 보고: TLPT, DR drill, major incident tabletop을 연 1회 이상 수행하고 finding 90일 내 조치, register completeness 100%를 감독 대응 자료로 유지함.

**결론 (2줄):**
- 기술사 판단: DORA는 보안 통제 목록이 아니라 금융 ICT 서비스의 장애 대응, 공급망, 감독 보고를 통합한 운영 복원력 규정임.
- 향후 방향: 클라우드·AI 서비스 공급망 집중이 커지므로 exit plan, subcontracting, 실시간 incident reporting 자동화가 DORA 대응의 핵심 과제가 됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "DORA를 설명하시오", "디지털 운영 복원력을 기술하시오" | 적용 범위, 5대 축, 감독 대응 흐름 | 기존 금융 ICT 관리와 DORA 차이 |
| 요구사항 명시형 | "준수 방안을 제시하시오", "금융기관 적용 방안을 설계하시오" | Article별 절차, register, TLPT, 보고 흐름 | 범위 누락, 보고 지연, 제3자 집중 통제 |

> 요약: 설명형은 법규 구조와 5대 축, 방안형은 Article별 증적과 감독 대응 중심으로 작성함.
