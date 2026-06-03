---
title: 509. 인가 (Authorization) 모델 - RBAC(역할 기반), ABAC(속성 기반, 조건부 규칙)
date: '2026-05-08'
tags:
- studynote-software-engineering
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 인가 (Authorization) 모델 - [[569_rbac|RBAC]](역할 기반), [[572_abac|ABAC]]([[082_attribute_types_er_model|속성]] 기반, 조건부 규칙)은(는) [[001_software_engineering_definition|소프트웨어 공학]]의 핵심 개념으로, 복잡한 시스템을 체계적으로 설계·관리하기 위한 원칙과 기법이다.
> 2. **가치**: 이 개념을 올바르게 적용하면 소프트웨어의 품질·[[346_maintainability_portability|유지보수성]]·재사용성이 향상되고, 개발 생산성과 팀 협업 효율이 높아진다.
> 3. **판단 포인트**: 도입 시에는 비용·복잡도·조직 성숙도를 함께 고려해야 하며, 맹목적 적용보다 프로젝트 특성에 맞는 선택적 적용이 핵심이다.

---

## Ⅰ. 개요 및 필요성

- **개념**: **[[303_authentication_authorization_patterns|인증]](AuthN)**이 "너 신분증 내놔(누구야?)"라면, **인가(AuthZ)**는 "네 신분증이 대리(Role)네? 그럼 이 VVIP 폴더는 못 읽어. 꺼져!" 라고 권한을 제어하는 행위다. 
  - **[[569_rbac|RBAC]] (Role-Based)**: 부장, 대리, 사원이라는 '명찰(역할)' 딱지를 기준으로 폴더 출입문을 막는다.
  - **[[572_abac|ABAC]] ([[082_attribute_types_er_model|Attribute]]-Based)**: 명찰뿐만 아니라, "퇴근 시간 후(시간 [[082_attribute_types_er_model|속성]])에 폰으로 접속(기기 [[082_attribute_types_er_model|속성]])"하면 부장이라도 폴더를 못 열게 하는 미친 듯이 깐깐한 동적 규칙이다.

- **필요성**: 병원 시스템을 만들었다. 의사(Role)는 환자의 차트를 볼 수 있어야 한다. 그래서 코드를 `if (role == '의사') return 환자정보;` 라고 RBAC로 대충 짰다. 그랬더니 서울 병원에 있는 A의사가, 부산 병원에 있는 B의사 환자의 차트까지 모조리 다 볼 수 있는 끔찍한 대참사([[418_idor|IDOR]] 해킹)가 터졌다. **단순한 '역할(Role)' 1차원 통제로는 "나와 관련된 진짜 [[001_dikw_pyramid|데이터]](Ownership)만 볼 수 있는가?"라는 복잡다단한 현대 비즈니스의 경계를 절대 지켜낼 수 없기 때문에, [[082_attribute_types_er_model|속성]]([[082_attribute_types_er_model|Attribute]])까지 쥐어짜 내 검사하는 고도의 인가 아키텍처가 필수적으로 진화했다.**

- **💡 비유**: 인가 모델은 **'군부대 출입 통제 [[238_switch_operation_principles|스위치]]'**와 똑같습니다. 위병소에서 민증 검사([[303_authentication_authorization_patterns|인증]])를 하고 들어왔다 칩시다. 
  - **[[569_rbac|RBAC]]**: 병사가 가슴에 **'대위'**라는 계급장(Role)을 달고 있으니까 식당과 연병장(일반 [[286_page_frame|페이지]])은 다 패스시키고, 장군 화장실(관리자 [[286_page_frame|페이지]])은 막는 단순 무식한 룰입니다.
  - **[[572_abac|ABAC]]**: 계급이 '대위'라도, **지금 시간이 밤 12시(시간 [[082_attribute_types_er_model|속성]])**이고, **대위가 만취 상태(상태 [[082_attribute_types_er_model|속성]])**라면, 식당(일반 [[286_page_frame|페이지]]) 출입조차 기계가 즉각 거부해 버리는 훨씬 정밀하고 융통성 있는 스마트 도어록입니다.

- **등장 배경 및 발전 과정**:
  1. **[[673_mac_message_authentication_code|MAC]]/DAC의 낭만 (과거)**: [[001_operating_system_purpose|운영체제]](리눅스 폴더 권한 777) 시절 쓰던 군대식 보안. 사용자가 직접 자기 폴더 권한을 남에게 주거나(DAC), 국가가 1급/2급 기밀 딱지를 붙여 통제([[673_mac_message_authentication_code|MAC]])했다. 웹 환경에 맞지 않아 버려졌다.
  2. **RBAC의 대통일 (2000년대)**: 엔터프라이즈(B2B) 기업 환경이 웹에 올라타며, 사원/대리/부장 이라는 '직급 그룹(Role)'에 권한 100개를 묶어서 던져주는 방식이 천하를 통일했다. (관리가 짱 편함)
  3. **ABAC와 제로 트러스트의 강림 (현재)**: MSA와 클라우드가 열리며 유저가 집(재택), 카페, 모바일 어디서 접속할지 모르는 시대가 왔다. Role만 믿다간 다 털린다! "접속 환경, 시간, 위치, 자원 주인(Owner)"의 [[082_attribute_types_er_model|속성]] 변수들을 런타임에 1초 단위로 씹어먹으며 허락해 주는 [[572_abac|ABAC]] 시대가 인프라를 장악 중이다.

- **📢 섹션 요약 비유**: 이 과정은 **'놀이공원 놀이기구 탑승 룰'**과 같습니다. 옛날([[569_rbac|RBAC]])엔 **"어른(Role)은 청룡열차 탈 수 있음, 애들은 회전목마만"** 이 끝이었습니다. 하지만 사고가 났죠. 지금([[572_abac|ABAC]])은 **"어른이라도 심장병이 있고([[082_attribute_types_er_model|속성]]), 비가 오는 날(환경)에는 청룡열차 탑승 불가!"**라는 복잡한 변수를 조합해 생명([[001_dikw_pyramid|데이터]])을 더욱 완벽하게 지켜내는 맞춤형 통제로 진화한 것입니다.

---

다음은 인가 (Authorization) 모의 핵심 구조와 흐름을 보여주는 다이어그램이다.

```text
┌─────────────────────────────────────────────────────────────┐
│                  인가 (Authorization) 모                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [입력/요구사항] ──▶ [핵심 처리 과정] ──▶ [출력/결과물]  │
│       │                    │                    │          │
│       ▼                    ▼                    ▼          │
│   요구 분석           설계·적용           품질 검증        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

이 다이어그램은 인가 (Authorization) 모가 입력 요구사항을 받아 핵심 처리 과정을 거쳐 검증된 결과물을 산출하는 흐름을 보여준다.

---

---

---

## Ⅱ. 아키텍처 및 핵심 원리

인가 (Authorization) 모델 - [[569_rbac|RBAC]](역할 기반), [[572_abac|ABAC]]([[082_attribute_types_er_model|속성]] 기반, 조건부 규칙)의 핵심 원리와 구성 요소를 이해하기 위해 다음 구조를 살펴본다.

| 구성 요소 | 역할 | 적용 기준 |
| :--- | :--- | :--- |
| 개념 정의 | 핵심 용어와 범위를 명확히 [[009_config|설정]] | 용어 혼용·오해 방지 |
| 원칙 및 규칙 | 적용 시 따라야 할 기본 방향 | [[194_consistency_database_integrity|일관성]]·품질 기준 |
| 기법 및 도구 | 실질적 구현 방법과 지원 도구 | 생산성·자동화 |
| 측정 지표 | 결과물의 품질을 정량화하는 지표 | 의사결정 근거 |

인가 (Authorization) 모델의 핵심 원리는 **복잡성 분해**, **역할 분리**, **품질 측정**의 세 축으로 이해할 수 있다. 복잡한 문제를 관리 가능한 단위로 나누고, 각 역할의 책임을 명확히 하며, 결과를 정량적 지표로 평가하는 과정이 반복된다.

- **📢 섹션 요약 비유**: 인가 (Authorization) 모델의 아키텍처는 공장의 생산 라인과 같다. 각 공정(구성 요소)이 명확한 역할을 가지고 정해진 순서대로 움직여야 최종 제품의 품질이 보장된다. 어느 한 공정이 부실하면 전체 제품이 불량이 된다.

---

---

---

## Ⅲ. 비교 및 연결

인가 (Authorization) 모델을(를) 유사 개념과 비교하면 경계와 특성이 더 명확해진다.

| 비교 항목 | 인가 (Authorization) 모델 | 유사 대안 |
| :--- | :--- | :--- |
| 핵심 목적 | 체계적 품질·생산성 향상 | 임시 방편적 해결 |
| 적용 규모 | 중·대규모 프로젝트에서 효과적 | 소규모에서는 오버헤드 발생 가능 |
| 조직 요건 | 팀 전체의 공통 이해와 훈련 필요 | 개인 역량 의존 |
| 측정 가능성 | 정량적 지표로 성과 측정 가능 | 주관적 판단에 의존 |

다른 [[001_software_engineering_definition|소프트웨어 공학]] 개념과의 연결을 보면, 인가 (Authorization) 모델은(는) 요구공학·설계·테스트·형상관리 전반에 걸쳐 영향을 미친다. 특히 품질 보증(QA, Quality Assurance)과 [[020_software_configuration_management|형상 관리]]([[167_scm_software_configuration_management|SCM]], [[020_software_configuration_management|Software Configuration Management]])와 긴밀하게 연계된다.

- **📢 섹션 요약 비유**: 인가 (Authorization) 모델과 유사 대안의 차이는 지도를 가지고 산에 오르는 것과 감으로만 오르는 차이와 같다. 지도(체계적 방법)가 있으면 정상까지 최단 경로를 찾을 수 있지만, 없으면 같은 곳을 맴돌거나 낭떠러지에 빠질 수 있다.

---

---

---

## Ⅳ. 실무 적용 및 기술사 판단

인가 (Authorization) 모델을(를) 실무에 적용할 때는 다음 판단 기준을 참고한다.

- **📢 섹션 요약 비유**: 인가 (Authorization) 모델은(는) 복잡한 공사 현장에서 설계도와 공정표를 기반으로 팀을 이끄는 현장 감독과 같다. 원칙 없이 무작정 짓기 시작하면 결국 재공사가 필요하듯, 소프트웨어도 올바른 원칙 위에서만 품질과 효율이 보장된다.

---

---

## Ⅴ. 기대효과 및 결론

인가 (Authorization) 모델을(를) 올바르게 적용하면 [[339_software_quality_definition|소프트웨어 품질]]·[[346_maintainability_portability|유지보수성]]·팀 생산성이 동시에 향상된다. 그러나 도입에는 학습 비용과 [[459_quic_fec_forward_error_correction|초기]] 투자가 필요하며, 조직 전체의 공감과 훈련이 선행되어야 한다.

**한계와 전제 조건**:
- 소규모 프로젝트에서는 오버헤드가 발생할 수 있다
- 팀 전체의 충분한 교육과 실습 기간이 필요하다
- 도구 지원 환경 구축에 [[459_quic_fec_forward_error_correction|초기]] 비용이 발생한다

**미래 발전 방향**:
- [[190_ai_llm_requirements_specification|AI]]·[[263_llm_large_language_model|LLM]] 기반 자동화 도구와의 통합으로 적용 효율 향상
- [[531_cloud_native_architecture|클라우드 네이티브]]·[[652_devops_calms_culture|DevOps]] 환경에서의 진화적 적용
- 정량적 측정 체계의 고도화를 통한 의사결정 지원 강화

인가 (Authorization) 모델은 '어떻게 빠르게 짜는가'가 아니라 '어떻게 오래 유지할 수 있는 소프트웨어를 짜는가'에 대한 답이다. 단기 속도보다 장기 지속 가능성을 추구하는 관점으로 기억해야 한다.

- **📢 섹션 요약 비유**: 인가 (Authorization) 모델의 기대효과는 마라톤 훈련과 같다. 처음에는 느리고 고통스럽지만, 올바른 훈련 원칙을 지킨 선수만이 결승선에서 최고의 기록을 낼 수 있다. [[001_software_engineering_definition|소프트웨어 공학]]의 원칙도 단기 편의보다 장기 완성도를 위한 투자다.

---

---

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[001_software_engineering_definition|소프트웨어 공학]] ([[001_software_engineering_definition|Software Engineering]]) | 인가 (Authorization) 모델의 상위 학문 체계이며 품질·생산성 향상의 공통 목표를 공유한다 |
| [[003_sdlc|소프트웨어 생명주기]] ([[131_sdlc_system_development_life_cycle_waterfall_agile|SDLC]], Software Development Life Cycle) | 인가 (Authorization) 모델은 SDLC의 특정 단계에서 핵심적으로 적용된다 |
| 품질 보증 (QA, Quality Assurance) | 인가 (Authorization) 모델 적용 결과는 QA 활동을 통해 검증되고 측정된다 |
| [[020_software_configuration_management|형상 관리]] ([[167_scm_software_configuration_management|SCM]], [[020_software_configuration_management|Software Configuration Management]]) | 인가 (Authorization) 모델에서 생성된 산출물은 SCM을 통해 체계적으로 관리된다 |

### 📈 관련 키워드 및 발전 흐름도

```text
소프트웨어 위기 (Software Crisis) 인식
    │
    ▼
인가 (Authorization) 모델 개념 정립
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

1. 인가 (Authorization) 모델은 레고 블록으로 성을 만들 때처럼, 규칙을 정하고 역할을 나누어 함께 작업하는 방법이에요.
2. 혼자서 막 만들면 나중에 무너지거나 고치기 어렵지만, 약속을 지키면 누구나 쉽게 고치고 더 크게 만들 수 있어요.
3. 그래서 [[001_software_engineering_definition|소프트웨어 공학]]은 프로그래머들이 좋은 프로그램을 빠르고 안전하게 만들 수 있게 도와주는 '규칙 모음집'이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 610 / 973

← **이전**: [[509_authorization_models|509. 인가 (Authorization) 모델 - RBAC, ABAC]]
**다음**: [[510_api_security_management|510. API 보안 관리 - OAuth 2.0, OIDC, JWT]] →

---
