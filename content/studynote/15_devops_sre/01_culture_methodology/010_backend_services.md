---
title: "10. 백엔드 서비스 (Backing Services) - DB, 큐, 캐시 등을 네트워크로 연결된 자원(Attached Resource)으로 취급"
date: "2026-04-05"
tags:
  - "devops_sre"
---


# 백엔드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 백엔드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)(Backing Services) 원칙은 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/), [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 큐, [SMTP](/studynote/03_network/09_application_layer_web_email/488_smtp_simple_mail_transfer_protocol/) 서버, 캐시 시스템([Redis](/studynote/05_database/04_transactions_concurrency/542_redis/)) 등 애플리케이션이 네트워크를 통해 리용하는すべ고의외부자원을"연결된 자원(Attached Resource)"으로 취급하고, 타문へ의 연결 정보를 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 통해 관리해야 한다는 12팩터 앱의 제4원칙이다.
> 2. **가치**: 백엔드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 [추상화](/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/)하여 관리하면, 례여 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)를 변경할 때 코드를 수정하지 않고 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)만 바꾸면 되므로 확장성과 [유지보수성](/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/)이 크게 향상된다.
> 3. **융합**: [마이크로서비스 아키텍처](/studynote/04_software_engineering/04_testing_quality/213_msa_microservices_architecture/)에서 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간통신과서비스발현( [Service Discovery](/studynote/12_it_management/05_security_compliance/946_service_discovery/))가 이 원칙의 확장이며, [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 환경에서 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)간 망락 연결은 이 원칙을 기반으로 설계된다.

---

### Ⅰ. 개요 및 필요성 ([Context](/studynote/02_operating_system/01_overview_architecture/033_context/) & Necessity)

백엔드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)란 애플리케이션이 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 저장하거나 외부 시스템과통신하기 위해 네트워크를 통해 리용하는すべ고의외부[서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 의미한다. 여기에는 전통적인 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)(MySQL, PostgreSQL)뿐만 아니라, [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 큐(RabbitMQ, [Apache Kafka](/studynote/14_data_engineering/05_exam_keywords/214_kafka_pubsub_topic_partition_offset_broker/)), [SMTP](/studynote/03_network/09_application_layer_web_email/488_smtp_simple_mail_transfer_protocol/) 서버, 캐시 시스템([Redis](/studynote/05_database/04_transactions_concurrency/542_redis/), Memcached), 타사 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/)(지부Gateway,단신서비스) 등광범위な [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 포함된다.

전통적인 접근법에서는 이러한 백엔드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 코드에 하드코딩된고정 URL 이나 연결 정보로 접근했다. 예를 들어:
```python
# ❌ 하드코딩된 백엔드 서비스 접근 (나쁜 예)
db_connection = mysql.connect("prod-db-server-01:3306", "admin", "password123")
redis_client = redis.connect("localhost:6379")
```

이렇게 하면 여러 문제점이 발생한다. 첫째, 개발 환경에서는 로컬 Redis를 사용하고 프로덕션에서는 관리 [Redis](/studynote/05_database/04_transactions_concurrency/542_redis/) 클러스터를 사용해야 할 때 코드를 수정해야 한다. 둘째, 백엔드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 제공업체를 변경（례여 MySQL -> PostgreSQL）하려면 코드의 모든 관련 부분을 수정해야 한다. 셋째, 백엔드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 연결 정보가 코드에 노출되어 보안 문제가 발생할 수 있다.

12팩터 앱의 백엔드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 원칙은 이러한 문제를 해결하기 위해"모든 백엔드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 네트워크로 연결된 자원으로 취급하라"고 명시한다. 즉, [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)든 캐시든 [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 큐든 모두"연결된 자원"이며, 타문へ의접속 정보는 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)([환경 변수](/studynote/02_operating_system/02_process_thread/156_environment_variables/))을 통해 관리되어야 한다. 이렇게 하면 코드는"어떤" 백엔드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에 연결되는지 알 필요 없이, 단순히 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)에 정의된 연결 대상에 연결하기만 하면 된다.

아래 다이어그램은 백엔드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 원칙의 핵심 개념을 [시각화](/studynote/16_bigdata/01_intro/003_bigdata_7v/)한 것이다.

```text
[백엔드 서비스 원칙: 모든 외부 자원을"연결된 자원"으로 취급]

❌ 전통적 접근: 서비스가您的位置를 코드에 하드코딩
+--------------------------------------------------------------+
|  코드                                            |
|  +----------------------------------------------+         |
|  | MySQL = "mysql://prod-db:3306"  <- 하드코딩    |         |
|  | Redis = "redis://prod-cache:6379" <- 하드코딩  |         |
|  +----------------------------------------------+         |
|           문제: 환경마다 코드 수정 필요, 유연성 없음         |
+--------------------------------------------------------------+

✓ 12팩터 접근: 모든 자원을"연결된 자원"으로 취급
+--------------------------------------------------------------+
|                                                             |
|     +-------------+         +-------------+                |
|     |  Database   |         |   Redis     |                |
|     |  (MySQL)    |         |  (Cache)    |                |
|     +------+------+         +------+------+                |
|            |    네트워크로 연결      |                        |
|            |<------------------------->|                       |
|            |                        |                        |
|     +------+------+         +------+------+                |
|     | 연결된 자원  |         | 연결된 자원  |  <- 추상화!    |
|     | (Attached   |         | (Attached   |                |
|     |  Resource)  |         |  Resource)  |                |
|     +-------------+         +-------------+                |
|            |                        |                        |
|            |    설정(환경 변수)에서 관리    |                        |
|            v                        v                        |
|     +----------------------------------------------+        |
|     |  DB_URL = mysql://${DB_HOST}:${DB_PORT}      |        |
|     |  REDIS_URL = redis://${REDIS_HOST}:${REDIS}  |        |
|     +----------------------------------------------+        |
|                                                             |
|     장점: 동일한 코드, 환경별 다른 자원 연결 가능            |
+--------------------------------------------------------------+
```

이 그림의 핵심은 백엔드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가"앱의 일부"가 아니라"외부에서 연결하는 자원"이라는 개념적 구분이다. 물리적으로 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) 서버가 어디에 있든(로컬, 클라우드, [온프레미스](/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/)), 그것이 어떤 제공업체이든( AWS RDS, Azure SQL, [온프레미스](/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) MySQL), 애플리케이션에게는 동일하게"연결된 자원"이며, 연결 문자열(Connection String)만으로 접근할 수 있다.

> 📢 **섹션 요약 비유**: 백엔드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를"호텔의 외주 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)"에 비유할 수 있다. 호텔(애플리케이션)이 세탁소를 직접운영하지 않고(자체 DB운영) 외부 세탁소(백엔드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))를 리용한다. 만약 세탁소 제공업체가 바뀌어도(로컬 -> 클라우드), 호텔은 전화번호(연결 정보)만 바꾸면 되고, 세탁 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 자체(코드)의 변화는 필요하지 않다. 이것이 백엔드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 원칙의 핵심이다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

백엔드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 원칙을 구현할 때 고려해야 할 주요 패턴과 그 내부 동작 메커니즘을 분석한다.

| 백엔드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 유형 | 예시 | [추상화](/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) 방법 | 연결 정보 관리 |
|:---|:---|:---|:---|
| <strong><a href="/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/">관계</a>형 <a href="/studynote/05_database/01_db_architecture_relational/002_database_definition/">데이터베이스</a></strong> | PostgreSQL, MySQL, MariaDB | 연결 문자열 (Connection URL) | [환경 변수](/studynote/02_operating_system/02_process_thread/156_environment_variables/) 또는 [시크릿](/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/) |
| <strong><a href="/studynote/14_data_engineering/01_infrastructure/035_nosql/">NoSQL</a> <a href="/studynote/05_database/01_db_architecture_relational/002_database_definition/">데이터베이스</a></strong> | [MongoDB](/studynote/05_database/04_transactions_concurrency/540_mongodb/), [Cassandra](/studynote/05_database/04_transactions_concurrency/541_cassandra/) | 연결 문자열 + 드라이버 | [환경 변수](/studynote/02_operating_system/02_process_thread/156_environment_variables/) |
| **캐시 시스템** | [Redis](/studynote/05_database/04_transactions_concurrency/542_redis/), Memcached | 연결 문자열 | [환경 변수](/studynote/02_operating_system/02_process_thread/156_environment_variables/) |
| <strong><a href="/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/">메시</a>지 큐</strong> | RabbitMQ, [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) | 연결 문자열 + [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) | [환경 변수](/studynote/02_operating_system/02_process_thread/156_environment_variables/) |
| <strong><a href="/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/">오브젝트 스토리지</a></strong> | S3, GCS, Azure Blob | [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 엔드포인트 + 자격 증명 | [시크릿 매니저](/studynote/15_devops_sre/02_cicd_gitops/095_secret_manager_hashicorp_vault_aws/) |
| <strong>타사 <a href="/studynote/02_operating_system/01_overview_architecture/014_api_posix/">API</a></strong> | Stripe, Twilio | [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) URL + [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 키 | [시크릿 매니저](/studynote/15_devops_sre/02_cicd_gitops/095_secret_manager_hashicorp_vault_aws/) |
| <strong><a href="/studynote/03_network/09_application_layer_web_email/488_smtp_simple_mail_transfer_protocol/">SMTP</a> 서버</strong> | SendGrid, SES | [SMTP](/studynote/03_network/09_application_layer_web_email/488_smtp_simple_mail_transfer_protocol/) 호스트/[포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)/자격 증명 | [환경 변수](/studynote/02_operating_system/02_process_thread/156_environment_variables/) 또는 [시크릿](/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/) |

아래는 백엔드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 연결의 내부 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 흐름을 보여주는 [ASCII](/studynote/01_computer_architecture/02_data_representation_arithmetic/103_ascii/) 다이어그램이다.

```text
[백엔드 서비스 연결: 설정 -> 추상화 -> 런타임 연결]

1. 설정 (Configuration)
+--------------------------------------------------------------+
|  환경 변수                                                   |
|  +------------------------------------------------------+  |
|  | DATABASE_URL=postgres://user:pass@db.example.com:5432|  |
|  | REDIS_URL=redis://redis.example.com:6379             |  |
|  | SMTP_HOST=smtp.sendgrid.net                          |  |
|  | SMTP_API_KEY=SG.xxxxxx                                |  |
|  +------------------------------------------------------+  |
+--------------------------------------------------------------+

2. 추상화 레이어 (Application Code)
+--------------------------------------------------------------+
|  코드 (백엔드 서비스에 직접アクセスしない)                      |
|  +------------------------------------------------------+  |
|  | class Database:                                       |  |
|  |     def __init__(self, url):                        |  |
|  |         self.connection = connect(url)  <- 추상화된 URL |  |
|  |                                                     |  |
|  | class Cache:                                          |  |
|  |     def __init__(self, url):                        |  |
|  |         self.client = redis.from_url(url)  <- 추상화  |  |
|  +------------------------------------------------------+  |
+--------------------------------------------------------------+

3. 런타임 연결 (Runtime Connection)
+--------------------------------------------------------------+
|  애플리케이션 실행 시                                         |
|                                                             |
|  +-----------------------------------------------------+   |
|  |  환경 변수에서 URL 읽기                              |   |
|  |  db_url = os.environ.get("DATABASE_URL")           |   |
|  |  redis_url = os.environ.get("REDIS_URL")           |   |
|  +-----------------------------------------------------+   |
|                         |                                  |
|                         v                                  |
|  +-----------------------------------------------------+   |
|  |  실제 연결 수립                                      |   |
|  |  +----------+    +----------+    +----------+     |   |
|  |  | PostgreSQL|<----|  앱      |---->|  Redis   |     |   |
|  |  |  Server  |    | (Code)   |    |  Server  |     |   |
|  |  +----------+    +----------+    +----------+     |   |
|  |   AWS RDS           동일한 코드        Elasticache   |   |
|  |   (Production)       어느 DB에든 연결     (Production)|   |
|  +-----------------------------------------------------+   |
+--------------------------------------------------------------+
```

> 📢 **섹션 요약 비유**: 백엔드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 연결은"전화 연결 시스템"과 같다. 먼저 전화 번호부([설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)/[환경 변수](/studynote/02_operating_system/02_process_thread/156_environment_variables/))에서 상대방 번호(DATABASE_URL)를 찾고, 그 번호로 전화를 건다(네트워크 연결). 만약 전화번호가 바뀌어도(예: 로컬 전화 -> 인터넷 전화) 전화번호부만 업데이트하면 되고, 전화를 거는 방법(코드)은 변경할 필요가 없다. 이것이"연결된 자원" [추상화](/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/)의위력이다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

백엔드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 원칙은 [마이크로서비스 아키텍처](/studynote/04_software_engineering/04_testing_quality/213_msa_microservices_architecture/), [서비스 메시](/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/), 그리고 현대적인 [클라우드 네이티브](/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) 패턴과 긴밀하게 연결되어 있다.

| 관련 개념 | 백엔드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 원칙과의 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 시너지 효과 |
|:---|:---|:---|
| <strong><a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/">마이크로서비스</a> (<a href="/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/">MSA</a>)</strong> | MSA의 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간통신이 이 원칙의 확장 | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 다른 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를"연결된 자원"처럼 취급 |
| <strong><a href="/studynote/04_software_engineering/05_devops_ci_cd/306_service_discovery_pattern/">서비스 디스커버리</a></strong> | Eureka, Consul등서비스발현 도구와 결합 | 동적 IP보다 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 이름으로 연결 |
| <strong><a href="/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/">서비스 메시</a> (<a href="/studynote/03_network/16_data_center_cloud/828_service_mesh_microservice_communication_infrastructure/">Service Mesh</a>)</strong> | [사이드카](/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)가 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)간통신을 관리 | [mTLS](/studynote/03_network/16_data_center_cloud/831_mtls_mutual_tls_microservices_zero_trust/), 회로 차단기 등 관문 제공 |
| <strong><a href="/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/">컨테이너 오케스트레이션</a></strong> | K8s [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 연결 단위 | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 이름으로 [DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) 기반 연결 |
| **다واء 환경 (Polyglot)** | 각 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 다른 DB 사용 가능 | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)별 최적 DB 선택 가능 |

[마이크로서비스](/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/) 환경에서 백엔드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 원칙은 더욱 중요해진다. MSA에서는 각 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 자체 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)를지유하며, 그 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)에 대한 연결 정보를 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 내부에서 관리해야 한다. 만약 백엔드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 원칙을 준수하지 않으면, [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 다른 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)에 직접 접근하는"공향 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)" [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)이 발생하여 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 결합이 증가하고, 독립적 배포가 어려워진다.

```text
[MSA에서의 백엔드 서비스 원칙 적용]

 monolith(모놀리스)
 +-----------------------------------------------+
 |  앱                                               |
 |  +---------+  +---------+  +---------+      |
 |  | 주문 서비스|  | 결제 서비스|  | 배송 서비스|      |
 |  +----+----+  +----+----+  +----+----+      |
 |       |            |            |              |
 |  +----+------------+------------+----+      |
 |  |         공유 데이터베이스              | <- 안티패턴!      |
 |  |    (서비스 간 결합 증가)              |      |
 |  +-------------------------------------+      |
 +-----------------------------------------------+

 MSA (마이크로서비스)
 +-----------------------------------------------+
 |                                                 |
 |  +---------+  +---------+  +---------+      |
 |  | 주문 서비스|  | 결제 서비스|  | 배송 서비스|      |
 |  +----+----+  +----+----+  +----+----+      |
 |       |            |            |              |
 |       v            v            v              |
 |  +---------+  +---------+  +---------+      |
 |  | 주문 DB  |  | 결제 DB  |  | 배송 DB  |      |
 |  +---------+  +---------+  +---------+      |
 |  (각 서비스가 자신의 DB를"소유")              |
 |                                                 |
 |  서비스 간 통신: API 호출 (연결된 자원처럼)       |
 +-----------------------------------------------+
```

> 📢 **섹션 요약 비유**: MSA에서의 백엔드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 원칙은"전문직 담당자제도"와 같다. 주문 담당자(주문 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))는 고객의 주문을 받지만 직접 결제를 처리하지 않고(직접 DB 접근 금지) 결제 담당자(결제 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))에게 요청한다([API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 호출). 결제 담당자는 자신의 결제 기록(결제 DB)만 관리한다. 만약 주문 담당자가 직접 결제 기록을 보려 한다면(공유 DB 접근) 업무 혼란이 발생한다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)

백엔드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 원칙을 실무에 적용할 때 흔히 발생하는 문제와 해결 방안을 분석한다.

**1. 실무 의사결정 시나리오**
- <strong>시나리오 A: 여러 <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a>가동일개 <a href="/studynote/05_database/01_db_architecture_relational/002_database_definition/">데이터베이스</a>를 공유하고 있는데 MSA로 전환해야 할 때</strong>
  - **상황**: 기존 모놀리스에서 여러 [모듈](/studynote/04_software_engineering/04_testing_quality/192_module_independence/)이 하나의 DB를 공유하고 있는데, MSA로 전환하려고 함.
  - **판단**: 이것은"공향 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)" [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)이다. 각 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)로 분리할 때, 가장 먼저 각 [모듈](/studynote/04_software_engineering/04_testing_quality/192_module_independence/)의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 접근 패턴을 분석하고, 어떤 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 어떤 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)"소유"인지 결정해야 한다. 공유 테이블은 피하면서, [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 또는 이벤트 기반통신으로 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)동보을 처리해야 한다.

- <strong>시나리오 B: 백엔드 <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 연결 정보 (Connection String)를안전하게관리해야 할 때</strong>
  - **상황**: [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)밀마와 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 키가 [환경 변수](/studynote/02_operating_system/02_process_thread/156_environment_variables/)에 plain text로 있어 [보안 감사](/studynote/04_software_engineering/11_testing_validation/919_security_audit_trail/) 시 지적받음.
  - **판단**: [시크릿 매니저](/studynote/15_devops_sre/02_cicd_gitops/095_secret_manager_hashicorp_vault_aws/)([Vault](/studynote/09_security/11_iam_access_control/567_vault/), AWS Secrets Manager, Azure [Key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) [Vault](/studynote/09_security/11_iam_access_control/567_vault/))를활용하여 연결 정보를 동적으로 관리해야 한다. 애플리케이션은 런타임에 [시크릿 매니저](/studynote/15_devops_sre/02_cicd_gitops/095_secret_manager_hashicorp_vault_aws/)에서 자격 증명을 가져와 연결하므로, 연결 정보가 [환경 변수](/studynote/02_operating_system/02_process_thread/156_environment_variables/)나 코드에 영구히보존되지 않는다.

```text
[백엔드 서비스 연결 관리: 보안 강화 단계]

Level 1: 환경 변수 (기본)
  DATABASE_URL=postgres://user:pass@host:port
  문제: 환경 변수 파일이 유출되면 비밀번호도 유출

Level 2: 시크릿 매니저 (권장)
  DATABASE_URL=postgres://vault:secret/data/db
  -> 런타임에 Vault에서 동적 자격증명 가져옴

Level 3: 동적 시크릿 (최고 보안)
  매 요청마다 새로운 일회성 자격증명 생성
  -> 기존 자격증명의 장기 유출 방지
```

> 📢 **섹션 요약 비유**: 백엔드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 연결 정보 관리는"호텔 금고 시스템"과 같다. Level 1은 금고 비밀번호를 종이에 적어두는 것(평문 [환경 변수](/studynote/02_operating_system/02_process_thread/156_environment_variables/))으로, 누군가가 종이를 발견하면 위험하다. Level 2는 비밀번호를 은행 금고에예け고두고 필요할 때 출납증을받고 금고를 여는 것이며([시크릿 매니저](/studynote/15_devops_sre/02_cicd_gitops/095_secret_manager_hashicorp_vault_aws/)), Level 3은 얼굴 인식으로 매번 새로운 임시 접근 권한을 받는 것이다(동적 [시크릿](/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/)).

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

백엔드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 원칙의 올바른 적용은 [마이크로서비스](/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/) 전환, [클라우드 네이티브 아키텍처](/studynote/12_it_management/05_security_compliance/204_cloud_native_architecture/), 그리고 [DevOps](/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) 문화 구축에fundamental한 기반이 된다.

| 관점 | 백엔드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 원칙 미준수 ([AS-IS](/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/)) | 백엔드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 원칙 준수 (TO-BE) | [핵심 성과 지표](/studynote/12_it_management/01_governance_strategy/018_kpi/) |
|:---|:---|:---|:---|
| **확장성** | DB 변경 시 대규모 코드 수정 | [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)만 변경하여 손쉽게절환 | DB 마이그레이션 시간 80% 단축 |
| <strong><a href="/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/">유지보수성</a></strong> | 백엔드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 변경 시 다수 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 수정 | [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 변경으로 끝, 코드 수정 불필요 | 변경영향범위 최소화 |
| **테스트** | 실제 백엔드 없이는 테스트 불가능 |[Mock](/studynote/04_software_engineering/11_testing_validation/854_mock_test_double/)/Fake로 쉽게 대체 가능 | [단위 테스트](/studynote/04_software_engineering/12_testing_maintenance/397_unit_test/) 커버리지 증가 |
| **보안** | 연결 정보가 코드/[설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)에 노출 | [시크릿 매니저](/studynote/15_devops_sre/02_cicd_gitops/095_secret_manager_hashicorp_vault_aws/)로 동적 관리 | 보안 취약점 감소 |
| <strong><a href="/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/">MSA</a> 전환</strong> | 공유 DB 의존도로 전환 어려움 | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)별 독립적 DB 관리 용이 | [MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 전환 실패율 감소 |

**미래 전망 및 결론**:
백엔드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 원칙은 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/), [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/), [서비스 메시](/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/) 등 현대적 아키텍처의 기본이 된다. 특히 [서비스 디스커버리](/studynote/04_software_engineering/05_devops_ci_cd/306_service_discovery_pattern/)와 결합하면, 애플리케이션이 백엔드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 실제 IP 나위패을 몰라도 되고, [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 이름으로만 접근할 수 있게 된다.

앞으로 백엔드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 원칙은"[서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 계약(Contract)"과"[API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 게이트웨이" 패턴으로 더욱 발전할 것이다. [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 통신은 이제 직접 IP 수준에서 이루어지는 것이 아니라, [서비스 메시](/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/)를 통해 [sidecar](/studynote/04_software_engineering/11_testing_validation/938_sidecar_proxy_pattern/) [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)가 개입하여 자동으로 재시도, 회로 차단, [mTLS](/studynote/03_network/16_data_center_cloud/831_mtls_mutual_tls_microservices_zero_trust/) 등의 기능을제공하게 된다.

결론적으로, 백엔드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 원칙은 12팩터 앱의 제4원칙으로, 애플리케이션과 외부 자원 사이의 decoupling을실현하는 핵심 개념이다. 이 원칙을 준수하면 백엔드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 변경, 확장, 마이그레이션이 훨씬 용이해지며, 궁극적으로 더 유연하고 확장 가능한 시스템을 구축할 수 있다. 모든 [개발 팀](/studynote/04_software_engineering/02_requirements_analysis/065_development_team_scrum/)은 백엔드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에 접근할 때 반드시 [추상화](/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/)된 연결 방식을 사용하고, 연결 정보는 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 또는 [시크릿 매니저](/studynote/15_devops_sre/02_cicd_gitops/095_secret_manager_hashicorp_vault_aws/)를 통해 관리해야 한다.

> 📢 **섹션 요약 비유**: 백엔드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 원칙은"호텔의 룸서비스 주문 시스템"과 같다. 손님(애플리케이션)이 룸서비스를 시키려고 할 때, 직접주방(백엔드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))에 가서 음식을 가져오지 않고(직접 DB 접근 안 함) 상담원([추상화](/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) 레이어)에게 주문하면(연결된 자원 접근), 상담원이주방에 연락해서 음식을 가져오게 한다(대행). 만약주방가 바뀌어도(백엔드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 변경) 상담원 연결만 유지하면 되고([설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 변경), 손님은 동일한 방법으로 주문할 수 있다(코드 불변).

### 📌 관련 개념 맵 ([Knowledge Graph](/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))

- 12팩터 앱 ([12-Factor App](/studynote/06_ict_convergence/03_cloud_infrastructure/200_12_factor_app_cloud_native_principles/)) | 현대적 [클라우드 네이티브](/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) 애플리케이션 설계 방법론, 백엔드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 제4원칙
- [환경 변수](/studynote/02_operating_system/02_process_thread/156_environment_variables/) ([Environment](/studynote/15_devops_sre/02_cicd_gitops/066_gitlab_flow_environment_branch_strategy/) Variable) | 코드와 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)을 분리하는 12팩터의 제3원칙
- [시크릿 매니저](/studynote/15_devops_sre/02_cicd_gitops/095_secret_manager_hashicorp_vault_aws/) ([Secret Manager](/studynote/15_devops_sre/02_cicd_gitops/095_secret_manager_hashicorp_vault_aws/)) | 연결 정보·자격증명을 코드 외부에서 안전하게 관리하는 도구
- [서비스 디스커버리](/studynote/04_software_engineering/05_devops_ci_cd/306_service_discovery_pattern/) ([Service Discovery](/studynote/12_it_management/05_security_compliance/946_service_discovery/)) | MSA에서 백엔드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 위치를 동적으로 찾는 메커니즘

### 📈 관련 키워드 및 발전 흐름도

```text
[하드코딩 (Hardcoding) — 코드에 DB URL·비밀번호 직접 삽입]
    |
    v
[환경 변수 분리 (Env Var) — 설정과 코드 분리, 12팩터 제3원칙]
    |
    v
[백엔드 서비스 추상화 (Backing Service) — 첨부 자원으로 취급]
    |
    v
[시크릿 매니저 (Secret Manager) — 동적 자격증명 안전 관리]
    |
    v
[서비스 메시 (Service Mesh) — 사이드카 프록시로 서비스 간 통신 추상화]
    |
    v
[서비스 디스커버리 (Service Discovery) — MSA 동적 엔드포인트 탐색]
```
백엔드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 원칙은 하드코딩 배제에서 출발해 [환경 변수](/studynote/02_operating_system/02_process_thread/156_environment_variables/) 분리 -> [시크릿 관리](/studynote/13_cloud_architecture/04_devops_observability/177_secrets_management_vault_kubernetes/) -> [서비스 메시](/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/)로 이어지는 [클라우드 네이티브](/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 연결의 진화 경로를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 집 전화기(앱)에 친구 집 번호(DB 주소)를 벽에 직접 써놓으면, 친구가 이사 가면 벽을 다시 칠해야 해요.
2. 그런데 메모장([환경 변수](/studynote/02_operating_system/02_process_thread/156_environment_variables/)·[시크릿 매니저](/studynote/15_devops_sre/02_cicd_gitops/095_secret_manager_hashicorp_vault_aws/))에 번호를 적어두면, 친구가 이사 가도 메모장만 고치면 된답니다.
3. 백엔드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 원칙은 앱이 언제나 메모장을 보고 연결하도록 만드는 규칙이에요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 10 / 373

<- **이전**: [9. 설정 (Config) - 환경 변수(Env Vars)에 설정을 저장하여 코드와 분리](/studynote/15_devops_sre/01_culture_methodology/009_config/)
**다음**: [11. 빌드, 릴리스, 실행 (Build, Release, Run) 단계의 엄격한 분리](/studynote/15_devops_sre/01_culture_methodology/011_build_release_run/) ->

---
