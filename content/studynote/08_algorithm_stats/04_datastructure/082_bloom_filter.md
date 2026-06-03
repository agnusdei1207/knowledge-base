+++
title = "28. 블룸 필터 (Bloom Filter)"
date = 2026-04-29

[taxonomies]
tags = ["studynote-algorithm-stats"]

[extra]
tags = ["studynote-algorithm-stats"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [블룸 필터](/knowledge-base/studynote/12_it_management/02_itsm_itil/061_bloomfilter/)([Bloom Filter](/knowledge-base/studynote/12_it_management/02_itsm_itil/061_bloomfilter/))는 원소가 집합에 속하는지를 확률적으로 판단하는 공간 효율적 자료구조다. False Positive(있다고 잘못 판단)는 가능하지만 False Negative(없다고 잘못 판단)는 절대 없다는 특성이 핵심이다.
> 2. **가치**: 거대한 집합의 멤버십 테스트를 O(k) 시간·고정 메모리로 처리한다. 해시셋 대비 수십~수백 배 메모리 절약. 브라우저 악성 URL 필터, [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 최적화, [CDN](/knowledge-base/studynote/03_network/09_application_layer_web_email/506_cdn_content_delivery_network_edge_caching/) [캐시 히트](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/263_cache_hit_miss/) 판단에 광범위하게 쓰인다.
> 3. **판단 포인트**: False Positive Rate(FPR)는 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) 크기(m)와 [해시 함수](/knowledge-base/studynote/03_network/13_network_security_basics/667_hash_function_integrity_one_way/) 수(k)로 조절한다. FPR ≈ (1 - e^(-kn/m))^k. FPR이 1%를 초과하면 사용을 재검토해야 하며, 삭제가 필요한 경우 Counting [Bloom Filter](/knowledge-base/studynote/12_it_management/02_itsm_itil/061_bloomfilter/) 변형을 사용한다.

---

## Ⅰ. 개요 및 필요성



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">블룸 필터 동작 원리</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">삽입: hash1("apple")=3, hash2("apple")=7, hash3("apple")=11</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">비트 배열:</div><div class="kb-diagram-node">0,0,0,1,0,0,0,1,0,0,0,1,0,0,0</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">조회: hash1("apple")=3 → 비트1? ✅</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">hash2("apple")=7 → 비트1? ✅</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">hash3("apple")=11 → 비트1? ✅ → "있을 수 있음"</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">False Positive: "banana"의 해시가 우연히 모두 1 → 오탐</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">False Negative: 절대 불가 (삽입된 원소 = 모든 비트 1)</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: [블룸 필터](/knowledge-base/studynote/12_it_management/02_itsm_itil/061_bloomfilter/)는 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 스탬프 시스템이다. 도서관 카드에 책 대출 이력을 여러 개의 작은 스탬프로 표시한다. 스탬프가 모두 찍혀 있으면 빌렸을 수도 있고(False Positive 가능), 하나라도 없으면 절대 빌리지 않은 것이다(False Negative 없음).

---

## Ⅱ. 아키텍처 및 핵심 원리

### 파라미터 설계

| 파라미터 | 기호 | 설명 |
|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/">비트</a> <a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/">배열</a> 크기</strong> | m | 클수록 FPR↓, 메모리↑ |
| <strong><a href="/knowledge-base/studynote/03_network/13_network_security_basics/667_hash_function_integrity_one_way/">해시 함수</a> 수</strong> | k | 최적값: k = (m/n) × ln2 |
| **원소 수** | n | 삽입 예상 원소 수 |
| **False Positive Rate** | FPR | ≈ (1-e^(-kn/m))^k |

### 변형 자료구조



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Counting Bloom Filter: 비트 → 카운터 → 삭제 가능</div>
<div class="kb-diagram-note">Scalable Bloom Filter: 자동 확장, 고정 FPR 유지</div>
<div class="kb-diagram-note">Cuckoo Filter: 삭제 지원 + FPR ≈ Bloom</div>
</div>
</div>



- **📢 섹션 요약 비유**: [블룸 필터](/knowledge-base/studynote/12_it_management/02_itsm_itil/061_bloomfilter/) 파라미터는 체(Sieve)의 구멍 크기다. 구멍이 작을수록(m↑) 불순물이 잘 걸러지지만 체가 커진다. 구멍 수가 많을수록(k↑) 더 정확하지만 처리 시간이 늘어난다.

---

## Ⅲ. 비교 및 연결

| 비교 | 해시셋 | [블룸 필터](/knowledge-base/studynote/12_it_management/02_itsm_itil/061_bloomfilter/) |
|:---|:---|:---|
| [정확성](/knowledge-base/studynote/16_bigdata/01_intro/002_bigdata_5v/) | 100% | FPR 존재 |
| 메모리 | 높음 | 매우 낮음 |
| 삭제 | ✅ | 기본형 불가 |
| 사용 사례 | [정확성](/knowledge-base/studynote/16_bigdata/01_intro/002_bigdata_5v/) 필수 | 공간 효율 우선 |

- **📢 섹션 요약 비유**: 해시셋 vs [블룸 필터](/knowledge-base/studynote/12_it_management/02_itsm_itil/061_bloomfilter/)는 고정밀 체중계 vs 체중계 저울이다. 고정밀 체중계는 정확하지만 크고 비싸며, 일반 저울은 약간의 오차가 있지만 작고 빠르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실제 사용 사례



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Chrome Safe Browsing → 악성 URL 블룸 필터 (로컬 조회 후 서버 확인)</div>
<div class="kb-diagram-note">Cassandra/HBase → SSTable 조회 전 블룸 필터로 불필요 디스크 I/O 제거</div>
<div class="kb-diagram-note">Redis → RedisBloom 모듈, 캐시 미스 방지</div>
<div class="kb-diagram-note">Akamai CDN → 원타임 URL 캐싱 여부 판단</div>
<div class="kb-diagram-note">비트코인 → 경량 클라이언트 트랜잭션 필터링</div>
</div>
</div>



- **📢 섹션 요약 비유**: [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) [블룸 필터](/knowledge-base/studynote/12_it_management/02_itsm_itil/061_bloomfilter/)는 사서의 기억이다. "이 책 있어요?"라고 물을 때 사서가 빠르게 "없어요"라고 하면 서가를 뒤질 필요가 없다. "있을 수도 있어요"라고 하면 그때 서가를 뒤진다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| **공간 효율** | 해시셋 대비 수십~수백 배 메모리 절약 |
| **속도** | O(k) 고정 시간 멤버십 테스트 |
| **확장성** | 수십억 원소도 수 MB 메모리로 처리 |

[블룸 필터](/knowledge-base/studynote/12_it_management/02_itsm_itil/061_bloomfilter/)는 빅데이터·[분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템에서 네거티브 캐시(Negative Cache)로 광범위하게 사용된다. FPR을 적절히 조절하면 디스크 I/O를 90% 이상 줄일 수 있어 [Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/)·[HBase](/knowledge-base/studynote/05_database/04_transactions_concurrency/543_hbase/) 같은 LSM 트리 기반 DB의 필수 구성 요소다.

- **📢 섹션 요약 비유**: [블룸 필터](/knowledge-base/studynote/12_it_management/02_itsm_itil/061_bloomfilter/)는 공항 보안 검색의 사전 스캐너다. 모든 사람을 정밀 검사(해시셋)하는 대신, 빠른 스캐너([블룸 필터](/knowledge-base/studynote/12_it_management/02_itsm_itil/061_bloomfilter/))로 확실히 문제없는 사람을 빠르게 통과시키고, 의심스러운 사람만 정밀 검사한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/03_network/13_network_security_basics/667_hash_function_integrity_one_way/">해시 함수</a></strong> | [블룸 필터](/knowledge-base/studynote/12_it_management/02_itsm_itil/061_bloomfilter/)의 핵심 메커니즘 |
| **False Positive** | [블룸 필터](/knowledge-base/studynote/12_it_management/02_itsm_itil/061_bloomfilter/)의 핵심 트레이드오프 |
| **LSM 트리** | [블룸 필터](/knowledge-base/studynote/12_it_management/02_itsm_itil/061_bloomfilter/) 활용 DB 엔진 |
| <strong>Counting <a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/061_bloomfilter/">Bloom Filter</a></strong> | 삭제 지원 변형 |
| **빅데이터 필터링** | 실무 적용 분야 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">기본 블룸 필터 — 비트 배열 + k개 해시 함수</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Counting Bloom Filter — 삭제 지원</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Scalable Bloom Filter — 자동 확장</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Cuckoo Filter — 삭제 + 공간 효율 개선</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">XOR Filter / Ribbon Filter — 차세대 초고효율 멤버십 필터</div></div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. [블룸 필터](/knowledge-base/studynote/12_it_management/02_itsm_itil/061_bloomfilter/)는 "이 사람 본 적 있나요?" 스탬프 시스템이에요! 스탬프가 모두 찍혀있으면 봤을 수도 있고, 하나라도 없으면 절대 못 봤던 거예요.
2. 메모리를 거의 안 써서 수십억 개의 데이터도 아주 작은 공간에서 빠르게 확인할 수 있어요!
3. Chrome이 악성 사이트 차단, [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)가 불필요한 검색 줄이기 등 여기저기서 사용한답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 82 / 175

← **이전**: [27. 스파스 테이블 (Sparse Table) — 정적 RMQ 최적 자료구조](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/081_sparse_table/)
**다음**: [28. 우선순위 큐 (Priority Queue)](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/083_priority_queue/) →

---
