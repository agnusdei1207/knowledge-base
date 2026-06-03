+++
title = "476. DREAD 모델 (DREAD Model)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: DREAD 모델은 소프트웨어 보안 위협의 위험도를 5가지 요소(Damage, Reproducibility, Exploitability, Affected Users, Discoverability)의 점수 합산으로 정량화하여, 제한된 보안 자원을 어느 위협부터 대응할지 우선순위를 결정하는 위험 산정 프레임워크다.
> 2. **가치**: 보안 팀이 수십 개의 위협을 동시에 받았을 때 "모두 중요하다"는 판단만으로는 실질적 개선이 불가능하다. DREAD는 주관적 판단을 배제하고 수치 기반의 객관적 우선순위를 제공하여 이해관계자 간 소통을 명확하게 한다.
> 3. **판단 포인트**: DREAD 점수는 절대적 진리가 아니라 토론의 출발점이다. 조직의 비즈니스 맥락과 자산 가치를 반드시 함께 고려해야 하며, 점수가 낮아도 비즈니스 임팩트가 크면 우선 대응해야 하는 경우가 있다.

---

## Ⅰ. 개요 및 필요성

### 등장 배경

DREAD 모델은 마이크로소프트가 SDL(Security Development Lifecycle) 개발 과정에서 위협 모델링의 결과물인 위협 목록의 우선순위를 결정하기 위해 개발했다. 2002년경 마이크로소프트 보안팀에서 내부적으로 사용되다가, 마이크로소프트의 보안 관련 서적과 SDL 문서를 통해 공개되었다.

DREAD 이전에는 위협 우선순위 결정이 전적으로 보안 전문가의 주관적 경험에 의존했다. 이는 두 가지 문제를 야기했다. 첫째, 팀원 간 우선순위 의견 불일치로 결정이 지연된다. 둘째, 경영진이나 개발팀에게 "이 취약점부터 수정해야 한다"고 설명할 객관적 근거가 없다. DREAD는 이 두 문제를 정량적 점수 체계로 해결하려 했다.

DREAD는 마이크로소프트 내부에서는 이후 CVSS(Common Vulnerability Scoring System)의 등장으로 대체되거나 병행 사용되고 있지만, 개념의 단순성 덕분에 교육 목적과 내부 위험 평가에서 여전히 널리 활용된다.

### 왜 위험도 정량화가 필요한가

보안 팀이 일반적으로 직면하는 현실적 문제는 다음과 같다. 침투 테스트 결과 20개의 취약점이 발견되었다. 개발팀은 2주 스프린트에 5개만 수정할 수 있다. 어느 5개를 먼저 수정해야 하는가? DREAD는 이 질문에 구조적으로 답하는 도구다.

- **📢 섹션 요약 비유**: 응급실에서 환자들을 치료 우선순위(중증도)에 따라 분류하는 트리아지(Triage) 시스템처럼, DREAD는 보안 취약점들의 위험도를 측정하여 치료 순서를 정한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### DREAD 5개 구성 요소

| 요소 | 영어 | 핵심 질문 | 점수 기준 (1-10) |
|:---|:---|:---|:---|
| D - 피해(Damage) | Damage | 공격 성공 시 피해 규모는? | 1(경미) ~ 10(치명적, 전체 시스템 장악) |
| R - 재현성(Reproducibility) | Reproducibility | 공격을 얼마나 쉽게 반복할 수 있나? | 1(재현 불가) ~ 10(항상 성공) |
| E - 악용성(Exploitability) | Exploitability | 공격을 실행하기 얼마나 쉬운가? | 1(전문가도 어려움) ~ 10(스크립트 수준) |
| A - 영향 사용자(Affected Users) | Affected Users | 얼마나 많은 사용자가 영향을 받나? | 1(개인) ~ 10(전체 사용자) |
| D - 발견성(Discoverability) | Discoverability | 공격자가 취약점을 얼마나 쉽게 찾나? | 1(찾기 매우 어려움) ~ 10(공개 정보로 확인 가능) |

**DREAD 점수 = (D + R + E + A + D) / 5** (평균값, 1~10 범위)

### 점수 해석 기준

| 점수 범위 | 위험 등급 | 권장 대응 |
|:---|:---|:---|
| 9-10 | 매우 높음(Critical) | 즉시 대응 (24시간 이내) |
| 7-8 | 높음(High) | 신속 대응 (1주일 이내) |
| 5-6 | 중간(Medium) | 계획적 대응 (다음 릴리스) |
| 3-4 | 낮음(Low) | 백로그 관리 |
| 1-2 | 매우 낮음(Informational) | 수용 가능 위험으로 기록 |

### DREAD 점수 산정 예시

SQL 인젝션 취약점이 발견되었다고 가정한다.

```
취약점: 사용자 검색 기능의 SQL 인젝션

D (Damage): 9
- 데이터베이스 전체 데이터 유출 가능
- 관리자 권한 탈취 가능

R (Reproducibility): 10
- 특정 파라미터에 따옴표만 입력하면 재현 가능
- 항상 같은 결과

E (Exploitability): 8
- sqlmap 같은 자동화 도구로 초보자도 공격 가능
- 기술 지식 거의 불필요

A (Affected Users): 10
- 전체 사용자 데이터 영향
- 약 1,000만 명

D (Discoverability): 9
- 에러 메시지에 SQL 구문이 노출됨
- 공개 스캐너로 쉽게 발견

DREAD 점수 = (9 + 10 + 8 + 10 + 9) / 5 = 9.2 → 매우 높음(Critical)
즉각적 수정 필요!
```

### DREAD vs CVSS 비교

CVSS(Common Vulnerability Scoring System)는 DREAD의 한계를 보완하기 위해 개발된 업계 표준 취약점 점수 체계다.

| 구분 | DREAD | CVSS v3.1 |
|:---|:---|:---|
| 개발 주체 | 마이크로소프트 | FIRST(Forum of Incident Response and Security Teams) |
| 점수 범위 | 1-10 | 0.0-10.0 |
| 구성 요소 | 5개 | 8개 (Base) + Temporal + Environmental |
- 공개 여부 | 비공식(내부 사용) | 공식 국제 표준 |
| 복잡도 | 단순 | 복잡(환경 변수 고려) |
| 사용 목적 | 내부 위험 우선순위 | CVE 공식 점수, 업계 공유 |
| NVD 연동 | 미지원 | NVD 공식 채택 |
| 현재 사용 | 교육·내부 평가 | 산업 표준 |

- **📢 섹션 요약 비유**: DREAD는 내 몸 상태를 직관적으로 1-10점으로 평가하는 자가 건강 체크표고, CVSS는 의사가 표준화된 진단 기준으로 작성하는 공식 의료 기록이다.

---

## Ⅲ. 비교 및 연결

### DREAD와 STRIDE의 상호 보완 관계

STRIDE와 DREAD는 위협 모델링 과정에서 자연스럽게 쌍으로 사용된다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">위협 모델링 프로세스</div></div>
<div class="kb-diagram-note">1. STRIDE로 위협 분류 → 위협 목록 생성</div>
<div class="kb-diagram-note">예: "로그인 API에 스푸핑(S) 위협이 있다"</div>
<div class="kb-diagram-note">2. DREAD로 각 위협 위험도 산정 → 우선순위 결정</div>
<div class="kb-diagram-note">예: "해당 스푸핑 위협의 DREAD 점수는 7.4 (High)"</div>
<div class="kb-diagram-note">3. 우선순위대로 대응책 설계·구현</div>
</div>
</div>



| 구분 | STRIDE | DREAD |
|:---|:---|:---|
| 역할 | 위협 식별·분류 | 위협 위험도 산정 |
| 질문 | "어떤 위협인가?" | "얼마나 위험한가?" |
| 출력 | 위협 유형 카탈로그 | 위험 점수 순위 |
| 사용 시점 | 위협 모델링 初 | 위협 목록 완성 후 |
| 결합 | STRIDE → DREAD 순서로 사용 시 가장 효과적 |

### DREAD 한계와 대안 모델

| 한계 | 설명 | 대안 |
|:---|:---|:---|
| 주관성 | 평가자에 따라 점수 편차 큼 | CVSS (표준화 기준 제공) |
| 발견성 역효과 | 발견하기 쉬운 취약점이 높은 점수 → 발견 어렵게 숨기려는 인센티브 | 발견성 항목 제거한 변형 DREAD |
| 비즈니스 맥락 부재 | 비즈니스 영향을 직접 반영 못함 | PASTA (비즈니스 위험 중심) |
| 환경 미반영 | 동일 취약점도 환경에 따라 위험도 달라짐 | CVSS Environmental Score |

마이크로소프트는 이런 한계로 인해 내부적으로 DREAD 사용을 중단하고 CVSS로 전환했다. 그러나 DREAD의 단순성은 교육 목적과 신속한 내부 평가에서 여전히 유용하다.

### 관련 개념 연결

| 관련 개념 | 연결 내용 |
|:---|:---|
| [위협 모델링](/knowledge-base/studynote/04_software_engineering/11_testing_validation/474_threat_modeling/) | DREAD는 위협 모델링으로 식별된 위협의 위험도를 산정하는 후속 도구 |
| [CVSS](/knowledge-base/studynote/04_software_engineering/11_testing_validation/490_cvss/) | DREAD의 현대적 대안. 국제 표준화된 취약점 점수 체계 |
| [CVE](/knowledge-base/studynote/04_software_engineering/11_testing_validation/489_cve/) | CVSS 점수가 부여되는 공개 취약점 목록 |
| [Microsoft SDL](/knowledge-base/studynote/04_software_engineering/11_testing_validation/473_microsoft_sdl/) | DREAD가 탄생한 보안 개발 프레임워크 |

- **📢 섹션 요약 비유**: 취약점들을 병원 응급실에 온 환자들로 비유하면, STRIDE는 증상 종류를 분류하는 것이고, DREAD는 중증도(생명 위협도)를 측정하여 치료 순서를 정하는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### DREAD 적용 워크숍 진행 방법

1. **대상 위협 목록 준비**: STRIDE 또는 침투 테스트 결과로 도출된 위협 목록을 준비한다.
2. **팀 구성**: 보안 엔지니어 1명 + 개발 아키텍트 1명 + 제품 관리자 1명 (3명 내외 최적)
3. **각자 독립 점수 부여**: 각 위협의 5개 항목에 1-10점을 각자 부여한다.
4. **토론 및 합의**: 점수 차이가 큰 항목을 중심으로 토론하여 합의 점수를 결정한다.
5. **순위 정렬**: 최종 DREAD 점수 순으로 위협을 정렬하고 비즈니스 맥락을 추가 고려한다.
6. **문서화**: 점수와 근거를 위협 모델 문서에 기록한다.

### 설계 판단 체크리스트

1. **점수 부여 기준이 팀 내에서 공유되었는가?** - "Damage 10점이란 무엇인가?"에 대한 공통 정의 없이 점수를 부여하면 개인마다 다른 기준이 적용된다.
2. **비즈니스 자산 가치를 점수에 반영했는가?** - 결제 시스템의 취약점과 이메일 알림의 취약점은 DREAD 점수가 같아도 비즈니스 임팩트가 다를 수 있다.
3. **발견성(Discoverability) 점수를 올바르게 이해했는가?** - 발견하기 쉬운 취약점일수록 점수가 높아 더 위험으로 분류된다. 일부에서는 이 항목을 제거한 변형 DREAD를 사용한다.
4. **CVSS와 DREAD를 혼동하지 않는가?** - 공개 CVE 취약점에는 이미 CVSS 점수가 있다. 오픈소스 의존성 취약점은 CVSS를 직접 참조하고, 내부 취약점에 DREAD를 보완적으로 사용하는 것이 효율적이다.
5. **점수 산정 결과를 이해관계자에게 어떻게 보고할 것인가?** - DREAD 점수를 이해하지 못하는 경영진을 위해 "High/Medium/Low" 등의 직관적 등급과 비즈니스 영향으로 번역하는 계층이 필요하다.

### 안티패턴

- **점수 인플레이션(Score Inflation)**: 자신이 담당하는 시스템의 취약점을 낮게 평가하는 경향. 보안팀이 직접 점수를 부여하면 객관성이 높아지지만, 시스템 맥락은 개발팀이 더 잘 안다. 반드시 혼합 팀이 평가해야 한다.
- **발견성 기반 '보안을 통한 불투명(Security Through Obscurity)' 유혹**: 발견하기 어렵게 만들면 DREAD 점수가 낮아지므로, 실제 취약점을 수정하지 않고 취약점을 숨기는 방향으로 대응하는 경우. 근본적 수정 없이 숨기기만 하는 것은 임시방편이다.
- **점수만으로 결정**: DREAD 점수 7.5인 취약점이 비즈니스 핵심 기능(결제)에 있고, DREAD 점수 8.0인 취약점이 거의 사용하지 않는 기능에 있다면, 점수만 보면 후자를 먼저 처리하게 된다. 비즈니스 가치를 항상 함께 고려해야 한다.
- **일회성 평가 후 방치**: 위협을 평가하고 우선순위를 정했지만, 낮은 우선순위 취약점들이 다음 검토 기회 없이 영구적으로 방치되는 경우. 정기적 재평가 스케줄이 필요하다.

- **📢 섹션 요약 비유**: 화재 시 어느 방에서 시작된 불부터 끌지 결정할 때, 단순히 불길 크기(DREAD 점수)만 보는 것이 아니라 그 방에 사람이 있는지(비즈니스 맥락)도 함께 봐야 한다.

---

## Ⅴ. 기대효과 및 결론

DREAD 모델을 도입하는 조직이 얻는 가장 큰 실질적 효과는 보안 커뮤니케이션의 명확화다. "이 취약점이 왜 다른 취약점보다 먼저 수정되어야 하는가?"라는 질문에 "피해 점수 9, 악용성 점수 8이므로 DREAD 8.4로 가장 위험합니다"라고 수치로 답할 수 있다. 이는 보안팀과 개발팀, 그리고 경영진 사이의 소통 효율을 크게 높인다.

그러나 DREAD는 현재 업계에서 CVSS로 많이 대체되고 있는 것이 현실이다. NVD(National Vulnerability Database)가 CVSS를 공식 채택하면서, 공개 취약점에 대한 위험도 참조는 CVSS가 표준이 되었다. DREAD의 현재 가치는 내부에서 발견된 취약점에 대한 신속한 위험 평가 도구로, 그리고 보안 교육에서 "위험도를 어떻게 정량화하는가"를 가르치는 입문 모델로 남아 있다.

결론적으로 DREAD는 "위협을 수치화하여 우선순위를 결정하는 위험 산정 도구"다. 완벽한 도구는 아니지만, 보안 결정을 주관적 경험에서 수치 기반으로 전환하는 첫 걸음으로서의 역할은 여전히 유효하다. 기술사 관점에서는 DREAD 자체보다 "위협을 왜 정량화해야 하는가, 그리고 어떤 기준으로 우선순위를 결정해야 하는가"라는 원리를 이해하는 것이 더 중요하다.

- **📢 섹션 요약 비유**: 운동화 끈을 묶는 법을 처음 배울 때는 하나씩 단계를 외우지만, 익숙해지면 원리를 이해하고 더 좋은 방법도 응용할 수 있다. DREAD는 위험 정량화의 "기초 운동화 끈 묶기"다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [위협 모델링](/knowledge-base/studynote/04_software_engineering/11_testing_validation/474_threat_modeling/) | DREAD의 사용 맥락. 위협 식별 후 위험도 산정 |
| [CVSS](/knowledge-base/studynote/04_software_engineering/11_testing_validation/490_cvss/) | DREAD의 현대적 대안이자 국제 표준 취약점 점수 |
| [CVE](/knowledge-base/studynote/04_software_engineering/11_testing_validation/489_cve/) | CVSS 점수가 부여되는 공개 취약점 목록 |
| [Microsoft SDL](/knowledge-base/studynote/04_software_engineering/11_testing_validation/473_microsoft_sdl/) | DREAD가 개발·활용된 보안 개발 프레임워크 |
| [Secure SDLC](/knowledge-base/studynote/04_software_engineering/11_testing_validation/471_secure_sdlc/) | DREAD가 적용되는 보안 개발 프로세스 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">위협 우선순위 결정 필요성 인식 (보안 팀의 과부하 문제)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">마이크로소프트 내부 DREAD 모델 개발 (2002년경)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Microsoft SDL 문서와 함께 공개 (2004+)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">보안 업계 교육·내부 평가 도구로 확산</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">CVSS v1.0 발표 (2005) - 국제 표준화 시작</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">CVSS v2.0 (2007), v3.0 (2015), v3.1 (2019)로 진화</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">NVD CVSS 공식 채택 → DREAD 대체 가속</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">DREAD: 내부 평가 및 교육 도구로 역할 재정립</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">CVSS v4.0 (2023) - 더 세밀한 위협 환경 반영</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. DREAD는 프로그램의 약한 부분(취약점)들이 얼마나 위험한지 점수를 매기는 방법이에요. "얼마나 큰 피해가 생기나?", "얼마나 쉽게 공격할 수 있나?" 같은 질문에 점수를 주는 거예요.
2. 점수가 높은 약한 부분부터 먼저 튼튼하게 고치면, 가장 위험한 공격부터 막을 수 있어요.
3. 점수만 너무 믿으면 안 되고, 그 약한 부분이 얼마나 중요한 기능에 있는지도 함께 생각해야 제대로 우선순위를 정할 수 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 543 / 973

← **이전**: [475. STRIDE 모델 - Spoofing, Tampering, Repudiation, Information Disclosure](/knowledge-base/studynote/04_software_engineering/11_testing_validation/475_stride_model/)
**다음**: [477. OWASP Top 10 (2021) - 웹 애플리케이션 주요 보안 위협](/knowledge-base/studynote/04_software_engineering/11_testing_validation/477_owasp_top_10_2021/) →

---
