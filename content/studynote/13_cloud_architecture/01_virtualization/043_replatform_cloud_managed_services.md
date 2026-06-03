+++
title = "043. Re-platform — 클라우드 관리형 서비스 전환"
date = 2026-04-05

[taxonomies]
tags = ["studynote-cloud-architecture"]

[extra]
tags = ["studynote-cloud-architecture"]
+++

> **핵심 인사이트**
> 1. Re-platform(재플랫폼)은 6R [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 중 Rehost(그대로 이전)와 Re-architect(전면 재설계)의 중간 단계로 — 최소한의 코드 변경으로 클라우드 관리형 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)(RDS, EKS, Elastic Beanstalk 등)로 전환하여 운영 부담을 줄이면서 클라우드 이점을 부분적으로 활용한다.
> 2. Re-platform의 핵심 원칙은 "Core Architecture는 유지, 단 플랫폼 레이어는 매니지드로"로 — 자체 운영 PostgreSQL을 AWS RDS로 교체하면 코드 변경 없이 자동 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/), 멀티 AZ, 패치 관리를 획득하며 [DBA](/knowledge-base/studynote/05_database/01_db_architecture_relational/025_dba_database_administrator/) 운영 부담을 80% 이상 줄일 수 있다.
> 3. Re-platform은 Rehost 이후 6~12개월 안정화 기간을 거친 후 [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/)하는 것이 최선이며 — 무리한 동시 마이그레이션은 장애 위험을 배가시키고, 단계적 접근이 클라우드 전환의 현실적 성공 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다.

---

## Ⅰ. Re-platform 개념과 위치



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">6R 전략 내 Re-platform 위치:</div>
<div class="kb-diagram-note">Retire → Retain → Rehost → Re-platform → Repurchase → Re-architect</div>
<div class="kb-diagram-note">(리프트앤시프트) ↑ (SaaS 전환) (클라우드 네이티브)</div>
<div class="kb-diagram-note">오늘 주제</div>
<div class="kb-diagram-note">Re-platform 특징:</div>
<div class="kb-diagram-note">최소한의 코드 변경</div>
<div class="kb-diagram-note">플랫폼/미들웨어 교체</div>
<div class="kb-diagram-note">클라우드 관리형 서비스 활용</div>
<div class="kb-diagram-note">변경 범위:</div>
<div class="kb-diagram-note">✓ DB 엔진 → 클라우드 관리형 DB (RDS, Cloud SQL)</div>
<div class="kb-diagram-note">✓ 앱 서버 → 컨테이너 (ECS, EKS, Cloud Run)</div>
<div class="kb-diagram-note">✓ 캐시 → 관리형 Redis (ElastiCache, Memorystore)</div>
<div class="kb-diagram-note">✓ 메시지 큐 → 관리형 (SQS, Pub/Sub)</div>
<div class="kb-diagram-note">✗ 앱 비즈니스 로직 변경 없음</div>
<div class="kb-diagram-note">✗ 마이크로서비스 분리 없음 (Re-architect 영역)</div>
<div class="kb-diagram-note">Rehost vs Re-platform vs Re-architect:</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">항목</div><div class="kb-diagram-cell">Rehost</div><div class="kb-diagram-cell">Re-platform</div><div class="kb-diagram-cell">Re-architect</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">코드 변경</div><div class="kb-diagram-cell">없음</div><div class="kb-diagram-cell">최소</div><div class="kb-diagram-cell">전면 재설계</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">클라우드 이점</div><div class="kb-diagram-cell">낮음</div><div class="kb-diagram-cell">중간</div><div class="kb-diagram-cell">높음</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">위험도</div><div class="kb-diagram-cell">낮음</div><div class="kb-diagram-cell">중간</div><div class="kb-diagram-cell">높음</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">비용 절감</div><div class="kb-diagram-cell">없거나 증가</div><div class="kb-diagram-cell">15~30%</div><div class="kb-diagram-cell">40~60%</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">기간</div><div class="kb-diagram-cell">빠름</div><div class="kb-diagram-cell">수주~수개월</div><div class="kb-diagram-cell">수개월~수년</div></div>
</div>
</div>



> 📢 **섹션 요약 비유**: Re-platform은 이사 후 가구 재배치 — 집(아키텍처)은 그대로인데, 낡은 장롱(자체 DB)을 빌트인 붙박이장(관리형 RDS)으로 교체. 인테리어 공사는 아님.

---

## Ⅱ. 주요 Re-platform 패턴



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Re-platform 주요 패턴:</div>
<div class="kb-diagram-note">1. DB 서버 → 관리형 DB 서비스:</div>
<div class="kb-diagram-note">온프레미스 MySQL → AWS RDS for MySQL</div>
<div class="kb-diagram-note">온프레미스 PostgreSQL → Amazon RDS for PostgreSQL</div>
<div class="kb-diagram-note">Oracle → AWS Aurora PostgreSQL (Oracle 탈피)</div>
<div class="kb-diagram-note">획득 이점:</div>
<div class="kb-diagram-note">자동 백업 + Point-in-Time Recovery</div>
<div class="kb-diagram-note">멀티 AZ 고가용성 자동 구성</div>
<div class="kb-diagram-note">보안 패치 자동 적용</div>
<div class="kb-diagram-note">성능 인사이트 (DBA 작업 80% 감소)</div>
<div class="kb-diagram-note">2. 앱 서버 → 컨테이너 서비스:</div>
<div class="kb-diagram-note">VM(Apache Tomcat) → AWS ECS/EKS</div>
<div class="kb-diagram-note">코드 변경: Dockerfile 작성만 필요</div>
<div class="kb-diagram-note">획득 이점:</div>
<div class="kb-diagram-note">오토스케일링</div>
<div class="kb-diagram-note">블루/그린 배포</div>
<div class="kb-diagram-note">컨테이너 오케스트레이션</div>
<div class="kb-diagram-note">3. 자체 Elasticsearch → OpenSearch Service:</div>
<div class="kb-diagram-note">운영 부담 제거</div>
<div class="kb-diagram-note">자동 확장, 백업</div>
<div class="kb-diagram-note">4. Nginx + 자체 SSL → ALB (Application Load Balancer):</div>
<div class="kb-diagram-note">SSL 인증서 자동 갱신 (ACM)</div>
<div class="kb-diagram-note">WAF 통합</div>
<div class="kb-diagram-note">5. 자체 Kafka → MSK (Managed Streaming for Kafka):</div>
<div class="kb-diagram-note">Kafka 운영 복잡성 제거</div>
<div class="kb-diagram-note">Auto Scaling, 모니터링 통합</div>
<div class="kb-diagram-note">Re-platform 시 주의:</div>
<div class="kb-diagram-note">RDS 파라미터 그룹 최적화 필요</div>
<div class="kb-diagram-note">연결 풀링 설정 (RDS Proxy 활용)</div>
<div class="kb-diagram-note">마이그레이션 다운타임 계획 (AWS DMS 활용)</div>
</div>
</div>



> 📢 **섹션 요약 비유**: Re-platform 패턴은 가전제품 업그레이드 — 냉장고(DB)를 자체 수리에서 삼성 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)센터 [AS](/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) 계약으로 바꾸는 것. 냉장고 안의 음식([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))은 그대로, 관리만 전문가에게.

---

## Ⅲ. RDS 마이그레이션 상세



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">온프레미스 DB → RDS 마이그레이션:</div>
<div class="kb-diagram-note">전략 선택:</div>
<div class="kb-diagram-note">1. 기존 방식 + RDS로 이전</div>
<div class="kb-diagram-note">mysqldump → S3 → RDS 복원</div>
<div class="kb-diagram-note">다운타임: 데이터 크기에 따라 수 시간</div>
<div class="kb-diagram-note">2. AWS DMS (Database Migration Service):</div>
<div class="kb-diagram-note">지속적 복제 (Change Data Capture)</div>
<div class="kb-diagram-note">다운타임 최소화 (수분 컷오버)</div>
<div class="kb-diagram-note">이기종 DB 마이그레이션 지원 (Oracle → Aurora)</div>
<div class="kb-diagram-note">DMS 마이그레이션 단계:</div>
<div class="kb-diagram-note">1. 소스 DB 연결 설정</div>
<div class="kb-diagram-note">2. 타겟 RDS 생성 및 연결 설정</div>
<div class="kb-diagram-note">3. 초기 전체 로드 (Full Load)</div>
<div class="kb-diagram-note">4. 지속적 CDC (Change Data Capture) 복제</div>
<div class="kb-diagram-note">5. 지연 최소화 확인 (수 초 이내)</div>
<div class="kb-diagram-note">6. 컷오버 (애플리케이션 연결 변경)</div>
<div class="kb-diagram-note">7. DMS 복제 태스크 중지</div>
<div class="kb-diagram-note">RDS 최적화:</div>
<div class="kb-diagram-note">인스턴스 유형:</div>
<div class="kb-diagram-note">범용: db.t3/m6g (소규모)</div>
<div class="kb-diagram-note">메모리 최적화: db.r6g (DB 서버)</div>
<div class="kb-diagram-note">스토리지:</div>
<div class="kb-diagram-note">gp3 (기본): 범용 SSD</div>
<div class="kb-diagram-note">io2: 고 IOPS (OLTP, 금융)</div>
<div class="kb-diagram-note">읽기 복제본:</div>
<div class="kb-diagram-note">읽기 쿼리를 Read Replica로 분산</div>
<div class="kb-diagram-note">→ Primary 부하 감소 50~80%</div>
<div class="kb-diagram-note">비용 비교:</div>
<div class="kb-diagram-note">온프레미스: EC2(DB) = $500/월 + DBA 인건비 $5,000/월</div>
<div class="kb-diagram-note">RDS: $800/월 (관리형) + DBA 부분 감소</div>
<div class="kb-diagram-note">실질: 인건비 절감 시 총비용 40% 감소</div>
</div>
</div>



> 📢 **섹션 요약 비유**: DMS 마이그레이션은 물 흐르게 하면서 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/) 교체 — 물 공급 끊지 않고([서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 지속), 새 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)(RDS)로 조금씩 물을 유도해서 최종 전환.

---

## Ⅳ. EKS/ECS [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)화



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">VM 앱 → EKS/ECS 컨테이너화:</div>
<div class="kb-diagram-note">ECS vs EKS 선택:</div>
<div class="kb-diagram-note">ECS (Elastic Container Service):</div>
<div class="kb-diagram-note">AWS 전용 오케스트레이터</div>
<div class="kb-diagram-note">설정 간단, AWS 서비스 통합 우수</div>
<div class="kb-diagram-note">소규모 / AWS 전용 팀 적합</div>
<div class="kb-diagram-note">EKS (Elastic Kubernetes Service):</div>
<div class="kb-diagram-note">Kubernetes 표준 API</div>
<div class="kb-diagram-note">이식성 높음 (멀티 클라우드)</div>
<div class="kb-diagram-note">Kubernetes 경험 팀 적합</div>
<div class="kb-diagram-note">Re-platform 컨테이너화 단계:</div>
<div class="kb-diagram-note">1. Dockerfile 작성:</div>
<div class="kb-diagram-note">FROM adoptopenjdk:11-jre-hotspot</div>
<div class="kb-diagram-note">COPY target/app.jar /app/app.jar</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">ENTRYPOINT</div><div class="kb-diagram-node">"java", "-jar", "/app/app.jar"</div></div>
<div class="kb-diagram-note">2. ECR(Elastic Container Registry)에 이미지 푸시</div>
<div class="kb-diagram-note">3. ECS Task Definition 정의:</div>
<div class="kb-diagram-note">CPU: 1vCPU, Memory: 2GB</div>
<div class="kb-diagram-note">환경변수: DB_URL, API_KEY (Secrets Manager 연동)</div>
<div class="kb-diagram-note">4. ECS Service 생성:</div>
<div class="kb-diagram-note">Desired Count: 3 (최소 인스턴스)</div>
<div class="kb-diagram-note">Auto Scaling: CPU 70% 이상 → 스케일 아웃</div>
<div class="kb-diagram-note">5. ALB (Application Load Balancer) 연동</div>
<div class="kb-diagram-note">6. CI/CD 파이프라인 연결 (CodePipeline/GitHub Actions)</div>
<div class="kb-diagram-note">Fargate 활용:</div>
<div class="kb-diagram-note">EC2 서버 관리 없이 컨테이너 실행</div>
<div class="kb-diagram-note">= Serverless Container</div>
<div class="kb-diagram-note">추가 Re-platform: EC2 기반 ECS → Fargate 이전</div>
<div class="kb-diagram-note">서버 패치, 용량 관리 부담 제거</div>
</div>
</div>



> 📢 **섹션 요약 비유**: ECS/EKS [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)화는 배달 표준 박스 포장 — 어느 차(서버)에도 실을 수 있는 표준 박스([컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/))에 물건(앱)을 담으면, 배달 차(서버)만 바꿔도 됨.

---

## Ⅴ. 실무 시나리오 — E-Commerce Re-platform



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">이커머스 플랫폼 Re-platform 사례:</div>
<div class="kb-diagram-note">현황 (Rehost 완료 후):</div>
<div class="kb-diagram-note">EC2: 온프레미스 VM → AWS EC2 이전 완료 (Rehost)</div>
<div class="kb-diagram-note">RDS: 자체 MySQL → 자체 운영 MySQL on EC2 (아직 비최적)</div>
<div class="kb-diagram-note">문제: DB 패치/백업 수동, 고가용성 없음</div>
<div class="kb-diagram-note">Re-platform 목표:</div>
<div class="kb-diagram-note">MySQL on EC2 → RDS for MySQL (Multi-AZ)</div>
<div class="kb-diagram-note">Apache Tomcat on EC2 → ECS Fargate</div>
<div class="kb-diagram-note">Nginx → ALB + WAF</div>
<div class="kb-diagram-note">Redis on EC2 → ElastiCache</div>
<div class="kb-diagram-note">단계별 실행:</div>
<div class="kb-diagram-note">Week 1-2: RDS 마이그레이션</div>
<div class="kb-diagram-note">DMS 설정 → 지속 복제 → 피크 시간 외 컷오버</div>
<div class="kb-diagram-note">다운타임: 15분</div>
<div class="kb-diagram-note">Week 3-4: Redis → ElastiCache</div>
<div class="kb-diagram-note">설정 변경: redis://old-host → cluster-endpoint</div>
<div class="kb-diagram-note">코드 변경: 없음 (Redis 클라이언트 호환)</div>
<div class="kb-diagram-note">Week 5-8: Tomcat → ECS Fargate</div>
<div class="kb-diagram-note">Dockerfile 작성 → 테스트 → 스테이징 → 운영</div>
<div class="kb-diagram-note">ALB 생성 → ECS Service 연결</div>
<div class="kb-diagram-note">Week 9-10: WAF 적용</div>
<div class="kb-diagram-note">OWASP Top 10 규칙 활성화</div>
<div class="kb-diagram-note">Week 11-12: 모니터링 최적화</div>
<div class="kb-diagram-note">RDS Performance Insights, CloudWatch 대시보드</div>
<div class="kb-diagram-note">결과:</div>
<div class="kb-diagram-note">가용성: 99.5% → 99.95% (멀티 AZ RDS)</div>
<div class="kb-diagram-note">DB 관리 시간: DBA 40시간/월 → 5시간/월</div>
<div class="kb-diagram-note">인프라 비용: $8,000/월 → $5,500/월 (-31%)</div>
<div class="kb-diagram-note">스케일링: 수동 → 오토스케일링 (트래픽 5배 급증 자동 대응)</div>
</div>
</div>



> 📢 **섹션 요약 비유**: Re-platform은 집 수리 공정표 — 전기(DB), 수도(캐시), 방화([WAF](/knowledge-base/studynote/03_network/13_network_security_basics/696_waf_web_application_firewall/)) 공사를 순서대로 하나씩 [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/). 동시에 다 하면 집에서 못 살아요.

---

## 📌 관련 개념 맵



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Re-platform</div>
<div class="kb-diagram-note">+-- 6R 위치</div>
<div class="kb-diagram-note">+-- Rehost → Re-platform → Re-architect</div>
<div class="kb-diagram-note">+-- 주요 패턴</div>
<div class="kb-diagram-note">+-- DB → RDS (DMS 마이그레이션)</div>
<div class="kb-diagram-note">+-- 앱 서버 → ECS/EKS</div>
<div class="kb-diagram-note">+-- Redis → ElastiCache</div>
<div class="kb-diagram-note">+-- Nginx → ALB + WAF</div>
<div class="kb-diagram-note">+-- 도구</div>
<div class="kb-diagram-note">+-- AWS DMS, SCT</div>
<div class="kb-diagram-note">+-- ECS Fargate, EKS</div>
<div class="kb-diagram-note">+-- 이점</div>
<div class="kb-diagram-note">+-- 운영 부담 감소</div>
<div class="kb-diagram-note">+-- 자동 HA/백업</div>
<div class="kb-diagram-note">+-- 비용 15~30% 절감</div>
</div>
</div>



---

## 📈 관련 키워드 및 발전 흐름도

```
[클라우드 도입 초기 (2010~)]
Rehost(리프트앤시프트) 중심
빠른 데이터센터 이전
      |
      v
[관리형 서비스 확대 (2013~)]
RDS, ElastiCache, SQS 성숙
Re-platform 경제성 확보
      |
      v
[컨테이너 혁명 (2014~)]
Docker, Kubernetes 등장
ECS/EKS Re-platform 표준화
      |
      v
[서버리스 Re-platform (2017~)]
Fargate, Lambda
서버 관리 완전 제거
      |
      v
[현재: AI/ML 관리형 서비스]
SageMaker, Vertex AI
AI 인프라 Re-platform
FinOps + 지속적 최적화
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. Re-platform은 집 리모델링 — 집 구조(앱 로직)는 그대로이지만, 낡은 보일러(DB)를 관리 편한 지역난방(RDS)으로 교체해요!
2. RDS는 DB를 전문 관리 회사에 맡기는 것 — [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/), 보안 패치, 이중화를 AWS가 자동으로 해줘서 [DBA](/knowledge-base/studynote/05_database/01_db_architecture_relational/025_dba_database_administrator/) 걱정이 줄어요.
3. 단계적으로 [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/) — 한 번에 모든 것을 바꾸면 위험하니까, 하나씩 천천히 교체해야 안전해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 42 / 371

← **이전**: [042. Rehost — Lift & Shift 마이그레이션](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/042_rehost_lift_and_shift_migration/)
**다음**: [044. Re-factor & Re-architect — 클라우드 네이티브 MSA](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/044_refactor_re_architect_cloud_native_msa/) →

---
