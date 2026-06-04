---
title: "741. CASB (Cloud Access Security Broker 클라우드 망 접속 보안 모니터/가시성 유지 시스템)"
date: "2026-05-08"
tags:
  - "studynote-network"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: CASB는 [네트워크 보안](/studynote/03_network/20_performance_evaluation_advanced/1117_network_security_zero_trust_policy/) 위협과 대응에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: CASB를 이해하면 탐지 가능성과 복구성 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 가트너(Gartner)가 명명한 용어로, <strong>기업의 내부 사용자(직원)와 외부 클라우드 <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 공급자(AWS, MS 365, 구글 드라이브 등) 사이에 위치하여, 보안 <a href="/studynote/10_ai/02_dl_architecture_new/164_policy/">정책</a>을 강제하고 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>의 가시성(Visibility)을 확보하는 보안 중개자(Broker) 솔루션</strong>입니다. (앞선 740번 [SASE](/studynote/03_network/14_network_security_threats/740_sase_secure_access_service_edge_sdwan_cloud/) 아키텍처의 핵심 구성 요소입니다.)
- **배경 (Shadow IT의 공포)**: 회사 IT 부서의 허락을 받지 않고 직원들이 몰래 카카오톡, 드롭박스, 에버노트 등을 업무에 쓰는 <strong>'섀도우 IT(<a href="/studynote/12_it_management/01_governance_strategy/049_shadow_it/">Shadow IT</a>)'</strong> 현상이 폭발하면서, 회사 기밀 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 통제 불능 상태로 새어 나가는 것을 막기 위해 탄생했습니다.

```text
[SASE]
    |
    v
[CASB]
    |
    +---> [SWG]
```

- **📢 섹션 요약 비유**: CASB는 왜 필요한지 보여주는 교통 규칙 표지판과 같다. 문제가 생긴 배경을 알면 이후 [선택도](/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/) 쉬워진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 가시성 (Visibility) - "숨은 앱 찾아내기"
- 회사 내에서 직원들이 회사 공식 메일(아웃룩) 대신 몰래 개인용 네이버 메일이나 텔레그램을 얼마나 쓰고 있는지(섀도우 IT 탐지) 엑스레이처럼 샅샅이 파악하여 대시보드에 띄워줍니다.

### 2. 규정 준수 ([Compliance](/studynote/07_enterprise_systems/01_strategy_governance/058_it_compliance_sox_basel_gdpr_isms/)) - "법적 제재 방지"
- 직원이 구글 드라이브에 올린 문서가 [개인정보보호법](/studynote/09_security/16_data_privacy/783_pipa_korea/)([GDPR](/studynote/09_security/16_data_privacy/791_gdpr_eu/), [HIPAA](/studynote/09_security/17_framework_compliance/1058_hipaa/))을 위반하는 '고객 주민등록번호 1,000명분' 리스트가 아닌지 스캔하여, 위반 사항이 있으면 클라우드 업로드를 즉각 차단합니다.

### 3. [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 보안 ([Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) / [DLP](/studynote/01_computer_architecture/10_parallel_processing_architecture/386_dlp/))
- 가장 중요한 기능입니다. 회사 밖(클라우드)으로 나가는 문서에 대해 강력한 <strong><a href="/studynote/01_computer_architecture/10_parallel_processing_architecture/386_dlp/">DLP</a>(<a href="/studynote/12_it_management/05_security_compliance/186_dlp_data_loss_prevention/">데이터 유출 방지</a>)</strong> 기능을 적용합니다. 사내 기밀문서를 감지하면 아예 업로드를 막거나, 업로드되더라도 문서를 강제로 <strong>암호화(Encryption)</strong>해 버려 해커가 클라우드를 털어도 열어보지 못하게 만듭니다.

### 4. 위협 방지 (Threat [Protection](/studynote/02_operating_system/10_security/571_protection_vs_security/))
- 클라우드에서 회사로 다운로드되는 파일에 랜섬웨어나 악성코드가 묻어있는지(샌드박스 연동) 스캔하고, 누군가 파리에서 로그인한 지 1시간 만에 뉴욕에서 클라우드에 접속하려 하면(불가능한 여행) 이상 행동으로 간주해 차단합니다.

```text
[SASE]
    |
    v
[CASB]
    |
    +---> [SWG]
```

- **📢 섹션 요약 비유**: CASB의 내부 원리는 기계의 톱니바퀴처럼 맞물려 돌아간다. 한 부분이 어긋나면 전체 효과가 떨어진다.

---

## Ⅲ. 비교 및 연결

CASB가 돋보기를 어디에 대고 감시하느냐에 따라 3가지로 나뉩니다.

1. <strong><a href="/studynote/02_operating_system/01_overview_architecture/014_api_posix/">API</a> 기반 방식 (가장 많이 쓰임)</strong>:
   - 사용자와 클라우드 사이에 물리적으로 끼어들지 않습니다. 대신 구글 드라이브, MS 365 등 클라우드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 자체의 <strong>관리자 API를 연동</strong>하여 클라우드 안에서 벌어지는 일들을 모니터링합니다. 속도 저하가 없고 과거 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)까지 스캔 가능하지만, 클라우드 업체가 API를 제공해야만 쓸 수 있습니다.
2. <strong><a href="/studynote/10_ai/03_llm_nlp/235_forward_backward_chaining/">Forward</a> <a href="/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/">Proxy</a> (포워드 <a href="/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/">프록시</a>)</strong>:
   - 사내 직원의 PC에서 나가는 트래픽을 모조리 가로채어 중간에서 검사한 뒤 클라우드로 넘깁니다. 실시간 업로드 차단([DLP](/studynote/01_computer_architecture/10_parallel_processing_architecture/386_dlp/))에 가장 강력합니다.
3. <strong>Reverse <a href="/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/">Proxy</a> (리버스 <a href="/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/">프록시</a>)</strong>:
   - 직원이 개인 폰(에이전트 미설치)으로 집에서 클라우드에 접속할 때, 클라우드가 직접 폰을 CASB 쪽으로 튕겨내어(리다이렉트) 검사받게 하는 방식입니다. 개인 기기 통제에 유리합니다.

CASB를 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. SASE가 기반 조건을 만든다면, CASB는 그 위에서 핵심 메커니즘을 구현하고, SWG는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 탐지 가능성과 복구성에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | SASE의 기반 정리 | CASB의 핵심 동작 | SWG의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 탐지 가능성 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: CASB는 대기업 정문에 앉아있는 '사설 탐정 겸 경호원'입니다. 과거엔 직원이 퇴근할 때 회사의 중요한 서류([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))를 자기 개인 가방(구글 드라이브)에 쑤셔 넣고 퇴근해도 막을 방법이 없었습니다(가시성 제로). CASB 경호원은 직원이 정문을 나설 때마다 엑스레이 스캐너로 가방 안을 샅샅이 뒤져(Visibility), 회사 기밀문서가 보이면 압수([DLP](/studynote/01_computer_architecture/10_parallel_processing_architecture/386_dlp/))하거나, 비밀번호 자물쇠를 걸어서(암호화) 밖으로 내보내는 완벽한 클라우드 시대의 출입 통제관입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 CASB를 단독 개념으로 외우기보다 어떤 병목을 줄이기 위한 선택인지 먼저 따져야 한다. 특히 [SASE](/studynote/03_network/14_network_security_threats/740_sase_secure_access_service_edge_sdwan_cloud/) 수준의 기본 대책으로 충분한지, 아니면 CASB가 제공하는 메커니즘이 실제로 필요한지 구분해야 한다. 이후 확장 단계에서는 SWG와 같은 후속 기술, 자동화 체계, 표준 호환성까지 함께 검토해야 한다.

### 실무 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 현재 문제의 핵심이 탐지 가능성 부족인지, 복구성 악화인지 먼저 분리한다.
2. CASB가 추가하는 복잡도와 운영 이득이 균형을 이루는지 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다.
3. 도입 후에는 인접 기술인 SWG와의 연계 방식을 함께 검증한다.

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- CASB의 장점만 보고 트래픽 패턴이나 운영 비용을 무시한 채 과도 도입하는 설계
- SASE와의 경계를 정리하지 않아 중복 투자나 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 충돌을 만드는 설계

- **📢 섹션 요약 비유**: CASB를 실제로 쓰는 판단은 도구 상자를 고르는 일과 비슷하다. 좋아 보이는 도구보다 지금 문제에 맞는 도구가 중요하다.

---

## Ⅴ. 기대효과 및 결론

CASB는 [네트워크 보안](/studynote/03_network/20_performance_evaluation_advanced/1117_network_security_zero_trust_policy/) 위협과 대응을 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 탐지 가능성 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [SWG](/studynote/03_network/14_network_security_threats/742_swg_secure_web_gateway/), 예측형 위협 대응, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 예측형 위협 대응 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: CASB는 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [SASE](/studynote/03_network/14_network_security_threats/740_sase_secure_access_service_edge_sdwan_cloud/) | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| 공격 표면 (Attack Surface) | 위협이 침투할 수 있는 노출 지점을 뜻한다. |
| [이상 탐지](/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/) ([Anomaly Detection](/studynote/16_bigdata/05_analysis/111_anomaly_detection/)) | 정상 패턴과 다른 징후를 찾아낸다. |
| [SWG](/studynote/03_network/14_network_security_threats/742_swg_secure_web_gateway/) | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: SASE]
    |
    v
[현재 개념: CASB]
    |
    +---> [확장 A: SWG]
    +---> [확장 B: 예측형 위협 대응]
```

CASB는 SASE에서 출발해 현재 메커니즘을 정교화하고, 이후 SWG와 예측형 위협 대응 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 나쁜 친구가 놀이터 규칙을 깨뜨리면 바로 알아차리고 막아야 해요.
2. 이 개념은 어떤 장난이 위험한지 미리 알고, 문제가 생기면 어떻게 다시 정리할지도 알려줘요.
3. 그래서 놀이터를 더 안전하게 지킬 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 862 / 1120

<- **이전**: [740. SASE (Secure Access Service Edge 브랜치 사무소 단말 네트워크 엣지 클라우드 보안 통합체계/ SD-WAN](/studynote/03_network/14_network_security_threats/740_sase_secure_access_service_edge_sdwan_cloud/)
**다음**: [742. SWG (Secure Web Gateway 시큐어 웹 게이트웨이 / 프록시 보안 패키지 모델 구조적 설계)](/studynote/03_network/14_network_security_threats/742_swg_secure_web_gateway/) ->

---
