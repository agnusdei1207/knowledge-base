---
title: "Serverless Architecture / FaaS"
date: "2026-05-08"
tags:
  - "studynote-software-engineering"
weight: 215
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 아키텍처 ([Serverless Architecture](/studynote/04_software_engineering/11_testing_validation/950_serverless_architecture/) / [FaaS](/studynote/12_it_management/05_security_compliance/342_faas/))은(는) [소프트웨어 공학](/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)의 핵심 개념으로, 복잡한 시스템을 체계적으로 설계·관리하기 위한 원칙과 기법이다.
> 2. **가치**: 이 개념을 올바르게 적용하면 소프트웨어의 품질·[유지보수성](/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/)·재사용성이 향상되고, 개발 생산성과 팀 협업 효율이 높아진다.
> 3. **판단 포인트**: 도입 시에는 비용·복잡도·조직 성숙도를 함께 고려해야 하며, 맹목적 적용보다 프로젝트 특성에 맞는 선택적 적용이 핵심이다.

---

## Ⅰ. 개요 및 필요성

- EC2나 [도커](/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/) 컨테이너는 어쨌든 리눅스가 부팅되어 24시간 내내 메모리(RAM)에 상주하며 윙윙 돌아갑니다.
- 1시간에 1번 호출되는 '이미지 리사이징(썸네일 깎기)' 서버를 위해 한 달 내내 10만 원짜리 서버를 켜두는 것은 미친 낭비(Over-provisioning)입니다.

- **📢 섹션 요약 비유**: [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 아키텍처 ([Serverless Architecture](/studynote/04_software_engineering/11_testing_validation/950_serverless_architecture/) / [FaaS](/studynote/12_it_management/05_security_compliance/342_faas/))은(는) 복잡한 공사 현장에서 설계도와 공정표를 기반으로 팀을 이끄는 현장 감독과 같다. 원칙 없이 무작정 짓기 시작하면 결국 재공사가 필요하듯, 소프트웨어도 올바른 원칙 위에서만 품질과 효율이 보장된다.

다음은 [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 아키텍처 (Serverles의 핵심 구조와 흐름을 보여주는 다이어그램이다.

```text
+-------------------------------------------------------------+
|                  서버리스 아키텍처 (Serverles                        |
+-------------------------------------------------------------+
|                                                             |
|  [입력/요구사항] ---> [핵심 처리 과정] ---> [출력/결과물]  |
|       |                    |                    |          |
|       v                    v                    v          |
|   요구 분석           설계·적용           품질 검증        |
|                                                             |
+-------------------------------------------------------------+
```

이 다이어그램은 [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 아키텍처 (Serverles가 입력 요구사항을 받아 핵심 처리 과정을 거쳐 검증된 결과물을 산출하는 흐름을 보여준다.

---

---

## Ⅱ. 아키텍처 및 핵심 원리

- <strong><a href="/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/">서버리스</a></strong>: 아마존 [데이터센터](/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) 어딘가에 물리적 서버는 분명히 있습니다! 단지 <strong>개발자(나)의 눈앞에서 '서버 관리(OS 패치, 용량 조절, 부팅)'라는 개념 자체가 100% 투명하게 사라져버렸다는 뜻(<a href="/studynote/04_software_engineering/02_requirements_analysis/094_less_large_scale_scrum/">Less</a>)</strong>입니다.
- <strong><a href="/studynote/12_it_management/05_security_compliance/342_faas/">FaaS</a> (Function <a href="/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/">as</a> a <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">Service</a>)</strong>: [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)를 구현하는 핵심 아키텍처. 거대한 앱 코드를 버리고, `이미지_자르기()`, `비번_검사하기()` 같은 아주 작은 <strong>단일 함수(Function) 단위의 조각 코드만 AWS 클라우드에 툭 던져놓고, 이 함수가 호출될 때마다 실행 환경이 찰나에 켜졌다가 죽는 <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a></strong>입니다. (대표작: <strong>AWS <a href="/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/">Lambda</a></strong>)

- **📢 섹션 요약 비유**: [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 아키텍처 ([Serverless Architecture](/studynote/04_software_engineering/11_testing_validation/950_serverless_architecture/) / [FaaS](/studynote/12_it_management/05_security_compliance/342_faas/))은(는) 복잡한 공사 현장에서 설계도와 공정표를 기반으로 팀을 이끄는 현장 감독과 같다. 원칙 없이 무작정 짓기 시작하면 결국 재공사가 필요하듯, 소프트웨어도 올바른 원칙 위에서만 품질과 효율이 보장된다.

| 항목 | 설명 | 비고 |
| :--- | :--- | :--- |
| 핵심 특성 | [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 아키텍처 ([Serverless Architecture](/studynote/04_software_engineering/11_testing_validation/950_serverless_architecture/) / [FaaS](/studynote/12_it_management/05_security_compliance/342_faas/))의 핵심 특성과 동작 방식 | 필수 이해 요소 |
| 적용 범위 | 어떤 프로젝트·상황에서 활용하는지 | 선택 기준 |
| 제약 조건 | 적용 시 주의해야 할 전제·한계 | 트레이드오프 |

---

---

## Ⅲ. 비교 및 연결

[서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 아키텍처 ([Serverless Architecture](/studynote/04_software_engineering/11_testing_validation/950_serverless_architecture/) / [FaaS](/studynote/12_it_management/05_security_compliance/342_faas/))을(를) 유사 개념과 비교하면 경계와 특성이 더 명확해진다.

| 비교 항목 | [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 아키텍처 ([Serverless Architecture](/studynote/04_software_engineering/11_testing_validation/950_serverless_architecture/) / [FaaS](/studynote/12_it_management/05_security_compliance/342_faas/)) | 유사 대안 |
| :--- | :--- | :--- |
| 핵심 목적 | 체계적 품질·생산성 향상 | 임시 방편적 해결 |
| 적용 규모 | 중·대규모 프로젝트에서 효과적 | 소규모에서는 오버헤드 발생 가능 |
| 조직 요건 | 팀 전체의 공통 이해와 훈련 필요 | 개인 역량 의존 |
| 측정 가능성 | 정량적 지표로 성과 측정 가능 | 주관적 판단에 의존 |

다른 [소프트웨어 공학](/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/) 개념과의 연결을 보면, [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 아키텍처 ([Serverless Architecture](/studynote/04_software_engineering/11_testing_validation/950_serverless_architecture/) / [FaaS](/studynote/12_it_management/05_security_compliance/342_faas/))은(는) 요구공학·설계·테스트·형상관리 전반에 걸쳐 영향을 미친다. 특히 품질 보증(QA, Quality Assurance)과 [형상 관리](/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)([SCM](/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/), [Software Configuration Management](/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/))와 긴밀하게 연계된다.

- **📢 섹션 요약 비유**: [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 아키텍처 ([Serverless Architecture](/studynote/04_software_engineering/11_testing_validation/950_serverless_architecture/) / [FaaS](/studynote/12_it_management/05_security_compliance/342_faas/))과 유사 대안의 차이는 지도를 가지고 산에 오르는 것과 감으로만 오르는 차이와 같다. 지도(체계적 방법)가 있으면 정상까지 최단 경로를 찾을 수 있지만, 없으면 같은 곳을 맴돌거나 낭떠러지에 빠질 수 있다.

---

---

## Ⅳ. 실무 적용 및 기술사 판단

- <strong><a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/559_serverless_cold_start_mitigation/">콜드 스타트</a> (<a href="/studynote/06_ict_convergence/05_data_science/347_cold_start_problem/">Cold Start</a>) 🌟</strong>: 함수가 냉동고에 죽어있다가, 첫 요청이 들어왔을 때 컨테이너를 띄우고 코드를 메모리에 올리느라 <strong>최초 실행 시 약 1~3초의 <a href="/studynote/03_network/01_data_communication/015_지연_데이터_관점/">지연</a>(딜레이)이 터지는 치명적 맹점</strong>입니다.
- 즉시 응답이 필요한 MMORPG 게임 서버나 0.01초가 중요한 주식 거래 시스템에는 절대 [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)를 쓰면 안 됩니다(계속 켜져 있는 [도커](/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/) 컨테이너를 써야 함). 가끔 비동기로 돌리는 배치(Batch) 작업이나 썸네일 처리에만 써야 하는 날카로운 비수입니다.

> 📢 **섹션 요약 비유**: 기존의 <strong>클라우드 서버(<a href="/studynote/06_ict_convergence/03_cloud_infrastructure/183_iaas_infrastructure_as_a_service/">IaaS</a>/<a href="/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/">PaaS</a>)</strong>는 회사 로비에 <strong>'월급을 300만 원씩 주고 24시간 앉혀둔 상주 경비원'</strong>입니다. 도둑이 오든 안 오든 1년 365일 책상을 지키고 있으니 월급(서버 유지비)이 미친 듯이 나갑니다. <strong><a href="/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/">서버리스</a> 아키텍처(<a href="/studynote/12_it_management/05_security_compliance/342_faas/">FaaS</a>, AWS <a href="/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/">Lambda</a>)</strong>는 상주 경비원을 다 해고하고 아예 빈 건물로 만들어둔 것입니다. 평소엔 텅 비어있어 인건비가 <strong>'0원'</strong>입니다. 그러다 로비 센서에 도둑(이벤트/트래픽)이 침입하는 찰나의 순간! 허공에서 **'용병(Function 함수)'** 한 명이 0.1초 만에 텔레포트로 튀어나와 도둑의 목을 따버리고, 그 즉시 다시 연기처럼 펑 사라져버립니다. 도둑이 100명 오면 허공에서 용병 100명이 튀어나와 1초 만에 처리하고 사라집니다(극강의 오토 [스케일링](/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/)). 사장님은 한 달 뒤에, 이 용병들이 나타나서 도둑의 목을 따는 데 걸린 '딱 1초'라는 시간 동안의 시급(초 단위 과금)만 계산해서 용역 회사(AWS)에 1,000원만 계좌이체 해주면 끝나는, IT 인프라 역사상 최고의 짠돌이 경제학 모델입니다.

- **📢 섹션 요약 비유**: [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 아키텍처 ([Serverless Architecture](/studynote/04_software_engineering/11_testing_validation/950_serverless_architecture/) / [FaaS](/studynote/12_it_management/05_security_compliance/342_faas/))은(는) 복잡한 공사 현장에서 설계도와 공정표를 기반으로 팀을 이끄는 현장 감독과 같다. 원칙 없이 무작정 짓기 시작하면 결국 재공사가 필요하듯, 소프트웨어도 올바른 원칙 위에서만 품질과 효율이 보장된다.

---

---

## Ⅴ. 기대효과 및 결론

[서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 아키텍처 ([Serverless Architecture](/studynote/04_software_engineering/11_testing_validation/950_serverless_architecture/) / [FaaS](/studynote/12_it_management/05_security_compliance/342_faas/))을(를) 올바르게 적용하면 [소프트웨어 품질](/studynote/04_software_engineering/06_software_architecture/339_software_quality_definition/)·[유지보수성](/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/)·팀 생산성이 동시에 향상된다. 그러나 도입에는 학습 비용과 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 투자가 필요하며, 조직 전체의 공감과 훈련이 선행되어야 한다.

**한계와 전제 조건**:
- 소규모 프로젝트에서는 오버헤드가 발생할 수 있다
- 팀 전체의 충분한 교육과 실습 기간이 필요하다
- 도구 지원 환경 구축에 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 비용이 발생한다

**미래 발전 방향**:
- [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)·[LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 기반 자동화 도구와의 통합으로 적용 효율 향상
- [클라우드 네이티브](/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/)·[DevOps](/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) 환경에서의 진화적 적용
- 정량적 측정 체계의 고도화를 통한 의사결정 지원 강화

[서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 아키텍처 ([Serverless Architecture](/studynote/04_software_engineering/11_testing_validation/950_serverless_architecture/) / [FaaS](/studynote/12_it_management/05_security_compliance/342_faas/))은 '어떻게 빠르게 짜는가'가 아니라 '어떻게 오래 유지할 수 있는 소프트웨어를 짜는가'에 대한 답이다. 단기 속도보다 장기 지속 가능성을 추구하는 관점으로 기억해야 한다.

- **📢 섹션 요약 비유**: [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 아키텍처 ([Serverless Architecture](/studynote/04_software_engineering/11_testing_validation/950_serverless_architecture/) / [FaaS](/studynote/12_it_management/05_security_compliance/342_faas/))의 기대효과는 마라톤 훈련과 같다. 처음에는 느리고 고통스럽지만, 올바른 훈련 원칙을 지킨 선수만이 결승선에서 최고의 기록을 낼 수 있다. [소프트웨어 공학](/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)의 원칙도 단기 편의보다 장기 완성도를 위한 투자다.

---

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [소프트웨어 공학](/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/) ([Software 엔진ering](/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)) | [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 아키텍처 ([Serverless Architecture](/studynote/04_software_engineering/11_testing_validation/950_serverless_architecture/) / [FaaS](/studynote/12_it_management/05_security_compliance/342_faas/))의 상위 학문 체계이며 품질·생산성 향상의 공통 목표를 공유한다 |
| [소프트웨어 생명주기](/studynote/04_software_engineering/01_overview_principles/003_sdlc/) ([SDLC](/studynote/12_it_management/04_sdlc_testing/131_sdlc_system_development_life_cycle_waterfall_agile/), Software Development Life Cycle) | [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 아키텍처 ([Serverless Architecture](/studynote/04_software_engineering/11_testing_validation/950_serverless_architecture/) / [FaaS](/studynote/12_it_management/05_security_compliance/342_faas/))은 SDLC의 특정 단계에서 핵심적으로 적용된다 |
| 품질 보증 (QA, Quality Assurance) | [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 아키텍처 ([Serverless Architecture](/studynote/04_software_engineering/11_testing_validation/950_serverless_architecture/) / [FaaS](/studynote/12_it_management/05_security_compliance/342_faas/)) 적용 결과는 QA 활동을 통해 검증되고 측정된다 |
| [형상 관리](/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/) ([SCM](/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/), [Software Configuration Management](/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)) | [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 아키텍처 ([Serverless Architecture](/studynote/04_software_engineering/11_testing_validation/950_serverless_architecture/) / [FaaS](/studynote/12_it_management/05_security_compliance/342_faas/))에서 생성된 산출물은 SCM을 통해 체계적으로 관리된다 |

### 📈 관련 키워드 및 발전 흐름도

```text
소프트웨어 위기 (Software Crisis) 인식
    |
    v
서버리스 아키텍처 (Serverless Architecture / FaaS) 개념 정립
    |
    v
표준화 및 방법론 체계화 (ISO, CMMI, Agile)
    |
    v
클라우드 네이티브·AI 기반 확장 적용
    |
    v
지속적 개선 및 DevOps·MLOps 통합
```

이 흐름은 [소프트웨어 위기](/studynote/04_software_engineering/01_overview_principles/002_software_crisis/) 인식 -> 체계적 방법론 개발 -> 표준화 -> 현대적 플랫폼 적용으로 이어지는 발전 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 아키텍처 ([Serverless Architecture](/studynote/04_software_engineering/11_testing_validation/950_serverless_architecture/) / [FaaS](/studynote/12_it_management/05_security_compliance/342_faas/))은 레고 블록으로 성을 만들 때처럼, 규칙을 정하고 역할을 나누어 함께 작업하는 방법이에요.
2. 혼자서 막 만들면 나중에 무너지거나 고치기 어렵지만, 약속을 지키면 누구나 쉽게 고치고 더 크게 만들 수 있어요.
3. 그래서 [소프트웨어 공학](/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)은 프로그래머들이 좋은 프로그램을 빠르고 안전하게 만들 수 있게 도와주는 '규칙 모음집'이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 215 / 973

<- **이전**: [214. 이벤트 드리븐 아키텍처 (EDA, Event-Driven Architecture)](/studynote/04_software_engineering/04_testing_quality/214_eda_event_driven_architecture_async/)
**다음**: [216. 헥사고날 아키텍처 (Hexagonal Architecture / Ports and Adapters)](/studynote/04_software_engineering/04_testing_quality/216_hexagonal_architecture_ports_and_adapters/) ->

---
