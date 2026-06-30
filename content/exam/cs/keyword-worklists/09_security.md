---
title: "09 보안 기출-grounded 키워드 워크리스트"
date: "2026-06-30"
tags:
  - "exam-keywords"
  - "cspe"
  - "keyword-worklist"
weight: 9
---

# 09 보안 기출-grounded 키워드 워크리스트 (목표 ~110개)
> 출처: 120~138회 컴퓨터시스템응용기술사 기출 대조 + content/exam/cs/keyword_list.md + frequency.md + keyword-universe.md + 출제 전망.

## 챕터: 01_intro_principles
001. 정보보안 3요소 CIA
002. 최소권한 원칙
003. 직무분리(SoD)
004. 심층방어(Defense in Depth)
005. 위험관리(식별·분석·평가·대응)
006. 정량적 분석(ALE=ARO×SLE)
007. 위험대응 4전략(회피·전가·완화·수용)
008. 잔여위험
009. NIST CSF 2.0
010. 제로 트러스트(Zero Trust, NIST SP 800-207) [출제:126,134,135,136회]
011. ZTA
012. 마이크로 세그멘테이션
013. Security by Design
014. 위협모델링(STRIDE·DREAD·PASTA)
015. MITRE ATT&CK
016. ISMS-P vs ISMS 비교 (ISMS-P vs ISMS) [출제:138회]

## 챕터: 02_crypto
017. 대칭키/비대칭키 암호
018. 하이브리드 암호
019. AES(SPN)
020. 블록암호 모드(CBC·CTR·GCM)
021. AEAD
022. 해시함수(SHA-2·SHA-3)
023. HMAC
024. salt·키스트레칭(bcrypt·scrypt)
025. RSA(소인수분해)
026. ECC(ECDLP)
027. DH/ECDHE 키교환
028. 전방비밀성(PFS)
029. TLS 1.3 핸드셰이크
030. PQC(CRYSTALS-Kyber·Dilithium) [출제:126,129,135,136회] [전망]
031. 양자위협(Shor·Grover)
032. 동형암호
033. 영지식증명(ZKP) [출제:132회]
034. HSM·TPM
035. PKI·CA·RA
036. CRL·OCSP
037. X.509 인증서
038. mTLS
039. 코드서명
040. 패스키 FIDO2 (Passkey WebAuthn) [출제:138회]
041. PQC 전환 Crypto Agility (Post-Quantum Migration) [출제:126,129,135,136회] [전망]
042. 기밀 컴퓨팅 TEE (Confidential Computing) [전망]

## 챕터: 03_network_security
043. 방화벽(상태검사·NGFW) [출제:128,131,134,137회]
044. DMZ·바스티온
045. East-West/North-South 트래픽
046. 네트워크 세그멘테이션(VLAN)
047. NAC(802.1X)
048. IDS/IPS(시그니처·이상탐지)
049. WAF(OWASP CRS)
050. DDoS(볼류메트릭·증폭·SYN Flood)
051. MITM·SSL Stripping·HSTS
052. ARP/DNS Spoofing·캐시포이즈닝 [출제:125,131,132,134회]
053. IPsec(AH·ESP·IKE)
054. SSL VPN
055. SASE/SSE
056. 세션 하이재킹·Replay Attack

## 챕터: 04_endpoint_security
057. EDR/XDR
058. 버퍼 오버플로우(스택·힙)
059. NX/DEP·ASLR·Stack Canary
060. ROP(Return-Oriented Programming)
061. Use-After-Free·Race Condition(TOCTOU)
062. 권한상승(LPE)
063. 루트킷·부트킷
064. 랜섬웨어(WannaCry)
065. APT
066. Fileless Malware
067. Spectre/Meltdown
068. SGX·TEE·TPM 2.0
069. 원격증명(Remote Attestation)
070. FDE(BitLocker)·TDE
071. CVSS·CVE·CWE
072. 시스템 하드닝(CIS Benchmark)
073. 펌웨어 보안 (Firmware Security)
074. 임베디드 보안 (Embedded Security)
075. 보안 운영체제 Secure OS (Secure Operating System) [출제:137회]

## 챕터: 05_web_app_security
076. OWASP Top 10
077. IDOR·접근제어 취약
078. SQL 인젝션(Blind·Time-based)
079. XSS(반사·저장·DOM)
080. CSP
081. CSRF·SameSite [출제:131회]
082. SSRF
083. Log4Shell
084. JWT(alg:none·HS256/RS256)
085. OAuth 2.0(PKCE)
086. OIDC·ID Token
087. IAM·SSO
088. SAML 2.0(IdP·SP)
089. MFA(TOTP·FIDO2/WebAuthn·Passkey) [출제:138회]
090. RBAC·ABAC
091. PAM·특권계정
092. Kerberos(KDC·TGT·Golden/Silver Ticket) [출제:138회]
093. NTLM(Pass-the-Hash)
094. OWASP LLM Top 10 (OWASP LLM Top 10) [출제:135,136,137,138회]
095. 간접 프롬프트 인젝션 (Indirect Prompt Injection) [출제:135,136,137,138회] [전망]

## 챕터: 13_secops_ir_forensics
096. SOC
097. SIEM(상관분석) [출제:138회]
098. SOAR(플레이북) [출제:138회]
099. Threat Intelligence(STIX/TAXII)
100. Cyber Kill Chain [출제:138회]
101. 인시던트 대응(NIST 6단계)
102. DFIR·디지털포렌식
103. Chain of Custody
104. 침투테스트·버그바운티
105. 레드/블루/퍼플팀
106. CTEM [출제:136,137회] [전망]
107. SBOM·공급망 보안 [출제:134,135,138회] [전망]
108. DevSecOps(SAST/DAST/IAST) [출제:128,134,135,136회]
109. 개인정보보호(비식별·마이데이터·ISMS-P·PIA) [출제:126,131,137회]
110. PET(개인정보보호 강화기술) [출제:126,131,137회]
111. SIEM vs SOAR 비교 (SIEM vs SOAR) [출제:138회]
112. CTI 위협 인텔리전스 (Cyber Threat Intelligence) [출제:138회]
113. MISP 위협 공유 플랫폼 (Malware Information Sharing Platform) [출제:125,128,132,135회]
114. 모바일 포렌식 (Mobile Forensics)
115. RaaS 랜섬웨어 생태계 (Ransomware-as-a-Service) [출제:138회]
116. 선제적 사이버보안 (Preemptive Cybersecurity) [출제:138회] [전망]

## 챕터: 17_framework_compliance
117. EU DORA 디지털 운영 복원력 (Digital Operational Resilience Act) [출제:137회]
118. 사이버 레질리언스 법규 (Cyber Resilience) [출제:138회]
119. 디지털 출처 증명 (Digital Provenance) [전망]

## 챕터: 19_ai_advanced_security
120. LLM 보안 위협 OWASP LLM Top 10 (OWASP LLM Top 10) [출제:135,136,137,138회]
121. AI 보안 플랫폼 (AI Security Platform) [전망]

## 챕터: 16_data_privacy
122. 개인정보 유출 사고 대응 PET (Privacy Incident and PET) [출제:126,131,137회]

> 생성 기준: 총 122개. 목표 수는 시험 출제 가능성 기준의 운영 상한이며, 지엽 키워드는 제외한다.
