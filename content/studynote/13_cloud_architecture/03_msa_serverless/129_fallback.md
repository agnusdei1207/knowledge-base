+++
title = "129. Fallback 패턴 - MSA 장애 시 대체 응답 전략"
date = 2026-04-19

[taxonomies]
tags = ["studynote-cloud-architecture"]

[extra]
tags = ["studynote-cloud-architecture"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Fallback은 <strong>원격 <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 호출 실패 시 미리 정의된 대체 응답을 반환</strong>하는 복원력 패턴이며, [Circuit Breaker](/knowledge-base/studynote/12_it_management/05_security_compliance/304_circuit_breaker/)·Retry와 함께 사용되어 사용자에게 <strong>부분적이라도 <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a>를 유지</strong>한다.
> 2. **가치**: 추천 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 장애 시 전체 페이지가 에러가 되는 대신, Fallback으로 <strong>인기 상품 목록(캐시)</strong>을 보여주면 사용자 경험 저하를 최소화한다.
> 3. **판단 포인트**: 캐시 Fallback·기본값·대체 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)·Graceful Degradation [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 상황에 맞게 선택하고, Fallback 자체의 실패도 고려(Fallback의 Fallback)해야 한다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    Fallback 전략 유형                                 |
+-------------------------------------------------------+
|  1. 캐시 반환: 이전 성공 응답 캐시                   |
|  2. 기본값: 정적 기본 데이터 반환                    |
|  3. 대체 서비스: 다른 서비스 호출                    |
|  4. 기능 비활성화: 해당 기능 숨김                    |
|  5. 에러 안내: 사용자에게 상태 안내                  |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: Fallback은 <strong>비상식량</strong>이다. 정상 배달([서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))이 안 오면 비상식량(캐시·기본값)으로 버틴다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | 장점 | 단점 |
|:---|:---|:---|
| **캐시** | 최신에 가까운 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | 오래된 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 위험 |
| **기본값** | 구현 간단 | 개인화 없음 |
| <strong>대체 <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a></strong> | 기능 유지 | 의존성 증가 |

- **📢 섹션 요약 비유**: 캐시는 냉동식품, 기본값은 컵라면, 대체 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 다른 식당 배달이다.

---

## Ⅲ. 비교 및 연결

| 비교 | Fallback 없음 | Fallback 있음 |
|:---|:---|:---|
| **장애 시** | 500 에러 | <strong>부분 <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 유지</strong> |
| **UX** | 최악 | **Graceful Degradation** |

---

## Ⅳ. 실무 적용 및 기술사 판단

- [Circuit Breaker](/knowledge-base/studynote/12_it_management/05_security_compliance/304_circuit_breaker/) Open 시 -> Fallback 자동 호출.
- Netflix: 추천 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 장애 -> Top [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) 목록(캐시) 반환.
- Resilience4j: `@Fallback` 어노테이션.

---

## Ⅴ. 기대효과 및 결론

Fallback은 <strong>MSA에서 사용자 경험을 지키는 마지막 방어선</strong>이며, Circuit Breaker와 함께 복원력의 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Fallback** | 장애 시 대체 응답 |
| <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/304_circuit_breaker/">Circuit Breaker</a></strong> | Fallback [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/) |
| **Graceful Degradation** | 기능 점진적 저하 |
| **캐시** | Fallback의 가장 흔한 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/308_bulkhead_pattern/">Bulkhead</a></strong> | 격벽 (다른 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)) |

### 📈 관련 키워드 및 발전 흐름도

```text
[직접 에러 반환 (~2010s)]
    -> [Hystrix Fallback (2012~)]
    -> [Resilience4j Fallback (2018~)]
    -> [서비스 메시 Fallback (Istio, 2020~)]
    -> [현재: AI Fallback — 상황별 최적 대체 자동 선택]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Fallback은 <strong>비상식량</strong>이에요. 정상 배달이 안 오면 **비상식량으로 버텨요**.
2. 추천 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 고장나도 <strong>인기 상품 목록(캐시)</strong>을 보여줘서 쇼핑은 계속돼요.
3. 비상식량이 없으면 **굶어야(에러)** 하니까, 꼭 준비해둬야 해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 128 / 371

<- **이전**: [128. Circuit Breaker - MSA 장애 전파 차단 패턴](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/128_circuit_breaker/)
**다음**: [130. Bulkhead 패턴 - 격벽으로 장애 격리](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/130_bulkhead_pattern/) ->

---
