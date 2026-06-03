+++
title = "133. 비기능 요구사항 (NFR) - 시스템 품질 속성 정의"
date = 2026-04-19

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: NFR(Non-Functional Requirements)은 <strong>시스템이 "어떻게" 동작해야 하는가의 품질 속성</strong>으로, 성능·보안·[가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)·확장성·[유지보수성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/) 등을 정의하며 ISO 25010이 분류 표준이다.
> 2. **가치**: NFR이 <strong>아키텍처를 결정</strong>한다. "초당 10만 요청"이면 분산 아키텍처, "99.999% 가용성"이면 Active-Active 이중화가 필요하며, NFR 없이는 아키텍처 결정이 불가능하다.
> 3. **판단 포인트**: NFR은 <strong>측정 가능한 수치</strong>로 명세해야 검증 가능하다. "빨라야 한다"(✗) → "P99 응답 시간 200ms 이내"(✓).

---

## Ⅰ. 개요 및 필요성

비기능 요구사항(NFR)은 소프트웨어 아키텍처의 핵심 동인(Architecture Driver)이다. 1970~80년대 소프트웨어 개발에서는 "기능만 동작하면 된다"는 인식이 지배적이었다. 그러나 시스템 규모가 커지고 사용자 수가 폭증하면서, 기능적으로 완벽한 시스템이 성능 문제로 운영 중단되거나 보안 취약점으로 침해당하는 사례가 급증했다. 이에 따라 1990년대부터 NFR이 독립적 연구 분야로 자리 잡기 시작했다.

ISO 9126(2001)이 소프트웨어 품질 특성을 처음 표준화했고, 이를 대폭 개선한 ISO 25010(2011)이 현재 가장 널리 사용되는 NFR 분류 표준이다. ISO 25010은 소프트웨어 품질을 8대 특성으로 분류하며, 각 특성 아래 하위 특성을 세분화한다. 기술사 시험에서는 이 8대 특성을 암기하고, 각각에 대한 측정 지표와 아키텍처 영향을 연결해서 답변하는 것이 고득점 포인트이다.

NFR이 아키텍처를 결정한다는 점이 핵심이다. "로그인 기능"(FR)은 단일 서버에서도 구현 가능하지만, "1000 동시 사용자 기준 P99 응답 2초 이내"(NFR)가 추가되면 캐시 레이어와 로드 밸런서가 필요해지고, "99.999% 가용성"(NFR)이 추가되면 멀티 리전 Active-Active 구성이 필요해진다. NFR은 추가 비용이 아닌 아키텍처 설계의 필수 입력이다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">ISO 25010 품질 모델 (8대 특성):</div>
<div class="kb-diagram-note">기능 적합성(Functional Suitability)</div>
<div class="kb-diagram-note">성능 효율성(Performance Efficiency) ← 응답 시간, 처리량, 자원 활용</div>
<div class="kb-diagram-note">호환성(Compatibility) ← 공존성, 상호운용성</div>
<div class="kb-diagram-note">사용성(Usability) ← 학습용이성, 운용가능성</div>
<div class="kb-diagram-note">신뢰성(Reliability) ← 성숙성, 가용성, 내결함성</div>
<div class="kb-diagram-note">보안(Security) ← 기밀성, 무결성, 부인방지</div>
<div class="kb-diagram-note">유지보수성(Maintainability) ← 모듈성, 수정가능성, 시험가능성</div>
<div class="kb-diagram-note">이식성(Portability) ← 적응성, 설치성, 교체성</div>
</div>
</div>



- **📢 섹션 요약 비유**: NFR은 자동차의 <strong>안전등급·연비·최고속도·소음레벨</strong>이다. "달린다"(FR)만으로는 차를 선택할 수 없다. 숫자로 표현된 품질 기준이 있어야 좋은 차인지 알 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### ISO 25010 품질 특성과 측정 지표

| NFR 특성 | 하위 특성 | 측정 지표 예 | 아키텍처 영향 |
|:---|:---|:---|:---|
| **기능 적합성** | 완전성, 정확성, 적절성 | 기능 커버리지 100% | 유스케이스 완성도 |
| **성능 효율성** | 시간 동작성, 자원 활용 | P99 < 200ms, TPS > 1000 | 캐시, CDN, 비동기 처리 |
| **호환성** | 공존성, 상호운용성 | API 표준(OpenAPI) 준수 | REST, gRPC, 표준 프로토콜 |
| **사용성** | 인식가능성, 학습용이성 | SUS 점수 > 80, NPS > 50 | UX 설계, 접근성(WCAG) |
| **신뢰성** | 성숙성, 가용성, 내결함성 | 가용성 99.9%, MTBF > 720h | 이중화, 헬스체크, 자동복구 |
| **보안** | 기밀성, 무결성, 부인방지 | OWASP Top 10 대응, 암호화 | WAF, TLS 1.3, RBAC, HSM |
| **유지보수성** | 모듈성, 수정가능성 | 코드 커버리지 > 80% | 마이크로서비스, CI/CD |
| **이식성** | 적응성, 설치성 | 컨테이너화 완료, IaC | Docker, Kubernetes, Terraform |

### NFR 수치화 방법: SMART 기준 적용

| SMART 요소 | 의미 | NFR 적용 예 |
|:---|:---|:---|
| **S (Specific)** | 구체적 | "응답 빠름" → "API 응답 시간" |
| **M (Measurable)** | 측정 가능 | "시간" → "P99 < 200ms" |
| **A (Achievable)** | 달성 가능 | 기술적으로 가능한 수치 |
| **R (Relevant)** | 관련성 | 비즈니스 목표와 연결 |
| **T (Time-bound)** | 시간 기준 명시 | "1000 동시 사용자 기준" |

### NFR과 아키텍처 패턴 연결



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">성능 NFR → 아키텍처 패턴:</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">NFR: TPS &gt; 10,000</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ 로드 밸런서 (트래픽 분산)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ 캐시 레이어 (Redis, Memcached)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ 비동기 메시지 큐 (Kafka, RabbitMQ)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ CQRS (읽기/쓰기 분리)</div></div>
<div class="kb-diagram-note">가용성 NFR → 아키텍처 패턴:</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">NFR: 가용성 99.99% (연간 다운타임 &lt; 52분)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ Active-Active 다중화</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ 헬스체크 + 자동 장애 조치(Failover)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ 멀티 AZ (가용 영역) 배포</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ Circuit Breaker 패턴</div></div>
<div class="kb-diagram-note">보안 NFR → 아키텍처 패턴:</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">NFR: OWASP Top 10 대응, 데이터 암호화</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ WAF (웹 방화벽)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ API Gateway (인증/인가 집중화)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ 전송 암호화 (TLS 1.3)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ 저장 암호화 (AES-256, 키 관리 HSM)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ Zero Trust 아키텍처</div></div>
</div>
</div>



### NFR 충돌(Trade-off) 관리

| 충돌 쌍 | 상충 이유 | 해결 전략 |
|:---|:---|:---|
| **성능 vs 보안** | 암호화가 CPU 부하 유발 | 하드웨어 가속(HSM), 선택적 암호화 |
| **가용성 vs 비용** | 이중화 = 2배 비용 | 티어별 가용성(핵심 기능만 고가용성) |
| **성능 vs 일관성** | 캐시는 데이터 지연 발생 | 최종 일관성(Eventual Consistency) 허용 |
| **유지보수성 vs 성능** | 추상화 레이어가 오버헤드 유발 | 핫패스 최적화 후 추상화 |

- **📢 섹션 요약 비유**: NFR 관리는 자동차 설계의 균형 잡기다. 최고 속도(성능)를 높이면 연비(비용)가 나빠지고, 안전장치(보안)를 늘리면 무게(성능)가 늘어난다. 이 균형을 명시적으로 결정하는 것이 아키텍처 설계이다.

---

## Ⅲ. 비교 및 연결

### NFR 도출 기법 비교

| 기법 | 방식 | 장점 | 단점 |
|:---|:---|:---|:---|
| **QAW (품질 속성 워크숍)** | 이해관계자 참여 워크숍 | 전사적 합의 | 시간 소요 |
| **ATAM** | 아키텍처 트레이드오프 분석 | 충돌 사전 발견 | 고수준 전문성 필요 |
| **벤치마킹** | 경쟁사·유사 시스템 비교 | 현실적 수치 | 맥락 차이 주의 |
| **SLA 분석** | 운영 계약 기반 | 명확한 기준 | 비즈니스 제약 |
| **ISO 25010 체크리스트** | 8대 특성 순차 검토 | 누락 방지 | 도메인 특화 부족 |

### NFR vs 기능 요구사항 비교

| 항목 | FR | NFR |
|:---|:---|:---|
| **질문** | 무엇을 해야 하는가? | 얼마나 잘 해야 하는가? |
| **아키텍처 영향** | 낮음 (기능 모듈) | 매우 높음 (전체 구조) |
| **도출 난이도** | 보통 (사용자가 표현 가능) | 높음 (전문 지식 필요) |
| **측정 방법** | 기능 테스트 | 성능/보안/사용성 테스트 |
| **변경 비용** | 보통 | 높음 (아키텍처 변경 수반) |

### 가용성 수준별 다운타임 기준

| 가용성 | 연간 다운타임 | 필요 아키텍처 | 비용 |
|:---|:---|:---|:---|
| **99%** | 87.6시간/년 | 단일 서버 | 낮음 |
| **99.9%** | 8.7시간/년 | Active-Standby | 보통 |
| **99.99%** | 52분/년 | Active-Active | 높음 |
| **99.999%** | 5.2분/년 | 멀티 리전 Active-Active | 매우 높음 |
| **99.9999%** | 31초/년 | 특수 설계 필요 | 극단적 |

- **📢 섹션 요약 비유**: NFR은 운전면허 시험의 기준표다. "운전할 수 있다"(FR)는 합격/불합격만 있지만, "제동 거리", "주차 정확도", "차선 유지"(NFR)는 구체적인 기준치가 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 설계 판단 체크리스트

1. **ISO 25010 8대 특성 점검**: 각 특성별로 NFR이 정의되었는가?
2. **수치화 완료**: 모든 NFR에 측정 가능한 수치와 측정 조건(동시 사용자 수, 데이터 규모)이 명시되었는가?
3. **아키텍처 연결**: 각 NFR이 구체적인 아키텍처 결정(캐시, 이중화, 암호화)에 연결되었는가?
4. **NFR 충돌 해결**: 상충하는 NFR 쌍(성능 vs 보안)에 대해 트레이드오프 결정이 기록되었는가?
5. **검증 계획**: 각 NFR을 어떤 테스트로 검증할지(부하 테스트, 보안 감사, 사용성 테스트) 계획되었는가?
6. **운영 관점 NFR**: 관찰가능성(로깅, 메트릭, 트레이싱), 배포 자동화, 장애 복구 시간(RTO/RPO) 같은 운영 NFR이 포함되었는가?

### 안티패턴

- **암묵적 NFR(Implicit NFR)**: 명시하지 않아도 당연히 충족되겠지 생각하는 NFR. "당연히 빠르겠지", "당연히 안전하겠지"는 NFR 명세서에 존재하지 않으면 개발팀의 의무가 아니다. 모든 NFR은 명시적으로 문서화해야 한다.

- **검증 불가 NFR(Unverifiable NFR)**: "사용자 친화적", "직관적 인터페이스", "확장 가능한 설계"처럼 테스트로 확인 불가능한 NFR. SUS 점수 > 80, 1000 RPS에서 선형 확장 등 구체적 기준으로 재정의해야 한다.

- **NFR 과대 설정**: 실제 필요보다 지나치게 높은 NFR 설정. "99.9999% 가용성"이 필요하지 않은 내부 관리 시스템에 이를 요구하면 비용이 폭증한다. NFR은 비즈니스 가치에 비례해야 한다.

- **운영 NFR 누락**: 개발 시점 NFR만 정의하고 운영 NFR(배포 자동화, 장애 탐지 시간, 변경 배포 빈도)을 누락하는 패턴. DevOps 시대에 운영 NFR은 개발 NFR만큼 중요하다.

- **📢 섹션 요약 비유**: NFR 안티패턴은 의약품 사용 설명서 미작성과 같다. "당연히 안전하겠지"(암묵적), "효과가 좋아야 함"(검증 불가)처럼 모호하게 두면 문제 발생 시 책임 소재가 불분명해진다.

---

## Ⅴ. 기대효과 및 결론

NFR을 체계적으로 정의하면 아키텍처 결정의 근거가 생긴다. "왜 Redis 캐시가 필요한가?"에 대해 "NFR: P99 응답 200ms, DB 조회 비용 절감"이라는 명확한 답변이 가능하다. 이는 기술 결정의 비즈니스 정당성을 확보하고, 이해관계자 승인을 용이하게 만든다.

NFR 기반 아키텍처 설계는 장기적 유지보수 비용을 절감한다. 초기에 명확한 성능·확장성 NFR을 정의하면, 후반에 "성능이 안 나온다"는 위기를 예방하고 단계별 스케일아웃 전략을 사전에 수립할 수 있다. 보안 NFR을 초기에 정의하면 보안 설계를 아키텍처에 내재화할 수 있으며, 추후 보안 패치의 범위를 최소화한다.

미래에는 AI 기반 NFR 관리가 발전할 것이다. 운영 모니터링 데이터를 실시간으로 NFR 명세와 비교하여 위반을 자동 탐지하고, 용량 계획(Capacity Planning)을 자동화하는 시스템이 확산될 것이다. NFR은 정적인 문서가 아닌, 시스템 생명주기 전반에 걸쳐 지속적으로 관리되어야 하는 살아있는 명세이다.

- **📢 섹션 요약 비유**: NFR은 자동차 제조의 품질 기준표다. 이 기준표가 명확해야 생산 단계에서 검사하고, 출고 전 품질을 보증하고, 리콜 기준을 판단할 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| **NFR** | 품질 속성 (How well) |
| **ISO 25010** | 8대 품질 특성 분류 표준 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/229_atam_architecture_trade_off_analysis_method/">ATAM</a></strong> | NFR 트레이드오프 아키텍처 분석 |
| **QAW** | 품질 속성 워크숍 (NFR 도출) |
| **Architecture Driver** | NFR이 아키텍처를 결정하는 동인 |
| **SLA/SLO/SLI** | NFR의 운영 서비스 수준 체계 |
| **부하 테스트** | 성능 NFR 검증 기법 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">비공식 NFR (~2000s) "빠르고 안전하게"</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">ISO 9126 (2001) ── 6대 품질 특성 최초 표준화</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">ISO 25010 (2011) ── 8대 특성으로 개선, 보안 독립</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">QAW + ATAM ── 아키텍처 관점 NFR 분석 체계화</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">클라우드 NFR (2015~) ── 탄력성, 비용 효율, 관찰가능성 추가</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">현재: AI NFR 추출 ── 요구사항 텍스트에서 품질 속성 자동 식별</div>
<div class="kb-diagram-tree-item" style="--depth:7">운영 데이터로 NFR 자동 검증</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명
1. NFR은 자동차의 <strong>안전등급·연비·최고속도</strong>예요.
2. "달린다"(기능)만으로는 **좋은 차인지** 알 수 없어요.
3. "200km/h, 연비 15km/L"처럼 **숫자로 정확히** 적어야 비교할 수 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 133 / 973

← **이전**: [132. 요구사항 유형 (기능·비기능·제약사항) - FR·NFR·Constraints 분류](/knowledge-base/studynote/04_software_engineering/03_design_architecture/132_types_of_requirements/)
**다음**: [134. 요구사항 공학 프로세스 - 도출→분석→명세→검증→관리 상세](/knowledge-base/studynote/04_software_engineering/03_design_architecture/134_requirements_engineering_process/) →

---
