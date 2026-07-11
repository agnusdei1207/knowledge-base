---
title: "시스템·응용 소프트웨어 키워드 워크리스트"
date: "2026-07-01"
tags:
  - "cspe-keywords"
weight: 1
---

# 3. 시스템·응용 소프트웨어 출제동향 키워드 (목표 320개)

> 출처: 120~138회 기출 + frequency.md + 공식 8대영역 + 전망. 개인 학습 목록 미사용.

## 운영체제 (Operating System)

001. 프로세스 vs 스레드 (Process vs Thread) [출제:120회]
002. PCB·컨텍스트 스위칭 (PCB Context Switching) [출제:120회]
003. 프로세스 생성·종료·상태 전이 (Process Lifecycle)
004. 프로세스 스케줄링 알고리즘 — FCFS·SJF·RR·MLFQ·CFS (Process Scheduling) [출제:122,129,131,138회]
005. 멀티레벨 피드백 큐 MLFQ (Multilevel Feedback Queue) [출제:138회]
006. CFS 완전 공정 스케줄러 (Completely Fair Scheduler) [출제:138회]
007. 실시간 스케줄링 — Rate Monotonic·EDF (Real-Time Scheduling) [출제:137회]
008. 스레드 스케줄링·스레드 풀 (Thread Scheduling Thread Pool)
009. 교착상태 조건·예방·회피·탐지·복구 (Deadlock) [출제:121,131,132,134,136회]
010. 은행원 알고리즘 (Banker's Algorithm) [출제:124회]
011. 기아·에이징 (Starvation Aging) [출제:138회]
012. 세마포어·뮤텍스·모니터 (Semaphore Mutex Monitor) [출제:125,126,132회]
013. 스핀락 vs 뮤텍스 (Spinlock vs Mutex) [출제:123회]
014. 임계 구역·상호 배제 (Critical Section Mutual Exclusion)
015. 프로세스 스레싱 (Process Thrashing) [출제:129,131회]
016. 가상 메모리·페이징·세그멘테이션 (Virtual Memory) [출제:120,121,125,126회]
017. 페이지 교체 알고리즘 (Page Replacement) [출제:121회]
018. 워킹 셋·페이지 폴트 (Working Set Page Fault) [출제:131회]
019. 다중프로그래밍·다중처리 (Multiprogramming Multiprocessing)
020. 가상화 — Type 1·Type 2 하이퍼바이저 (Virtualization Hypervisor) [출제:128,131,132,137회]
021. 전가상화·반가상화·컨테이너 비교 (Full Para Container Virtualization) [출제:137회]
022. 파일 시스템 — FAT·NTFS·ext4·APFS (File System)
023. 파일 시스템 저널링 (File System Journaling)
024. I/O 관리·디스크 스케줄링 (I/O Management Disk Scheduling)
025. UNIX 커널·쉘·파일시스템 3요소 (UNIX Kernel Shell) [출제:125회]
026. 마이크로커널 vs 모놀리식 커널 (Microkernel vs Monolithic) [출제:138회]
027. 가상 스레드 — Java Project Loom (Virtual Thread) [출제:138회]
028. 비동기 I/O·이벤트 루프 (Async I/O Event Loop) [출제:138회]
029. 리액티브 프로그래밍 (Reactive Programming) [전망]
030. 다중 프로세서 스케줄링 — SQMS·MQMS (Multiprocessor Scheduling SQMS MQMS) [출제:129회]
031. NUMA 인지 스케줄링 (NUMA-aware Scheduling) [전망]

## 소프트웨어 공학 (Software Engineering)

032. 소프트웨어 개발 생명주기 SDLC (Software Development Lifecycle)
033. 폭포수 모델 vs 애자일 (Waterfall vs Agile) [출제:121회]
034. 애자일 스크럼 (Agile Scrum) [출제:121,134회]
035. SAFe 대규모 애자일 프레임워크 (Scaled Agile Framework) [출제:122,134,137회]
036. XP — 페어 프로그래밍·TDD (Extreme Programming) [출제:129회]
037. 칸반 (Kanban) [전망]
038. 애자일 DORA 메트릭 (DORA Metrics) [출제:124회]
039. 요구사항 분석·명세 (Requirements Analysis)
040. UML 다이어그램 유형 (UML Diagrams)
041. 소프트웨어 아키텍처 패턴 — MVC·MSA·이벤트드리븐 (Architecture Patterns) [출제:120회]
042. 마이크로서비스 아키텍처 MSA (Microservice Architecture) [출제:120,121,123,135회]
043. MSA 분해 전략 — 도메인 주도 설계 (MSA Decomposition DDD) [출제:136회]
044. API 게이트웨이 (API Gateway) [출제:120회]
045. 서킷 브레이커 패턴 (Circuit Breaker Pattern) [출제:136회]
046. 서비스 메시 — Istio·Envoy (Service Mesh) [출제:123,136,138회]
047. 이벤트 소싱·CQRS (Event Sourcing CQRS) [출제:121회]
048. Saga 패턴 — 분산 트랜잭션 (Saga Pattern) [출제:121회]
049. 12 팩터 앱 (12 Factor App) [출제:123회]
050. SOLID 원칙 (SOLID Principles) [출제:121,128,132회]
051. 디자인 패턴 — GoF 23종 (Design Patterns GoF)
052. 헥사고날 아키텍처 — 포트·어댑터 (Hexagonal Architecture) [출제:127회]
053. DDD 도메인 주도 설계 (Domain-Driven Design) [출제:127,137회]
054. 바운디드 컨텍스트 (Bounded Context) [출제:137회]
055. 애그리게이트·이벤트 스토밍 (Aggregate Event Storming) [출제:127회]
056. 서버리스 아키텍처 패턴 (Serverless Architecture Pattern) [출제:130,136회]
057. 모놀리식 vs 마이크로서비스 비교 (Monolith vs Microservice) [출제:135회]
058. 형상 관리 — Git·브랜치 전략 (Configuration Management Git) [출제:121회]
059. CI/CD 파이프라인 (CI/CD Pipeline) [출제:120,121회]
060. 지속적 배포 Continuous Deployment (Continuous Deployment) [출제:138회]
061. GitOps (GitOps) [출제:136회]
062. DevOps 파이프라인 (DevOps Pipeline) [출제:120회]
063. DevSecOps (DevSecOps) [출제:128,134,135,136회]
064. 소프트웨어 테스트 — 단위·통합·시스템·인수 (Software Testing) [출제:120회]
065. 테스트 주도 개발 TDD (Test-Driven Development) [출제:129회]
066. 화이트박스·블랙박스 테스트 (White-box Black-box Testing)
067. 테스트 커버리지 — 구문·분기·조건·경로·MC/DC (Test Coverage) [출제:136회]
068. 뮤테이션 테스트 (Mutation Testing) [전망]
069. 알파·베타·인수 테스트 (Alpha Beta Acceptance Testing) [출제:129회]
070. 카나리 배포·블루-그린 배포 (Canary Blue-Green Deployment) [출제:132,138회]
071. 피처 플래그 (Feature Flag) [출제:138회]
072. 소프트웨어 리팩터링·기술부채 (Refactoring Technical Debt) [출제:123,129,130회]
073. 코드 스멜 (Code Smell) [출제:130회]
074. 소프트웨어 기술부채 사분면 (Technical Debt Quadrant) [출제:123회]
075. 정적 분석 SAST (Static Application Security Testing) [출제:128,135회]
076. 동적 분석 DAST (Dynamic Application Security Testing) [출제:128,135회]
077. 소프트웨어 품질 ISO/IEC 25010 (Software Quality ISO 25010) [출제:120,128회]
078. CMMI 프로세스 성숙도 모델 (CMMI Maturity Model) [출제:122,125회]
079. ATAM 아키텍처 트레이드오프 분석 (ATAM) [출제:121,131회]
080. CBAM 비용-편익 분석 (CBAM) [출제:131회]
081. SW 기능점수 FP 측정 (Function Point) [출제:126회]
082. SW 기능점수 간이법·정통법 (FP Estimation Method) [출제:126회]
083. COCOMO 비용 산정 (COCOMO)
084. 소프트웨어 대가산정 (SW Cost Estimation) [출제:135,138회]
085. 아키텍처 결정 기록 ADR (Architecture Decision Record) [출제:133회]
086. 소프트웨어 안전 — GAMAB·ALARP (Software Safety GAMAB ALARP) [출제:128회]
087. 기능 안전 ISO 26262·ASIL (Functional Safety ISO 26262) [출제:134회]
088. ISO 29119 테스트 설계 (ISO 29119 Test Design) [출제:128회]
089. SP 소프트웨어 프로세스 품질 인증 (SP Quality Certification) [출제:134회]
090. AI 코드 생성 — GitHub Copilot (AI Code Generation) [출제:133회]
091. 생성형 AI 기반 DevOps 자동화 (GenAI DevOps Automation) [출제:133회]
092. 플랫폼 엔지니어링 IDP (Platform Engineering IDP) [출제:133,134,135회]
093. 내부 개발자 플랫폼 골든 패스 (Internal Developer Platform Golden Path) [출제:135회]

## 데이터베이스 (Database)

094. 관계형 데이터베이스 기본 — 릴레이션·키·제약조건 (Relational Database)
095. 트랜잭션 ACID (Transaction ACID) [출제:120,129,131회]
096. 트랜잭션 격리 수준 4단계 (Transaction Isolation Levels) [출제:120,136,138회]
097. Dirty Read·Non-Repeatable Read·Phantom Read (Read Anomalies) [출제:136회]
098. MVCC 다중 버전 동시성 제어 (MVCC) [출제:136회]
099. 락 관리 — 2단계 잠금 프로토콜 (2PL Two-Phase Locking)
100. 데이터베이스 정규화 1NF~BCNF (Database Normalization) [출제:120,135회]
101. 반정규화·성능 트레이드오프 (Denormalization) [출제:135회]
102. 이상 현상 — 삽입·삭제·갱신 (Update Anomaly)
103. 데이터베이스 무결성 제약 조건 (Database Integrity Constraints) [출제:128,134회]
104. 개체 무결성·참조 무결성 (Entity Referential Integrity) [출제:128회]
105. SQL 기본 — DML·DDL·DCL (SQL DML DDL DCL)
106. 인덱스 구조 — B+Tree·해시·복합 (Index Structure) [출제:122,135,137회]
107. 클러스터드 인덱스·커버링 인덱스 (Clustered Covering Index) [출제:137회]
108. 실행 계획·쿼리 최적화 (Query Execution Plan Optimization) [출제:137회]
109. 조인 알고리즘 — NLJ·Hash Join·Merge Join (Join Algorithms) [출제:137회]
110. B-Tree vs LSM-Tree 비교 (B-Tree vs LSM-Tree) [출제:137회]
111. 파티셔닝 — 범위·해시·리스트 (Partitioning)
112. 샤딩 — 수평 분할 (Sharding) [출제:123회]
113. 데이터베이스 복제 — 마스터-슬레이브·멀티마스터 (Database Replication)
114. 캐시 계층 — Redis·Memcached (Cache Layer)
115. 데이터베이스 용량 산정 (DB Capacity Planning) [출제:131회]
116. NoSQL 유형 — 문서·키값·컬럼·그래프 (NoSQL Types) [출제:121,131,137회]
117. CAP 정리 (CAP Theorem) [출제:121,131회]
118. PACELC 정리 (PACELC Theorem) [출제:136회]
119. BASE vs ACID (BASE vs ACID) [출제:121,131회]
120. 최종 일관성 (Eventual Consistency) [출제:136회]
121. CRDT 충돌 없는 복제 데이터 (Conflict-free Replicated Data Type) [출제:124회]
122. MongoDB 도큐먼트 DB (MongoDB Document Database) [출제:137회]
123. Redis 인메모리 DB (Redis In-Memory Database) [출제:137회]
124. Cassandra 컬럼 패밀리 DB (Cassandra Column Family) [출제:137회]
125. Neo4j 그래프 DB (Neo4j Graph Database) [출제:124,137,138회]
126. 시계열 데이터베이스 (Time Series Database)
127. 데이터 독립성 — 논리·물리 (Data Independence) [출제:128회]
128. 3단계 스키마 — 외부·개념·내부 (Three-Level Schema) [출제:128회]
129. 클라우드 DB — RDS·Aurora·DynamoDB 비교 (Cloud Database) [출제:138회]
130. 분산 데이터베이스 (Distributed Database) [출제:124회]
131. NewSQL — CockroachDB·Spanner (NewSQL) [전망]
132. DB 커서·키셋 페이지네이션 (Cursor Keyset Pagination) [출제:133회]

## 빅데이터·데이터 엔지니어링 (Big Data)

133. 빅데이터 분산 처리 — Hadoop·MapReduce·HDFS (Hadoop MapReduce) [출제:120회]
134. Apache Spark (Apache Spark) [출제:120회]
135. 람다 아키텍처 (Lambda Architecture) [출제:120회]
136. 카파 아키텍처 (Kappa Architecture) [출제:121회]
137. Apache Kafka 이벤트 스트리밍 (Apache Kafka) [출제:124,136회]
138. Apache Flink 스트림 처리 (Apache Flink) [출제:136회]
139. 정확히 한 번 처리 Exactly-Once (Exactly-Once Semantics) [출제:136회]
140. 실시간 스트리밍 플랫폼 (Real-Time Streaming Platform) [출제:136회]
141. 변경 데이터 캡처 CDC (Change Data Capture) [출제:136회]
142. 데이터 웨어하우스 (Data Warehouse)
143. 데이터 레이크 (Data Lake) [출제:122회]
144. 데이터 레이크하우스 (Data Lakehouse) [출제:127,130,137회]
145. Delta Lake (Delta Lake) [출제:127,130,137회]
146. Apache Iceberg (Apache Iceberg) [출제:127,137회]
147. Apache Hudi (Apache Hudi) [전망]
148. 오픈 테이블 포맷 비교 (Open Table Format) [출제:137회]
149. 메달리온 아키텍처 (Medallion Architecture) [전망]
150. 데이터 메시 (Data Mesh) [출제:123,135회]
151. 데이터 패브릭 (Data Fabric) [출제:135,136회]
152. 데이터 카탈로그 (Data Catalog) [출제:121,136회]
153. 데이터 계보 Data Lineage (Data Lineage) [출제:136회]
154. 데이터 거버넌스 (Data Governance) [출제:121,136회]
155. 마스터 데이터 관리 MDM (Master Data Management) [출제:121회]
156. 데이터 품질 관리 — 완전성·정확성·일관성 (Data Quality Management) [출제:136회]
157. ETL·ELT 파이프라인 (ETL ELT Pipeline)
158. 데이터 파이프라인 오케스트레이션 — Airflow (Data Pipeline Orchestration)
159. 데이터 계약 (Data Contract) [전망]
160. 데이터 제품 (Data Product) [전망]

## 클라우드·컨테이너 (Cloud)

161. 클라우드 서비스 모델 — IaaS·PaaS·SaaS (Cloud Service Models) [출제:120,121,125,131,132회]
162. 클라우드 배포 모델 — 퍼블릭·프라이빗·하이브리드·멀티 (Cloud Deployment Models)
163. 멀티 클라우드 전략 (Multi Cloud Strategy) [출제:135회]
164. 하이브리드 클라우드 (Hybrid Cloud) [출제:135회]
165. 클라우드 공유 책임 모델 (Shared Responsibility Model) [출제:137회]
166. 클라우드 마이그레이션 6R (Cloud Migration 6R) [출제:121,138회]
167. FinOps 클라우드 비용 최적화 (FinOps) [출제:123,127,135,136회]
168. 예약 인스턴스·스팟 인스턴스 (Reserved Spot Instance) [출제:130,135회]
169. 오토 스케일링 HPA·VPA (Auto Scaling HPA VPA)
170. Docker 컨테이너 (Docker Container) [출제:120,128,131,132회]
171. VM vs 컨테이너 비교 (VM vs Container) [출제:128,131,132,137회]
172. 컨테이너 런타임 — containerd·CRI-O (Container Runtime)
173. 쿠버네티스 아키텍처 (Kubernetes Architecture) [출제:122,135,136,137회]
174. 쿠버네티스 Pod 생명주기 (Kubernetes Pod Lifecycle) [출제:123회]
175. 쿠버네티스 Pod 스케줄링 (Kubernetes Pod Scheduling) [출제:135회]
176. 쿠버네티스 서비스·인그레스 (Kubernetes Service Ingress) [출제:130,137회]
177. 쿠버네티스 NetworkPolicy·CNI (Kubernetes NetworkPolicy CNI) [출제:127,130,137회]
178. 쿠버네티스 스토리지 — PVC·PV·StorageClass (Kubernetes Storage) [출제:133회]
179. StatefulSet (StatefulSet) [출제:133회]
180. 컨테이너 보안 — Seccomp·AppArmor·OPA (Container Security) [출제:121,130,136회]
181. Rootless 컨테이너 (Rootless Container) [출제:130회]
182. 서버리스 컴퓨팅·FaaS (Serverless FaaS) [출제:120,122,136회]
183. 서비스 메시 Istio (Service Mesh Istio) [출제:123,136,138회]
184. eBPF 네트워크 관측 (eBPF) [전망]
185. Cilium CNI (Cilium) [전망]
186. WASM 서버사이드 (WebAssembly Server-side) [출제:133,136회]
187. WASI (WASI) [전망]
188. 클라우드 네이티브 관측성 — 메트릭·로그·트레이싱 (Cloud Native Observability) [출제:133,135회]
189. OpenTelemetry (OpenTelemetry) [출제:135회]
190. 분산 추적 (Distributed Tracing) [출제:127,135회]
191. SRE 사이트 신뢰성 공학 (Site Reliability Engineering) [출제:137회]
192. SLO·SLA·SLI (SLO SLA SLI) [출제:123,137회]
193. 오류 예산 Error Budget (Error Budget) [출제:137회]
194. AIOps (AIOps) [출제:137회]
195. 클라우드 네이티브 보안 4C (Cloud Native Security 4C) [출제:136회]
196. CNAPP (Cloud Native Application Protection Platform) [출제:127회]
197. 소버린 클라우드 (Sovereign Cloud) [출제:138회]
198. 클라우드 회귀 (Cloud Repatriation) [전망]

## 소프트웨어 개발 방법론 및 품질 (Methods & Quality)

199. SOAP vs REST 비교 (SOAP vs REST) [출제:135회]
200. RESTful API 설계 원칙 (RESTful API Design) [출제:122회]
201. GraphQL (GraphQL) [전망]
202. gRPC (gRPC) [전망]
203. OAuth 2.0·OIDC (OAuth 2.0 OIDC) [출제:123회]
204. OpenAPI·Swagger (OpenAPI Swagger)
205. API 버저닝 전략 (API Versioning)
206. 메시지 큐 — RabbitMQ·ActiveMQ (Message Queue)
207. 이벤트 기반 아키텍처 (Event-Driven Architecture) [전망]
208. 분산 시스템 일관성 모델 (Distributed System Consistency) [출제:136회]
209. 분산 합의 — Raft·Paxos (Distributed Consensus Raft Paxos)
210. gRPC·Protocol Buffers (gRPC Protocol Buffers) [전망]
211. 웹 소켓·Server-Sent Events (WebSocket SSE) [전망]
212. 마이크로서비스 사가 패턴 vs 2PC (Saga vs 2PC) [출제:121회]
213. 서비스 디스커버리 (Service Discovery)
214. 로드 밸런싱 전략 (Load Balancing Strategy)
215. 캐싱 전략 — Cache-Aside·Write-Through (Caching Strategy)
216. CDN 콘텐츠 전송 네트워크 (CDN Content Delivery Network) [출제:122회]
217. 프록시·리버스 프록시 (Proxy Reverse Proxy)
218. 레이트 리미팅·스로틀링 (Rate Limiting Throttling)
219. 불변 인프라 (Immutable Infrastructure) [전망]
220. IaC 인프라스트럭처 코드 (Infrastructure as Code)
221. Terraform·Pulumi (Terraform Pulumi)
222. Ansible·Chef·Puppet (Ansible Chef Puppet)
223. 소프트웨어 라이선스 — GPL·MIT·Apache (Software License) [출제:127회]
224. 오픈소스 컴플라이언스 (Open Source Compliance) [출제:127회]
225. SBOM 소프트웨어 자재명세서 (SBOM) [출제:128,130,134,135,138회]
226. VEX 취약점 악용 가능성 교환 (VEX) [출제:138회]
227. SLSA 공급망 보안 프레임워크 (SLSA) [전망]
228. 소프트웨어 공급망 보안 (Software Supply Chain Security) [출제:128,130,134,135회]
229. 소프트웨어 품질 평가 시험 — TTA (TTA SW Quality Test) [출제:126,134회]
230. ISMP 정보화 마스터플랜 (ISMP) [출제:125,128,132,135회]
231. ISP 정보화 전략 계획 (ISP Information Strategy Planning) [출제:120,121회]
232. EA 전사적 아키텍처 (Enterprise Architecture) [출제:125,128,132,134,135회]
233. TOGAF 아키텍처 프레임워크 (TOGAF) [출제:124회]
234. 범정부 EA 참조 모형 TRM·DRM (Government EA TRM DRM) [출제:135회]
235. PMO 프로젝트 관리 위탁 (PMO) [출제:132회]
236. 소프트웨어 사업 영향 평가 (SW Business Impact Assessment) [출제:128,131,132회]
237. 공공 SW 분리 발주 (SW Separate Procurement) [출제:124회]
238. SW 조달 — 상용SW 직접구매 (SW Direct Purchase) [출제:126,129회]
239. 디지털 전환 DX (Digital Transformation) [출제:121회]
240. 디지털 접근성 — WCAG 2.1 (Digital Accessibility WCAG) [출제:137회]
241. 소프트웨어 그린 엔지니어링 SCI 지수 (Green Software SCI) [출제:133,137회]
242. 탄소 인지 소프트웨어 (Carbon-Aware Software) [전망]
243. 사이버 레질리언스 — 예방·감지·대응·복구 (Cyber Resilience) [출제:130,137회]
244. 재해 복구 RTO·RPO (Disaster Recovery RTO RPO) [출제:121회]
245. 고가용성 설계 — Active-Active·Active-Standby (High Availability Design) [출제:130,137회]
246. 단일 장애점 SPOF 제거 (SPOF Elimination) [출제:137회]
247. 자동 페일오버 (Auto Failover) [출제:137회]
248. 멱등성 설계 (Idempotency Design) [출제:130회]
249. 이벤트 소싱 패턴 (Event Sourcing Pattern) [출제:121회]
250. Outbox 패턴 (Outbox Pattern) [전망]

## AI 응용 소프트웨어 개발

251. MLOps 파이프라인 (MLOps Pipeline) [출제:135,137회]
252. LLMOps (LLMOps) [출제:136,138회]
253. 피처 스토어 (Feature Store) [출제:135회]
254. 모델 레지스트리 (Model Registry) [출제:135회]
255. 실험 추적 — MLflow·W&B (Experiment Tracking) [전망]
256. 모델 모니터링·드리프트 감지 (Model Monitoring Drift Detection) [출제:124,135회]
257. 카나리 모델 배포 (Canary Model Deployment) [전망]
258. 섀도 배포 (Shadow Deployment) [전망]
259. A/B 테스트 모델 평가 (A/B Testing Model Evaluation) [출제:124회]
260. LLM 기반 서비스 개발 — RAG 구현 (LLM Service Development) [출제:136회]
261. AI 코드 생성 보안 취약점 (AI Code Security Vulnerabilities) [출제:133회]
262. AI 기반 테스트 자동화 (AI Test Automation) [전망]
263. AI 기반 로그 분석 (AI Log Analysis) [전망]
264. Vector Lakehouse (Vector Lakehouse) [전망]
265. 온디바이스 AI 모델 배포 — TFLite·ONNX (On-Device Model Deployment) [출제:130,134회]
266. RPA 로보틱 프로세스 자동화 (RPA Robotic Process Automation) [출제:131회]
267. Low-Code·No-Code 플랫폼 (Low-Code No-Code) [전망]
268. AI 네이티브 애플리케이션 (AI-Native Application) [전망]
269. 초개인화 서비스 (Hyper-Personalization Service) [출제:138회]

## 추가 SW 키워드

270. 컴파일러·인터프리터 비교 (Compiler vs Interpreter)
271. JIT 컴파일 (Just-In-Time Compilation)
272. 가비지 컬렉션 알고리즘 (Garbage Collection)
273. 메모리 누수·힙 오버플로우 (Memory Leak Heap Overflow)
274. 스레드 안전 프로그래밍 (Thread-Safe Programming)
275. 불변 객체·함수형 프로그래밍 (Immutable Object Functional Programming)
276. 리액티브 스트림 (Reactive Streams) [전망]
277. WebSocket 실시간 통신 (WebSocket Real-Time)
278. 소프트웨어 리팩터링 패턴 (Refactoring Patterns) [출제:129,130회]
279. 기술부채 측정·관리 (Technical Debt Measurement) [출제:123회]
280. 소프트웨어 형상 관리 기준선 (Software Baseline Configuration) [출제:121회]
281. 소프트웨어 변경 관리 프로세스 (Change Management Process)
282. 빌드 자동화 — Maven·Gradle (Build Automation)
283. 패키지 관리 — npm·pip·Maven (Package Manager)
284. 컨테이너 이미지 보안 스캔 — Trivy (Container Image Security Scan) [출제:130,136회]
285. OPA 정책 엔진 (Open Policy Agent) [출제:136회]
286. Falco 런타임 보안 (Falco Runtime Security) [출제:130회]
287. Seccomp·AppArmor (Seccomp AppArmor) [출제:130회]
288. DORA 메트릭 — 배포 빈도·변경 실패율·복구 시간 (DORA Metrics) [출제:124회]
289. SRE 온콜 관리·인시던트 대응 (SRE Oncall Incident Management) [출제:137회]
290. 카오스 엔지니어링 (Chaos Engineering) [전망]
291. 의존성 취약점 스캔 (Dependency Vulnerability Scanning) [출제:130회]
292. 비밀 관리 — Vault·AWS Secrets Manager (Secrets Management) [출제:130회]
293. 아티팩트 서명·검증 (Artifact Signing Verification) [출제:130회]
294. 재현 가능 빌드 (Reproducible Build) [전망]
295. 플랫폼 엔지니어링 셀프서비스 (Platform Engineering Self-Service) [출제:133,134,135회]
296. Backstage 개발자 포털 (Backstage Developer Portal) [출제:130회]
297. 소프트웨어 아키텍처 4+1 뷰 (4+1 View Model)
298. TOGAF ADM (TOGAF ADM) [출제:124회]
299. 미들웨어 — ESB·MOM·Message Broker (Middleware ESB MOM)
300. 웹 서비스 보안 — SAML·JWT (Web Service Security SAML JWT)
301. REST API 보안 — API Key·OAuth·mTLS (REST API Security)
302. 마이크로프론트엔드 아키텍처 (Micro Frontend) [전망]
303. BFF 백엔드 포 프론트엔드 (Backend for Frontend Pattern) [전망]
304. 사이드카 패턴 (Sidecar Pattern) [출제:136,138회]
305. 앰배서더 패턴 (Ambassador Pattern) [전망]
306. 스트랭글러 패턴 (Strangler Fig Pattern) [출제:123회]
307. 피처 토글·실험 플랫폼 (Feature Toggle Experimentation) [출제:138회]
308. 프로그레시브 딜리버리 (Progressive Delivery) [전망]
309. 소프트웨어 아키텍처 품질 속성 트레이드오프 (Architecture Quality Tradeoff) [출제:120,121회]
310. 운영 프로파일 기반 테스트 (Operational Profile Testing)
311. 비기능 요구사항 — 성능·보안·가용성·확장성 (Non-Functional Requirements)
312. 성능 테스트 지표 — TPS·응답시간·동시 사용자 (Performance Test Metrics) [출제:131회]
313. 부하 테스트·스트레스 테스트·소크 테스트 (Load Stress Soak Testing)
314. APM 애플리케이션 성능 관리 (Application Performance Management) [출제:137회]
315. 소프트웨어 기술성 평가 (SW Technology Evaluation) [출제:132,137회]
316. BMT 벤치마크 테스트 (Benchmark Test BMT) [출제:123,127,129회]
317. 지능정보화 기본법 적용 (Intelligent Information Act) [출제:131회]
318. 소프트웨어 진흥법 (Software Promotion Act) [출제:124,126,129회]
319. AI 소프트웨어 감리 점검 항목 (AI Software Audit) [출제:130,133,135회]
320. 디지털 서비스 성숙도 모형 (Digital Service Maturity Model) [출제:138회]
