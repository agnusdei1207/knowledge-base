---
title: 62. 코로케이션 (Colocation) - 데이터센터 공간 임대 서비스
date: '2026-04-07'
tags:
- studynote-enterprise
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 코로케이션(Colocation)은 고객이 소유한 서버를 전문 [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]]에 두고, 공간·전력·네트워크·냉각만 임대하는 방식이다.
> 2. **가치**: [[061_on_premise_legacy_infrastructure|온프레미스]]의 통제권을 유지하면서도 전산실 구축 비용과 물리적 운영 부담을 줄인다.
> 3. **융합**: [[838_direct_connect_expressroute_cloud_leased_line|Direct Connect]] 같은 [[266_leased_line_basics_e1_t1_t3|전용선]]과 결합해 [[009_hybrid_cloud|하이브리드 클라우드]]의 거점으로 [[289_cqrs_db|쓰기]] 좋다.

---

## Ⅰ. 개요 및 필요성

전산실을 직접 짓는 것은 비싸고, [[007_public_cloud|퍼블릭 클라우드]]만 쓰는 것도 규제와 비용 문제로 어려울 수 있다. 그 중간 해법이 코로케이션이다.

즉, 서버는 내가 사고, 장소와 인프라는 전문 [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]]에 맡긴다. 그래서 소유와 운영을 적절히 분리할 수 있다.

- **📢 섹션 요약 비유**: 내 차는 내가 사지만, 주차장은 잘 관리되는 공영 주차장을 빌리는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
고객 서버
   ↓
데이터센터 Rack
   ├─ 전력
   ├─ 냉각
   ├─ 네트워크
   └─ 물리 보안
```

| 책임 | 고객 | [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]] |
| :-- | :-- | :-- |
| 하드웨어 | 소유 | 공간 제공 |
| [[001_operating_system_purpose|운영체제]]/애플리케이션 | 관리 | 지원 |
| 전력/냉각 | - | 제공 |
| 회선/[[140_bandwidth|대역폭]] | 설계 | 제공 |
| 물리 보안 | 일부 책임 | 주요 책임 |

코로케이션은 "하드웨어 소유 + 시설 임대"의 조합이다. 그래서 장비 튜닝과 통제는 유지하면서, 건물과 전력 [[096_risk_non_risk_architecture_evaluation_flaws|리스크]]를 외부 전문업체로 넘길 수 있다.

- **📢 섹션 요약 비유**: 화분은 내 것이지만, 온도와 물은 식물원에 맡기는 방식이다.

---

## Ⅲ. 비교 및 연결

| 항목 | [[061_on_premise_legacy_infrastructure|온프레미스]] | 코로케이션 | [[007_public_cloud|퍼블릭 클라우드]] |
| :-- | :-- | :-- | :-- |
| 소유 | 고객 | 고객 | 사업자 |
| 공간/전력 | 고객 | 사업자 | 사업자 |
| 통제권 | 매우 높음 | 높음 | 상대적으로 낮음 |
| 확장성 | 낮음 | 중간 | 높음 |

코로케이션은 [[009_hybrid_cloud|하이브리드 클라우드]]의 중간 거점이 되기 좋다. 특히 대용량 트래픽이나 규제 산업에서 [[176_direct_addressing|Direct]] Connect와 연결해 활용한다.

- **📢 섹션 요약 비유**: 집은 내 것이고, 입구와 경비는 전문 빌딩에 맡긴 셈이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[435_checklist_based_testing|체크리스트]]

1. 서버 소유권이 필요한가?
2. 전력/냉각/물리 보안 비용을 줄여야 하는가?
3. 클라우드와 [[266_leased_line_basics_e1_t1_t3|전용선]]으로 연결할 계획이 있는가?
4. 원격 관리와 장애 대응 체계가 준비됐는가?
5. 규제나 [[141_latency|지연 시간]] 요구가 강한가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 코로케이션을 단순 창고처럼 생각하는 설계
- 회선, 전력, 원격 핸즈 지원을 과소평가하는 설계
- 클라우드와의 연결 비용을 계산하지 않는 설계
- 장비 소유와 운영 책임을 분리하지 않는 설계

기술사 관점에서는 코로케이션을 "구식 IDC"가 아니라, 통제권과 비용을 균형 있게 조정하는 인프라 [[268_strategy_pattern|전략]]으로 봐야 한다.

- **📢 섹션 요약 비유**: 내 가구를 들고, 관리가 잘되는 창고에 맡겨 두는 것과 같다.

---

## Ⅴ. 기대효과 및 결론

코로케이션은 [[061_on_premise_legacy_infrastructure|온프레미스]]와 클라우드 사이의 현실적인 절충안이다. 통제와 확장, 비용과 안정성의 균형을 맞추기 좋다.

결국 코로케이션의 핵심은 "장비는 내가, 시설은 전문가가" 맡는 분업이다.

- **📢 섹션 요약 비유**: 물건은 직접 고르고, 보관은 잘하는 곳에 맡기는 방식이다.

---

## 관련 개념 맵

```text
Customer-owned Hardware
   ↓
Colocation
   ↓
Direct Connect
   ↓
Hybrid Cloud
   ↓
Private Edge
```

---

## 관련 키워드 및 발전 흐름도

```text
온프레미스
   ↓
코로케이션
   ↓
Direct Connect
   ↓
하이브리드 클라우드
```

---

## 어린이를 위한 3줄 비유 설명

내 물건은 내가 사요.  
그 물건을 잘 지켜 주는 창고만 빌려요.  
그래서 안전하면서도 내가 직접 관리할 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 62 / 482

← **이전**: [[061_on_premise_legacy_infrastructure|61. 온프레미스 (On-Premise) 프라이빗 IT 인프라]]
**다음**: [[063_cloud_vendor_lock_in_avoidance|63. 클라우드 벤더 락인 (Cloud Vendor Lock-in) 회피 전략]] →

---
