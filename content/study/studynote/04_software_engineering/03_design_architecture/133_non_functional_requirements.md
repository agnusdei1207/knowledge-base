+++
weight = 133
title = "133. 비기능 요구사항 (NFR) - 시스템 품질 속성 정의"
date = "2026-04-19"
[extra]
categories = "studynote-software-engineering"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: NFR(Non-Functional Requirements)은 **시스템이 "어떻게" 동작해야 하는가의 품질 [[082_attribute_types_er_model|속성]]**으로, [[282_performance_tactics|성능]]·보안·[[452_availability|가용성]]·확장성·[[346_maintainability_portability|유지보수성]] 등을 정의하며 ISO 25010이 [[104_classification_analysis|분류]] 표준이다.
> 2. **가치**: NFR이 **아키텍처를 결정**한다. "초당 10만 요청"이면 [[136_variance|분산]] 아키텍처, "99.999% [[452_availability|가용성]]"이면 Active-Active 이중화가 필요하며, NFR 없이는 아키텍처 결정이 불가능하다.
> 3. **판단 포인트**: NFR은 **측정 가능한 수치**로 명세해야 [[395_verification_process_review|검증]] 가능하다. "빨라야 한다"(✗) → "P99 [[138_response_time|응답 시간]] 200ms 이내"(✓).

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
| **[[282_performance_tactics|성능]]** | P99 < 200ms | 캐시, [[506_cdn_content_delivery_network_edge_caching|CDN]] |
| **[[452_availability|가용성]]** | 99.99% | Active-Active |
| **확장성** | 10x 트래픽 | 오토스케일링 |
| **보안** | [[416_owasp_top_10|OWASP Top 10]] | [[696_waf_web_application_firewall|WAF]], 암호화 |

---

## Ⅲ~Ⅴ. 결론

NFR은 **아키텍처의 핵심 동인([[319_architecture|Architecture]] Driver)**이며, 수치로 명세하지 않으면 [[395_verification_process_review|검증]]이 불가능하다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **NFR** | 품질 [[082_attribute_types_er_model|속성]] (How well) |
| **ISO 25010** | 8대 품질 특성 |
| **[[229_atam_architecture_trade_off_analysis_method|ATAM]]** | NFR 트레이드오프 분석 |
| **QAW** | 품질 [[082_attribute_types_er_model|속성]] 워크숍 |
| **[[319_architecture|Architecture]] Driver** | NFR이 아키텍처를 결정 |

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
