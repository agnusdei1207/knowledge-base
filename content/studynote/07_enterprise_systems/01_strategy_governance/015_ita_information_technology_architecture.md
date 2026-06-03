+++
title = "15. ITA (Information Technology Architecture) - 과거 EA와 동의어로 쓰이던 용어 (법제화 명칭)"
description = "정보시스템의 효율적 도입 및 상호운용성을 위한 정보기술아키텍처(ITA)의 개념, 법제화 의의 및 EA와의 관계 심층 분석"
date = 2024-05-24

[taxonomies]
tags = ["enterprise_systems"]

[extra]
tags = ["enterprise_systems"]
+++

# 15. ITA (Information Technology [Architecture](/knowledge-base/studynote/12_it_management/05_security_compliance/319_architecture/))

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: ITA(정보기술아키텍처)는 조직의 비즈니스 목적을 달성하기 위해 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), 애플리케이션, 기술 인프라를 체계화한 청사진으로, 과거에 전사적 아키텍처([EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/))와 동의어로 쓰이던 명칭이다.
> 2. **가치**: 단순히 기술 지침을 넘어서, 대한민국에서 공공기관의 무분별한 IT 투자를 통제하고 시스템 간 [상호운용성](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/287_interoperability_tactics/)을 강제하기 위해 <strong>'법제화(ITA법)'</strong>된 강력한 규제 및 관리 도구다.
> 3. **융합**: 기술 지향적인 명칭(ITA)에서 비즈니스 중심의 명칭([EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/))으로 패러다임이 진화하였으며, [ISP](/knowledge-base/studynote/12_it_management/03_ea_isp/101_isp_information_strategy_planning_4_steps/)(정보화전략계획)와 결합하여 기술적 구조뿐만 아니라 IT 투자 평가와 조직 거버넌스를 아우르는 기틀이 되었다.

---

### Ⅰ. 개요 및 필요성 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Necessity)

<strong>ITA (Information Technology <a href="/knowledge-base/studynote/12_it_management/05_security_compliance/319_architecture/">Architecture</a>, 정보기술아키텍처)</strong>는 기업이나 공공기관이 정보시스템을 구축할 때 기준이 되는 [마스](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)터플랜이자 아키텍처 체계이다. 현대의 IT 실무에서는 이 용어가 전사적 아키텍처([EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/), [Enterprise Architecture](/knowledge-base/studynote/12_it_management/01_governance_strategy/010_ea_enterprise_architecture/))로 대체되어 쓰이고 있으나, 개념적 뿌리와 특히 '국가 정보화 법제도' 측면에서는 매우 중요한 역사적, 실무적 의미를 갖는다.

1990년대 후반부터 2000년대 초반, 각 부처와 기업들은 쏟아지는 신기술을 경쟁적으로 도입했다. 그 결과, 기관 내부에 서로 호환되지 않는 이기종 하드웨어, 독자적 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/), 고립된 애플리케이션이 난립하는 이른바 'IT 스파게티(Spaghetti)' 상태가 되었다. 정보의 섬(Islands of Information) 현상으로 인해 유지보수 비용은 기하급수적으로 증가했고, 비즈니스 변경에 따른 IT 시스템의 민첩성은 제로에 가까워졌다.

이러한 무질서를 바로잡고 정보화 투자의 타당성을 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하기 위해 도입된 것이 ITA이다. 한국에서는 2005년 <strong>'정보시스템의 효율적 도입 및 운영 등에 관한 법률(속칭 ITA법)'</strong>을 제정하여, 일정 규모 이상의 공공기관은 정보화 예산을 집행하기 전 반드시 ITA를 수립하도록 강제하였다. 즉, ITA는 단순한 기술적 도면이 아니라 국가가 IT 중복 투자를 묻지도 따지지도 않고 삭감하기 위해 고안한 강력한 통제 및 거버넌스 잣대인 것이다.

```text
[ITA 도입 전후의 IT 투자 및 구조 패러다임 변화]

(도입 전) 벤더/기술 종속적 파편화
[영업부] ─▶ 독자 예산 ─▶ A사 Unix 서버 + X사 DB ┐ (서로 통신 불가,
[인사부] ─▶ 독자 예산 ─▶ B사 NT 서버 + Y사 DB   ┘  데이터 중복 저장)

       ▼ ITA(정보기술아키텍처) 기반 통제 도입 ▼

(도입 후) 아키텍처/표준 기반 전사 최적화
[전사 비즈니스 목표]
       │
[ITA / EA 위원회] ◀── 기술표준(TRM), 데이터표준(DRM) 통제
       │
       ├─▶ [영업부] 표준 개방형 리눅스 + 표준 통합 DB 접근 API
       └─▶ [인사부] 표준 개방형 리눅스 + 표준 통합 DB 접근 API
       => 벤더 종속(Lock-in) 타파, 인프라 비용 절감, 데이터 통합 달성
```
*해설: 이 다이어그램은 ITA가 기술의 영역을 넘어 예산과 거버넌스를 어떻게 통제하는지 보여준다. 도입 전에는 힘 있는 부서가 원하는 벤더의 기술을 임의로 도입했지만, ITA 도입 후에는 전사 기술 [참조 모델](/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model/)([TRM](/knowledge-base/studynote/12_it_management/03_ea_isp/120_trm_technical_reference_model/))을 준수하지 않는 프로젝트는 예산 배정 자체가 차단된다.*

📢 **섹션 요약 비유**: ITA는 난개발로 엉망이 된 도시에 내려진 강력한 '건축법'과 같습니다. 이전에는 누구나 자기 땅에 마음대로 판잣집이나 빌딩을 지었다면, ITA 도입 후에는 하수도 규격과 도로 폭 등 도시 전체의 표준 도면을 먼저 승인받아야만 건물을 올릴 수 있게 통제한 것입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

법제도 관점에서 규정된 ITA의 구성 요소는 크게 <strong><a href="/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/">EA</a>(<a href="/knowledge-base/studynote/12_it_management/01_governance_strategy/010_ea_enterprise_architecture/">Enterprise Architecture</a>, 아키텍처 매트릭스 자체), <a href="/knowledge-base/studynote/12_it_management/03_ea_isp/120_trm_technical_reference_model/">TRM</a>(기술 <a href="/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model/">참조 모델</a>), <a href="/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/166_sp/">SP</a>(표준 프로파일)</strong> 3가지 기둥으로 이루어진다. [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)에는 ITA라는 큰 개념 안에 EA가 속해 있는 구조로 정의되었다.

#### ITA의 3대 핵심 구성 요소
1. <strong>전사적 아키텍처 (<a href="/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/">EA</a>, <a href="/knowledge-base/studynote/12_it_management/01_governance_strategy/010_ea_enterprise_architecture/">Enterprise Architecture</a>)</strong>
   - 비즈니스 업무와 이를 지원하는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), 애플리케이션, 기술 간의 상호 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 구조화한 청사진.
   - 현행 아키텍처([As-Is](/knowledge-base/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/)), 목표 아키텍처(To-Be), 이행 계획(Transition Plan)으로 구성된다.
2. <strong>기술 <a href="/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model/">참조 모델</a> (<a href="/knowledge-base/studynote/12_it_management/03_ea_isp/120_trm_technical_reference_model/">TRM</a>, Technical <a href="/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model/">Reference Model</a>)</strong>
   - 정보시스템을 구축하는 데 필요한 정보 기술 요소를 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)하고 계층화한 개념적 틀.
   - 예: '플랫폼', '네트워크', '보안', '[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 관리' 등으로 기술 영역을 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적으로 나눈 체계.
3. <strong>표준 프로파일 (<a href="/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/166_sp/">SP</a>, Standards Profile)</strong>
   - TRM에서 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)된 각 기술 영역에 대해, 실제로 기업/기관이 채택할 '구체적인 기술 표준 및 규격'들의 집합.
   - 예: [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 관리 영역의 표준은 'ANSI SQL' 준수, [네트워크 보안](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1117_network_security_zero_trust_policy/) 표준은 '[TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.3' 사용 지정. 특정 벤더(특정 회사 제품) 종속을 막기 위해 철저히 **개방형 표준(Open Standard)** 위주로 작성된다.

이 세 가지 요소는 상위의 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)가 하위의 물리적 표준으로 구체화되는 엄격한 계층 구조를 갖는다.

```text
[ITA 구성요소 간의 작동 및 연계 메커니즘]

[EA (전사 아키텍처)] "목표: 전국망 실시간 민원 서비스 구축"
         │ (기술적 구현 요구)
         ▼
[TRM (기술 참조 모델)] 기술 요소 분류 체계 적용
  ├─ 1. 애플리케이션 서비스
  ├─ 2. 데이터 관리
  └─ 3. 보안 통제 ◀── (어떤 보안 규격을 쓸 것인가?)
         │
         ▼
[SP (표준 프로파일)] 범정부 개방형 표준 규격 매핑
  ├─ 인증 표준: SAML 2.0 / OAuth 2.0 필수
  ├─ 암호화 표준: AES-256 / SHA-256 적용 필수
  └─ (특정 보안 솔루션 제품명을 명시하지 않고 규격을 강제함)
```
*해설: 이 계층 흐름도는 IT 기획 단계에서 ITA가 작동하는 원리를 명확히 보여준다. 현업의 요구사항([EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/))은 TRM이라는 큰 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)표를 거쳐, 최종적으로 SP라는 강력한 기술적 가드레일(표준안)을 통과해야만 개발로 이어질 수 있다. 이를 통해 개발자는 임의의 비표준 기술을 사용할 수 없게 된다.*

📢 **섹션 요약 비유**: ITA 체계를 집 짓기에 비유하면, EA는 전체 조감도와 방의 개수이고, TRM은 배관, 전기, 단열이라는 공사 공정의 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)표이며, SP는 '배관 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)는 반드시 KS [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 15mm 규격을 써라'라고 정해둔 구체적인 시공 규격집입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

시간이 흐르면서 업계에서는 'ITA'와 '[EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/)' 용어의 위상에 역전 현상이 일어났다. 이 차이를 명확히 이해하는 것은 정보화 역사를 파악하는 핵심 포인트이다.

| 구분 | [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 관점 (ITA 중심, 2000년대 중반) | 현대 관점 ([EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/) 중심, 현재) |
|:---|:---|:---|
| **상위 개념** | <strong>ITA</strong>가 상위 체계 (ITA = [EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/) + [TRM](/knowledge-base/studynote/12_it_management/03_ea_isp/120_trm_technical_reference_model/) + [SP](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/166_sp/)) | <strong><a href="/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/">EA</a></strong>가 상위 체계 (비즈니스부터 IT까지 포괄) |
| **포커스** | '정보 기술(IT)' 인프라의 표준화와 통합 | '비즈니스(Enterprise)' [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)과 IT의 정렬(Alignment) |
| **진화 방향** | 하드웨어/[소프트웨어 아키텍처](/knowledge-base/studynote/04_software_engineering/04_testing_quality/201_software_architecture_definition/) 통제 | 기업 비즈니스 프로세스 혁신, [디지털 전환](/knowledge-base/studynote/12_it_management/01_governance_strategy/055_digital_transformation/)(DT)의 기반 |
| **활용 무대** | 주로 공공기관 법제도, 감리, 컴플라이언스 | 전 산업군의 IT 경영전략, 클라우드 거버넌스 |

과거에는 컴퓨터 시스템 자체(IT)를 어떻게 잘 구성할 것인가가 목적이었기 때문에 '정보기술(IT) 아키텍처'라는 이름이 쓰였다. 하지만 IT가 비즈니스를 돕는 보조 수단을 넘어 비즈니스 자체로 진화함에 따라, 단순히 기술을 정렬하는 것을 넘어 전사적인 비즈니스(Enterprise)를 정렬해야 한다는 철학이 지배하며 <strong>EA로 명칭과 사상이 통합</strong>되었다. 현재 ITA라는 용어는 주로 학술적, 법적 문서(정보화 감리 등)에 역사적 흔적으로 남아있다.

```text
[ITA와 ISP(정보화전략계획)의 시너지 및 역할 분담]

┌──────────── ISP (기획 관점) ─────────────┐ 
│ 1. 비즈니스 환경 분석 및 목표 수립       │  ===> [WHY & WHEN] 
│ 2. 추진 과제 도출 및 예산/ROI 편성       │       "무엇을 언제 할 것인가"
└──────────────────┬───────────────────────┘
                   │ 연계 및 제약 작용
                   ▼
┌──────────── ITA/EA (구조 관점) ────────────┐
│ 1. 목표 아키텍처(To-Be)의 청사진 제공    │  ===> [HOW & WHERE]
│ 2. 기술 참조 모델(TRM) 및 표준 검증      │       "어떤 구조와 표준으로 할 것인가"
└──────────────────────────────────────────┘
```
*해설: 이 대조도는 IT 기획의 두 축인 ISP와 ITA의 상호보완적 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 보여준다. ISP가 "내년에 100억을 들여 CRM을 구축하자"라는 사업적 결정을 내리면, ITA는 "그 CRM은 기존 시스템과 충돌하지 않도록 [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 구조와 표준 API를 적용해 설계해야 한다"는 구조적 통제력을 행사한다. 둘 중 하나라도 없으면 투자는 실패하거나 난개발로 이어진다.*

📢 **섹션 요약 비유**: [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) ITA가 컴퓨터 부품이 잘 조립되도록 규격을 맞추는 '하드웨어 매뉴얼'이었다면, 현대의 EA는 회사가 돈을 버는 방식과 IT를 완벽하게 일치시키는 '기업 경영 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)서'로 거대하게 진화한 것입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)

실무(특히 공공 정보화 사업이나 감리 현장)에서 ITA 체계의 유무는 프로젝트의 질서를 결정짓는 핵심 기준이다.

1. <strong><a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/287_interoperability_tactics/">상호운용성</a>(<a href="/knowledge-base/studynote/06_ict_convergence/01_blockchain/084_blockchain_interoperability_polkadot_cosmos/">Interoperability</a>) 시험/감리</strong>: 감리원은 프로젝트 완료 시 단순히 기능이 동작하는지를 보지 않는다. ITA 법령에 따라, 구축된 시스템이 사전에 정의된 '표준 프로파일([SP](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/166_sp/))'을 100% 준수했는지 소스코드와 아키텍처를 검열한다. 만약 승인되지 않은 비표준 기술을 사용했다면 기능이 정상이어도 감리 부적합 판정을 내린다.
2. <strong><a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/">기술 부채</a>(<a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/">Technical Debt</a>) 통제</strong>: 최신 유행 기술(Hype)이라 하더라도 전사 TRM에 등재되지 않았다면 실무 도입을 보류해야 한다. 개발팀은 불만을 가질 수 있으나, 표준을 이탈한 기술 [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/)은 3~5년 뒤 유지보수 인력을 구하지 못해 거대한 [기술 부채](/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/)로 전락한다. 아키텍트는 혁신과 표준 통제 사이에서 트레이드오프 밸런스를 잡아야 한다.
3. <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/">오픈소스</a>와 ITA의 결합</strong>: 최신 ITA 실무 지침은 특정 상용 벤더의 [Lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/)-in을 극도로 경계한다. 따라서 TRM과 SP를 갱신할 때 의무적으로 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)된 [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/)(예: [Oracle](/knowledge-base/studynote/05_database/03_relational_model/188_pl_sql_t_sql_procedural/) 대신 PostgreSQL, WebLogic 대신 Tomcat)을 최우선 표준으로 권고하여 [총 소유 비용](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/006_tco_total_cost_of_ownership/)([TCO](/knowledge-base/studynote/12_it_management/01_governance_strategy/016_tco/))을 획기적으로 낮추는 방향으로 의사결정을 내린다.

```text
[실무 의사결정 트리: 개발팀의 신기술 도입 요구 시 ITA 통제 플로우]

[개발팀] "이번 프로젝트에 최신 NoSQL DB(예: MongoDB)를 쓰고 싶습니다."
         │
         ▼
[ITA / 아키텍트 위원회 심의]
[TRM/SP 조회] 전사 표준 프로파일(SP)에 해당 기술이 등재되어 있는가?
   ├─ (Yes) ──▶ 즉시 사용 승인 및 아키텍처 도면(EA) 반영
   │
   └─ (No) ───▶ [기술 타당성 평가] 기존 RDBMS 표준으로 구현 불가능한 요구사항인가?
                  ├─ (No) ──▶ [기각] 유지보수 비용 증가 우려. 기존 표준 RDBMS 사용 지시.
                  │
                  └─ (Yes) ─▶ 파일럿(PoC) 진행 후, 전사 TRM/SP에 신규 규격으로 
                               '공식 등재(업데이트)' 처리 후 사용 조건부 승인
```
*해설: 이 프로세스는 ITA가 낡은 기술을 고집하는 장애물이 아니라, 체계적인 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)을 통해 전사 기술 생태계를 건강하게 진화시키는 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인임을 증명한다. 예외적 도입을 허용하더라도, 반드시 '표준 업데이트'라는 문서를 남겨 시스템 사각지대([Shadow IT](/knowledge-base/studynote/12_it_management/01_governance_strategy/049_shadow_it/))가 발생하지 않도록 차단하는 것이 핵심이다.*

📢 **섹션 요약 비유**: ITA 통제는 엄격한 면역 체계와 같습니다. 외부의 새로운 기술([바이러스](/knowledge-base/studynote/02_operating_system/10_security/589_virus/))이 들어올 때, 덮어놓고 배척하는 것이 아니라 꼼꼼히 백신 테스트를 거친 후 안전하다고 판단되면 전사 면역 명부(표준 프로파일)에 정식 등록하여 시스템 전체를 업그레이드하는 과정입니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

ITA 개념의 등장과 법제화는 대한민국 IT 역사에서 [사일로](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/)식 주먹구구 개발을 마감하고 체계적 아키텍처 엔지니어링 시대를 연 분수령이다.

| 지표 | 정량적 / 정성적 기대효과 | 비고 |
|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/287_interoperability_tactics/">상호운용성</a></strong> | 부처 간, 부서 간 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 교환 비용 50% 이상 감소 | 표준 프로파일([SP](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/166_sp/)) 준수의 결과 |
| **운영 효율성** | 표준화된 인프라([TRM](/knowledge-base/studynote/12_it_management/03_ea_isp/120_trm_technical_reference_model/))를 통한 IT 유지보수 인력 및 라이선스 비용 절감 | [벤더 종속](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/051_vendor_lock_in_cloud_computing/)([Lock-in](/knowledge-base/studynote/12_it_management/05_security_compliance/362_lock_in_portability/)) [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) 헷지 |
| **투명성** | 중복 투자 방지를 통한 연간 정보화 예산 효율화 극대화 | ITA 기반 사전 투자 타당성 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) |

미래의 ITA/EA는 정적인 문서 형태를 넘어, [인프라 코드](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/)화([IaC](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/), Infrastructure 가 [Code](/knowledge-base/studynote/02_operating_system/02_process_thread/082_process_memory_structure/))와 [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/) 환경에 맞춰 동적으로 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 강제하는 '[Policy](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) [as](/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) [Code](/knowledge-base/studynote/02_operating_system/02_process_thread/082_process_memory_structure/)' 형태로 진화하고 있다. 즉, 개발자가 배포 스크립트를 실행할 때 [TRM](/knowledge-base/studynote/12_it_management/03_ea_isp/120_trm_technical_reference_model/)/[SP](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/166_sp/) 규격을 어기면 클라우드 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인에서 배포가 자동 차단되는 등, 아키텍처는 문서가 아닌 '자동화된 실행 엔진'으로 변화하여 엔터프라이즈의 뼈대를 굳건히 유지할 것이다.

📢 **섹션 요약 비유**: ITA는 나무를 심기 전 땅의 토질과 물길을 분석하는 '조경의 기초'와 같습니다. 이 기초가 잘 다져진 땅(조직) 위에서만 클라우드, [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/), 빅데이터라는 화려한 디지털 혁신의 꽃과 열매가 시들지 않고 만개할 수 있습니다.

---

### 📌 관련 개념 맵 ([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
* <strong><a href="/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/">EA</a> (<a href="/knowledge-base/studynote/12_it_management/01_governance_strategy/010_ea_enterprise_architecture/">Enterprise Architecture</a>)</strong> | ITA의 진화된 형태로, IT뿐 아니라 비즈니스 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)과 프로세스까지 기업 전체를 아우르는 최상위 아키텍처 청사진
* <strong><a href="/knowledge-base/studynote/12_it_management/03_ea_isp/120_trm_technical_reference_model/">TRM</a> (Technical <a href="/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model/">Reference Model</a>)</strong> | ITA의 핵심 구성요소로, 기업이 사용할 정보기술 요소들을 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적으로 쪼개어 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)한 프레임워크
* <strong><a href="/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/166_sp/">SP</a> (Standards Profile)</strong> | TRM의 각 기술 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)마다 실제로 사용을 허가할 구체적이고 개방적인 기술 규격들의 집합
* <strong><a href="/knowledge-base/studynote/12_it_management/03_ea_isp/101_isp_information_strategy_planning_4_steps/">ISP</a> (Information <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">Strategy</a> Planning)</strong> | 중장기 정보화 [마스](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)터플랜으로, ISP가 '무엇을 구축할지' 결정하면 ITA는 그것을 '어떤 구조와 표준으로 만들지' 통제함
* <strong><a href="/knowledge-base/studynote/06_ict_convergence/01_blockchain/084_blockchain_interoperability_polkadot_cosmos/">Interoperability</a> (<a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/287_interoperability_tactics/">상호운용성</a>)</strong> | ITA 도입의 가장 큰 목적으로, 서로 다른 시스템이나 부처 간에 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 기능을 장애 없이 주고받을 수 있는 능력


### 📈 관련 키워드 및 발전 흐름도

```text
[ISP (Information Strategy Planning) — 중장기 정보화 마스터플랜 수립]
    │
    ▼
[ITA (Information Technology Architecture) — TRM+SP 기반 IT 구조·표준 통제 체계]
    │
    ▼
[EA (Enterprise Architecture) — 비즈니스·데이터·앱·기술 4계층 통합 아키텍처]
    │
    ▼
[TOGAF / FEA — 글로벌 EA 프레임워크, ADM 방법론 국제 표준화]
    │
    ▼
[디지털 트윈 아키텍처 — EA 기반 실물-가상 동기화, 스마트정부·스마트시티 적용]
```

이 흐름은 정보화 [마스](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)터플랜([ISP](/knowledge-base/studynote/12_it_management/03_ea_isp/101_isp_information_strategy_planning_4_steps/))에서 출발해 IT 구조를 표준화하는 ITA로 구체화되고, 기업 전체를 아우르는 [EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/)([TOGAF](/knowledge-base/studynote/12_it_management/03_ea_isp/113_togaf/)/FEA)로 확장된 뒤, 현실과 디지털 세계를 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)하는 [디지털 트윈](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/126_digital_twin_concept/) 아키텍처로 진화하는 공공·기업 IT 거버넌스의 발전 계보를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. 옛날에는 회사나 관공서 사람들이 컴퓨터를 살 때 자기 마음대로 사서, 서로 케이블이나 프로그램이 맞지 않아 큰 문제가 생겼어요.
2. 그래서 "아무 컴퓨터나 사지 말고, 무조건 나라에서 정해준 규칙과 튼튼한 설계도(ITA)에 맞춰서만 만들어라!" 하고 아예 법으로 딱 정해버렸답니다.
3. 이 튼튼한 규칙(ITA) 덕분에 지금은 모든 컴퓨터가 서로 사이좋게 정보를 나누고, 불필요하게 돈을 두 번 쓰는 일도 사라지게 되었어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 15 / 482

← **이전**: [14. 범정부 EA 프레임워크 (GEA) - 공공기관 정보화 아키텍처 의무 지침](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/014_gea_framework/)
**다음**: [16. BPR (Business Process Reengineering) - 마이클 해머, 획기적 성과 향상을 위해 비즈니스 프로세스를](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/016_bpr/) →

---
