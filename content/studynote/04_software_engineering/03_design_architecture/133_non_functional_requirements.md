+++
title = "133. 비기능 요구사항 (NFR) - 시스템 품질 속성 정의"
date = 2026-04-19

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: NFR(Non-Functional Requirements)은 **시스템이 "어떻게" 동작해야 하는가의 품질 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)**으로, [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)·보안·[가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)·확장성·[유지보수성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/) 등을 정의하며 ISO 25010이 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 표준이다.
> 2. **가치**: NFR이 **아키텍처를 결정**한다. "초당 10만 요청"이면 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 아키텍처, "99.999% [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)"이면 Active-Active 이중화가 필요하며, NFR 없이는 아키텍처 결정이 불가능하다.
> 3. **판단 포인트**: NFR은 **측정 가능한 수치**로 명세해야 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 가능하다. "빨라야 한다"(✗) → "P99 [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/) 200ms 이내"(✓).

---

## Ⅰ. 개요 및 필요성

```text
ISO 25010 품질 모델 (8대 특성):
  기능 적합성, 성능 효율성, 호환성, 사용성,
  신뢰성, 보안, 유지보수성, 이식성
```

- **📢 섹션 요약 비유**: NFR은 자동차의 **안전등급·연비·최고속도**이다. "달린다"(FR)만으로는 차를 선택할 수 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| NFR | 수치화 예 | 아키텍처 영향 |
|:---|:---|:---|
| **[성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)** | P99 < 200ms | 캐시, [CDN](/knowledge-base/studynote/03_network/09_application_layer_web_email/506_cdn_content_delivery_network_edge_caching/) |
| **[가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)** | 99.99% | Active-Active |
| **확장성** | 10x 트래픽 | 오토스케일링 |
| **보안** | [OWASP Top 10](/knowledge-base/studynote/09_security/05_web_app_security/416_owasp_top_10/) | [WAF](/knowledge-base/studynote/03_network/13_network_security_basics/696_waf_web_application_firewall/), 암호화 |

---

## Ⅲ~Ⅴ. 결론

NFR은 **아키텍처의 핵심 동인([Architecture](/knowledge-base/studynote/12_it_management/05_security_compliance/319_architecture/) Driver)**이며, 수치로 명세하지 않으면 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)이 불가능하다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **NFR** | 품질 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) (How well) |
| **ISO 25010** | 8대 품질 특성 |
| **[ATAM](/knowledge-base/studynote/04_software_engineering/04_testing_quality/229_atam_architecture_trade_off_analysis_method/)** | NFR 트레이드오프 분석 |
| **QAW** | 품질 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 워크숍 |
| **[Architecture](/knowledge-base/studynote/12_it_management/05_security_compliance/319_architecture/) Driver** | NFR이 아키텍처를 결정 |

### 📈 관련 키워드 및 발전 흐름도

```text
[비공식 NFR (~2000s)] → [ISO 9126 (2001)]
    → [ISO 25010 (2011)] → [QAW·ATAM (아키텍처 관점)]
    → [현재: AI NFR 추출 — 요구사항에서 품질 속성 자동 식별]
```

### 👶 어린이를 위한 3줄 비유 설명
1. NFR은 자동차의 **안전등급·연비·최고속도**예요.
2. "달린다"(기능)만으로는 **좋은 차인지** 알 수 없어요.
3. "200km/h, 연비 15km/L"처럼 **숫자로 정확히** 적어야 비교할 수 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 133 / 973

← **이전**: [132. 요구사항 유형 (기능·비기능·제약사항) - FR·NFR·Constraints 분류](/knowledge-base/studynote/04_software_engineering/03_design_architecture/132_types_of_requirements/)
**다음**: [134. 요구사항 공학 프로세스 - 도출→분석→명세→검증→관리 상세](/knowledge-base/studynote/04_software_engineering/03_design_architecture/134_requirements_engineering_process/) →

---
