---
title: "시스템 보안 키워드 워크리스트"
date: "2026-07-01"
tags:
  - "cspe-keywords"
weight: 1
---

# 5. 시스템 보안 출제동향 키워드 (목표 240개)

> 출처: 120~138회 기출 + frequency.md + 공식 8대영역 + 전망. 개인 학습 목록 미사용.

## 암호학 (Cryptography)

001. 대칭 암호화 — AES·DES·3DES (Symmetric Encryption) [출제:122회]
002. 비대칭 암호화 — RSA·ECC (Asymmetric Encryption) [출제:122회]
003. 하이브리드 암호 (Hybrid Cryptography) [출제:122회]
004. 해시 알고리즘 — SHA-256·SHA-3 (Hash Algorithm) [출제:121회]
005. HMAC 메시지 인증 코드 (HMAC) [출제:121회]
006. 디피-헬만 키 교환 (Diffie-Hellman Key Exchange) [출제:128회]
007. 타원 곡선 암호 ECC (Elliptic Curve Cryptography)
008. 전자 서명 (Digital Signature)
009. PKI 공개키 기반구조 (Public Key Infrastructure) [출제:120,138회]
010. X.509 인증서 (X.509 Certificate) [출제:120회]
011. CA 인증 기관·인증서 발급 절차 (Certificate Authority) [출제:120회]
012. CRL·OCSP 인증서 폐지 (CRL OCSP Certificate Revocation) [출제:120회]
013. TLS·SSL 프로토콜 (TLS SSL Protocol)
014. TLS 1.3 핸드셰이크 (TLS 1.3 Handshake) [전망]
015. 양자내성암호 PQC (Post-Quantum Cryptography) [출제:126,129,135,136회]
016. ML-KEM CRYSTALS-Kyber (ML-KEM CRYSTALS-Kyber) [출제:136회]
017. ML-DSA CRYSTALS-Dilithium (ML-DSA CRYSTALS-Dilithium) [출제:136회]
018. SLH-DSA 해시 기반 서명 (SLH-DSA Hash-Based Signature) [전망]
019. PQC 전환 로드맵·하이브리드 방식 (PQC Migration Hybrid) [출제:133회]
020. QKD 양자 키 분배 (Quantum Key Distribution) [출제:126회]
021. 동형 암호 (Homomorphic Encryption) [출제:132,135회]
022. 영지식 증명 ZKP (Zero-Knowledge Proof) [출제:132회]
023. 안전한 다자간 연산 MPC (Secure Multi-Party Computation) [출제:135회]
024. 차등 프라이버시 (Differential Privacy) [출제:134,135회]
025. 신뢰 실행 환경 TEE (Trusted Execution Environment) [전망]
026. 기밀 컴퓨팅 (Confidential Computing) [전망]
027. 랜덤 오라클 모델 (Random Oracle Model)
028. 스트림 암호 — ChaCha20 (Stream Cipher ChaCha20)
029. 블록 암호 운영 모드 — CBC·CTR·GCM (Block Cipher Modes)
030. 키 관리 — HSM·KMS (Key Management HSM KMS)

## 네트워크·시스템 보안 (Network/System Security)

031. 방화벽 — 패킷 필터·상태기반·NGFW (Firewall) [출제:129,137회]
032. 차세대 방화벽 NGFW vs WAF vs CASB 비교 (NGFW WAF CASB Comparison) [출제:137회]
033. IDS·IPS 탐지 vs 차단 (IDS IPS) [출제:129,134회]
034. 침입 탐지 — 서명 기반·이상 탐지 (Intrusion Detection)
035. 허니팟·허니넷 (Honeypot Honeynet)
036. 네트워크 스푸핑 — ARP·IP·DNS (Network Spoofing) [출제:128,134회]
037. DDoS 공격·대응 — SYN Flood·반사 증폭 (DDoS Attack) [출제:125회]
038. 맬웨어 유형 — 바이러스·웜·트로이·랜섬웨어 (Malware Types) [출제:121회]
039. 랜섬웨어 공격 분석·대응 (Ransomware) [출제:121회]
040. APT 고급 지속 위협 (Advanced Persistent Threat) [출제:128,134회]
041. 사이버 킬체인 (Cyber Kill Chain) [출제:130,137회]
042. MITRE ATT&CK 프레임워크 (MITRE ATT&CK) [출제:124,130,137회]
043. 위협 헌팅 (Threat Hunting) [출제:138회]
044. 사이버 위협 인텔리전스 CTI (Cyber Threat Intelligence) [출제:123,138회]
045. STIX·TAXII 위협 공유 (STIX TAXII) [출제:123,138회]
046. MISP 위협 공유 플랫폼 (MISP) [출제:138회]
047. SOC 보안 운영 센터 (Security Operations Center) [출제:128,129회]
048. SIEM — 보안 이벤트 집계·분석 (SIEM) [출제:128,129,138회]
049. SOAR — 보안 자동화·대응 (SOAR) [출제:127,138회]
050. SIEM vs SOAR 비교 (SIEM vs SOAR) [출제:138회]
051. UEBA 사용자·엔티티 행동 분석 (UEBA) [출제:138회]
052. NDR 네트워크 탐지·대응 (NDR Network Detection Response) [전망]
053. XDR 확장 탐지·대응 (XDR Extended Detection Response) [전망]
054. EDR 엔드포인트 탐지·대응 (EDR Endpoint Detection Response) [출제:121회]
055. 보안 정보 관리 SIM vs SEM (SIM SEM) [전망]
056. CTEM 지속적 위협 노출 관리 (CTEM Continuous Threat Exposure Management) [출제:136,137회]
057. 취약점 스캔 — Nessus·OpenVAS (Vulnerability Scanner)
058. 침투 테스트 방법론 (Penetration Testing Methodology)
059. 버그 바운티 (Bug Bounty) [전망]
060. 레드팀·블루팀·퍼플팀 (Red Blue Purple Team) [출제:124회]
061. 제로데이 취약점·대응 체계 (Zero-Day Vulnerability) [출제:134,136회]
062. CVE·CVSS 취약점 채점 (CVE CVSS) [출제:127,130회]
063. NVD 국가 취약점 DB (NVD National Vulnerability Database) [출제:130회]
064. 패치 관리·가상 패치 (Patch Management Virtual Patching) [출제:136회]
065. PSIRT 제품 보안 대응 팀 (PSIRT) [출제:136회]
066. 보안 구성 관리 (Security Configuration Management)
067. 최소 권한 원칙 (Principle of Least Privilege)
068. 심층 방어 전략 (Defense in Depth)

## 웹·애플리케이션 보안 (Web/App Security)

069. OWASP Top 10 (OWASP Top 10) [출제:120,129회]
070. SQL 인젝션 (SQL Injection) [출제:120,123회]
071. XSS 크로스사이트 스크립팅 (XSS) [출제:120회]
072. CSRF 크로스사이트 요청 위조 (CSRF) [출제:131회]
073. XXE 외부 엔티티 인젝션 (XXE External Entity Injection)
074. SSRF 서버측 요청 위조 (SSRF Server-Side Request Forgery) [전망]
075. 인증·권한 결함 (Broken Authentication Authorization)
076. 민감 데이터 노출 (Sensitive Data Exposure)
077. 보안 오설정 (Security Misconfiguration)
078. 취약한 의존성 컴포넌트 (Vulnerable Components)
079. 로깅·모니터링 불충분 (Insufficient Logging Monitoring)
080. 스택 오버플로우 공격 (Stack Overflow Attack) [출제:136회]
081. 버퍼 오버플로우 — 카나리·DEP·ASLR (Buffer Overflow Canary DEP ASLR) [출제:125,136회]
082. 쉘코드·ROP 공격 (Shellcode ROP) [출제:125회]
083. 포맷 스트링 공격 (Format String Attack)
084. Use-after-free 취약점 (Use-After-Free)
085. 시큐어 코딩 가이드 (Secure Coding Guide) [출제:126회]
086. 입력값 검증·파라미터 바인딩 (Input Validation Parameter Binding) [출제:123회]
087. 보안 API 설계 — JWT·OAuth·mTLS (Secure API Design) [출제:123회]
088. 콘텐츠 보안 정책 CSP (Content Security Policy) [전망]
089. 서브리소스 무결성 SRI (Subresource Integrity) [전망]
090. 웹 서비스 보안 — SAML·WS-Security (Web Service Security)
091. API 보안 게이트웨이 (API Security Gateway) [전망]

## 인증·접근 제어 (Authentication & Access Control)

092. 인증 방식 — 지식·소유·생체 (Authentication Factors)
093. MFA 다중 인증 (Multi-Factor Authentication)
094. FIDO2·WebAuthn (FIDO2 WebAuthn) [출제:138회]
095. 패스키 비밀번호 없는 인증 (Passkey Passwordless) [출제:138회]
096. OAuth 2.0·OIDC (OAuth 2.0 OIDC) [출제:123회]
097. SAML 2.0 (SAML 2.0) [출제:123회]
098. SSO 단일 로그인 (Single Sign-On SSO)
099. RBAC 역할 기반 접근 제어 (Role-Based Access Control) [출제:122회]
100. ABAC 속성 기반 접근 제어 (Attribute-Based Access Control) [출제:122회]
101. PBAC 정책 기반 접근 제어 (Policy-Based Access Control) [전망]
102. IAM 신원·접근 관리 (Identity and Access Management) [출제:120,135회]
103. PAM 특권 접근 관리 (Privileged Access Management) [전망]
104. 최소 권한·직무 분리 (Least Privilege Separation of Duties)
105. 제로 트러스트 아키텍처 (Zero Trust Architecture) [출제:124,126,134,135,136회]
106. ZTNA 제로 트러스트 네트워크 접근 (ZTNA) [출제:135,136회]
107. 마이크로 세그멘테이션 (Micro-Segmentation) [출제:135회]
108. BeyondCorp 모델 (BeyondCorp) [출제:124회]
109. 연속 인증·동적 신뢰 평가 (Continuous Authentication) [전망]
110. 디지털 신원 — DID·SSI (Decentralized Identity DID SSI) [출제:123,128,132회]
111. 검증가능 자격증명 VC (Verifiable Credential) [출제:132회]
112. W3C DID 표준 (W3C DID Standard) [출제:132회]
113. CAPTCHA·reCAPTCHA (CAPTCHA) [출제:128회]
114. 생체 인식 — 지문·얼굴·홍채 (Biometric Authentication) [출제:126회]

## 클라우드·컨테이너 보안 (Cloud/Container Security)

115. 클라우드 보안 공유 책임 모델 (Cloud Shared Responsibility) [출제:137회]
116. CASB 클라우드 접근 보안 브로커 (CASB) [출제:122,137회]
117. CSPM 클라우드 보안 형상 관리 (CSPM) [출제:136회]
118. CWPP 클라우드 워크로드 보호 (CWPP) [전망]
119. CNAPP 클라우드 네이티브 보호 플랫폼 (CNAPP) [출제:127,136회]
120. CIEM 클라우드 ID 권한 관리 (CIEM) [출제:133회]
121. DSPM 데이터 보안 형상 관리 (DSPM) [출제:133회]
122. 클라우드 네이티브 보안 4C (Cloud Native Security 4C) [출제:136회]
123. 컨테이너 이미지 취약점 스캔 — Trivy (Container Image Scan) [출제:130,136회]
124. OPA Gatekeeper 정책 엔진 (OPA Gatekeeper) [출제:130회]
125. Falco 런타임 보안 (Falco Runtime Security) [출제:130회]
126. Seccomp·AppArmor·SELinux (Seccomp AppArmor SELinux) [출제:130회]
127. 네임스페이스·cgroup 격리 (Namespace Cgroup Isolation) [출제:121회]
128. Rootless 컨테이너 보안 (Rootless Container Security) [출제:130회]
129. 클라우드 CSAP 보안 인증 등급제 (CSAP) [출제:128,132,136,138회]
130. 소프트웨어 공급망 보안 — SBOM·VEX (Supply Chain Security) [출제:128,130,134,135,138회]
131. SLSA 공급망 보안 프레임워크 (SLSA) [전망]
132. 아티팩트 서명 — Cosign·Sigstore (Artifact Signing) [출제:130회]
133. 비밀 관리 — Vault·AWS Secrets (Secrets Management) [출제:130회]

## AI·LLM 보안 (AI Security)

134. AI 보안 위협 전체 구조 (AI Security Threat Landscape) [출제:135,137,138회]
135. 프롬프트 인젝션 (Prompt Injection) [출제:135,137,138회]
136. 간접 프롬프트 인젝션 (Indirect Prompt Injection) [출제:137,138회]
137. 탈옥 Jailbreak 공격 (Jailbreak Attack) [출제:137,138회]
138. 프롬프트 유출 (Prompt Leakage) [전망]
139. 모델 역전 공격 (Model Inversion Attack) [출제:137회]
140. 모델 추출 공격 (Model Extraction Attack) [출제:137회]
141. 데이터 오염 공격 (Data Poisoning) [출제:137회]
142. 백도어 공격 (Backdoor Attack) [출제:137회]
143. 적대적 예제 공격 (Adversarial Example) [출제:131회]
144. 모델 DoS (Model Denial of Service) [출제:138회]
145. OWASP LLM Top 10 (OWASP LLM Top 10) [출제:137,138회]
146. LLM01 프롬프트 인젝션 (LLM01 Prompt Injection) [전망]
147. LLM02 민감 정보 노출 (LLM02 Sensitive Information Disclosure) [전망]
148. LLM06 과도한 에이전시 (LLM06 Excessive Agency) [전망]
149. LLM10 무제한 소비 (LLM10 Unbounded Consumption) [전망]
150. AI 레드팀 (AI Red Teaming) [출제:135,137,138회]
151. 에이전트 보안 — 권한 통제·가드레일 (Agent Security) [출제:138회]
152. 에이전트 샌드박스 격리 (Agent Sandbox) [전망]
153. AI 워터마킹 (AI Watermarking) [전망]
154. 딥페이크 탐지 (Deepfake Detection) [전망]
155. C2PA 콘텐츠 진위 표준 (C2PA Content Provenance) [전망]
156. AI 공급망 보안 (AI Supply Chain Security) [출제:138회]

## 개인정보·프라이버시 보호 (Privacy Protection)

157. 개인정보보호법 — 수집·이용·제공·파기 (Personal Data Protection Act) [출제:121,137회]
158. 개인정보보호법 2023 개정 — 마이데이터·과징금 (PIPA 2023 Amendment) [출제:137회]
159. 전송 요구권·마이데이터 (Data Portability MyData) [출제:137회]
160. GDPR — 동의·잊혀질 권리·DPO (GDPR) [전망]
161. 개인정보 영향평가 PIA (Privacy Impact Assessment) [출제:133회]
162. 개인정보 비식별 처리 — 가명·익명·마스킹 (De-identification) [출제:124,131회]
163. k-익명성·l-다양성·t-근접성 (k-Anonymity l-Diversity) [출제:124회]
164. 마이데이터 서비스 보안 (MyData Service Security) [출제:126회]
165. 개인정보보호 강화기술 PET (Privacy Enhancing Technologies) [출제:134,135회]
166. 프라이버시 중심 설계 (Privacy by Design) [전망]
167. ISO 29100·ISO 27701 (ISO 29100 ISO 27701) [출제:126회]
168. 연합 학습 — 프라이버시 보존 AI (Federated Learning) [출제:136회]
169. CBPR 국경 간 개인정보 규칙 (CBPR Cross-Border Privacy Rules) [출제:131회]

## 보안 관리·거버넌스 (Security Management)

170. 정보보호 관리 체계 ISMS-P (ISMS-P) [출제:126,134,138회]
171. ISMS-P 인증 심사 절차 (ISMS-P Certification) [출제:138회]
172. ISO/IEC 27001 정보보안 경영 시스템 (ISO 27001) [출제:137회]
173. ISO/IEC 27001:2022 주요 개정 (ISO 27001 2022) [출제:137회]
174. ISO/IEC 27701 개인정보 경영 시스템 (ISO 27701) [출제:126회]
175. 정보 보호 위험 평가 — 자산·위협·취약점 (Information Security Risk Assessment) [출제:122회]
176. 위험 처리 전략 — 수용·회피·전가·감소 (Risk Treatment) [출제:122회]
177. BCP 업무 연속성 계획 (Business Continuity Plan) [출제:136회]
178. DRP 재해복구 계획 (Disaster Recovery Plan) [출제:121,136회]
179. ISO 22301 비즈니스 연속성 (ISO 22301) [출제:136회]
180. NIST Cybersecurity Framework (NIST CSF) [출제:130,137회]
181. NIST CSF 2.0 — Govern 기능 추가 (NIST CSF 2.0) [출제:130회]
182. NIST AI RMF AI 위험 관리 (NIST AI RMF) [출제:133회]
183. 정보보호 거버넌스 (Information Security Governance) [출제:120회]
184. 보안 정책·지침·절차 (Security Policy Procedure)
185. 내부자 위협 관리 (Insider Threat Management)
186. 보안 인식 교육 (Security Awareness Training)
187. 디지털 포렌식 — 증거 수집·체인 오브 커스터디 (Digital Forensics) [출제:128,129회]
188. 모바일 포렌식 (Mobile Forensics) [출제:137회]
189. 디스크 이미징·해시 무결성 (Disk Imaging Hash Integrity) [출제:129회]
190. 국가정보원 보안성 검토 (NIS Security Review) [출제:131회]
191. 망분리 — CC 인증·보안적합성 (Network Separation CC) [출제:125회]

## 보안 운영·신기술 (Security Operations)

192. 사이버 레질리언스 (Cyber Resilience) [출제:130,137회]
193. 사이버 보험 (Cyber Insurance) [전망]
194. CISA 권고 사항 (CISA Advisory) [전망]
195. 취약점 우선순위 관리 — EPSS·CVSS (Vulnerability Prioritization EPSS CVSS) [전망]
196. 보안 오케스트레이션 플레이북 (Security Orchestration Playbook) [출제:138회]
197. 능동적 방어 전략 (Active Cyber Defense) [전망]
198. 인텔리전스 기반 CTI 자동화 (CTI Automation) [출제:138회]
199. 사이버 보안 훈련 — 사이버 레인지 (Cyber Range Training) [전망]
200. EU DORA 디지털 운영 복원력 (EU DORA) [출제:138회]
201. EU CRA 사이버 레질리언스 법 (EU Cyber Resilience Act) [전망]
202. 정보통신 기반 보호법 (Critical Infrastructure Protection Act) [전망]
203. 전자정부법 보안 요건 (e-Government Security) [전망]

## 임베디드·하드웨어 보안 (Embedded/HW Security)

204. 임베디드 시스템 보안 취약점 (Embedded Security Vulnerabilities) [출제:138회]
205. 펌웨어 보안 — 하드코딩 자격증명 (Firmware Security) [출제:138회]
206. Secure Boot 보안 부팅 (Secure Boot) [출제:138회]
207. ARM TrustZone (ARM TrustZone) [출제:138회]
208. 하드웨어 보안 모듈 HSM (HSM) [전망]
209. TPM 신뢰 플랫폼 모듈 (Trusted Platform Module) [전망]
210. PUF 물리적 복제 불가 함수 (PUF) [출제:125회]
211. 사이드채널 공격 (Side-Channel Attack) [전망]
212. 폴트 인젝션 공격 (Fault Injection Attack) [전망]
213. JTAG 디버그 포트 보안 (JTAG Security) [출제:126회]
214. IoT 디바이스 보안 — AIoT (AIoT Security) [출제:132회]
215. 스마트팩토리 OT 보안 (OT Security Smart Factory) [출제:126회]
216. ICS·SCADA 보안 (ICS SCADA Security) [전망]
217. 차량 사이버 보안 — V2X 위협 (Vehicle Cybersecurity V2X) [출제:138회]
218. ISO/PAS 8800 AI 안전 (ISO PAS 8800) [출제:138회]
219. PKI 차량 인증 (Vehicle PKI) [출제:138회]

## 보안 아키텍처·설계 원칙

220. 보안 아키텍처 — CIA 삼각형 (CIA Triad)
221. 보안 설계 원칙 — 페일 세이프·최소 노출 (Security Design Principles)
222. 만리장성 보안 모델 (Brewer-Nash Model) [출제:132회]
223. Bell-LaPadula 기밀성 모델 (Bell-LaPadula Model)
224. Biba 무결성 모델 (Biba Integrity Model)
225. Clark-Wilson 무결성 모델 (Clark-Wilson Model)
226. 보안 아키텍처 평가 — SABSA (SABSA Security Architecture) [전망]
227. 망분리·망연계 솔루션 (Network Separation Bridging) [출제:125회]
228. 비무장 지대 DMZ (DMZ Demilitarized Zone)
229. 점프 서버·배스천 호스트 (Jump Server Bastion Host)
230. SASE 아키텍처 (SASE Architecture) [출제:135,136회]
231. 소프트웨어 정의 경계 SDP (Software Defined Perimeter) [출제:124회]
232. 데이터 보안 — DRM·DLP 비교 (DRM DLP) [출제:128회]
233. 보안 정보 공유 플랫폼 — ISAC (ISAC) [출제:129회]
234. DevSecOps 보안 시프트 레프트 (DevSecOps Shift-Left) [출제:128,134,135,136회]
235. SAST·DAST·IAST·RASP (SAST DAST IAST RASP) [출제:128,135회]
236. 보안 코드 리뷰 (Security Code Review) [전망]
237. 위협 모델링 — STRIDE·DREAD (Threat Modeling STRIDE) [전망]
238. PASTA 위협 모델링 방법론 (PASTA Threat Modeling) [전망]
239. 공격 표면 분석 (Attack Surface Analysis) [출제:136회]
240. 보안 성숙도 모델 (Security Maturity Model) [전망]
