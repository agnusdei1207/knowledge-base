+++
title = "142. 스키마리스 설계 패턴 (Schemaless Design Patterns) — 임베딩 vs 참조"
date = 2026-04-21

[taxonomies]
tags = ["studynote-bigdata"]

[extra]
tags = ["studynote-bigdata"]
+++

## 핵심 인사이트 (3줄 요약)
- **본질**: [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)리스(Schemaless)는 "[스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)가 없음"이 아니라 "[스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)가 애플리케이션 코드에 있음"으로, [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/)링의 책임이 DB에서 애플리케이션으로 이동한 것이다.
- **가치**: [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/)(비정규화)과 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)([정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/))의 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)적 조합으로 특정 접근 패턴에 최적화된 [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/)을 구성하면, RDBMS [JOIN](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/) 비용 없이 단일 조회로 필요한 모든 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 가져올 수 있다.
- **판단 포인트**: 설계 원칙은 "접근 패턴(Query Pattern)으로 설계하고, 엔티티 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)로 설계하지 말라"로, 가장 빈번한 읽기 패턴에 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 비정규화하여 정렬하는 것이 [NoSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/035_nosql/) 모델링의 핵심이다.

---

## Ⅰ. 개요 및 필요성

### [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)리스의 실제 의미

```text
RDBMS 스키마 변경 흐름:
  1. ALTER TABLE 계획
  2. DBA 검토 및 승인
  3. 야간 유지보수 시간 확보
  4. 데이터 마이그레이션 실행 (수시간~수일)
  5. 애플리케이션 코드 배포

NoSQL 스키마 변경 흐름:
  1. 애플리케이션 코드에서 새 필드 추가
  2. 즉시 배포

단, 스키마 검증(validation)은 애플리케이션이 수행:
  - 타입 검사, 필수 필드 확인 → 앱 코드 책임
  - MongoDB: JSON Schema Validation으로 서버 측 강제 가능
```

### 접근 패턴 우선 설계 원칙



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">잘못된 설계 방식 (엔티티 중심):</div>
<div class="kb-diagram-note">"주문과 고객이 있으니 orders, customers 테이블을 만들자"</div>
<div class="kb-diagram-note">→ JOIN이 필요한 쿼리 발생</div>
<div class="kb-diagram-note">올바른 설계 방식 (접근 패턴 중심):</div>
<div class="kb-diagram-note">Q1: "주문 상세 페이지에서 무엇을 보여줄 것인가?"</div>
<div class="kb-diagram-note">→ 주문 + 고객 이름 + 주문 상품 목록이 필요</div>
<div class="kb-diagram-note">→ 하나의 orders 문서에 모두 임베딩</div>
<div class="kb-diagram-note">Q2: "고객 프로필 수정이 주문 내역에도 반영되어야 하는가?"</div>
<div class="kb-diagram-note">→ 반드시 → 참조 전략 사용 (또는 Extended Reference 패턴)</div>
</div>
</div>



📢 **섹션 요약 비유**
> [NoSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/035_nosql/) [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)리스 설계는 맞춤 양복과 같다. 기성품(RDBMS [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/))은 어느 몸에나 맞지만 완벽하지 않고, 맞춤 양복(접근 패턴 기반 설계)은 특정 사람(워크로드)에게 최적이지만 다른 사람이 입기엔 맞지 않을 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) vs [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) 결정 매트릭스



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">임베딩 vs 참조 선택 기준</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">임베딩(Embedding) 선호:</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">✅ "자식은 부모 없이 독립적으로 의미 없음"</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(주문 없는 주문 상품이 존재하지 않음)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">✅ "항상 함께 조회"</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(주문 페이지에서 항상 상품 목록도 표시)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">✅ "자식 수가 제한적이고 예측 가능"</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(최대 100개 리뷰 → 하나의 문서에 ok)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">✅ "원자적 업데이트 필요"</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(주문 상태와 배송 추적을 동시에 업데이트)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">참조(Referencing) 선호:</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">✅ "자식이 독립적으로 의미 있음"</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(상품은 여러 주문에서 참조, 독립 수정 가능)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">✅ "동일 데이터를 여러 문서에서 공유"</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(동일 사용자 정보가 수천 개 주문에서 참조)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">✅ "자식 수가 무한정 증가 가능"</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(소셜 포스트의 댓글이 수만 개)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">✅ "자식 데이터만 독립적으로 쿼리"</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(최근 댓글 10개만 페이지네이션)</div></div>
</div>
</div>



### [MongoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/540_mongodb/) 고급 설계 패턴 ([Design Patterns](/knowledge-base/studynote/04_software_engineering/04_testing_quality/251_design_patterns_gof_overview/))



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1. 버킷 패턴 (Bucket Pattern) — IoT 시계열</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">문제: 센서가 초당 1개 문서 → 시간당 3600개 문서</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">해결: 1시간 분량을 하나의 버킷 문서에 배열로 저장</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">{ sensorId: "S1",</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">hour: "2026-04-21T09:00:00",</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">readings:</div><div class="kb-diagram-node">23.5, 23.7, 23.6, ...</div><div class="kb-diagram-note">, // 3600개 임베딩</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">count: 3600, avg: 23.6, min: 22.1, max: 24.0 }</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">효과: 문서 수 3600 → 1 (99.97% 감소), 집계 필드 포함</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2. 아웃라이어 패턴 (Outlier Pattern) — 소수의 예외 처리</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">문제: 일반 영화는 리뷰 수백 개, 블록버스터는 수백만 개</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">해결: has_extras 플래그 + 오버플로우 문서</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">{ movieId: "avatar", reviews:</div><div class="kb-diagram-node">...첫 1000개</div><div class="kb-diagram-note">,</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">has_extras: true }</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">{ movieId: "avatar", extras_page: 2,</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">reviews:</div><div class="kb-diagram-node">...다음 1000개</div><div class="kb-diagram-note">}</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">3. 계산된 패턴 (Computed Pattern) — 집계 캐싱</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">문제: 상품 평점 평균을 매번 리뷰 전체 집계로 계산</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">해결: 문서에 계산된 값을 미리 저장</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">{ productId: "P1",</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">review_count: 1500,</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">rating_sum: 6750,</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">avg_rating: 4.5 } // 쓸 때 계산, 읽을 때 즉시 반환</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">4. 확장 참조 패턴 (Extended Reference Pattern)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">문제: 주문에서 고객 이름이 항상 필요한데 매번 JOIN 시 느림</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">해결: 자주 쓰는 필드를 참조하는 문서에 복사</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">{ orderId: "O1",</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">customerId: "C1", // 참조 (ID)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">customerName: "홍길동", // 복사 (비정규화)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">customerPhone: "010-xxxx" // 복사 (자주 쓰는 것만)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">}</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">고객 이름 변경 시 → customerId로 최신 정보 조회 + 주문 이력</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">은 당시 이름 유지 (실제 비즈니스 요구와 일치)</div></div>
</div>
</div>



### 다형성 패턴 (Polymorphic Pattern)

```text
문제: 상품이 의류·전자기기·식품으로 각기 다른 속성을 가짐
      RDBMS: 30개 NULL 컬럼 or EAV 패턴의 복잡성

MongoDB 해결: 같은 컬렉션에 다른 구조 허용
  { _id: "P1", type: "clothing",
    size: ["S","M","L"], color: "red" }
  { _id: "P2", type: "electronics",
    voltage: 220, warranty_months: 24 }
  { _id: "P3", type: "food",
    expiry: "2026-12", allergens: ["nuts"] }

공통 인덱스: type, name, price
타입별 인덱스: type="clothing" 필터 인덱스
```

📢 **섹션 요약 비유**
> 버킷 패턴은 장보기 영수증 관리와 같다. 매번 산 물건을 낱장 영수증(각 문서)으로 보관하면 서랍이 가득 차지만, 한 달치를 봉투(버킷 문서)에 모아두면 훨씬 관리가 쉽고 월 지출 합계도 봉투에 미리 적어두면 바로 알 수 있다.

---

## Ⅲ. 비교 및 연결

### 전체 설계 패턴 요약 테이블

| 패턴 | 문제 | 해결 | 트레이드오프 |
|:---:|:---:|:---|:---:|
| <strong><a href="/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/">임베딩</a></strong> | [JOIN](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/) 비용 | 관련 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 한 문서에 | 중복, 큰 문서 |
| <strong><a href="/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/">참조</a></strong> | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 중복 | ID로만 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) | 추가 조회 필요 |
| **버킷** | 문서 폭발 | 시간/범위로 묶음 | 문서 설계 복잡 |
| **아웃라이어** | 소수 예외 처리 | [플래그](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/) + [오버플로우](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/095_overflow/) | 앱 로직 복잡 |
| **계산된** | 집계 반복 계산 | 미리 계산 저장 | [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 오버헤드 |
| <strong>확장 <a href="/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/">참조</a></strong> | 반복 [JOIN](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/) | 자주 쓰는 필드 복사 | [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 비용 |
| **다형성** | 타입별 다른 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) | 같은 컬렉션, 다른 구조 | 타입 관리 |

### 문서 크기 제한과 청크 패턴

```text
MongoDB 문서 크기 제한: 16MB

대용량 데이터 처리:
  GridFS: 청크로 나눠 binary 파일 저장 (이미지·동영상)
  청크 패턴: 데이터를 여러 문서로 분할, 공통 시퀀스 키로 연결

  { orderId: "O1", page: 1, items: [...처음 100개...] }
  { orderId: "O1", page: 2, items: [...다음 100개...] }
```

📢 **섹션 요약 비유**
> 계산된 패턴은 쇼핑몰의 베스트셀러 랭킹 게시판과 같다. 손님이 올 때마다 모든 판매 기록을 헤아리는 대신(실시간 집계), 이미 계산된 순위표(계산된 필드)를 보여주고 판매가 일어날 때마다 순위표를 갱신한다([쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 시 계산). 읽기가 10만 배 빠른 대신 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)가 약간 더 걸린다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 전자상거래 플랫폼 [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/) 설계 예시



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">설계 과정:</div>
<div class="kb-diagram-note">STEP 1: 핵심 접근 패턴 정의</div>
<div class="kb-diagram-note">Q1. 상품 상세 페이지 조회 (초당 수천 번)</div>
<div class="kb-diagram-note">Q2. 주문 내역 조회 (사용자별, 시간 역순)</div>
<div class="kb-diagram-note">Q3. 카테고리별 상품 목록 (필터·정렬)</div>
<div class="kb-diagram-note">Q4. 리뷰 조회 (상품별, 최근 20개)</div>
<div class="kb-diagram-note">STEP 2: 컬렉션·임베딩·참조 결정</div>
<div class="kb-diagram-note">products 컬렉션:</div>
<div class="kb-diagram-note">+ 기본 정보, 가격, 재고 → 임베딩</div>
<div class="kb-diagram-note">+ 카테고리 → 참조 (카테고리 독립 수정)</div>
<div class="kb-diagram-note">+ 평균 평점, 리뷰 수 → 계산된 필드 임베딩</div>
<div class="kb-diagram-note">+ 리뷰 전체 → 별도 컬렉션 참조 (무한 증가)</div>
<div class="kb-diagram-note">orders 컬렉션:</div>
<div class="kb-diagram-note">+ 주문자 이름/연락처 → 확장 참조 (당시 정보 보존)</div>
<div class="kb-diagram-note">+ 주문 상품 목록 (qty, price, name) → 임베딩 (당시 가격 보존)</div>
<div class="kb-diagram-note">+ 배송 상태 이력 → 임베딩 (함께 조회)</div>
</div>
</div>



### [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리 패턴

```text
스키마 진화(Schema Evolution) 처리:

{ _id: "P1",
  schema_version: 2,   // 버전 필드 추가
  name: "키보드",
  price: 89000
  // v2 추가 필드:
  tags: ["mechanical", "wireless"]
}

앱 코드:
  if doc.schema_version == 1:
    doc = migrate_v1_to_v2(doc)
    db.save(doc)  // 읽을 때 마이그레이션 (Lazy Migration)
```

📢 **섹션 요약 비유**
> [Lazy](/knowledge-base/studynote/06_ict_convergence/05_data_science/380_computational_graph_lazy_eager_execution/) Migration은 도서관 책 재분류와 같다. 모든 책을 한꺼번에 재분류(빅뱅 마이그레이션)하면 도서관 문을 닫아야 하지만, 손님이 대출할 때마다 새 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 체계로 이동([Lazy](/knowledge-base/studynote/06_ict_convergence/05_data_science/380_computational_graph_lazy_eager_execution/) Migration)하면 도서관은 계속 운영하면서 서서히 완전히 이전된다.

---

## Ⅴ. 기대효과 및 결론

### [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)리스 설계의 정량적 효과

| 항목 | RDBMS [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) | [NoSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/035_nosql/) 접근 패턴 설계 | 개선 |
|:---:|:---:|:---:|:---:|
| 상품 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 조회 | 8개 테이블 [JOIN](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/) | 1개 문서 조회 | 5~10배 빠름 |
| [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 변경 | 수시간 다운타임 | 즉시 ([Lazy](/knowledge-base/studynote/06_ict_convergence/05_data_science/380_computational_graph_lazy_eager_execution/) 마이그레이션) | 개발 민첩성 |
| 주문 이력 보존 | 최신 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 반영 | 주문 당시 가격 보존 | 비즈니스 [정확성](/knowledge-base/studynote/16_bigdata/01_intro/002_bigdata_5v/) |
| 저장 공간 | [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) 최소 | 비정규화 약간 증가 | [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 우선 |

### 결론
[스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)리스 설계는 자유가 아니라 책임의 이동이다. 접근 패턴 분석 → [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/)/[참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) 결정 → 고급 패턴(버킷·계산된·확장 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)) 적용의 단계적 설계 방법론을 따르면, RDBMS가 할 수 없는 수준의 읽기 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 최적화가 가능하다. 기술사 시험에서는 <strong><a href="/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/">임베딩</a> vs <a href="/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/">참조</a> 선택 기준</strong>, <strong>버킷 패턴의 <a href="/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/">IoT</a> 적용</strong>, **계산된 패턴의 읽기 최적화 원리**, <strong>확장 <a href="/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/">참조</a> 패턴의 설계 의도</strong>가 핵심 논점이다.

📢 **섹션 요약 비유**
> [NoSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/035_nosql/) [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)리스 설계를 [마스](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)터한 개발자는 뷔페 요리사와 같다. 손님([쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 패턴)이 원하는 음식을 미리 예측해서 이미 조리해둔다([임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/)). 주문이 들어올 때마다 처음부터 요리하는 식당([JOIN](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/) [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/))과 달리, 이미 준비된 음식을 그릇에 담기만 하면 된다. 단, 메뉴를 잘못 예측하면 음식을 버려야 한다(비정규화 비용).

---

### 📌 관련 개념 맵

| 개념 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---:|:---:|:---|
| 비정규화 | 핵심 원칙 | 읽기 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 위한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 중복 허용 |
| 접근 패턴 | 설계 기준 | [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 기반 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 설계 |
| [JSON](/knowledge-base/studynote/11_design_supervision/06_exam_summary/343_json/) [Schema](/knowledge-base/studynote/05_database/04_transactions_concurrency/505_schema/) | 유효성 검사 | [MongoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/540_mongodb/) 서버 측 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 강제 |
| [Lazy](/knowledge-base/studynote/06_ict_convergence/05_data_science/380_computational_graph_lazy_eager_execution/) Migration | [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리 | 읽기 시 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 업그레이드 |
| GridFS | 대용량 처리 | [MongoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/540_mongodb/) 16MB 초과 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 청크 저장 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">관계형 DB (RDBMS) — 엄격한 스키마 사전 정의 필수</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">NoSQL 등장 — 스키마리스, 수평 확장, 다양한 데이터 모델 지원</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">스키마리스 설계 패턴 — 문서(Document) / 컬럼(Column) / 그래프(Graph) 모델</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Schema-on-Read — 저장 시 자유, 조회 시 스키마 적용 (데이터 레이크 철학)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">하이브리드 접근 — HTAP(OLTP+OLAP 혼합) 및 NewSQL로 스키마 유연성+ACID 양립</div></div>
</div>
</div>


[관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 DB의 엄격한 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 제약을 NoSQL이 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)리스 패턴으로 극복했고, [Schema-on-Read](/knowledge-base/studynote/14_data_engineering/01_infrastructure/009_schema_on_read/) 철학과 NewSQL의 등장으로 유연성과 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)을 동시에 추구하고 있다.

### 👶 어린이를 위한 3줄 비유 설명
1. [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)리스는 "자유 일기장"처럼 형식이 없는 게 아니라, 형식을 내가 직접 정해야 한다는 것 — 더 자유롭지만 더 많은 책임이 있어요.
2. [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/)은 도시락에 밥·반찬을 모두 담는 것(한 번에 꺼낼 수 있음), [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)는 밥과 반찬을 각각 다른 통에 넣는 것(각자 다른 사람이 먹을 수 있음)이에요.
3. 버킷 패턴은 매일 소액 동전들을 저금통에 모아두다가 주기적으로 은행에 가는 것 — 매번 은행을 가는(개별 문서) 대신 모아서(버킷) 한 번에 처리해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 142 / 262

← **이전**: [141. 멀티 마스터 복제 (Multi-Master Replication) — CouchDB/DynamoDB Global Tables](/knowledge-base/studynote/16_bigdata/06_nosql/141_multi_master_replication/)
**다음**: [데이터 레이크 (Data Lake)](/knowledge-base/studynote/16_bigdata/07_data_lake/143_data_lake/) →

---
