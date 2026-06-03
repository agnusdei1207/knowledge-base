+++
title = "294. 점유 대기 부정 (Deny Hold And Wait)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [교착 상태 예방](/knowledge-base/studynote/02_operating_system/05_deadlock/292_deadlock_prevention/) 중 '[점유 대기](/knowledge-base/studynote/02_operating_system/04_synchronization/231_hold_and_wait/) 부정 (Deny [Hold-and-Wait](/knowledge-base/studynote/02_operating_system/05_deadlock/284_hold_and_wait/))' 모델은, 프로세스가 특정 자원을 보유한(Hold) 채 다른 여분의 퍼즐 조각 자원(Wait)을 가져오려 욕심부리는 걸 시스템 강제로 끊어내어 "한 번에 다 쥐게 하거나, 모두 포기시켜 빈손으로 다시 줍게 만드는(All-Or-Nothing)" 할당 철학이다.
> 2. **가치**: "내가 쥔 것을 안 놓고 버티며 남의 것을 노리는" 교차 폭발 지점을 원천 소멸시키므로, 상대방 스레드가 대기 순환 고리([Circular Wait](/knowledge-base/studynote/02_operating_system/05_deadlock/286_circular_wait/))로 얽혀 들어가는 것을 물리적으로 완전 차단한다.
> 3. **융합**: 하지만 시작할 때 모든 자원을 미리 독점하는 `사전 선점 방식`은 자원의 낭비(Low Utilization)를 극대화하고, 자원을 다 못 모으면 계속 반납 재시도해야 하는 `순차 포기 방식`은 무한 양보에 빠지는 [기아 상태](/knowledge-base/studynote/02_operating_system/05_deadlock/314_starvation_prevention/)([Starvation](/knowledge-base/studynote/02_operating_system/05_deadlock/314_starvation_prevention/))를 유발하므로 실무에선 `tryLock()` 백오프 제한 외에는 도태되었다.

---

## Ⅰ. 개요 및 필요성

두루마리 휴지 하나와 비누 하나가 있어야만 씻고 나올 수 있는 두 사람이 있다. 
A는 비누를, B는 휴지를 끝끝내 손에 꼭 쥐고 놔주질 않으니 하염없는 데드락([교착 상태](/knowledge-base/studynote/02_operating_system/05_deadlock/281_deadlock_definition/))에 빠졌다. 

데드락 예방을 위한 <strong><a href="/knowledge-base/studynote/02_operating_system/04_synchronization/231_hold_and_wait/">점유 대기</a>(<a href="/knowledge-base/studynote/02_operating_system/05_deadlock/284_hold_and_wait/">Hold-and-Wait</a>) 부정 <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a></strong>은 아주 시원하게 이 꼬라지를 박살 낸다. 
1. **사전 일괄 획득 (Pre-allocation)**: "샤워실 들어가기 전 바깥 거실에서 휴지와 비누 두 개 세트가 다 모일 때까지 절대 네 몸 하나 까딱하지 말고 기다려라."
2. **점유 자원 완전 방출 (Release and Request)**: "비누 쥐고 있다가 10초 내로 휴지 못 찾으면? 손에 든 비누 바닥에 내던져버리고(반납), 빈손으로 나갔다가 처음부터 두 개 다 주우러 다시 도전해!"

**💡 비유**: 양손 가득 짐을 물고 문고리를 잡으려 버티지 말고, 다 바닥에 내려놓고 처음부터 싹 담아오라는 룰. 상대방 입장에선 너의 얌체 같은 '일부 점유' 알박기가 사라지니 속이 시원해 데드락이 사라진다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">점유 대기(Hold-and-Wait) 부정을 위한 2가지 알고리즘</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">전략 1</div><div class="kb-diagram-note">All-at-Once (일괄 요청 기반)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 프로그램이 10시간 도는 동안, 맨 마지막 1초에 쓸 파일 락</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">하나라도 못 얻으면 아예 시작 로딩조차 안 시킴.</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 문제: 남은 9시간 59분 59초 동안 그 파일 락은 놀면서 낭비.</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">전략 2</div><div class="kb-diagram-note">Release-and-Request (전면 반납형 기반)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 필요할 때마다 락을 잡되, 추가 락 B가 필요한데 막혀있으면</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">기존에 잡고 있던 소중한 A 락을 모조리 OS에 자동 헌납.</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 나중에 다시 A와 B를 패키지로 재요청함 (Retry).</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 문제: 인기도 높은 A 락을 놓는 순간 남이 채가서 영원히</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">A, B를 동시 완성 못 하고 미아(Starvation)가 됨.</div></div>
</div>
</div>



**📢 섹션 요약 비유**: [점유 대기](/knowledge-base/studynote/02_operating_system/04_synchronization/231_hold_and_wait/) 부정은 뷔페 얌체 방지법 — "접시에 김밥 하나 올려놓고 탕수육 줄 30분 서면서 남들 못 먹게 알박기(점유+대기) 금지! 접시도 반납하고 처음부터 세트 맞춰 떠오렴!"

---

## Ⅱ. 아키텍처 및 핵심 원리

### 기아 현상 ([Starvation](/knowledge-base/studynote/02_operating_system/05_deadlock/314_starvation_prevention/)) & 낭비 딜레마

`점유 대기 부정`은 운영체제에서 <strong>자원 활용률(Utilization)을 땅바닥으로 처박는 가장 주된 원흉</strong>으로 혹평받는다. 

1. **치명적인 자원 낭비율**: DVD 쓰기를 위해 프로세스는 메모리, CPU, 디스크, DVD 레코더를 동시에 선점한다. 그런데 데이터를 굽기 위해 1시간 연산을 돌릴 때, DVD 레코더는 1시간 내내 유휴([Idle](/knowledge-base/studynote/02_operating_system/10_security/611_cpu_idle_wait_optimization/)) 상태로 전세가 나간 채 썩고 있다. 다른 사람의 1분 컷 인쇄/굽기도 막아버린다.
2. <strong>기아 (<a href="/knowledge-base/studynote/02_operating_system/05_deadlock/314_starvation_prevention/">Starvation</a>) 가능성 폭증</strong>: 인기 만점인 자원 3개를 동시에 잡아야 하는 스레드는, 자원 1.2개를 잡고 3번 기다리다 뺏기고, 다시 1번 다시 잡다 뺏기고 핑퐁 릴레이를 무한 반복하며 언제 작업을 마칠지 모르는 '기아'의 나락([Livelock](/knowledge-base/studynote/02_operating_system/05_deadlock/315_livelock_vs_deadlock/) 성향)으로 떨어진다.

**📢 섹션 요약 비유**: 효율성 빵점 운영 — DVD 레코더 쓸 1시간 뒤를 위해 1시간 전부터 레코더 스위치를 잠가서 남들 손가락만 빨게 만들고, 반납형으로 시달리다 결국 일처리는 하나도 못 하는 황당한 패러다임입니다.

---

## Ⅲ. 비교 및 연결

| 처리 기준 | [점유 대기](/knowledge-base/studynote/02_operating_system/04_synchronization/231_hold_and_wait/) 보장 ([Deadlock](/knowledge-base/studynote/02_operating_system/05_deadlock/281_deadlock_definition/) 허용 후 타조/[복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)) | [점유 대기](/knowledge-base/studynote/02_operating_system/04_synchronization/231_hold_and_wait/) 부정 (완전 예방) |
|:---|:---|:---|
| 프로그래머 난이도 | 중간 (때때로 코딩 순서 조심) | 매우 높음 (시작 전 리소스 수요를 100% 코딩으로 선언해야 함) |
| OS 시스템 활용률 | <strong>최대 스루풋 (Maximum <a href="/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/">Throughput</a>)</strong> | 쓰레기 수준의 낭비 (수십 % 하락) |
| 데드락 안전 보장 | [타임아웃](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/) 롤백으로 보완 | 안전 보장은 투명하게 100% |

**📢 섹션 요약 비유**: 필요할 때 잠깐 쥐고 쓰는 요즘 시대에, "너네 데드락 낼까 봐 무서우니 탈 것들 아침에 한방에 선점신청 안 하면 아예 안 빌려줌" 하는 철통방어 공산주의적 예약 배급 시스템과 똑같습니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**실무 시나리오**:
1. **소프트웨어 락 백오프 (Backoff/Retry) 융합**: 이론적인 R&R(반납 재요청)이 기아에 빠지니, 현대 실무는 `Thread.sleep` + Random 백오프(지수 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/))를 통해 "내가 쥐고 3초 대기해보고 안 되면 놔줄게. 대신 그 후 5초 뒤나 8초 뒤(랜덤 난수)에 재도전할게!" 라며 동시 경합자들끼리 시간축을 분산시켜 기아를 회피하며 [점유 대기](/knowledge-base/studynote/02_operating_system/04_synchronization/231_hold_and_wait/)를 우회 타파한다.
2. <strong><a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/511_two_phase_locking/">Two-Phase Locking</a> (<a href="/knowledge-base/studynote/02_operating_system/05_deadlock/320_two_phase_locking_deadlock/">2PL</a>)의 극복</strong>: DB 트랜잭션의 교과서는 오직 점유([Growing phase](/knowledge-base/studynote/05_database/04_transactions_concurrency/217_growing_phase_2pl/))만 하다가 약속된 분기점에 도달해야만 반납([Shrinking phase](/knowledge-base/studynote/05_database/04_transactions_concurrency/218_shrinking_phase_2pl_cascading_rollback/))하게 만들어, 일체의 `점유 대기 부정`을 극혐하고 오히려 [점유 대기](/knowledge-base/studynote/02_operating_system/04_synchronization/231_hold_and_wait/)를 보장하는 철학 아래 만들어졌다(직렬성 보장).

<strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/">안티패턴</a></strong>:
- **정적 자원 리스트업의 붕괴**: OS에 다짜고짜 "나 이 함수 시작할 건데 `Thread_Pool` 30개랑 `DB_Conn` 50개 지금 한 번에 몰아줘"라고 선언(일괄 요청). 트래픽이 부족할 땐 낭비뿐이고 몰려올 땐 시작부터 저 많은 패키지가 조립되지 않아 아예 함수 진입이 봉쇄(초장기 무한 홀딩)된다. 

**📢 섹션 요약 비유**: 모든 재료가 완벽히 오기 전까지 요리 시작조차 안 하는 결벽증 셰프(예방)보다, 일단 야채 썰면서 소고기 오길 기다리다 너무 늦으면 다른 찌개 끓이는 셰프([타임아웃](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/))가 매출이 훨씬 나옵니다.

---

## Ⅴ. 기대효과 및 결론

| 기준 | All at Once 방식 | Release and Request 방식 |
|:---|:---|:---|
| 자원 묶임 현상 | 극단적 고착. 미사용 시간 거대함 | 일시 대방출로 여유 자원 순환율 증대 |
| 작업 완료율 보증 | 잡기만 하면 빛의 속도로 논스톱 완료 | 운 나쁘면 무한 반복되는 기아 나락 |

[점유 대기](/knowledge-base/studynote/02_operating_system/04_synchronization/231_hold_and_wait/) 부정([Hold-and-Wait](/knowledge-base/studynote/02_operating_system/05_deadlock/284_hold_and_wait/) Prevention)은 운영체제가 극도로 부족한 클록과 메모리를 어떻게 쥐어짜야 하는가를 포기한, 시스템 생리학적 자살이나 다름없는 접근이었다. 컴퓨터 과학이 범용 시스템에서 데드락 예방 모델 전체를 역사 속으로 폐기 처분하게 만든 가장 큰 원흉이 바로 이 2번 조건 부정이 낳은 극악의 오버헤드 퍼포먼스 때문이라 해도 과언이 아니다.

- **📢 섹션 요약 비유**: 도구의 장점만 외우는 것이 아니라 어디까지 믿고 어디서 보완해야 하는지 기억하는 정리 노트와 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [교착 상태 예방](/knowledge-base/studynote/02_operating_system/05_deadlock/292_deadlock_prevention/) ([Deadlock Prevention](/knowledge-base/studynote/02_operating_system/05_deadlock/292_deadlock_prevention/)) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [상호 배제 부정](/knowledge-base/studynote/02_operating_system/05_deadlock/293_deny_mutual_exclusion/) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [비선점 부정](/knowledge-base/studynote/02_operating_system/05_deadlock/295_deny_no_preemption/) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [순환 대기 부정](/knowledge-base/studynote/02_operating_system/05_deadlock/296_deny_circular_wait/) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">상호 배제 부정</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">점유 대기 부정 (Deny Hold And Wait)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">비선점 부정</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">순환 대기 부정</div></div>
</div>
</div>



이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [점유 대기](/knowledge-base/studynote/02_operating_system/04_synchronization/231_hold_and_wait/) 안 하기 규칙은 "양손에 장난감 다 쥘 때까지 아무것도 갖고 놀지 마!" (일방적 구속) 예요.
2. 하나를 잡고 있다가 다른 하나가 없다고 "지금 손에 든 것도 도로 상자에 넣어놔!"라고 하면 데드락(서로 대치)은 안 생기지만 엄청 화가 나겠죠?
3. 계속 다른 친구가 먼저 집어가버리면 난 종일 장난감을 도로 넣었다 빼기만 하다 하루가 끝나는([기아 상태](/knowledge-base/studynote/02_operating_system/05_deadlock/314_starvation_prevention/) 굶어 죽음) 슬픈 놀이법이랍니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 294 / 800

← **이전**: [293. 상호 배제 부정 (Deny Mutual Exclusion)](/knowledge-base/studynote/02_operating_system/05_deadlock/293_deny_mutual_exclusion/)
**다음**: [295. 비선점 부정 (Deny No Preemption)](/knowledge-base/studynote/02_operating_system/05_deadlock/295_deny_no_preemption/) →

---
