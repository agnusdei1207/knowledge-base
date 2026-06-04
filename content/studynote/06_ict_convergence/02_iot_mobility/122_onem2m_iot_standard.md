+++
title = "122. oneM2M IoT 표준 - 글로벌 IoT 서비스 플랫폼 표준 아키텍처"
date = 2026-04-19

[taxonomies]
tags = ["studynote-ict-convergence"]

[extra]
tags = ["studynote-ict-convergence"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: oneM2M은 <strong><a href="/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/">IoT</a> <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 플랫폼의 글로벌 표준 아키텍처</strong>로, 디바이스 관리·[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장·구독/알림·보안 등 <strong>공통 <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 기능(<a href="/knowledge-base/studynote/12_it_management/01_governance_strategy/017_csf/">CSF</a>)</strong>을 표준화하여 [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 애플리케이션 개발의 중복을 제거한다.
> 2. **가치**: oneM2M 없이는 스마트 홈·[스마트 시티](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/171_smart_city_platform_architecture/)·헬스케어 등 <strong>각 도메인마다 플랫폼을 별도 개발</strong>해야 하지만, oneM2M의 공통 플랫폼 위에서 애플리케이션만 개발하면 된다.
> 3. **판단 포인트**: IN-CSE(인프라)·MN-CSE(미들 노드)·ASN-CSE(디바이스 노드)의 3계층 아키텍처와 AE(Application Entity)·CSE(Common [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) Entity) 관계를 이해해야 한다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    oneM2M 아키텍처                                    |
+-------------------------------------------------------+
|  [AE — Application Entity]                            |
|   스마트홈 앱, 환경 모니터링 앱                       |
|      ↕ Mca 인터페이스                                 |
|  [CSE — Common Service Entity]                        |
|   등록·디스커버리·데이터관리·구독·보안                |
|      ↕ Mcc 인터페이스                                 |
|  [CSE (다른 노드)]                                    |
|      ↕ Mcn 인터페이스                                 |
|  [NSE — Network Service Entity]                       |
|   전송 네트워크 (LTE, Wi-Fi, LoRa)                   |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: oneM2M은 IoT의 <strong>안드로이드</strong>다. 스마트폰(디바이스)마다 OS(플랫폼)를 따로 만들 필요 없이, 공통 OS 위에 앱(AE)만 개발하면 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [CSF](/knowledge-base/studynote/12_it_management/01_governance_strategy/017_csf/) (Common [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) Functions)

| 기능 | 설명 |
|:---|:---|
| **등록 (Registration)** | 디바이스·앱 등록 |
| **디스커버리** | 리소스 검색 |
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 관리</strong> | 센서 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장·검색 |
| **구독/알림** | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 변경 시 Push |
| **보안** | [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)·[인가](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/)·암호화 |

- **📢 섹션 요약 비유**: CSF는 스마트폰의 기본 앱(전화·메시지·카메라)처럼, [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 플랫폼의 필수 공통 기능이다.

---

## Ⅲ. 비교 및 연결

| 비교 | 독자 플랫폼 | oneM2M |
|:---|:---|:---|
| **상호운용** | 불가 | **표준 보장** |
| **개발 비용** | 높음 | <strong>공통 <a href="/knowledge-base/studynote/12_it_management/01_governance_strategy/017_csf/">CSF</a> 재사용</strong> |
| **확장** | 어려움 | **표준 인터페이스** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 적용 분야
- [스마트 시티](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/171_smart_city_platform_architecture/) (환경 모니터링, 교통).
- 스마트 헬스케어 (원격 건강 모니터링).
- 국내: SKT ThingPlug가 oneM2M 기반.

---

## Ⅴ. 기대효과 및 결론

oneM2M은 <strong><a href="/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/">IoT</a> 플랫폼의 글로벌 표준</strong>이며, [Matter](/knowledge-base/studynote/03_network/12_iot_wpan_edge/612_matter_csa_smart_home_standard/)(스마트 홈)·[LwM2M](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/121_lwm2m_lightweight_m2m/)(디바이스 관리)과 함께 [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 표준 생태계를 구성한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **CSE** | oneM2M의 공통 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 엔진 |
| **AE** | oneM2M 위의 응용 엔터티 |
| <strong><a href="/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/121_lwm2m_lightweight_m2m/">LwM2M</a></strong> | 디바이스 관리 (oneM2M 보완) |
| <strong><a href="/knowledge-base/studynote/03_network/12_iot_wpan_edge/612_matter_csa_smart_home_standard/">Matter</a></strong> | 스마트 홈 앱 표준 |
| <strong><a href="/knowledge-base/studynote/03_network/12_iot_wpan_edge/622_mqtt_publish_subscribe_qos/">MQTT</a>/<a href="/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/120_coap_constrained_application_protocol/">CoAP</a></strong> | oneM2M의 전송 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 바인딩 |

### 📈 관련 키워드 및 발전 흐름도

```text
[독자 IoT 플랫폼 (사일로, 2010s)]
    |
    v
[oneM2M Release 1 (2015) — 글로벌 IoT 플랫폼 표준]
    |
    v
[Release 2~4 (2017~2022) — 기능 확장]
    |
    v
[oneM2M + Matter + LwM2M (IoT 표준 생태계)]
    |
    v
[현재: AI + oneM2M — 지능형 IoT 플랫폼]
```

### 👶 어린이를 위한 3줄 비유 설명
1. oneM2M은 IoT의 <strong>안드로이드(공통 OS)</strong>예요. 앱만 만들면 돼요.
2. 디바이스 등록·[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장·알림 같은 **기본 기능을 미리 만들어 놨어요**.
3. 덕분에 스마트홈·스마트시티 앱을 **빠르고 쉽게** 개발할 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 122 / 552

<- **이전**: [121. LwM2M (Lightweight M2M) - OMA 표준 IoT 디바이스 관리 프로토콜](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/121_lwm2m_lightweight_m2m/)
**다음**: [123. OCF (Open Connectivity Foundation) - IoT 상호운용성 표준](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/123_ocf_open_connectivity_foundation/) ->

---
