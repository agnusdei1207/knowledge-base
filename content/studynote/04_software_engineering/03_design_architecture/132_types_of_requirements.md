+++
title = "132. 요구사항 유형 (기능·비기능·제약사항) - FR·NFR·Constraints 분류"
date = 2026-04-19

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 요구사항은 **기능 요구사항(FR, 시스템이 해야 하는 것)**·<strong><a href="/knowledge-base/studynote/04_software_engineering/03_design_architecture/133_non_functional_requirements/">비기능 요구사항</a>(<a href="/knowledge-base/studynote/04_software_engineering/03_design_architecture/133_non_functional_requirements/">NFR</a>, 성능·보안·<a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">가용성</a> 등 품질 속성)</strong>·<strong>제약사항(Constraints, 기술·법적 제한)</strong>의 3가지로 분류된다.
> 2. **가치**: FR만 정의하면 "로그인은 되는데 3초 걸리고 해킹에 취약한" 시스템이 되며, NFR이 <strong>시스템의 품질 수준</strong>을 결정한다. 기술사 시험에서 [NFR](/knowledge-base/studynote/04_software_engineering/03_design_architecture/133_non_functional_requirements/) 누락이 가장 흔한 감점 포인트이다.
> 3. **판단 포인트**: NFR은 ISO 25010 품질 모델(기능성·신뢰성·사용성·효율성·유지보수성·이식성·보안·호환성)로 체계적으로 도출하며, <strong>측정 가능한 수치</strong>로 명세해야 한다.

---

## Ⅰ. 개요 및 필요성

소프트웨어 요구사항은 크게 세 가지 유형으로 나뉜다. 이 분류는 1970년대 폭포수 개발 방법론이 정착되면서 체계화되었고, 1998년 IEEE 830 SRS 표준에서 공식화되었다. 이 구분이 중요한 이유는, 각 유형에 따라 **도출 방법, 명세 형식, 검증 방법이 완전히 다르기** 때문이다.

기능 요구사항(FR)은 가장 직관적이다. 사용자가 "무엇을 원하는가"에 대한 답이다. 그러나 FR만 정의한 시스템은 비유하면 "달리기는 하지만 브레이크도 없고 에어백도 없는 자동차"와 같다. 실제 운행 가능하려면 안전성·성능·연비라는 비기능 요구사항이 함께 정의되어야 한다.

제약사항(Constraints)은 시스템이 반드시 지켜야 할 외부적 한계이다. 기술 스택 제약(Java 17 사용), 법적 제약(GDPR 준수, 개인정보보호법), 예산 제약, 일정 제약 등이 포함된다. 제약사항은 요구사항이 아닌 전제 조건으로 보는 시각도 있지만, 설계 결정에 강력한 영향을 미치므로 별도로 관리해야 한다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">요구사항 분류 체계:</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">FR</div><div class="kb-diagram-note">"사용자는 이메일로 로그인할 수 있다"</div></div>
<div class="kb-diagram-note">→ 동사+목적어 형태, 유스케이스로 표현</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">NFR</div><div class="kb-diagram-note">"로그인 응답 시간은 99%ile에서 2초 이내이다" (성능)</div></div>
<div class="kb-diagram-note">"99.9% 가용성을 보장한다" (가용성)</div>
<div class="kb-diagram-note">"OWASP Top 10 취약점에 대응한다" (보안)</div>
<div class="kb-diagram-note">→ 수치+측정기준 형태, 품질 속성으로 표현</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">제약</div><div class="kb-diagram-note">"Java 17 사용", "AWS 클라우드 배포", "GDPR 준수"</div></div>
<div class="kb-diagram-note">→ 전제 조건 형태, 아키텍처 제한으로 표현</div>
</div>
</div>



- **📢 섹션 요약 비유**: FR은 "차가 달린다(기능)", NFR은 "200km/h·연비 15km/L·에어백 10개(품질)", 제약은 "경유만 사용·국내 도로 운행(제한)"이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 세 가지 요구사항 유형 상세 비교

| 항목 | FR (기능 요구사항) | NFR (비기능 요구사항) | 제약사항 |
|:---|:---|:---|:---|
| **질문** | What to do? (무엇을?) | How well? (얼마나 잘?) | What limits? (제한은?) |
| **표현** | 사용자 동작 + 시스템 반응 | 측정 가능한 수치 | 전제 조건, 법규 |
| **예시** | 이메일 로그인 가능 | P99 < 2s | Java 17 사용 |
| **도출 기법** | 유스케이스, User Story | QAW, 벤치마킹 | 법률 검토, 기술 제약 분석 |
| **명세 방법** | 유스케이스 명세, Gherkin | 수치 + 측정 조건 | 조건 목록 |
| **검증 방법** | 기능 테스트, 인수 테스트 | 성능 테스트, 보안 감사 | 기술 검토, 법적 검토 |
| **아키텍처 영향** | 모듈 설계, API 설계 | 아키텍처 패턴 선택 | 기술 스택 결정 |

### ISO 25010 NFR 분류 체계 (8대 특성)

| 품질 특성 | 설명 | 측정 지표 예 | 아키텍처 영향 |
|:---|:---|:---|:---|
| **기능 적합성** | 요구 기능의 올바른 제공 | 기능 커버리지 100% | 유스케이스 완성도 |
| **성능 효율성** | 자원 대비 응답 시간 | P99 < 200ms, TPS > 1000 | 캐시, CDN, 비동기 |
| **호환성** | 공존 및 상호운용 | API 표준 준수 | REST, OpenAPI |
| **사용성** | 사용 용이성 | SUS 점수 > 80 | UX 설계 |
| **신뢰성** | 정상 운영 시간 | 가용성 99.9%, MTBF > 720h | 이중화, 장애 복구 |
| **보안** | 무단 접근 차단 | OWASP Top 10 대응 | WAF, 암호화, IAM |
| **유지보수성** | 수정·개선 용이성 | 코드 커버리지 > 80% | 모듈화, CI/CD |
| **이식성** | 다른 환경으로 이전 가능 | 컨테이너화 완료 | Docker, 클라우드 네이티브 |

### NFR이 아키텍처를 결정하는 원리



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">NFR 수치 → 아키텍처 결정 영향 다이어그램:</div>
<div class="kb-diagram-note">성능 NFR (TPS &gt; 10만):</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">단일 서버 → 불가능</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">분산 아키텍처 → 필요</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">캐시 레이어(Redis) → 필요</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">CDN → 필요</div></div>
<div class="kb-diagram-note">가용성 NFR (99.999%, 5 nines):</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">단일 데이터센터 → 불가능</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Active-Active 이중화 → 필요</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">멀티 리전 배포 → 필요</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">RPO=0, RTO&lt;1분 → 설계 제약</div></div>
<div class="kb-diagram-note">보안 NFR (OWASP Top 10 대응):</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">WAF(웹 방화벽) → 필요</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">전송 암호화(TLS 1.3) → 필수</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">저장 암호화(AES-256) → 필수</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">인증/인가(OAuth2, RBAC) → 필요</div></div>
</div>
</div>



### FR과 NFR 명세 예시 비교

| 구분 | 나쁜 명세 | 좋은 명세 |
|:---|:---|:---|
| **FR** | "로그인 기능 구현" | "사용자는 이메일과 비밀번호로 로그인할 수 있으며, 5회 실패 시 계정이 잠긴다" |
| **NFR** | "빠른 응답" | "로그인 API 응답 시간은 P50 < 100ms, P99 < 500ms이어야 한다 (1000 동시 사용자 기준)" |
| **제약** | "보안 고려" | "개인정보보호법 제23조에 따라 민감 정보는 AES-256으로 암호화하여 저장해야 한다" |

- **📢 섹션 요약 비유**: FR·NFR·제약은 자동차 구매 명세와 같다. FR="4인승 세단", NFR="최고속도 200km/h, 연비 15km/L, 충돌 안전등급 5점", 제약="경유 엔진, 국내 출시 모델"이다. 이 세 가지 모두 명확해야 원하는 차를 정확히 구매할 수 있다.

---

## Ⅲ. 비교 및 연결

### FR vs NFR vs 제약사항 구분 판단 기준

| 판단 기준 | FR | NFR | 제약사항 |
|:---|:---|:---|:---|
| **사용자가 직접 요청?** | 예 (기능 요청) | 부분적 | 아니오 (외부 강제) |
| **아키텍처 결정 영향?** | 낮음 (기능 모듈) | 매우 높음 | 높음 (기술 스택) |
| **측정 방법?** | 기능 테스트 | 성능/보안 테스트 | 준수 여부 검토 |
| **변경 빈도?** | 보통 | 낮음 (안정적) | 매우 낮음 |

### 요구사항 분류가 어려운 경계 사례

| 요구사항 | 분류 | 이유 |
|:---|:---|:---|
| "검색 결과를 1초 내에 표시" | NFR (성능) | "1초 내"가 품질 수치 |
| "다크 모드 지원" | FR | 기능적 요구 |
| "모바일 화면에서 사용 가능" | NFR (호환성) | 플랫폼 호환성 |
| "AWS에서 운영" | 제약 | 기술 스택 제한 |
| "로그아웃 후 세션 즉시 종료" | FR + NFR | 기능+보안 요구 혼합 |

### 연결 개념

| 개념 | FR/NFR과의 관계 |
|:---|:---|
| **ATAM** | NFR 트레이드오프를 아키텍처 관점에서 분석하는 방법 |
| **QAW (품질 속성 워크숍)** | NFR을 체계적으로 도출하는 워크숍 기법 |
| **유스케이스** | FR을 구조화하는 표준 표현 방식 |
| **User Story** | Agile에서 FR을 표현하는 방식 (As a... I want... So that...) |
| **SLO/SLA** | NFR의 운영 서비스 수준 합의로 확장된 개념 |

- **📢 섹션 요약 비유**: FR·NFR·제약을 구분하는 것은 병원에서 환자의 증상(FR)·건강 기준(NFR)·투약 제한(제약)을 구분하는 것이다. 증상만 치료하고 건강 기준과 약물 제한을 무시하면 치료가 위험해진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 설계 판단 체크리스트

1. **FR 명세 완전성**: 모든 사용자 시나리오(정상+예외)가 FR로 명세되었는가?
2. **NFR 수치화**: "빠른", "안정적인", "사용하기 쉬운" 등 모호한 표현이 없는가?
3. **ISO 25010 점검**: 8대 품질 특성(성능·가용성·보안·사용성·유지보수성·이식성·호환성·기능적합성) 각각에 대해 NFR이 정의되었는가?
4. **제약사항 식별**: 법적(GDPR, 개인정보보호법), 기술적(플랫폼, 언어), 비용적 제약이 모두 식별되었는가?
5. **아키텍처 연결**: 핵심 NFR이 아키텍처 결정 사항에 반영되었는가?
6. **NFR 충돌 해결**: 상충하는 NFR(성능 vs 보안, 가용성 vs 비용) 간 트레이드오프가 결정되고 기록되었는가?

### 안티패턴

- **NFR 후기 발견(Late NFR Discovery)**: 구현 완료 후 "응답이 너무 느리다", "보안이 취약하다"는 NFR이 발견되는 패턴. 아키텍처를 전면 재설계해야 할 수 있으며, 비용은 초기 발견 대비 100배 이상이다. NFR은 아키텍처 설계 전 반드시 정의해야 한다.

- **NFR 무시(NFR Neglect)**: FR 개발에만 집중하여 성능·보안 NFR을 개발 후반으로 미루는 패턴. "나중에 성능 튜닝하면 된다"는 생각은 아키텍처 근본 변경이 필요한 상황에서는 통하지 않는다.

- **제약사항 미확인**: GDPR, 의료 기기 규제(IEC 62304), 금융 보안 규제(PCI-DSS) 등 법적 제약을 개발 후반에 발견하는 패턴. 규제 준수를 위해 전체 데이터 흐름을 재설계해야 할 수도 있다.

- **모순된 NFR**: "99.999% 가용성"과 "월 10만 원 운영 비용" 같이 달성이 불가능한 NFR 조합. 이해관계자와 함께 트레이드오프를 명시적으로 논의하고 결정해야 한다.

- **📢 섹션 요약 비유**: NFR 무시는 자동차 설계에서 엔진(FR)만 만들고 브레이크(안전 NFR)를 나중에 추가하려는 것이다. 이미 차 구조가 완성된 후 브레이크를 추가하면 전체를 뜯어내야 한다.

---

## Ⅴ. 기대효과 및 결론

FR·NFR·제약사항의 체계적 분류와 명세는 소프트웨어 프로젝트 성공의 기초이다. 정량적 효과로는 NFR을 명세하지 않은 프로젝트에서 성능 재설계 비용이 평균 개발비의 30~40%를 차지한다는 연구 결과가 있다. NFR을 초기에 정의하면 아키텍처 결정이 근거를 갖게 되며, 설계 트레이드오프가 명시적으로 기록된다.

ISO 25010 품질 모델은 NFR 도출의 체크리스트 역할을 한다. 8대 품질 특성을 순서대로 검토하면 NFR 누락을 최소화할 수 있다. 특히 유지보수성과 이식성은 흔히 간과되는 NFR이지만, 운영 단계에서 큰 비용 차이를 만들어낸다.

미래 방향으로는 AI가 비정형 데이터(고객 리뷰, 지원 티켓, 회의록)에서 NFR을 자동 도출하는 기술이 발전하고 있다. 또한 운영 모니터링 데이터(응답 시간, 오류율)를 실시간으로 NFR 명세와 비교하여 위반을 자동 탐지하는 시스템도 등장하고 있다.

- **📢 섹션 요약 비유**: FR·NFR·제약사항은 집 짓기의 3요소다. FR=방 개수·구조(기능), NFR=단열 등급·소음 차단·전기 용량(품질), 제약=건축법·용도지역(한계). 이 세 가지를 모두 명확히 해야 쓸 만한 집이 나온다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| **FR** | 기능 요구사항 (What to do) |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/03_design_architecture/133_non_functional_requirements/">NFR</a></strong> | 비기능 요구사항 (How well) |
| **ISO 25010** | 품질 모델 (8대 특성) |
| **QAW** | 품질 속성 워크숍 (NFR 도출 기법) |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/229_atam_architecture_trade_off_analysis_method/">ATAM</a></strong> | 아키텍처 트레이드오프 분석 |
| **SLA/SLO** | NFR의 운영 서비스 수준 합의 |
| **GDPR** | 개인정보 처리 제약사항 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">비공식 요구 (기능만)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">IEEE 830 SRS (FR + NFR 분리, 1998)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">ISO 9126 품질 모델 (2001)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">ISO 25010 (8대 품질 특성, 2011) ←── QAW, ATAM 활용</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">클라우드 시대 NFR (탄력성, 비용 효율, 관찰가능성 추가)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">현재: AI NFR 자동 도출 요구사항→품질 속성 추출</div>
<div class="kb-diagram-tree-item" style="--depth:8">운영 데이터→NFR 위반 탐지</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명
1. FR은 "차가 **달린다**"(기능), NFR은 "**얼마나 빨리**, 얼마나 안전하게"(품질)예요.
2. "달리기만 하면 돼"라고 하면 **느리고 위험한** 차가 만들어져요.
3. "200km/h, 에어백 10개"처럼 **숫자로 정확히** 적어야 좋은 차가 나와요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 132 / 973

← **이전**: [131. 요구사항 공학 (Requirements Engineering) - 체계적 요구 수집·분석·관리](/knowledge-base/studynote/04_software_engineering/03_design_architecture/131_requirements_engineering/)
**다음**: [133. 비기능 요구사항 (NFR) - 시스템 품질 속성 정의](/knowledge-base/studynote/04_software_engineering/03_design_architecture/133_non_functional_requirements/) →

---
