---
title: 702. 다중 스트림 쓰기 (Multi-stream Write)
date: '2026-05-08'
tags:
- studynote-computer-architecture
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[560_multi_stream_file_fork_ads|다중 스트림]] [[289_cqrs_db|쓰기]] ([[560_multi_stream_file_fork_ads|Multi-stream]] Write)는 [[327_ssd|SSD]] ([[327_ssd|Solid State Drive]])에 기록되는 [[001_dikw_pyramid|데이터]]를 "[[501_file_definition_logical_record|파일]] 종류"가 아니라 "예상 수명" 기준으로 구분해 배치하도록 호스트가 [[167_sql_hint_optimizer_override|힌트]]를 주는 기술이다.
> 2. **가치**: 자주 지워질 [[001_dikw_pyramid|데이터]]와 오래 남을 [[001_dikw_pyramid|데이터]]를 같은 블록에 섞지 않게 해 [[380_garbage_collection|가비지 컬렉션]] 부담과 [[289_cqrs_db|쓰기]] 증폭을 줄인다.
> 3. **판단 포인트**: 스트림을 많이 만든다고 무조건 좋아지는 것이 아니며, 수명이 비슷한 [[001_dikw_pyramid|데이터]]만 소수의 안정된 그룹으로 [[104_classification_analysis|분류]]할 때 효과가 크다.

---

## Ⅰ. 개요 및 필요성

[[560_multi_stream_file_fork_ads|다중 스트림]] [[289_cqrs_db|쓰기]] ([[560_multi_stream_file_fork_ads|Multi-stream]] Write)는 호스트가 [[001_dikw_pyramid|데이터]]의 예상 생존 기간을 알려 주고, SSD가 그 [[167_sql_hint_optimizer_override|힌트]]를 바탕으로 비슷한 수명의 [[001_dikw_pyramid|데이터]]를 같은 물리 블록 쪽에 모아 쓰도록 유도하는 기법이다. 핵심은 저장 위치를 세밀하게 직접 지정하는 것이 아니라, [[001_dikw_pyramid|데이터]]의 "온도"를 알려 주어 컨트롤러의 배치 결정을 돕는 데 있다.

이 기술이 필요한 이유는 낸드 플래시가 [[286_page_frame|페이지]] 단위로 쓰고 블록 단위로 지우는 구조이기 때문이다. 예를 들어 10분 뒤 사라질 임시 [[568_logs_distributed_logging_elk_fluentd|로그]]와 3년간 남을 [[555_backup_and_restore_strategy|백업]] 메타데이터가 같은 블록에 섞여 있으면, 짧은 [[001_dikw_pyramid|데이터]]가 먼저 무효화될 때 SSD는 살아남은 긴 [[001_dikw_pyramid|데이터]]를 다른 곳으로 복사한 뒤 블록 전체를 지워야 한다. 이 과정이 반복되면 [[696_waf_web_application_firewall|WAF]] ([[480_write_amplification|Write Amplification]] Factor)가 올라가고, GC ([[380_garbage_collection|Garbage Collection]])가 배경에서 더 자주 돌며 [[141_latency|지연 시간]]도 흔들린다.

문제는 [[327_ssd|SSD]] 내부의 [[478_ftl_flash_translation_layer|FTL]] ([[478_ftl_flash_translation_layer|Flash Translation Layer]])이 [[001_dikw_pyramid|데이터]]의 "의미"를 모른다는 점이다. 컨트롤러는 주소와 접근 패턴은 보지만, 이 [[289_cqrs_db|쓰기]]가 곧 지워질 캐시인지 오래 남을 사용자 [[001_dikw_pyramid|데이터]]인지는 호스트가 더 잘 안다. [[560_multi_stream_file_fork_ads|다중 스트림]] [[289_cqrs_db|쓰기]]는 이 정보 비대칭을 줄여, 호스트가 알고 있는 수명 정보를 저장 장치가 활용하게 만든다.

- **📢 섹션 요약 비유**: [[560_multi_stream_file_fork_ads|다중 스트림]] [[289_cqrs_db|쓰기]]는 냉장고 정리와 같다. 오늘 먹을 반찬과 몇 달 보관할 냉동식품을 한 칸에 섞어 넣으면, 짧게 둘 음식 때문에 긴 보관 음식까지 계속 꺼내 옮겨야 한다.

---

## Ⅱ. 동작 원리와 배치 방식

[[560_multi_stream_file_fork_ads|다중 스트림]] [[289_cqrs_db|쓰기]]의 핵심 절차는 단순하다. 호스트는 [[289_cqrs_db|쓰기]] 요청마다 "이 [[001_dikw_pyramid|데이터]]는 얼마나 오래 살아남을 가능성이 큰가"를 나타내는 스트림 번호나 [[289_cqrs_db|쓰기]] 수명 [[167_sql_hint_optimizer_override|힌트]]를 함께 보낸다. 그러면 [[327_ssd|SSD]] 컨트롤러는 같은 [[167_sql_hint_optimizer_override|힌트]]를 받은 [[001_dikw_pyramid|데이터]]끼리 비슷한 [[289_cqrs_db|쓰기]] 전선을 유지하며 기록한다. 결과적으로 무효화 시점이 비슷한 [[286_page_frame|페이지]]들이 한 블록에 모이고, 나중에 블록 회수도 한꺼번에 쉬워진다.

| 단계 | 호스트 역할 | [[327_ssd|SSD]] 역할 | 기대 효과 |
| :--- | :--- | :--- | :--- |
| [[104_classification_analysis|분류]] | 임시·[[568_logs_distributed_logging_elk_fluentd|로그]]·장기보관 [[001_dikw_pyramid|데이터]] 구분 | 스트림별 [[289_cqrs_db|쓰기]] 큐 유지 | 서로 다른 수명 [[001_dikw_pyramid|데이터]] 분리 |
| 기록 | 스트림 [[167_sql_hint_optimizer_override|힌트]]와 함께 [[289_cqrs_db|쓰기]] 전송 | 같은 스트림 블록에 우선 배치 | 블록 내부 수명 일치도 상승 |
| 회수 | 별도 동작 없음 | 무효 [[286_page_frame|페이지]]가 많은 스트림 블록 정리 | 복사량과 지우기 횟수 감소 |

아래 그림은 혼합 기록과 스트림 분리 기록의 차이를 보여준다.

```text
┌──────────────────────────────────────────────────────────────┐
│              Mixed placement vs stream-aware placement      │
├──────────────────────────────────────────────────────────────┤
│ Legacy block                     Stream-aware blocks         │
│ [Hot][Cold][Hot][Cold]           [Hot][Hot][Hot][Hot]       │
│        │                         [Cold][Cold][Cold][Cold]   │
│        └─ Hot data dies early    Reclaim hot block at once  │
│           => copy cold pages     Keep cold block untouched   │
└──────────────────────────────────────────────────────────────┘
```

현실적으로는 스트림 수가 무한하지 않다. 많은 장치가 동시에 잘 처리할 수 있는 활성 스트림 수는 제한적이며, 스트림마다 열어 둬야 하는 블록과 메타데이터가 늘어난다. 그래서 보통은 임시 [[001_dikw_pyramid|데이터]], [[568_logs_distributed_logging_elk_fluentd|로그]]성 [[001_dikw_pyramid|데이터]], 장기 보관 [[001_dikw_pyramid|데이터]]처럼 3~5개 정도의 굵은 수명 그룹으로 나누는 편이 효과적이다.

- **📢 섹션 요약 비유**: 택배 상자를 "당일 폐기", "이번 주 사용", "장기 보관" 정도로만 나눠도 창고 정리가 훨씬 쉬워진다. 반대로 상자마다 세부 꼬리표를 너무 많이 붙이면 창고 관리가 더 복잡해진다.

---

## Ⅲ. 일반 [[289_cqrs_db|쓰기]]·존 기반 SSD와의 비교 및 연결

[[560_multi_stream_file_fork_ads|다중 스트림]] [[289_cqrs_db|쓰기]]는 SSD가 모든 배치를 알아서 하던 기본 방식과, 호스트가 훨씬 더 큰 책임을 지는 [[703_zns_ssd|ZNS]] ([[703_zns_ssd|Zoned Namespace]]) [[327_ssd|SSD]] 사이의 중간 지점에 있다. 기본 방식에서는 장치가 [[001_dikw_pyramid|데이터]]를 알아서 섞어 쓰고, ZNS에서는 호스트가 존 단위의 순차 기록 규칙까지 맞춰야 한다. [[560_multi_stream_file_fork_ads|다중 스트림]] [[289_cqrs_db|쓰기]]는 그 중간에서 "배치 [[167_sql_hint_optimizer_override|힌트]]는 주되 세부 배치는 장치가 맡는" 절충안이다.

| 구분 | 기본 [[327_ssd|SSD]] [[289_cqrs_db|쓰기]] | [[560_multi_stream_file_fork_ads|다중 스트림]] [[289_cqrs_db|쓰기]] | [[703_zns_ssd|ZNS SSD]] |
| :--- | :--- | :--- | :--- |
| 호스트 책임 | 거의 없음 | 수명 [[167_sql_hint_optimizer_override|힌트]] 제공 | 존 단위 배치와 정리 주도 |
| 장치 자유도 | 매우 높음 | [[167_sql_hint_optimizer_override|힌트]] 범위 안에서 높음 | 순차 [[289_cqrs_db|쓰기]] 규칙으로 제한 |
| 소프트웨어 변경량 | 작음 | 중간 | 큼 |
| 기대 효과 | 범용성 우수 | 수명 분리 최적화 | 최대 수준의 배치 제어 |

또한 이 기술은 [[377_lsm_tree_storage_engine|LSM-Tree]] ([[221_lsm_tree_memtable_sequential_flush_compaction|Log-Structured Merge-Tree]]) 기반 [[002_database_definition|데이터베이스]]와 궁합이 좋다. 선행 기록 [[568_logs_distributed_logging_elk_fluentd|로그]], [[494_memtable_sstable_flush|멤테이블]] 플러시 결과, [[347_compaction|압축]] 완료 [[501_file_definition_logical_record|파일]]은 수명이 다르므로 별도 스트림으로 나누기 쉽다. 반대로 이미 완전한 순차 적재 구조로 동작하는 워크로드에서는 추가 이득이 제한될 수 있다.

즉, [[560_multi_stream_file_fork_ads|다중 스트림]] [[289_cqrs_db|쓰기]]는 "장치가 다 알아서 해 주길 원하지만, 최소한 [[001_dikw_pyramid|데이터]] 수명 정도는 알려 줄 수 있다"는 환경에 잘 맞는다. 이 때문에 기존 [[501_file_definition_logical_record|파일]] 시스템과 응용 구조를 크게 바꾸지 않으면서도 플래시 친화적 최적화를 끼워 넣을 수 있다.

- **📢 섹션 요약 비유**: 기본 SSD가 "창고 직원 마음대로 적재"라면, ZNS는 "어디에 어떻게 쌓을지 주인이 직접 지시"하는 방식이다. [[560_multi_stream_file_fork_ads|다중 스트림]] [[289_cqrs_db|쓰기]]는 그 사이에서 "이 상자들은 비슷한 날 버려질 물건이니 같이 둬 주세요"라고 알려 주는 수준이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 스트림을 애플리케이션 이름으로 나누기보다 [[001_dikw_pyramid|데이터]] 수명으로 나누는 것이 중요하다. 예를 들어 [[002_database_definition|데이터베이스]]라면 선행 기록 [[568_logs_distributed_logging_elk_fluentd|로그]], 일시적 정렬 결과, 오래 유지되는 [[001_dikw_pyramid|데이터]] [[501_file_definition_logical_record|파일]]을 각각 다른 스트림으로 보는 편이 낫다. 같은 [[090_service_kubernetes_network_load_balancing|서비스]]에서 나온 [[001_dikw_pyramid|데이터]]라도 지워지는 시점이 다르면 분리해야 하고, 반대로 다른 [[090_service_kubernetes_network_load_balancing|서비스]] [[001_dikw_pyramid|데이터]]라도 수명이 비슷하면 같은 스트림에 넣을 수 있다.

### 적용 [[435_checklist_based_testing|체크리스트]]

1. 장치가 지원하는 활성 스트림 수를 먼저 확인한다.
2. 스트림은 기능 [[104_classification_analysis|분류]]가 아니라 수명 [[104_classification_analysis|분류]] 기준으로 잡는다.
3. 짧게 사라지는 [[001_dikw_pyramid|데이터]]와 오래 남는 [[001_dikw_pyramid|데이터]]를 가장 먼저 분리한다.
4. 효과는 [[696_waf_web_application_firewall|WAF]], [[141_latency|지연 시간]] [[136_variance|분산]], [[327_ssd|SSD]] 마모 지표로 [[395_verification_process_review|검증]]한다.

### 대표 [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 스트림을 테이블별·고객별로 과도하게 늘려 블록 파편화만 키우는 설계
- 실제로는 자주 갱신되는 [[001_dikw_pyramid|데이터]]를 "장기 보관" 스트림에 넣어 예측을 망치는 설계
- 장치가 [[167_sql_hint_optimizer_override|힌트]]를 완벽히 보장한다고 믿고 [[395_verification_process_review|검증]] 없이 적용하는 운영 방식

실무 판단의 핵심은 "[[104_classification_analysis|분류]] 비용보다 회수 이득이 큰가"다. [[568_logs_distributed_logging_elk_fluentd|로그]] 구조 [[002_database_definition|데이터베이스]], 분석 파이프라인의 임시 산출물, 객체 저장소의 메타데이터처럼 수명 차이가 분명한 워크로드는 채택 가치가 높다. 반면 [[001_dikw_pyramid|데이터]] 수명이 고르게 섞여 있거나 장치 지원이 약한 환경에서는 기대 효과가 작을 수 있다.

- **📢 섹션 요약 비유**: 옷장을 정리할 때 계절별로 나누면 편하지만, 옷 한 벌마다 칸을 따로 만들면 오히려 옷장을 더 엉망으로 만든다. [[104_classification_analysis|분류]]는 적당히 굵고 의미 있게 해야 한다.

---

## Ⅴ. 기대효과 및 결론

[[560_multi_stream_file_fork_ads|다중 스트림]] [[289_cqrs_db|쓰기]]의 가장 큰 효과는 블록 회수 시점의 정렬이다. 비슷한 수명의 [[001_dikw_pyramid|데이터]]가 한곳에 모이면 살아 있는 [[286_page_frame|페이지]]를 다른 블록으로 옮기는 복사량이 줄고, 그만큼 WAF가 낮아진다. 이는 [[327_ssd|SSD]] 수명 연장, 배경 GC 감소, 테일 레이턴시 완화로 이어진다.

하지만 이 기술은 어디까지나 [[167_sql_hint_optimizer_override|힌트]] 기반이다. 컨트롤러 구현에 따라 효과 차이가 있고, 호스트가 잘못 [[104_classification_analysis|분류]]하면 오히려 빈 블록 관리가 어려워질 수 있다. 따라서 [[560_multi_stream_file_fork_ads|다중 스트림]] [[289_cqrs_db|쓰기]]는 "마법의 [[282_performance_tactics|성능]] 옵션"이 아니라, [[001_dikw_pyramid|데이터]] 수명 정보를 알고 있는 소프트웨어와 플래시 제약을 가진 저장 장치 사이의 가벼운 협약으로 이해하는 편이 정확하다.

결론적으로 [[560_multi_stream_file_fork_ads|다중 스트림]] [[289_cqrs_db|쓰기]]는 [[327_ssd|SSD]] 내부를 호스트가 완전히 통제하지 않으면서도, 최소한의 의미 정보를 전달해 저장 효율을 끌어올리는 현실적인 타협안이다. 플래시의 물리 제약을 무시하지 않되, 기존 소프트웨어를 전면 개조하지 않고 개선하고 싶을 때 특히 유효하다.

- **📢 섹션 요약 비유**: [[560_multi_stream_file_fork_ads|다중 스트림]] [[289_cqrs_db|쓰기]]는 이삿짐 박스에 "금방 풀 것"과 "창고에 오래 둘 것" 스티커를 붙이는 일이다. 기사님이 집 구조를 다 알 필요는 없지만, 이 스티커만으로도 짐 정리가 훨씬 쉬워진다.

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[696_waf_web_application_firewall|WAF]] | 스트림 분리 효과를 가장 직접적으로 보여 주는 수명·효율 지표다. |
| GC | 비슷한 수명의 블록을 회수하기 쉬워져 배경 정리 부담이 줄어든다. |
| [[478_ftl_flash_translation_layer|FTL]] | 호스트가 준 수명 [[167_sql_hint_optimizer_override|힌트]]를 실제 블록 배치에 반영하는 [[327_ssd|SSD]] 내부 계층이다. |
| [[289_cqrs_db|쓰기]] 수명 [[167_sql_hint_optimizer_override|힌트]] | 호스트가 [[001_dikw_pyramid|데이터]] 온도를 전달하는 핵심 입력값이다. |
| [[377_lsm_tree_storage_engine|LSM-Tree]] | 수명 차이가 뚜렷한 [[501_file_definition_logical_record|파일]] 계층을 만들어 스트림 분리와 잘 맞는다. |

### 📈 관련 키워드 및 발전 흐름도

```text
혼합 수명 데이터 기록
    │
    ▼
블록 내부 온도 혼합
    │
    ▼
GC 증가 · WAF 상승
    │
    ▼
쓰기 수명 힌트 제공
    │
    ▼
스트림 분리 배치 · 마모 완화
```

이 흐름은 "플래시의 숨은 정리 비용"을 호스트 [[167_sql_hint_optimizer_override|힌트]]로 줄여 가는 사고방식을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 금방 버릴 장난감 종이와 오래 보관할 그림책을 한 상자에 넣으면 정리할 때 힘들어.
2. 그래서 비슷한 것끼리 다른 상자에 넣어 두면 버릴 때 한 상자만 치우면 돼.
3. [[560_multi_stream_file_fork_ads|다중 스트림]] [[289_cqrs_db|쓰기]]는 컴퓨터가 이런 상자 [[104_classification_analysis|분류]]표를 SSD에게 알려 주는 방법이야.
