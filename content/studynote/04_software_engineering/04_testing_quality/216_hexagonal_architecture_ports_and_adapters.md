+++
title = "216. 헥사고날 아키텍처 (Hexagonal Architecture / Ports and Adapters)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 헥사고날 아키텍처 ([Hexagonal Architecture](/knowledge-base/studynote/11_design_supervision/06_exam_summary/366_process/) / Ports and Adapters)은(는) [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)의 핵심 개념으로, 복잡한 시스템을 체계적으로 설계·관리하기 위한 원칙과 기법이다.
> 2. **가치**: 이 개념을 올바르게 적용하면 소프트웨어의 품질·[유지보수성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/)·재사용성이 향상되고, 개발 생산성과 팀 협업 효율이 높아진다.
> 3. **판단 포인트**: 도입 시에는 비용·복잡도·조직 성숙도를 함께 고려해야 하며, 맹목적 적용보다 프로젝트 특성에 맞는 선택적 적용이 핵심이다.

---

## Ⅰ. 개요 및 필요성

- 205번 3계층(UI ➜ 비즈니스 ➜ DB)의 치명적 단점은 화살표의 방향이 <strong>위에서 아래로(<a href="/knowledge-base/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/">단방향</a>)</strong> 향한다는 것입니다.
- 2층(비즈니스 뇌)이 1층(DB [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/))을 직접 호출(`Call`)하기 때문에, 오라클 전용 SQL 문법이 뇌 코드 안으로 더럽게 파고들어 섞입니다. 뇌([도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/))가 껍데기 기계 기술(DB)에 노예처럼 종속되어버렸습니다.

- **📢 섹션 요약 비유**: 헥사고날 아키텍처 ([Hexagonal Architecture](/knowledge-base/studynote/11_design_supervision/06_exam_summary/366_process/) / Ports and Adapters)은(는) 복잡한 공사 현장에서 설계도와 공정표를 기반으로 팀을 이끄는 현장 감독과 같다. 원칙 없이 무작정 짓기 시작하면 결국 재공사가 필요하듯, 소프트웨어도 올바른 원칙 위에서만 품질과 효율이 보장된다.

다음은 헥사고날 아키텍처 (Hexagonal의 핵심 구조와 흐름을 보여주는 다이어그램이다.

```text
+-------------------------------------------------------------+
|                  헥사고날 아키텍처 (Hexagonal                        |
+-------------------------------------------------------------+
|                                                             |
|  [입력/요구사항] ---> [핵심 처리 과정] ---> [출력/결과물]  |
|       |                    |                    |          |
|       v                    v                    v          |
|   요구 분석           설계·적용           품질 검증        |
|                                                             |
+-------------------------------------------------------------+
```

이 다이어그램은 헥사고날 아키텍처 (Hexagonal가 입력 요구사항을 받아 핵심 처리 과정을 거쳐 검증된 결과물을 산출하는 흐름을 보여준다.

---

---

## Ⅱ. 아키텍처 및 핵심 원리

- **개념**: 앨리스터 코오번(Alistair Cockburn)이 제안한 구조로, 시스템의 가장 핵심인 <strong>'비즈니스 로직(<a href="/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/">도메인</a> 모델)'을 정중앙(육각형의 안쪽)에 꽁꽁 숨겨두고, 외부의 모든 기술(웹 화면, DB, 외부 <a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/">API</a>)은 육각형 바깥쪽에서 '<a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/">포트</a>(<a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/">Port</a>)'와 '<a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/">어댑터</a>(<a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/">Adapter</a>)'를 통해서만 내부 뇌와 통신하도록 설계하여, 내부 <a href="/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/">도메인</a> 코드를 외부 기술 변화로부터 100% 완벽하게 격리시키는 패턴</strong>입니다.

- **📢 섹션 요약 비유**: 헥사고날 아키텍처 ([Hexagonal Architecture](/knowledge-base/studynote/11_design_supervision/06_exam_summary/366_process/) / Ports and Adapters)은(는) 복잡한 공사 현장에서 설계도와 공정표를 기반으로 팀을 이끄는 현장 감독과 같다. 원칙 없이 무작정 짓기 시작하면 결국 재공사가 필요하듯, 소프트웨어도 올바른 원칙 위에서만 품질과 효율이 보장된다.

| 항목 | 설명 | 비고 |
| :--- | :--- | :--- |
| 핵심 특성 | 헥사고날 아키텍처 ([Hexagonal Architecture](/knowledge-base/studynote/11_design_supervision/06_exam_summary/366_process/) / Ports and Adapters)의 핵심 특성과 동작 방식 | 필수 이해 요소 |
| 적용 범위 | 어떤 프로젝트·상황에서 활용하는지 | 선택 기준 |
| 제약 조건 | 적용 시 주의해야 할 전제·한계 | 트레이드오프 |

---

---

## Ⅲ. 비교 및 연결

헥사고날 아키텍처 ([Hexagonal Architecture](/knowledge-base/studynote/11_design_supervision/06_exam_summary/366_process/) / Ports and Adapters)을(를) 유사 개념과 비교하면 경계와 특성이 더 명확해진다.

| 비교 항목 | 헥사고날 아키텍처 ([Hexagonal Architecture](/knowledge-base/studynote/11_design_supervision/06_exam_summary/366_process/) / Ports and Adapters) | 유사 대안 |
| :--- | :--- | :--- |
| 핵심 목적 | 체계적 품질·생산성 향상 | 임시 방편적 해결 |
| 적용 규모 | 중·대규모 프로젝트에서 효과적 | 소규모에서는 오버헤드 발생 가능 |
| 조직 요건 | 팀 전체의 공통 이해와 훈련 필요 | 개인 역량 의존 |
| 측정 가능성 | 정량적 지표로 성과 측정 가능 | 주관적 판단에 의존 |

다른 [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/) 개념과의 연결을 보면, 헥사고날 아키텍처 ([Hexagonal Architecture](/knowledge-base/studynote/11_design_supervision/06_exam_summary/366_process/) / Ports and Adapters)은(는) 요구공학·설계·테스트·형상관리 전반에 걸쳐 영향을 미친다. 특히 품질 보증(QA, Quality Assurance)과 [형상 관리](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)([SCM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/), [Software Configuration Management](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/))와 긴밀하게 연계된다.

- **📢 섹션 요약 비유**: 헥사고날 아키텍처 ([Hexagonal Architecture](/knowledge-base/studynote/11_design_supervision/06_exam_summary/366_process/) / Ports and Adapters)과 유사 대안의 차이는 지도를 가지고 산에 오르는 것과 감으로만 오르는 차이와 같다. 지도(체계적 방법)가 있으면 정상까지 최단 경로를 찾을 수 있지만, 없으면 같은 곳을 맴돌거나 낭떠러지에 빠질 수 있다.

---

---

## Ⅳ. 실무 적용 및 기술사 판단

- **의존성의 방향**: 화살표가 밖에서 무조건 안쪽(정중앙 육각형)을 향해 꽂힙니다. 1층(DB)이 2층(뇌)을 향해 거꾸로 꽂히는 <strong><a href="/knowledge-base/studynote/11_design_supervision/02_architecture_principles/106_dip_dependency_inversion_principle/">의존성 역전 원칙</a>(<a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/247_dip_dependency_inversion_principle/">Dependency Inversion Principle</a>)</strong>이 발동한 것입니다!
- **기적의 결과**: 나중에 DB를 오라클에서 몽고DB로 바꿉니다. 정중앙의 '비즈니스 뇌' 코드는 1줄도 수정하지 않습니다. 그냥 육각형 바깥에 꽂혀있던 '오라클 [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/) 돼지코'를 뽑아버리고, 1시간 만에 새로 짠 '몽고DB [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/) 돼지코'를 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 구멍에 찰칵 끼워 넣으면 끝납니다. (플러그 앤 플레이)
- **테스트**: DB 없이도 뇌 코드만 쏙 빼서 1초 만에 수만 번 [유닛 테스트](/knowledge-base/studynote/15_devops_sre/05_devsecops/263_unit_test_mocking_stubbing/)(Mocking)를 돌릴 수 있는 [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 환경의 최고급 엘리트 아키텍처입니다.

> 📢 **섹션 요약 비유**: 기존 <strong>계층형(Layered) 아키텍처</strong>는 회사의 핵심 두뇌인 <strong>'회장님(비즈니스 로직)'이 지하 창고(DB)에 직접 내려가서 먼지를 뒤집어쓰고 엑셀 파일을 뒤지는 꼴</strong>이었습니다. 창고가 이사 가면 회장님도 짐을 싸야 했습니다(DB [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/)). 이를 부숴버린 <strong>헥사고날(Hexagonal) 아키텍처</strong>는 회장님을 빌딩 꼭대기 <strong>'무균실 유리 캡슐(육각형 내부 <a href="/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/">도메인</a>)'</strong> 안에 가둬버린 것입니다. 회장님은 절대 방 밖으로 나가지 않고 오직 회사 운영(핵심 로직)만 고민합니다. 유리 캡슐 벽면에는 여러 개의 <strong>'마이크와 스피커 구멍(<a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/">Port</a>)'</strong>이 뚫려 있습니다. 지하 창고에서 서류를 올려보낼 때는 비서([어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/) [Adapter](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/))가 서류를 받아, 회장님이 쓰는 표준 한국어(자바 인터페이스)로 깔끔하게 통역하여 스피커 구멍으로 쏙 넣어줍니다. 내일 창고가 미국식(몽고DB)으로 바뀌어 영어가 올라와도, 회장님은 알 바 아닙니다. 영어 통역이 가능한 새 비서(새 [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/))로 갈아치우기만 하면, 회장님은 여전히 한국어만 들으며 영원히 무균실에서 평화롭게 회사를 통치할 수 있는 궁극의 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 아키텍처입니다.

- **📢 섹션 요약 비유**: 헥사고날 아키텍처 ([Hexagonal Architecture](/knowledge-base/studynote/11_design_supervision/06_exam_summary/366_process/) / Ports and Adapters)은(는) 복잡한 공사 현장에서 설계도와 공정표를 기반으로 팀을 이끄는 현장 감독과 같다. 원칙 없이 무작정 짓기 시작하면 결국 재공사가 필요하듯, 소프트웨어도 올바른 원칙 위에서만 품질과 효율이 보장된다.

---

---

## Ⅴ. 기대효과 및 결론

헥사고날 아키텍처 ([Hexagonal Architecture](/knowledge-base/studynote/11_design_supervision/06_exam_summary/366_process/) / Ports and Adapters)을(를) 올바르게 적용하면 [소프트웨어 품질](/knowledge-base/studynote/04_software_engineering/06_software_architecture/339_software_quality_definition/)·[유지보수성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/)·팀 생산성이 동시에 향상된다. 그러나 도입에는 학습 비용과 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 투자가 필요하며, 조직 전체의 공감과 훈련이 선행되어야 한다.

**한계와 전제 조건**:
- 소규모 프로젝트에서는 오버헤드가 발생할 수 있다
- 팀 전체의 충분한 교육과 실습 기간이 필요하다
- 도구 지원 환경 구축에 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 비용이 발생한다

**미래 발전 방향**:
- [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)·[LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 기반 자동화 도구와의 통합으로 적용 효율 향상
- [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/)·[DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) 환경에서의 진화적 적용
- 정량적 측정 체계의 고도화를 통한 의사결정 지원 강화

헥사고날 아키텍처 ([Hexagonal Architecture](/knowledge-base/studynote/11_design_supervision/06_exam_summary/366_process/) / Ports and Adapters)은 '어떻게 빠르게 짜는가'가 아니라 '어떻게 오래 유지할 수 있는 소프트웨어를 짜는가'에 대한 답이다. 단기 속도보다 장기 지속 가능성을 추구하는 관점으로 기억해야 한다.

- **📢 섹션 요약 비유**: 헥사고날 아키텍처 ([Hexagonal Architecture](/knowledge-base/studynote/11_design_supervision/06_exam_summary/366_process/) / Ports and Adapters)의 기대효과는 마라톤 훈련과 같다. 처음에는 느리고 고통스럽지만, 올바른 훈련 원칙을 지킨 선수만이 결승선에서 최고의 기록을 낼 수 있다. [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)의 원칙도 단기 편의보다 장기 완성도를 위한 투자다.

---

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/) ([Software 엔진ering](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)) | 헥사고날 아키텍처 ([Hexagonal Architecture](/knowledge-base/studynote/11_design_supervision/06_exam_summary/366_process/) / Ports and Adapters)의 상위 학문 체계이며 품질·생산성 향상의 공통 목표를 공유한다 |
| [소프트웨어 생명주기](/knowledge-base/studynote/04_software_engineering/01_overview_principles/003_sdlc/) ([SDLC](/knowledge-base/studynote/12_it_management/04_sdlc_testing/131_sdlc_system_development_life_cycle_waterfall_agile/), Software Development Life Cycle) | 헥사고날 아키텍처 ([Hexagonal Architecture](/knowledge-base/studynote/11_design_supervision/06_exam_summary/366_process/) / Ports and Adapters)은 SDLC의 특정 단계에서 핵심적으로 적용된다 |
| 품질 보증 (QA, Quality Assurance) | 헥사고날 아키텍처 ([Hexagonal Architecture](/knowledge-base/studynote/11_design_supervision/06_exam_summary/366_process/) / Ports and Adapters) 적용 결과는 QA 활동을 통해 검증되고 측정된다 |
| [형상 관리](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/) ([SCM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/), [Software Configuration Management](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)) | 헥사고날 아키텍처 ([Hexagonal Architecture](/knowledge-base/studynote/11_design_supervision/06_exam_summary/366_process/) / Ports and Adapters)에서 생성된 산출물은 SCM을 통해 체계적으로 관리된다 |

### 📈 관련 키워드 및 발전 흐름도

```text
소프트웨어 위기 (Software Crisis) 인식
    |
    v
헥사고날 아키텍처 (Hexagonal Architecture / Ports and Adapters) 개념 정립
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

이 흐름은 [소프트웨어 위기](/knowledge-base/studynote/04_software_engineering/01_overview_principles/002_software_crisis/) 인식 -> 체계적 방법론 개발 -> 표준화 -> 현대적 플랫폼 적용으로 이어지는 발전 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 헥사고날 아키텍처 ([Hexagonal Architecture](/knowledge-base/studynote/11_design_supervision/06_exam_summary/366_process/) / Ports and Adapters)은 레고 블록으로 성을 만들 때처럼, 규칙을 정하고 역할을 나누어 함께 작업하는 방법이에요.
2. 혼자서 막 만들면 나중에 무너지거나 고치기 어렵지만, 약속을 지키면 누구나 쉽게 고치고 더 크게 만들 수 있어요.
3. 그래서 [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)은 프로그래머들이 좋은 프로그램을 빠르고 안전하게 만들 수 있게 도와주는 '규칙 모음집'이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 216 / 973

<- **이전**: [215. 서버리스 아키텍처 (Serverless Architecture / FaaS)](/knowledge-base/studynote/04_software_engineering/04_testing_quality/215_serverless_architecture_faas_aws_lambda/)
**다음**: [217. 클린 아키텍처 (Clean Architecture) - Robert C. Martin (Uncle Bob)](/knowledge-base/studynote/04_software_engineering/04_testing_quality/217_clean_architecture_dependency_rule/) ->

---
