---
title: "컴퓨터시스템응용기술사 핵심 키워드 1000"
date: "2026-06-30"
tags:
  - "exam-keywords"
  - "cspe"
weight: 50
---

## Ⅰ. 개요

- **정의**: 본 문서는 컴퓨터시스템응용기술사 120~138회 기출, 빈도 분석, 최신 공개 기출, 출제기준·출제동향을 기준으로 약 **1,000개** 내외의 답안형 키워드를 압축한 마스터 세트이다.
- **필요성**: 개인 학습용 CS 노트 범위가 아니라, 실제 시험에서 1교시 단답과 2~4교시 서술로 전환 가능한 빈출·비교·구조·설계형 키워드를 우선 회독하기 위함이다.
- **점검 결과(2026-06-30)**: 쉼표 기준 보수 집계로 **975개**, 중복 정규화 기준 **908개** 수준이다. 따라서 사용 목표인 "1천여 개, 2천개 미만" 조건을 충족한다.
- **활용 원칙**:
  1. **1교시 단답형**: 정의 1문장 + 핵심 3포인트로 즉시 전환 가능한 정의형·구조형 키워드를 본다.
  2. **2~4교시 서술형**: 구조도 + 비교표 + 적용 방안으로 확장 가능한 비교형·설계형 키워드를 본다.
  3. 각 과목 TOP★ 키워드는 한 줄 **답안 각(answer pointer)** 으로 골격을 먼저 잡는다.
  4. 상세 학습 자료와 별개로, 본 문서는 시험 답안 전환 가능성을 기준으로 운영한다.

## Ⅰ-1. 기출·출제기준·미래 예측 반영 점검

| 점검 축 | 반영 상태 | 답안 관점 판단 |
|:---|:---|:---|
| Q-net 출제기준(2023~2026) | 필기 과목은 `하드웨어시스템, 소프트웨어시스템에 관한 분석, 설계 및 구현, 그 밖에 컴퓨터 응용에 관한 내용`의 통합 과목 | 본 문서의 01~16은 실제 시험 과목 수가 아니라 답안 준비용 내부 도메인 분류 |
| 120~138회 로컬 기출 | `content/exam/cs/past/`와 `frequency.md`의 반복 키워드 반영 | 캐시, 교착상태, TCP/UDP, VM/컨테이너, 제로트러스트, AI 가속기, LLM/RAG, DevSecOps를 상위 배치 |
| 137~138회 최근 경향 | 온디바이스 AI, HBM, RAG/Fine-tuning, 멀티모달, GPU/NPU, 에이전트형 AI 축 반영 | 최신 문제는 단순 정의보다 `비교표 + 구조도 + 적용 한계`를 요구하므로 TOP★ 답안 각에 우선 편입 |
| 차기 출제 예측 | Agentic AI, MCP, 소버린 클라우드, PQC 전환, CTEM, Green SW, HBM/CXL, QEC 반영 | 미래 예측 키워드는 단독 암기보다 기존 빈출군과 연결해 서술형 확장용으로 사용 |
| 수량 통제 | 975개/908개 수준 | 2,000개 미만 조건 충족. 추가 편입은 기출 확인 후 기존 저빈도 키워드와 교체하는 방식으로 관리 |

> 운영 원칙: 최신 공개 기출이 추가되면 키워드 총량을 늘리지 않고, **저빈도·단순 명칭 키워드 제거 → 신규 고빈도/정책/표준 키워드 교체** 방식으로 1,000개 안팎을 유지한다.

## Ⅱ. 도메인별 압축 배분표

| 내부 도메인 | 목표 키워드 수 | 출제 비중 | 1교시 vs 2~4교시 성격 |
|:---|:--:|:--:|:---|
| 10 인공지능 | 110 | ★★★ | 정의·구조형(LLM/RAG/Transformer) 1교시 + 설계·운영형(MLOps) 서술 |
| 09 보안 | 110 | ★★★ | 정의·위협형 1교시 + 방안·통제 매핑 서술 |
| 04 소프트웨어공학 | 100 | ★★★ | 비교·원칙형(SOLID/패턴) 1교시 + 방법론·아키텍처 서술 |
| 01 컴퓨터구조 | 90 | ★★★ | 정의·구조형(캐시/파이프라인) 1교시 + 성능·병렬 서술 |
| 05 데이터베이스 | 80 | ★★★ | 정의·비교형(ACID/정규화) 1교시 + 튜닝·분산 서술 |
| 02 운영체제 | 80 | ★★★ | 정의·비교형(교착/스케줄링) 1교시 + 알고리즘 서술 |
| 03 네트워크 | 80 | ★★★ | 구조·비교형(TCP/OSI) 1교시 + 라우팅·보안 서술 |
| 13 클라우드 아키텍처 | 70 | ★★ | 정의형(K8s/IaC) 1교시 + 플랫폼 설계 서술 |
| 14 데이터 엔지니어링 | 45 | ★★ | 비교형(ETL/ELT) 1교시 + 파이프라인 설계 서술 |
| 15 DevOps/SRE | 45 | ★★ | 정의형(CI/CD/SLO) 1교시 + 운영체계 서술 |
| 07 엔터프라이즈 시스템 | 45 | ★★ | 비교형(EA/통합) 1교시 + 통합 아키텍처 서술 |
| 12 IT 경영 | 40 | ★★ | 비교형(ISP/ITIL) 1교시 + 거버넌스·산정 서술 |
| 16 빅데이터 | 30 | ★ | 정의형(레이크하우스/CAP) 1교시 + 처리 아키텍처 서술 |
| 08 알고리즘/통계 | 25 | ★ | 정의·비교형(복잡도/정렬) 1교시 중심 |
| 11 IT 설계/감리 | 25 | ★ | 정의형(감리/ATAM) 1교시 + 평가 절차 서술 |
| **합계** | **약 1,000** | — | 1교시 단답 + 2~4교시 서술 통합 회독 |

## Ⅲ. 도메인별 핵심 키워드 (압축본)

### 10. 인공지능

- **탐색·전통 ML 기초**: 튜링 테스트, 전문가 시스템(지식베이스·추론엔진), 퍼지 논리, A*(A-Star) 탐색, 미니맥스·알파베타 가지치기, 몬테카를로 트리탐색(MCTS), 지도/비지도/강화학습, 편향-분산 트레이드오프(과적합·과소적합), 차원의 저주, 교차검증(K-Fold), 하이퍼파라미터, 혼동행렬·정밀도·재현율·F1, ROC-AUC
- **앙상블·핵심 알고리즘**: 앙상블 학습, 배깅(랜덤포레스트), 부스팅(XGBoost·LightGBM), 스태킹, 결정트리(엔트로피·지니), 로지스틱 회귀, K-NN, K-Means(EM), SVM(마진·초평면), 커널 트릭, 나이브 베이즈, PCA·SVD 차원축소, DBSCAN, GMM
- **딥러닝 기초·CNN·RNN**: 퍼셉트론·MLP(XOR 한계), 활성화함수(Sigmoid·ReLU·Softmax), 순전파·역전파(연쇄법칙), 경사하강법(SGD), Adam 옵티마이저, 기울기 소실/폭발, 드롭아웃·배치정규화·조기종료, L1/L2 규제, CNN(합성곱·풀링·스트라이드·패딩), ResNet(잔차연결), 객체탐지(YOLO·R-CNN), 이미지분할(U-Net·Mask R-CNN), RNN·장기의존성, LSTM·GRU, Seq2Seq(인코더-디코더)
- **Transformer·LLM·생성형 AI**: 어텐션 메커니즘(Q·K·V), Transformer, 셀프/멀티헤드 어텐션, 포지셔널 인코딩, 파운데이션 모델, 자기지도학습, 전이학습·파인튜닝, PEFT, LoRA(Low-Rank Adaptation), BERT(인코더·MLM), GPT(디코더·자기회귀), LLM(Large Language Model), 창발능력(Emergent Abilities), 프롬프트 엔지니어링, 퓨샷/제로샷, CoT(Chain-of-Thought), 할루시네이션(Hallucination), RAG(Retrieval-Augmented Generation), 벡터DB·임베딩, 코사인 유사도, Word2Vec, RLHF, 지식증류(Knowledge Distillation), 양자화(Quantization), GAN, 디퓨전 모델(Diffusion), 멀티모달 AI
- **강화학습·MLOps·AI 인프라**: 강화학습·MDP, 가치함수·정책, 탐험-활용 딜레마, Q-Learning, DQN, 정책경사·Actor-Critic, PPO, MLOps(CI/CD/CT), 데이터/컨셉 드리프트, 피처스토어·모델레지스트리, Kubeflow·MLflow, 데이터 병렬·모델 병렬, ZeRO, 연합학습(Federated Learning), XAI(LIME·SHAP), 온디바이스 AI, SLM(Small Language Model), GNN, KV캐시·PagedAttention(vLLM), AI 윤리·편향성, 적대적 예제(Adversarial Attack), AI 거버넌스(EU AI Act), AI 에이전트(Agentic AI)·MCP

**★ TOP 5 답안 각**
- ★ **RAG** — 외부 문서 검색(Retrieve)→프롬프트 주입(Augment)→생성, LLM 환각·최신성 결여 해결, 벡터DB+임베딩 인프라
- ★ **Transformer** — "Attention Is All You Need", 셀프/멀티헤드 어텐션·포지셔널 인코딩으로 RNN 배제·병렬연산 극대화, BERT/GPT 기반
- ★ **할루시네이션** — LLM이 사실 아닌 내용 생성, 방어: RAG·프롬프트 제약·파인튜닝·팩트체커 교차검증
- ★ **CNN** — 합성곱(필터·스트라이드·패딩)+풀링으로 공간정보 보존, ResNet 잔차연결로 기울기소실 파훼
- ★ **앙상블 학습** — 배깅(랜덤포레스트, 분산↓) vs 부스팅(XGBoost, 편향↓), 약분류기 결합으로 성능 강화

### 09. 보안

- **보안 원칙·거버넌스**: 정보보안 3요소 CIA, 최소권한 원칙, 직무분리(SoD), 심층방어(Defense in Depth), 위험관리(식별·분석·평가·대응), 정량적 분석(ALE=ARO×SLE), 위험대응 4전략(회피·전가·완화·수용), 잔여위험, NIST CSF 2.0, 제로 트러스트(Zero Trust, NIST SP 800-207), ZTA, 마이크로 세그멘테이션, Security by Design, 위협모델링(STRIDE·DREAD·PASTA), MITRE ATT&CK
- **암호학·PKI**: 대칭키/비대칭키 암호, 하이브리드 암호, AES(SPN), 블록암호 모드(CBC·CTR·GCM), AEAD, 해시함수(SHA-2·SHA-3), HMAC, salt·키스트레칭(bcrypt·scrypt), RSA(소인수분해), ECC(ECDLP), DH/ECDHE 키교환, 전방비밀성(PFS), TLS 1.3 핸드셰이크, PQC(CRYSTALS-Kyber·Dilithium), 양자위협(Shor·Grover), 동형암호, 영지식증명(ZKP), HSM·TPM, PKI·CA·RA, CRL·OCSP, X.509 인증서, mTLS, 코드서명
- **네트워크 보안**: 방화벽(상태검사·NGFW), DMZ·바스티온, East-West/North-South 트래픽, 네트워크 세그멘테이션(VLAN), NAC(802.1X), IDS/IPS(시그니처·이상탐지), WAF(OWASP CRS), DDoS(볼류메트릭·증폭·SYN Flood), MITM·SSL Stripping·HSTS, ARP/DNS Spoofing·캐시포이즈닝, IPsec(AH·ESP·IKE), SSL VPN, SASE/SSE, 세션 하이재킹·Replay Attack
- **시스템·엔드포인트 보안**: EDR/XDR, 버퍼 오버플로우(스택·힙), NX/DEP·ASLR·Stack Canary, ROP(Return-Oriented Programming), Use-After-Free·Race Condition(TOCTOU), 권한상승(LPE), 루트킷·부트킷, 랜섬웨어(WannaCry), APT, Fileless Malware, Spectre/Meltdown, SGX·TEE·TPM 2.0, 원격증명(Remote Attestation), FDE(BitLocker)·TDE, CVSS·CVE·CWE, 시스템 하드닝(CIS Benchmark)
- **웹·API·인증 보안**: OWASP Top 10, IDOR·접근제어 취약, SQL 인젝션(Blind·Time-based), XSS(반사·저장·DOM), CSP, CSRF·SameSite, SSRF, Log4Shell, JWT(alg:none·HS256/RS256), OAuth 2.0(PKCE), OIDC·ID Token, IAM·SSO, SAML 2.0(IdP·SP), MFA(TOTP·FIDO2/WebAuthn·Passkey), RBAC·ABAC, PAM·특권계정, Kerberos(KDC·TGT·Golden/Silver Ticket), NTLM(Pass-the-Hash)
- **보안운영(SecOps)·법규**: SOC, SIEM(상관분석), SOAR(플레이북), Threat Intelligence(STIX/TAXII), Cyber Kill Chain, 인시던트 대응(NIST 6단계), DFIR·디지털포렌식, Chain of Custody, 침투테스트·버그바운티, 레드/블루/퍼플팀, CTEM, SBOM·공급망 보안, DevSecOps(SAST/DAST/IAST), 개인정보보호(비식별·마이데이터·ISMS-P·PIA), PET(개인정보보호 강화기술)

**★ TOP 5 답안 각**
- ★ **제로 트러스트** — "Never Trust, Always Verify"(NIST SP 800-207), 마이크로 세그멘테이션·측면이동 차단, 경계 소멸 시대 핵심 모델
- ★ **CIA 3요소** — 기밀성(암호화·접근제어)·무결성(해시·전자서명)·가용성(HA·DDoS방어), 모든 보안설계의 출발점
- ★ **OWASP Top 10** — 인젝션(SQLi)·접근제어취약·암호화실패·SSRF 등, 웹 보안 표준 위협 + SAST/DAST/WAF 방어
- ★ **TLS 1.3** — 1-RTT 핸드셰이크, AEAD·PFS 의무화, 취약 알고리즘 제거, 전송계층 기밀성·무결성 보장
- ★ **PKI/PQC** — 공개키 인증서 체계(CA·CRL·OCSP), 양자위협(Shor) 대비 PQC 전환(Kyber/Dilithium)·crypto agility

### 04. 소프트웨어공학

- **프로세스·프로젝트관리**: SDLC, 폭포수·V-모델·나선형(위험분석)·프로토타입, CMMI 5단계, 형상관리(SCM·CCB·베이스라인), 기술부채(Technical Debt), WBS·CPM·PERT, EVM, COCOMO·기능점수(FP), 델파이 기법, 브룩스의 법칙, 위험관리 4단계
- **애자일·DevOps**: 애자일 선언문, 스크럼(PO·SM·스프린트·백로그), 번다운 차트, XP(짝프로그래밍·TDD·리팩토링·CI), 칸반(WIP 제한), 린·MVP, SAFe·LeSS, DevOps, IaC, 지속적 배포(CD), SRE(에러예산·SLI/SLO/SLA), DevSecOps(Shift-Left), MLOps·LLMOps, 플랫폼 엔지니어링(IDP), 옵저버빌리티(Metrics·Logs·Traces), 카오스 엔지니어링, 카나리/블루그린/롤링 배포, GitOps, 12-Factor App, BDD(Given-When-Then)
- **요구공학**: 요구공학(도출·분석·명세·확인·관리), 기능/비기능 요구사항, 유스케이스 다이어그램, DFD·자료사전, SRS, V&V, 인스펙션·워크쓰루, 요구사항 추적성(RTM), 범위 크리프, 골드 플래팅, MoSCoW, 카노 모델(Kano), QFD, 유저스토리 맵·에픽
- **설계·아키텍처·패턴**: 응집도·결합도, 추상화·정보은닉, 4+1 뷰, 계층형·파이프필터·이벤트드리븐(EDA), MVC·MVP·MVVM, SOA·MSA(마이크로서비스), 헥사고날·클린 아키텍처, DDD(바운디드컨텍스트·애그리게이트), CQRS·이벤트소싱, ATAM, UML(클래스·시퀀스·상태·액티비티), SOLID(SRP·OCP·LSP·ISP·DIP), DRY·KISS·YAGNI, GoF 디자인패턴(싱글톤·팩토리·옵저버·전략·데코레이터·프록시·어댑터·퍼사드)
- **구현·품질·테스팅**: OOP 4대특징(캡슐화·상속·다형성·추상화), 함수형 프로그래밍, IoC·DI(의존성주입), AOP, 클린코드·코드스멜, 정적/동적 분석, ISO 25010(SQuaRE) 품질모델, 맥케이브 순환복잡도, 가용성(MTBF/MTTR), 테스팅 7원리(살충제 패러독스), 블랙박스(동등분할·경계값·결정테이블), 화이트박스 커버리지(구문·결정·조건·MC/DC), 단위·통합·시스템·인수테스트, 회귀테스트, 테스트더블(Mock·Stub·Spy·Fake), 성능테스트(부하·스트레스·스파이크), TDD
- **클라우드네이티브·MSA 심화·SW 보안**: 컨테이너·쿠버네티스(Pod·Service·Ingress), 서비스메시(Istio·사이드카), API 게이트웨이·BFF, 서비스 디스커버리, 서킷브레이커·벌크헤드·재시도, 사가(Saga) 패턴(오케스트레이션·코레오그래피)·보상트랜잭션, 2PC 한계, 분산추적(OpenTelemetry), 서버리스·콜드스타트, 모듈러 모놀리스, 스트랭글러 피그, Secure SDLC, STRIDE, SCA·SBOM·공급망 보안, 시크릿 관리(Vault), 가상 스레드, WebAssembly(WASM), AI4SE(Copilot·LangChain·Agentic AI)

**★ TOP 5 답안 각**
- ★ **SOLID** — SRP·OCP·LSP·ISP·DIP, 객체지향 설계 5원칙, 유지보수성·확장성·결합도↓의 근간
- ★ **MSA** — 독립배포·DB per Service, 서킷브레이커·사가패턴·API게이트웨이로 분산 탄력성·트랜잭션 일관성 확보
- ★ **GoF 디자인패턴** — 생성(싱글톤·팩토리)·구조(어댑터·프록시·데코레이터)·행위(옵저버·전략·템플릿메서드), 재사용 설계 해법
- ★ **TDD/테스트 커버리지** — Red-Green-Refactor, 블랙박스(경계값·동등분할)+화이트박스(MC/DC), 품질 좌측이동
- ★ **DevOps/CI·CD** — 문화·자동화·측정·공유, SRE 에러예산, IaC·GitOps·카나리배포로 배포 속도와 안정성 양립

### 01. 컴퓨터구조

- **데이터 표현·논리회로**: 부울대수·카르노맵, 조합/순차 논리회로, 플립플롭, 2의 보수, 부동소수점(IEEE 754·FP32/FP16/bfloat16), 오버플로우·언더플로우, 해밍코드, CRC·체크섬, 빅/리틀 엔디안, ALU
- **성능평가·ISA**: 폰 노이만 아키텍처·병목현상, 하버드 아키텍처, CPI·IPC·MIPS·FLOPS, 성능방정식, 암달의 법칙(Amdahl's Law), 구스타프슨의 법칙, 무어의 법칙·데나드 스케일링, SPEC 벤치마크, ISA, 주소지정방식, RISC vs CISC, x86·ARM·RISC-V, SIMD(AVX·NEON)
- **파이프라이닝·고성능**: 명령어 사이클, 하드와이어드/마이크로프로그래밍 제어, 명령어 파이프라이닝(IF·ID·EX·MEM·WB), 파이프라인 해저드(구조·데이터·제어), RAW·WAR·WAW, 데이터 포워딩, 파이프라인 스톨, 분기예측(정적·동적·BTB·BHT), 수퍼스칼라, 비순차실행(OoO), 레지스터 리네이밍, 토마술로 알고리즘, ROB, VLIW
- **메모리계층·캐시·가상메모리**: 메모리 계층구조, 참조의 지역성(시간·공간), SRAM·DRAM·DDR, 캐시메모리(L1/L2/L3), 적중률·AMAT, 캐시 사상(직접·완전연관·집합연관), 캐시미스 3C, 교체알고리즘(LRU·LFU·FIFO), 쓰기정책(Write-Through·Write-Back)·더티비트, 프리패칭, 가상메모리·MMU, 페이징·페이지테이블, TLB, 세그멘테이션, 단편화(내부·외부), 요구페이징·페이지폴트, 페이지교체(OPT·LRU·클럭), 스래싱·워킹셋
- **병렬·멀티코어·동기화**: 플린의 분류법(SISD·SIMD·MIMD), 벡터 프로세서, 공유/분산 메모리, UMA·NUMA, SMP, 클러스터·그리드 컴퓨팅, TLP·DLP, 멀티코어·big.LITTLE, 동시멀티스레딩(SMT·하이퍼스레딩), 캐시 일관성(Cache Coherence), 스누핑·디렉터리 프로토콜, MESI/MOESI, 거짓공유(False Sharing), 메모리 일관성 모델, Test-and-Set·CAS, 메모리 배리어
- **I/O·스토리지·AI 가속기·HW 보안**: 인터럽트·DMA, 폴링, HDD(탐색시간)·SSD(웨어레벨링·FTL), RAID(0·1·5·6·10), SAN·NAS·DAS, NVMe·NVMe-oF, PCIe·RDMA, GPU·CUDA·SIMT, NPU·TPU(시스톨릭 어레이), 텐서코어, PIM(Processing-In-Memory)·메모리월, CXL·메모리풀링, HBM·칩렛, ECC메모리, DVFS, TEE(TrustZone·SGX)·Secure Boot, 사이드채널공격(Spectre·Meltdown·Rowhammer), 뉴로모픽 컴퓨팅

**★ TOP 5 답안 각**
- ★ **캐시 일관성** — MESI 프로토콜(Modified·Exclusive·Shared·Invalid), 멀티코어 공유데이터 정합성, 스누핑 vs 디렉터리, 거짓공유
- ★ **가상메모리** — MMU·페이징·페이지테이블·TLB로 논리↔물리 변환, 요구페이징·페이지폴트, 스래싱은 워킹셋으로 방어
- ★ **파이프라이닝** — IF/ID/EX/MEM/WB 중첩으로 처리량↑, 3대 해저드(구조·데이터·제어), 포워딩·분기예측·OoO로 해소
- ★ **메모리 계층구조·캐시** — 참조 지역성(시간·공간), 사상(직접·집합연관)·교체(LRU)·쓰기정책(Write-Back), AMAT 성능평가
- ★ **암달의 법칙** — 병렬화 가능 비율이 전체 속도향상 한계 결정, 구스타프슨 법칙과 대비, 멀티코어 정당화 근거

### 05. 데이터베이스

- **모델링·정규화**: 3단계 스키마(ANSI/SPARC), 데이터 독립성, 키(슈퍼/후보/기본/대체/외래), 무결성(개체/참조/도메인), ER 모델, 함수적 종속(부분/이행), 이상현상(삽입/삭제/갱신), 정규화(1NF~BCNF/4NF/5NF), 무손실분해, 반정규화, 논리/물리설계
- **SQL·옵티마이저·인덱스**: 조인(Inner/Outer/Cross/Self), 서브쿼리, 윈도우함수, 뷰/구체화뷰, 인덱스(B+Tree/해시/비트맵/클러스터드/결합), 옵티마이저(RBO/CBO), 실행계획, 조인기법(NL/Sort-Merge/Hash), 선택도·카디널리티, 파티셔닝(Range/Hash/List), 힌트, 바인드변수
- **트랜잭션·동시성·복구**: ACID, 트랜잭션 상태전이, 병행수행 문제(Lost Update/Dirty Read/Phantom), 직렬가능성, 락(S/X-Lock), 2PL(Strict/Rigorous), 타임스탬프 순서, 낙관적 제어, MVCC, 격리수준(4단계), Redo/Undo, WAL, 체크포인트, ARIES, 교착상태(Wait-Die/Wound-Wait), 대기그래프
- **분산·NoSQL·NewSQL**: 분산DB 투명성, 데이터분할(수평/수직), 복제(동기/비동기·Master-Slave), 2PC/3PC, Saga, CAP/PACELC, BASE·결과적일관성, Raft/Paxos, Split Brain, NoSQL 4모델(KV/Document/Column/Graph), 샤딩·샤드키, 일관된 해싱, NewSQL(Spanner), HTAP, LSM-Tree, CDC
- **DW·OLAP·최신**: DW 4특징, 데이터마트·ODS, ETL/ELT, OLTP vs OLAP, OLAP연산(롤업/드릴다운/슬라이스/다이스/피벗), 스타/스노우플레이크 스키마, 데이터레이크·레이크하우스, 스키마 온 리드/라이트, 벡터DB·임베딩, 유사도검색(코사인/L2), ANN/HNSW, RAG, TDE·데이터마스킹, SQL 인젝션

**★ TOP 5 답안 각**
- ★ **정규화(1NF~BCNF)** — 이상현상→FD 분석→단계 분해, 무손실·종속성보존 트레이드오프, 성능 위한 반정규화 절충
- ★ **ACID·격리수준** — 4특성 보장주체(원자성/영속성=회복, 일관성/격리성=병행제어), 격리수준 4단계와 Dirty/Phantom 매핑
- ★ **MVCC** — 스냅샷 기반 읽기-쓰기 무충돌(읽기가 쓰기를 막지 않음), Undo세그먼트 활용, 락 블로킹 완화
- ★ **교착상태** — 4필요조건→예방/회피(은행원)/탐지(대기그래프)/복구, DB는 Wait-Die·Wound-Wait로 희생자 롤백
- ★ **CAP·샤딩** — 분산DB는 C·A·P 중 2개, 분할 시 CP(MongoDB)/AP(Cassandra) 선택, 샤드키 설계로 수평확장

### 02. 운영체제

- **아키텍처·가상화**: 듀얼모드, 시스템콜, 인터럽트(HW/SW/Trap), 커널구조(모놀리식/마이크로/하이브리드), 문맥교환, 하이퍼바이저(Type1/2), 전/반가상화, HW보조 가상화(VT-x), 컨테이너, 네임스페이스, cgroups, 도커
- **프로세스·스레드·IPC**: 프로세스 상태전이, PCB, 스레드(User/Kernel), 멀티스레드 모델(1:1/N:1/N:M), fork/exec, COW, 좀비/고아 프로세스, IPC(공유메모리/메시지전달), 파이프, 소켓, RPC, 시그널
- **CPU 스케줄링**: 선점/비선점, 디스패처, 스케줄링 기준(반환/대기/응답시간), FCFS(호위효과), SJF/SRTF, RR(Time Quantum), 우선순위(기아/Aging), 다단계큐/MLFQ, HRN, 다중처리기(부하균등/친화성), 실시간(RM/EDF), CFS
- **동기화·교착상태**: 경쟁조건, 임계구역(상호배제/진행/한정대기), Peterson, TAS/CAS, 뮤텍스, 스핀락, 세마포어(이진/카운팅), 모니터·조건변수, 생산자-소비자, 독자-저자, 식사철학자, 우선순위역전·상속, 교착상태 4조건, 예방/회피(은행원)/탐지/복구, 안전상태
- **메모리·가상메모리**: 주소바인딩, MMU, 스와핑, 연속할당(First/Best/Worst-Fit), 단편화(내부/외부), 페이징, 페이지테이블(다단계/역), TLB, 세그멘테이션, 요구페이징, 페이지부재, 페이지교체(OPT/FIFO/LRU/Clock/LFU), 벨라디 모순, 스래싱, 워킹셋
- **저장장치·파일시스템**: 디스크접근시간, 디스크스케줄링(FCFS/SSTF/SCAN/C-SCAN/LOOK), SSD/FTL/마모평준화, RAID(0/1/5/6/10), DMA, 블로킹/논블로킹/비동기 I/O, i-node, 파일할당(연속/연결/색인), 저널링/LFS/COW FS, VFS, 접근권한(rwx)

**★ TOP 5 답안 각**
- ★ **CPU 스케줄링** — 선점/비선점, FCFS 호위효과·SJF 최적평균대기·RR 시분할, 기아는 Aging 해결, 실시간 RM(정적)/EDF(동적)
- ★ **교착상태** — 4필요조건(상호배제/점유대기/비선점/순환대기)→예방/회피(은행원·안전상태)/탐지(대기그래프)/복구
- ★ **가상메모리·페이지교체** — 요구페이징으로 물리메모리 초과 실행, LRU근사=Clock(참조비트), 스래싱은 워킹셋·PFF로 조절
- ★ **세마포어·동기화** — 임계구역 3조건, 이진/카운팅 wait(P)/signal(V) 원자연산, 모니터 자동 상호배제, 우선순위역전→상속
- ★ **페이징·TLB** — 논리주소→프레임 매핑, 다단계 페이지테이블로 크기절감, TLB 캐시로 EAT 단축, 내부단편화 트레이드오프

### 03. 네트워크

- **기초·물리·다중화**: 전송방식(단/반/전이중, 동기/비동기), 나이퀴스트/샤논 채널용량, 변조(ASK/FSK/PSK/QAM), PCM, 다중화(FDM/TDM/WDM/OFDM), 다중접속(FDMA/TDMA/CDMA/OFDMA), MIMO·빔포밍, 전송매체(UTP/광섬유)
- **데이터링크·오류제어**: 프레이밍(비트스터핑), 오류검출(패리티/체크섬/CRC), 해밍코드, FEC vs ARQ, ARQ(Stop-and-Wait/GBN/SR), 슬라이딩윈도우, 흐름제어, HDLC, PPP, 피기배킹
- **LAN·2계층 장비**: 이더넷(CSMA/CD), MAC주소, 충돌/브로드캐스트 도메인, 스위치(학습/플러딩), 스위칭방식(컷스루/스토어앤포워드), VLAN(802.1Q), STP/RSTP(BPDU/루트브리지), 링크어그리게이션(LACP), CSMA/CA(RTS/CTS)
- **네트워크계층·IP**: IPv4 헤더, 단편화/MTU/PMTU, TTL, 서브네팅/CIDR/VLSM, NAT/PAT, ARP/RARP/GARP, ICMP(Ping/Traceroute), IPv6(128비트/SLAAC/NDP), IPv4-IPv6 전환(듀얼스택/터널링/NAT64), IGMP·멀티캐스트
- **라우팅·QoS·VPN**: 정적/동적 라우팅, 메트릭/관리거리, AS/IGP/EGP, 거리벡터(RIP) vs 링크상태(OSPF/다익스트라), EIGRP, BGP(경로벡터), MPLS, 터널링(GRE/L2TP), IPsec(AH/ESP/IKE), QoS(IntServ/DiffServ/DSCP), 토큰버킷, VRRP/HSRP
- **전송·응용계층·신기술**: TCP vs UDP, 3-way/4-way handshake, TIME_WAIT, 흐름제어(슬라이딩윈도우/Nagle), 혼잡제어(슬로우스타트/AIMD/빠른재전송·회복), TCP변종(Reno/CUBIC/BBR), QUIC, HTTP(1.1/2/3), HTTPS/TLS, REST/GraphQL/gRPC, DNS, SDN/NFV·서비스메시, Wi-Fi 7·5G/6G·Open RAN

**★ TOP 5 답안 각**
- ★ **OSI 7계층·TCP/IP** — 계층별 역할·PDU·장비 매핑, 캡슐화/역캡슐화, 전송계층 다중화·오류·흐름·혼잡제어
- ★ **TCP 3/4-way handshake** — SYN→SYN/ACK→ACK 연결설정, FIN 4단계 종료, TIME_WAIT(2MSL) 이유, ISN 무작위
- ★ **TCP 혼잡제어** — 슬로우스타트(지수)→ssthresh→혼잡회피(AIMD 선형), 3 Dup-ACK 시 빠른재전송·회복, Reno/CUBIC/BBR
- ★ **서브네팅·CIDR** — 클래스풀 고갈→CIDR 가변길이, AND연산 서브넷 산출, VLSM 효율분할, NAT로 사설IP 공유
- ★ **라우팅 프로토콜** — 거리벡터(RIP, 벨만-포드, Split Horizon) vs 링크상태(OSPF, 다익스트라·SPF), AS간 BGP(경로벡터)

### 13. 클라우드 아키텍처

- **클라우드 모델·가상화**: 클라우드 5대특징(NIST), 서비스모델(IaaS/PaaS/SaaS/FaaS), 배포모델(퍼블릭/프라이빗/하이브리드/멀티), 소버린 클라우드, 엣지컴퓨팅, 멀티테넌시, 하이퍼바이저(Type1/2), VPC, 스케일업/아웃, 오토스케일링, 로드밸런서, 스토리지(블록/파일/오브젝트), CDN, 마이그레이션 6R, 벤더락인, SDN/SDDC, VXLAN·오버레이
- **컨테이너·쿠버네티스**: 컨테이너 vs VM, 네임스페이스/cgroups, 도커(이미지/레이어드FS), OCI/컨테이너런타임, K8s 아키텍처(마스터/워커), Kube-API/etcd/Scheduler/Controller, Kubelet/Kube-proxy, Pod/ReplicaSet/Deployment, StatefulSet/DaemonSet, Service(ClusterIP/NodePort/LoadBalancer), Ingress, HPA/VPA/CA, PV/PVC/CSI, CNI, ConfigMap/Secret, Helm, 프로브(Liveness/Readiness), 선언적 API
- **MSA·서버리스**: 모놀리식 vs MSA, API게이트웨이, 서비스디스커버리, 서킷브레이커/폴백/벌크헤드, DB per Service, 폴리글랏 퍼시스턴스, Saga(보상트랜잭션), 트랜잭셔널 아웃박스, 이벤트소싱, CQRS, EDA, 서비스메시(사이드카/Istio/mTLS), DDD·바운디드컨텍스트, 스트랭글러 피그, 서버리스·콜드스타트
- **DevOps·옵저버빌리티**: DevOps/CALMS, CI/CD, GitOps(ArgoCD), IaC(Terraform·멱등성), 불변인프라, DevSecOps(Shift-Left), SRE·토일, SLI/SLO/SLA, 에러예산, 옵저버빌리티 3요소(메트릭/로그/추적), 골든시그널, 분산추적(OpenTelemetry/Jaeger), 카오스엔지니어링, 무중단배포(롤링/블루그린/카나리), DORA메트릭, FinOps

**★ TOP 5 답안 각**
- ★ **쿠버네티스 아키텍처** — 마스터(API서버/etcd/스케줄러/컨트롤러)+워커(kubelet/proxy), Pod 최소단위, 선언적 API로 자가치유
- ★ **MSA** — 도메인 중심 독립배포, 분산트랜잭션은 2PC 대신 Saga(보상트랜잭션), 서킷브레이커로 연쇄장애 차단, DB per Service
- ★ **가상화·컨테이너** — 하이퍼바이저(Type1 베어메탈/Type2 호스트형), 컨테이너는 커널공유 경량(네임스페이스+cgroups), 빠른 기동
- ★ **CI/CD·GitOps** — CI(빌드·테스트)→CD(배포), GitOps는 Git을 SSOT로 선언적 동기화(ArgoCD), IaC 멱등성·불변인프라
- ★ **SRE·SLI/SLO/SLA** — SLI(지표)→SLO(목표)→SLA(계약), 에러예산(100%-SLO)으로 배포속도 vs 안정성 조율, 토일 자동화

### 14. 데이터 엔지니어링

- **분산처리 인프라**: 빅데이터 3V/5V, 하둡(Hadoop)/HDFS, 맵리듀스(MapReduce), YARN, 스파크(Spark)/RDD, 지연평가(Lazy Evaluation), 데이터 지역성, 스케일 아웃
- **저장 아키텍처**: 데이터 웨어하우스(DW), 데이터 마트, 데이터 레이크, 레이크하우스(Lakehouse), 스키마 온 리드/라이트, 컬럼지향(Parquet/ORC), 오픈 테이블 포맷(Iceberg/Delta/Hudi), 메달리온 아키텍처(Bronze/Silver/Gold)
- **파이프라인·스트리밍**: ETL, ELT, CDC(Change Data Capture·Debezium), 카프카(Kafka·토픽/파티션/오프셋/컨슈머그룹), 플링크(Flink·워터마크/윈도우), 람다 아키텍처, 카파 아키텍처, 에어플로우(Airflow) DAG, Exactly-Once
- **NoSQL·분산이론**: NoSQL 4유형(KV/Document/Wide-Column/Graph), CAP 정리, PACELC, BASE, 컨시스턴트 해싱, 주키퍼(ZooKeeper·Quorum/스플릿브레인)
- **거버넌스·MLOps**: 데이터 메시(Data Mesh), 데이터 패브릭, 데이터 카탈로그, 데이터 리니지(Lineage), 데이터옵스(DataOps/dbt), 연방쿼리(Trino/Presto), MLOps·피처스토어, 모델 레지스트리(MLflow), 데이터/컨셉 드리프트

**★ TOP 5 답안 각**
- ★ **ELT** — ETL 변환 병목 극복, 클라우드 DW 연산력으로 적재 후 변환(현대 표준), ETL 대비표로 답안 시작
- ★ **카프카** — Pub/Sub 분산 이벤트 스트리밍, 토픽/파티션 병렬·오프셋 보존·컨슈머그룹 부하분산, 실시간 파이프라인 백본
- ★ **CDC** — 운영DB 트랜잭션 로그(Binlog) 캡처로 무부하 실시간 동기화(Debezium), DB 이관·이벤트소싱 연계
- ★ **레이크하우스** — 레이크 유연성+DW의 ACID/SQL 결합, 오픈테이블포맷(Delta/Iceberg)으로 타임트래블·스키마 에볼루션
- ★ **데이터 메시** — 중앙집중 사일로 타파, 도메인 분산 오너십+데이터 프로덕트+셀프서빙 인프라(조직론 혁신)

### 15. DevOps/SRE

- **DevOps 문화·방법론**: 데브옵스/CALMS, 12-Factor App, DORA 메트릭스(배포빈도/리드타임/변경실패율/MTTR), 피처 플래그·토글, 트렁크 기반 개발, 시프트 레프트, 플랫폼 엔지니어링/IDP, 콘웨이의 법칙, 비난없는 포스트모템
- **CI/CD·GitOps**: CI/CD(통합/전달/배포), Git 브랜치 전략(Git Flow/GitHub Flow), 무중단 배포(롤링/블루그린/카나리), GitOps(ArgoCD·Push vs Pull), Helm/Kustomize, 아티팩트 리포지토리, 시크릿 매니저(Vault), 이미지 사이닝(Cosign)
- **SRE·신뢰성**: SRE, SLI/SLO/SLA, 에러 버짓(Error Budget), 토일(Toil), 4대 골든 시그널, USE/RED 메서드, 서킷 브레이커, 재시도(백오프/지터), 카오스 엔지니어링, AIOps
- **옵저버빌리티**: 옵저버빌리티 3대 기둥(메트릭/로그/트레이스), 프로메테우스(Pull), 그라파나, 분산 추적(Trace/Span), 오픈텔레메트리(OTel), EFK/ELK, eBPF
- **IaC·클라우드 네이티브**: IaC/테라폼(tfstate/멱등성), 불변 인프라, 구성 편류(Drift), 쿠버네티스 Operator, 서비스 메시(Istio/사이드카/mTLS), 사가 패턴, 서버리스, 스트랭글러 피그
- **DevSecOps**: DevSecOps, SAST/DAST/IAST, SCA, SBOM(공급망 보안), 컨테이너 이미지 스캐닝, 마이크로 세그멘테이션, 제로 트러스트(ZTA), CSPM/CWPP/CNAPP, 정책 애즈 코드(OPA/Rego)

**★ TOP 5 답안 각**
- ★ **DORA 메트릭스** — 배포빈도·변경리드타임·변경실패율·MTTR 4대 지표로 DevOps 성과 정량 측정, SPACE와 비교
- ★ **GitOps** — 목표상태를 Git에 선언적 저장, 클러스터 내 에이전트(ArgoCD)가 Pull로 동기화, Push 대비 보안 우위
- ★ **SLO·에러 버짓** — 100% 가용성 불가 전제, (100%-SLO)를 합법적 장애예산으로 배포 리스크 통제, SLI/SLA 위계
- ★ **카나리 배포** — 트래픽 1%→10%→100% 점진 확대하며 5xx 모니터링, 이상 시 자동 롤백(통계분석)
- ★ **옵저버빌리티** — MSA 분산환경 Unknown-Unknowns 추론, 메트릭/로그/트레이스 3기둥+OTel 표준

### 07. 엔터프라이즈 시스템

- **IT전략·거버넌스**: IT 거버넌스 5대 도메인, COBIT, ISP, ISMP, EA(BA/DA/AA/TA), 잭맨 프레임워크, TOGAF(ADM), BPR/PI, BSC, KPI/CSF, OKR, 가치사슬, 5 Forces, SWOT
- **ITSM·서비스관리**: ITIL(V3→V4 SVS), ITSM, SLA/OLA/UC, CMDB/CI, 인시던트 관리, 문제 관리(Root Cause), 변경 관리(CAB), BCP/DR/BIA, ITO/BPO/MSP
- **ERP·SCM·CRM**: ERP(MRP→MRP II→ERP II), 포스트모던/컴포저블 ERP, SCM·채찍효과, S&OP, JIT, CRM·LTV/CAC, CDP, MES, PLM/BOM, KMS·SECI 모델, MDM·골든레코드
- **애플리케이션 통합 아키텍처**: P2P, EAI(허브앤스포크), SOA(WSDL/UDDI/SOAP), ESB, REST/HATEOAS, MSA, API 게이트웨이/BFF, 서비스 디스커버리, 서킷 브레이커, 사가 패턴, CQRS·이벤트소싱, 트랜잭셔널 아웃박스, 서비스 메시, 스트랭글러 피그, gRPC
- **BI·데이터·프로세스**: DW(Inmon)/데이터마트(Kimball), ODS, ETL/ELT, OLTP/OLAP, 스타/스노우플레이크 스키마, SCD(Type 2), 데이터 레이크하우스·데이터 메시, BPM/BPMN, 프로세스 마이닝, RPA·초자동화, MECE, DX, ISMS-P

**★ TOP 5 답안 각**
- ★ **EA** — 비즈니스/데이터/앱/기술 4계층 청사진, 잭맨(분류)·TOGAF ADM(절차)로 IT-비즈니스 정렬, 거버넌스(ARB) 연계
- ★ **ISP vs ISMP** — ISP는 전사 중장기 마스터플랜(AS-IS/TO-BE/이행), ISMP는 특정사업 상세 실행계획(RFP/FP 산정)
- ★ **사가 패턴** — MSA 분산 트랜잭션 2PC 락 회피, 로컬 트랜잭션 체인+보상 트랜잭션 롤백(코레오/오케스트레이션)
- ★ **ITIL 4 SVS** — V3 생명주기에서 서비스 가치 시스템으로 진화, 가치사슬+4차원+애자일/DevOps 통합
- ★ **EAI/ESB→MSA** — 중앙집중 통합(허브앤스포크/버스)에서 분산 자율(API게이트웨이·메시)로의 진화 비교

### 12. IT 경영

- **IT거버넌스·전략**: IT 거버넌스 5대 도메인, COBIT 2019(EDM/APO/BAI/DSS/MEA), ISP/ISMP, EA/TOGAF ADM, BPR/PI, BSC/IT BSC, KPI/CSF, OKR, IT PPM, 바이모달 IT
- **투자평가**: ROI, NPV, IRR, PP(회수기간), TCO(CAPEX/OPEX), IT ROI 사전/진행/사후
- **ITSM·ITIL**: ITSM, ITIL V3 생명주기 vs V4 SVS, 서비스 데스크/SPOC, 인시던트 관리·워크어라운드, 문제 관리/KEDB, 변경 관리/CAB, SLA/OLA/UC, CMDB/CI, ISO 20000
- **PM·비용산정·품질**: PMBOK 10대 영역, WBS(100% Rule), CPM/PERT, EVM(PV/EV/AC/CPI/SPI), CMMI 5단계, SPICE, 기능점수(FP), COCOMO, 인스펙션/워크스루, V 모델
- **보안·감리·컴플라이언스·신기술**: ISMS-P, ISO 27001, PIA, BCP/DR(RTO/RPO·미러/핫/웜/콜드), 망분리/망연계, 제로 트러스트, 접근제어(MAC/DAC/RBAC/ABAC), 정보시스템 감리, CSAP, 클라우드 6R, AI 거버넌스(EU AI Act), AIOps

**★ TOP 5 답안 각**
- ★ **ITIL V3 vs V4** — V3 5단계 생명주기에서 V4 SVS(가치사슬+4차원+가이딩원칙)로 진화, DevOps/애자일 통합
- ★ **EVM** — PV/EV/AC 기반 CV=EV-AC, SV=EV-PV, CPI/SPI로 일정·원가 통합 통제(1 초과 시 우수)
- ★ **기능점수(FP)/COCOMO** — FP는 사용자관점 규모산정(ILF/EIF/EI/EO/EQ), COCOMO는 LOC 기반 인월(유기적/준분리/내장형)
- ★ **BCP/DR(RTO·RPO)** — RTO(복구시간)/RPO(데이터손실시점)로 DR등급(미러/핫/웜/콜드) 결정, BIA 연계
- ★ **ISMS-P** — 관리체계 수립+보호대책+개인정보 처리 3영역 인증, ISO 27001·PIA 연계

### 16. 빅데이터

- **개론·특성**: 빅데이터 3V→5V→7V, 비정형/반정형 데이터, 데이터 경제·마이데이터, 비식별화(k-익명성/l-다양성/t-근접성), 데이터 주권
- **저장·처리**: Hadoop(HDFS/MapReduce/YARN), Spark(인메모리/RDD/Lazy), Hive, NoSQL, CAP 정리, BASE 원칙
- **레이크하우스**: 데이터 레이크·데이터 스왐프, 데이터 웨어하우스, 레이크하우스(Delta/Iceberg/Hudi), 메달리온(Bronze/Silver/Gold), 데이터 메시, ELT vs ETL
- **실시간·분석**: 스트리밍(Flink/Kafka), 람다/카파 아키텍처, Exactly-Once, 실시간 OLAP(Druid/Pinot), 분석기법(군집/연관규칙/시계열/이상탐지)
- **거버넌스**: 데이터 거버넌스, 데이터 품질 6차원, 데이터 계보(Lineage), MDM, 차등 프라이버시, 데이터 3법 가명처리

**★ TOP 5 답안 각**
- ★ **레이크하우스** — 레이크(Schema-on-Read)+DW(ACID/성능) 결합, 오픈테이블포맷(Delta/Iceberg/Hudi), 메달리온 3계층
- ★ **CAP 정리** — 분산DB는 일관성·가용성·분할내성 중 2개 선택, PACELC로 지연 vs 일관성 트레이드오프 확장
- ★ **Spark** — 인메모리 분산처리로 MapReduce 대비 최대 100배, RDD(불변/Lineage)+Lazy+Catalyst 최적화
- ★ **람다 vs 카파** — 람다는 배치+속도 계층 이원화, 카파는 스트리밍 단일화(Kafka+Flink)로 단순화
- ★ **비식별화** — k-익명성/l-다양성/t-근접성, 가명처리(데이터3법)·차등프라이버시(노이즈)로 프라이버시 보존

### 08. 알고리즘/통계

- **복잡도·설계**: 시간복잡도(Big-O/Ω/Θ), 분할정복, 동적프로그래밍(DP·메모이제이션), 탐욕 알고리즘, 백트래킹
- **정렬·탐색**: 비교정렬(퀵/병합/힙 O(n log n)), 선형정렬(계수/기수/버킷), 정렬 안정성, 이진탐색, 해시탐색
- **그래프·자료구조**: DFS/BFS, 다익스트라/벨만포드/플로이드워샬, MST(크루스칼/프림), 유니온파인드, 해시테이블(개방주소/체이닝), B+트리(DB 인덱스)
- **NP·계산이론**: P vs NP, NP-완전/NP-하드, SAT(Cook-Levin), TSP
- **확률·통계**: 베이즈 정리, 중심극한정리(CLT), 가설검정(귀무/대립/p-value), 카이제곱검정, t-검정/F-검정/ANOVA, 회귀분석·MLE

**★ TOP 5 답안 각**
- ★ **시간복잡도** — Big-O 점근표기, O(1)<O(log n)<O(n)<O(n log n)<O(n²)<O(2ⁿ), 알고리즘 효율성 평가 기준
- ★ **정렬 알고리즘 비교** — 비교기반 하한 O(n log n)(퀵/병합/힙), 비교없는 O(n+k)(계수/기수), 안정성·제자리·환경별 선택
- ★ **해시테이블** — 평균 O(1), 충돌처리(개방주소법 vs 체이닝), 적재율 관리, B+트리는 디스크/DB 인덱스용 O(log n)
- ★ **가설검정** — 귀무/대립가설, p-value<유의수준 기각, 카이제곱(범주형)·t검정(평균차)·ANOVA(3집단↑)
- ★ **P vs NP** — P(다항시간 해결) vs NP(다항시간 검증), NP-완전(SAT/TSP 환산), 미해결 난제

### 11. IT 설계/감리

- **감리 개요**: 정보시스템 감리 3대 목적(효과성/효율성/안전성), 감리 3차원(영역×관점×단계), 3단계 감리(요구/설계/종료), PMO vs 감리, 전자정부법 제57조, 과업대비표(추적성)
- **감리 점검**: 위험기반 감리, 데이터 품질 6대 지표, 기능점수(FP) 검증, 시큐어코딩(KISA 47개), 데이터 이행 무결성, RTO/RPO, ISMS-P/CISA
- **아키텍처 평가**: 4+1 View, ATAM(트레이드오프), 민감도점/상충점, CBAM(경제성), 품질속성 시나리오, ADR
- **설계 원칙·패턴**: SOLID(SRP/OCP/LSP/ISP/DIP), 응집도/결합도, DRY/KISS/YAGNI, 디미터 법칙, 계층형/헥사고날/클린, MSA(바운디드컨텍스트/사가), CQRS/이벤트소싱, DDD, GoF 23패턴, 서킷브레이커

**★ TOP 5 답안 각**
- ★ **감리 3대 목적·3차원** — 효과성·효율성·안전성 점검, 감리영역×관점(절차/산출물/성과)×단계(요구/설계/종료) 프레임워크
- ★ **PMO vs 감리** — PMO는 발주자 편 능동적 문제해결 개입, 감리는 제3자 객관적 평가·권고(독립성)
- ★ **ATAM** — 아키텍처 트레이드오프 분석, 민감도점/상충점/리스크 도출, CBAM은 경제성(ROI) 관점 확장
- ★ **SOLID** — SRP(단일책임)·OCP(확장개방·수정폐쇄)·LSP(치환)·ISP(인터페이스분리)·DIP(의존역전/IoC)
- ★ **GoF 디자인 패턴** — 생성5(싱글톤/팩토리/빌더)·구조7(어댑터/데코레이터/퍼사드/프록시)·행위11(옵저버/전략/상태)

## Ⅳ. 1교시 / 2~4교시 전환 가이드

| 구분 | 대표 키워드군 | 답안 전개 |
|:---|:---|:---|
| 정의형 (1교시) | 캐시 일관성, 세마포어, 정규화, CAP 정리, Zero Trust, RAG, 디지털 트윈 | 정의 1문장 → 핵심 3포인트 → 한 줄 활용/효과 |
| 구조형 (1교시·서술 겸용) | 파이프라인, TCP 3-way handshake, K8s 구성요소, Transformer, 레이크하우스 | 정의 → 구조도(블록) → 구성요소별 역할 |
| 비교형 (1교시·서술 겸용) | 프로세스 vs 스레드, SQL vs NoSQL, VM vs 컨테이너, ETL vs ELT, ISP vs ISMP | 비교표(항목×대상) + 선택 기준 |
| 설명형 (2~4교시) | MSA, 서비스 메시, MLOps, SDN/NFV, 데이터 메시 | 정의 → 구조도 → 특징 → 적용 사례 |
| 방안형 (2~4교시) | 공급망 보안(SBOM), 장애 대응(SRE), 데이터 거버넌스, PQC 전환 | 문제점 → 원인 → 개선안(단·중·장기) |
| 설계형 (2~4교시) | 쿠버네티스 플랫폼, Observability 체계, 데이터 파이프라인, Zero Trust 아키텍처 | 계층도 → 구성요소 → 운영 절차·고려사항 |

## Ⅴ. 결론 및 회독 방향

- 본 압축본은 컴퓨터시스템응용기술사 기출·출제동향 기준의 **빈출·비교·구조 핵심 약 1,000개**를 추린 것으로, 시험 직전 단기 회독에서는 각 과목 **★ TOP 5 답안 각**으로 골격을 먼저 잡은 뒤 클러스터 키워드로 외연을 채우는 순서로 운영한다.
- 단순 정의 암기보다 성능·운영 복잡도·비용·보안성을 묶어 쓰고, 최신 확장군(LLM·RAG·PQC·CXL·소버린 클라우드)은 반드시 기존 기술과의 **비교 기준**과 함께 답안화한다.
- 도메인별 답안 골격은 [시험 도메인별 키워드](@/exam/cs/subject-focus/_index.md), 빈도는 [기출 빈도 분석](@/exam/cs/frequency.md).
