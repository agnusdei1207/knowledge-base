+++
title = "537. 분산 모놀리스 (Distributed Monolith) 안티패턴"
date = 2026-05-08

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 분산 모놀리스(Distributed Monolith)는 시스템이 물리적으로는 여러 서비스로 분산되었지만, 논리적으로는 강한 결합도를 유지하여 모놀리식의 단점과 분산 시스템의 복잡성을 동시에 가진 최악의 아키텍처 상태이다.
> 2. **가치**: 이 안티패턴을 인식하고 회피하는 것은 마이크로서비스 아키텍처의 핵심 목표인 독립 배포, 장애 격리, 팀 자율성을 실현하기 위한 전제 조건이다.
> 3. **판단 포인트**: "A 서비스를 변경하면 B 서비스도 동시에 배포해야 하는가?"라는 질문에 "예"라면 분산 모놀리스 징후이며, 원인은 공유 데이터베이스, 강한 동기 의존, 잘못된 서비스 경계 중 하나다.

---

## Ⅰ. 개요 및 필요성

마이크로서비스 전환을 시도하는 많은 조직이 빠지는 함정이 바로 분산 모놀리스다. 겉으로 보기에는 마이크로서비스 구조를 갖추었으나 실제로는 모놀리식보다 더 복잡하고 관리하기 어려운 상태가 된다. 이는 모놀리식의 단점(강한 결합, 일괄 배포 필요)에 분산 시스템의 복잡성(네트워크 장애, 분산 트랜잭션, 관측성 부재)이 더해진 "최악의 조합"이다.

분산 모놀리스는 보통 다음과 같은 경로로 발생한다. 팀이 마이크로서비스 전환을 결정하고 모놀리식 코드베이스를 물리적으로 분리한다. 그러나 서비스 경계를 비즈니스 도메인이 아닌 기술 레이어(Controller/Service/Repository)로 나누거나, 기존 공유 데이터베이스를 그대로 유지하거나, 서비스 간 직접 데이터베이스 참조를 허용하면서 논리적 결합도는 전혀 낮아지지 않는다.

이 안티패턴을 이해하는 것이 중요한 이유는, 마이크로서비스 도입의 실질적 성공을 가로막는 가장 흔한 장애물이기 때문이다. 가트너(Gartner)의 연구에 따르면 마이크로서비스 도입 실패의 상당 부분이 잘못된 서비스 분해와 공유 데이터베이스로 인한 분산 모놀리스 문제에서 비롯된다. 반대로 이 안티패턴을 의식하고 회피하는 팀은 마이크로서비스의 핵심 이점인 독립 배포와 팀 자율성을 실현할 수 있다.

- **📢 섹션 요약 비유**: 큰 집을 여러 가구로 나눴는데, 모든 가구가 공용 전기 스위치를 함께 쓰고, 냉방·난방을 동시에 켜고 꺼야 한다면 집을 나눈 의미가 없다. 각 가구가 독립적으로 전기를 쓸 수 있어야 진짜 분리된 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 분산 모놀리스의 발생 원인과 구조



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">분산 모놀리스 발생 패턴</div></div>
<div class="kb-diagram-note">잘못된 분해 (기술 레이어 기준):</div>
<div class="kb-diagram-note">클라이언트</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Controller 서비스</div>
<div class="kb-diagram-note">↓ (동기 HTTP 호출 - 항상 함께 배포)</div>
<div class="kb-diagram-note">Service Layer 서비스</div>
<div class="kb-diagram-note">↓ (동기 HTTP 호출 - 항상 함께 배포)</div>
<div class="kb-diagram-note">Repository 서비스</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">공유 데이터베이스 (모든 서비스가 직접 접근)</div>
</div>
</div>



이 구조는 마이크로서비스처럼 보이지만, 실제로는 다음 이유로 모놀리스와 동일하다.
- Controller 하나 변경 → Service, Repository 동시 배포 필요
- 공유 DB 스키마 변경 → 모든 서비스 동시 영향

### 분산 모놀리스의 3가지 핵심 징후

| 징후 | 설명 | 진단 질문 |
|:---|:---|:---|
| 동기 배포 의존 | 한 서비스 변경 시 다른 서비스도 동시 배포 | "A만 단독 배포하면 오류가 나는가?" |
| 공유 데이터베이스 | 여러 서비스가 동일 DB 스키마 직접 접근 | "DB 테이블을 여러 서비스가 직접 조인하는가?" |
| 강한 동기 결합 | 하나의 서비스 장애가 전체를 마비 | "A 서비스가 죽으면 B, C, D도 장애가 나는가?" |

### 분산 모놀리스 vs 진정한 마이크로서비스 비교



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">분산 모놀리스</div><div class="kb-diagram-node">진정한 마이크로서비스</div></div>
<div class="kb-diagram-note">서비스 A → 서비스 B → 서비스 C 서비스 A</div>
<div class="kb-diagram-note">↘ ↗ ↘ ↕ (이벤트/API)</div>
<div class="kb-diagram-note">공유 DB 서비스 D 서비스 B</div>
<div class="kb-diagram-note">↕ (이벤트/API)</div>
<div class="kb-diagram-note">(강한 결합, 공유 상태) 서비스 C</div>
<div class="kb-diagram-note">(느슨한 결합, 독립 DB)</div>
</div>
</div>



| 비교 항목 | 분산 모놀리스 | 진정한 마이크로서비스 |
|:---|:---|:---|
| 배포 단위 | 여러 서비스 동시 배포 필요 | 단일 서비스 독립 배포 |
| 데이터 소유 | 공유 데이터베이스 | 서비스별 독립 데이터베이스 |
| 장애 격리 | 연쇄 장애 (Cascading Failure) | 장애 격리 및 폴백 |
| 팀 자율성 | 낮음 (다른 팀과 조율 필수) | 높음 (독립적 결정) |
| 롤백 | 여러 서비스 동시 롤백 | 단일 서비스 독립 롤백 |
| 네트워크 복잡도 | 높음 | 높음 |
| 운영 복잡도 | 매우 높음 | 관리 가능 수준 |

### 공유 데이터베이스 안티패턴 구체 사례

```sql
-- 분산 모놀리스의 전형: 주문 서비스가 고객 DB에 직접 조인
SELECT o.*, c.name, c.email
FROM order_service.orders o
JOIN customer_service.customers c  -- 다른 서비스의 테이블 직접 접근!
ON o.customer_id = c.id
WHERE o.status = 'CREATED';

-- 올바른 마이크로서비스: API를 통한 데이터 조회
-- 주문 서비스 내부:
SELECT * FROM orders WHERE status = 'CREATED';
-- 고객 정보는 Customer API를 통해 별도 조회
```

### 분산 모놀리스 자가 진단 체크리스트

| 점검 항목 | 징후 (분산 모놀리스) | 건강 (진정한 MSA) |
|:---|:---|:---|
| 배포 독립성 | 동시 배포 필요 | 단독 배포 가능 |
| 데이터 접근 | 공유 DB 또는 직접 테이블 접근 | API 또는 이벤트를 통해서만 |
| 서비스 다운 영향 | 연쇄 장애 발생 | 관련 기능만 저하 |
| 팀 소유권 | 여러 팀이 하나의 서비스 | 한 팀이 한 서비스 전담 |
| 인터페이스 계약 | 없거나 암묵적 | 명확한 API 계약 (OpenAPI 등) |

- **📢 섹션 요약 비유**: 아파트처럼 보이지만 각 세대가 같은 가스 밸브, 같은 수도 계량기를 공유하고, 한 세대에서 가스를 잠그면 모든 세대가 영향받는다면? 겉모습은 개별 세대지만 실질적으로 한 집이다.

---

## Ⅲ. 비교 및 연결

### 아키텍처 진화 스펙트럼



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">아키텍처 진화 단계</div></div>
<div class="kb-diagram-note">모놀리식 분산 모놀리스 진정한 마이크로서비스</div>
<div class="kb-diagram-note">(Monolith) (안티패턴) (True MSA)</div>
<div class="kb-diagram-note">단일 배포 물리 분리만 논리+물리 분리</div>
<div class="kb-diagram-note">단순 운영 최악의 복잡도 관리 가능한 복잡도</div>
<div class="kb-diagram-note">느린 확장 확장 어려움 독립 확장</div>
<div class="kb-diagram-note">낮은 결합도 높은 결합도 낮은 결합도</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">판단 기준</div></div>
<div class="kb-diagram-note">분산 모놀리스 리스크 &gt; 모놀리식 리스크</div>
<div class="kb-diagram-note">→ 차라리 모놀리스로 유지하는 것이 나음</div>
</div>
</div>



### 모놀리식 vs 분산 모놀리스 vs 진정한 MSA

| 비교 항목 | 모놀리식 | 분산 모놀리스 | 진정한 MSA |
|:---|:---|:---|:---|
| 운영 복잡도 | 낮음 | 매우 높음 | 높음 (관리 가능) |
| 개발 속도 | 초기 빠름 | 매우 느림 | 서비스별 빠름 |
| 확장성 | 전체 확장 | 제한적 | 서비스별 독립 |
| 장애 격리 | 전체 장애 | 전체 장애 + 네트워크 오류 | 부분 장애 |
| 데이터 일관성 | ACID 트랜잭션 | 복잡한 분산 트랜잭션 | 최종 일관성 |
| 추천 상황 | 소규모 팀, 초기 | 피해야 할 상태 | 성숙한 팀, 복잡한 도메인 |

- **📢 섹션 요약 비유**: 분산 모놀리스는 팀은 여러 팀으로 나뉘었는데 모든 결재는 CEO에게 받아야 하는 조직과 같다. 팀을 나눈 의미가 없고, 오히려 의사소통 경로만 늘어나 더 느려진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 분산 모놀리스 탈출 전략

```
[분산 모놀리스 → 진정한 MSA 마이그레이션]

현재 상태: 공유 DB + 강한 동기 결합

1단계: 서비스 경계 재설계
    - 도메인 이벤트 스토밍 실시
    - 비즈니스 능력/DDD 기반 경계 재정의

2단계: 데이터 분리 (가장 어려운 단계)
    - 공유 DB 테이블 소유권 명확화
    - 각 서비스별 독립 DB 마이그레이션
    - API를 통한 데이터 접근으로 전환

3단계: 동기 의존 제거
    - 강한 동기 호출 체인을 이벤트 기반으로 전환
    - 사가 패턴으로 분산 트랜잭션 처리

4단계: 독립 배포 파이프라인 구축
    - 서비스별 독립 CI/CD 파이프라인
    - 독립 배포 테스트 자동화
```

### 설계 판단 체크리스트

1. **독립 배포 테스트**: 특정 서비스만 단독으로 배포하고 전체 시스템이 정상 동작하는가?
2. **데이터 소유권 명확화**: 각 서비스가 자신의 데이터에만 직접 접근하고, 다른 서비스 데이터는 API를 통해 조회하는가?
3. **장애 격리 검증**: 특정 서비스를 의도적으로 다운시켰을 때(카오스 엔지니어링) 다른 서비스가 계속 동작하는가?
4. **팀 소유권 단순성**: 각 서비스를 정확히 하나의 팀이 소유하고 책임지는가?
5. **배포 의존성 그래프**: 서비스 배포 의존성 그래프를 그렸을 때 순환 의존이나 긴 체인이 없는가?

### 안티패턴 상세 사례

- **공유 도메인 모델 라이브러리 (Shared Domain Model Library)**: 여러 서비스가 공통 도메인 모델(User, Order, Product 클래스)을 하나의 공유 라이브러리로 관리하면, 모델 변경 시 모든 서비스가 동시에 업데이트·재배포되어야 한다. 각 서비스는 자체 도메인 모델을 독립적으로 유지해야 하며, 필요시 Anti-Corruption Layer로 번역해야 한다.
- **동기 오케스트레이션 과다 (Orchestration Overload)**: 하나의 중앙 오케스트레이터 서비스가 수십 개의 서비스를 순서대로 동기 호출하면, 오케스트레이터가 단일 실패 지점이 되고 처리 지연이 누적된다. 코레오그래피(이벤트 기반) 방식이나 사가 패턴으로 전환해야 한다.
- **데이터베이스 직접 접근 (Database Bypass)**: 성능을 이유로 서비스 A가 서비스 B의 데이터베이스에 직접 접근하면, B의 내부 스키마 변경이 A를 즉시 깨뜨린다. 반드시 API 또는 이벤트를 통해 데이터를 공유해야 한다.
- **과도한 공유 라이브러리**: 공통 인증, 로깅, 설정 등 공유 기능을 하나의 거대한 라이브러리로 묶으면, 라이브러리 업데이트 시 모든 서비스의 동시 업데이트가 필요해진다.

- **📢 섹션 요약 비유**: 각 가구가 독립적으로 사용할 수 있는 전기 계량기(독립 DB)와 자물쇠(독립 배포)가 있어야 진짜 분리된 것이다. 공용 계량기와 공용 열쇠를 쓰면 이름만 다른 한 집이다.

---

## Ⅴ. 기대효과 및 결론

분산 모놀리스 안티패턴을 인식하고 회피하면, 마이크로서비스 도입의 핵심 가치인 독립 배포, 장애 격리, 팀 자율성을 실현할 수 있다.

**회피 효과**: 공유 DB를 독립 DB로 전환하면 각 팀은 자신의 데이터 스키마를 다른 팀에 영향 없이 자유롭게 변경할 수 있다. 독립 배포가 가능해지면 팀별 배포 빈도가 높아져 비즈니스 기능을 빠르게 출시할 수 있다. 장애 격리로 하나의 서비스 장애가 전체 시스템을 마비시키지 않아 가용성이 향상된다.

**교훈적 관점**: 분산 모놀리스는 "모놀리식으로 돌아가는 것이 더 나을 수 있다"는 역설을 가르쳐 준다. 마이크로서비스는 복잡성을 추가하는 대신 독립성을 얻는 트레이드오프다. 독립성 없는 복잡성만 추가했다면 전환을 재검토해야 한다. "분산이 목표가 아니라 독립이 목표다"라는 원칙을 기억해야 한다.

결론적으로, 분산 모놀리스 안티패턴은 마이크로서비스 아키텍처의 최대 위험 요소다. 이를 방지하기 위해 서비스 경계를 비즈니스 도메인 중심으로 설계하고, 데이터 소유권을 명확히 하며, 독립 배포를 설계 목표로 삼아야 한다.

- **📢 섹션 요약 비유**: 팀을 여러 개 만들었는데 모든 결정에 전체 팀이 모여야 한다면 팀을 나눈 이유가 없다. 각 팀이 자기 영역에서 독립적으로 결정하고 실행할 때 비로소 팀 분리의 가치가 생긴다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 마이크로서비스 분해 패턴 (532) | 잘못된 분해 기준이 분산 모놀리스를 만든다 |
| 비즈니스 능력 분해 (533) | 올바른 분해 기준 - 기술 레이어 대신 비즈니스 능력 |
| 하위 도메인 분해 / DDD (534) | 서비스 경계 재설계를 위한 도메인 중심 접근 |
| 사가 패턴 (550) | 분산 모놀리스의 공유 트랜잭션 대안 |
| 이벤트 기반 아키텍처 (538) | 강한 동기 결합 제거를 위한 이벤트 기반 전환 |
| 서킷 브레이커 (572) | 분산 모놀리스의 연쇄 장애를 격리하는 패턴 |
| 데이터베이스 per 서비스 패턴 | 공유 DB 안티패턴의 해결책 |
| 스트랭글러 피그 패턴 (Strangler Fig) | 모놀리스를 점진적으로 마이크로서비스로 전환 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">마이크로서비스 전환 붐 (2014~2017)</div>
<div class="kb-diagram-note">(성급한 MSA 도입, 분산 모놀리스 다수 발생)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">분산 모놀리스 문제 인식 및 사례 공유</div>
<div class="kb-diagram-note">(Sam Newman "Building Microservices", 2015)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">안티패턴 분류 및 탈출 전략 체계화</div>
<div class="kb-diagram-note">(도메인 이벤트 스토밍, 데이터 분리 전략)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">"Monolith First" 전략 대두 (Martin Fowler)</div>
<div class="kb-diagram-note">(성숙도 없는 팀은 모놀리스가 더 나음)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">스트랭글러 피그 패턴 확산</div>
<div class="kb-diagram-note">(점진적 MSA 전환으로 리스크 감소)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">카오스 엔지니어링으로 독립성 검증</div>
<div class="kb-diagram-note">(의도적 장애 주입으로 격리 확인)</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. 방이 여러 개인 집을 만들었는데 각 방에 열쇠가 따로 없고, 한 방 불이 나면 모든 방이 대피해야 한다면 방을 나눈 게 의미 없어요 - 이게 분산 모놀리스예요.
2. 진짜로 분리된 집이라면 한 방에 문제가 생겨도 다른 방은 계속 쓸 수 있고, 각 방을 독립적으로 수리할 수 있어야 해요.
3. 마이크로서비스를 제대로 나누려면 서비스끼리 "공용 열쇠(공유 DB)"를 없애고 각자의 자물쇠(독립 DB)를 써야 진짜 독립된 서비스가 돼요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 666 / 973

← **이전**: [537. 안티패턴: 분산 모놀리스 (Distributed Monolith) - 독립 배포 불가능한 MSA](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/537_anti_pattern_distributed_monolith/)
**다음**: [538. 이벤트 기반 아키텍처 (EDA)](/knowledge-base/studynote/04_software_engineering/11_testing_validation/538_event_driven_architecture/) →

---
