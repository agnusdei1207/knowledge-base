+++
title = "143. Strangler Fig 패턴 - 모놀리스->MSA 점진적 전환"
date = 2026-04-19

[taxonomies]
tags = ["studynote-cloud-architecture"]

[extra]
tags = ["studynote-cloud-architecture"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Strangler Fig는 <strong>기존 모놀리스 시스템을 한 번에 교체하지 않고, 새 기능을 MSA로 만들어 점진적으로 모놀리스를 교살(Strangle)</strong>하여 최종적으로 대체하는 마이그레이션 패턴이다(Martin Fowler).
> 2. **가치**: 빅뱅 교체(Big Bang Rewrite)는 <strong>고위험·장기간·실패 <a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/">확률</a> 높음</strong>이지만, Strangler Fig는 <strong>점진적·저위험</strong>으로 운영 중인 시스템을 중단 없이 전환한다.
> 3. **판단 포인트**: [API Gateway](/knowledge-base/studynote/04_software_engineering/11_testing_validation/934_api_gateway/)/Proxy가 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)을 담당하여 <strong>기능별로 새 <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a>->모놀리스 트래픽을 점진 전환</strong>하며, Anti-corruption Layer([ACL](/knowledge-base/studynote/02_operating_system/09_file_system/549_acl_access_control_list/))로 신·구 시스템 간 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 변환을 처리한다.

---

## Ⅰ. 개요 및 필요성

```text
1단계: 새 기능 -> MSA로 개발 (모놀리스 옆에)
2단계: API GW -> 새 기능은 MSA로 라우팅, 나머지는 모놀리스
3단계: 기능 하나씩 MSA로 이전 -> 모놀리스 축소
4단계: 모놀리스 완전 제거 (교살 완료)
```

- **📢 섹션 요약 비유**: Strangler Fig는 <strong>무화과 나무가 기존 나무를 감싸며 대체</strong>하는 것이다. 기존 나무(모놀리스)가 점차 사라진다.

---

## Ⅱ~Ⅴ. 결론

Strangler Fig는 <strong>모놀리스-><a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/">MSA</a> 전환의 사실상 표준 <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a></strong>이며, [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) Gateway와 ACL이 핵심 인프라이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/310_strangler_fig_pattern/">Strangler Fig</a></strong> | 점진적 교체 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/11_testing_validation/934_api_gateway/">API Gateway</a></strong> | [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 전환 |
| <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/549_acl_access_control_list/">ACL</a></strong> | 신·구 변환 레이어 |
| **Big Bang** | 위험한 대안 |
| **Feature Toggle** | 점진 전환 제어 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Big Bang Rewrite (고위험)] -> [Strangler Fig (Fowler, 2004)]
    -> [API GW 기반 라우팅 (2015~)]
    -> [현재: 도메인별 Strangler — DDD 기반 분해]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Strangler Fig는 **덩굴이 큰 나무를 감싸** 천천히 대체하는 거예요.
2. 한 번에 바꾸면 **위험하니까** 조금씩 새것으로 바꿔요.
3. 결국 큰 나무(모놀리스)는 사라지고 <strong>덩굴(<a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/">MSA</a>)만</strong> 남아요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 142 / 371

<- **이전**: [142. Externalized Configuration - 외부 설정 관리 패턴](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/142_externalized_configuration/)
**다음**: [144. 서비스 메시 (Service Mesh) - 사이드카 기반 통신 인프라](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/144_service_mesh/) ->

---
