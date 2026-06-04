+++
title = "597. 양자 통신 양자 키 분배 QKD (Quantum Communication Quantum Key Distribution)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-ict-convergence"]

[extra]
tags = ["studynote-ict-convergence"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 단일 광자의 양자 상태(편광/위상)를 정보 매개체로 사용하고, **Heisenberg 불확정성 원리**와 **No-Cloning Theorem**에 의해 도청 시도 시 필연적으로 발생하는 양자 상태 붕괴를 탐지하여 정보이론적 보안(Information-Theoretic Security, ITS)을 달성하는 키 합의(Key Agreement) 프로토콜이다.
> 2. **가치**: RSA/ECC 등 공개키 암호 체계는 **Shor 알고리즘** 등장으로 양자 컴퓨터 시대에 무력화되며, "Harvest Now, Decrypt Later(HNDL)" 공격이 이미 진행 중이다. QKD는 미래의 양자 연산 능력에 무관하게 도청 물리적 불가능성을 보장하는 **Quantum-Safe 유일의 수학적 보장**을 제공한다.
> 3. **판단 포인트**: BB84의 **QBER(Quantum Bit Error Rate) 11% 임계치** 초과 시 보안 증명이 붕괴하며, 광섬유 손실(0.2~0.3 dB/km @1550nm)로 인한 **PNS(Photon Number Splitting) 공격 취약성**, 신뢰 노드(Trusted Node) 문제, 그리고 **PQC( Post-Quantum Cryptography) NIST 표준(ML-KEM, ML-DSA)**과의 **하이브리드 운영 아키텍처**가 실무 핵심 의사결정 포인트다.

---

## Ⅰ. 개요 및 필요성

기존 공개키 암호 체계(RSA-2048, ECC P-256)는 **이산 로그 문제** 또는 **정수 인수분해**의 계산 복잡성에 보안성을 의존한다. 그러나 1994년 Peter Shor가 개발한 양자 알고리즘은 Shor 알고리즘을 통해 두 문제 모두를 **다항식 시간(O((log N)³))**에 해결할 수 있어, 4,000+ 논리 큐비트를 가진 **오류 허용 양자 컴퓨터(FTQC)**가 실현되면 현재의 TLS, SSH, IPsec 기반 모든 통신 보안이 붕괴한다.

게다가 현재 능동적으로는 암호 해독이 불가능한 **HNDL 공격** 위협이 존재한다. 공격자는 이미 암호화된 대량의 인터넷 트래픽(의료·군사·외교 데이터)을 저장소에 보관하고 있으며, 향후 양자 컴퓨터가 등장하는 시점에 일괄 복호화할 의도를 가지고 있다. 이는 특히 **민감 데이터의 기밀성 유지 기간(Information Lifecycle)**이 10~30년 이상인 경우에 치명적이다.

QKD는 이 위협에 대한 근본적 해답을 제시한다. 키 교환 과정에서 발생하는 모든 도청 시도가 양자역학 법칙에 의해 **물리적으로 원천 차단**되므로, 공격자의 연산 능력이나 알고리즘의 진보에 무관하게 보안성이 보장된다. 즉, **Computational Security -> Information-Theoretic Security**로의 패러다임 전환이다.

다만 QKD는 **암호 알고리즘이 아니라 키 분배 메커니즘**이므로, 실제 데이터 평문(Plaintext) 암호화에는 AES-256-GCM 같은 **대칭키 세션 암호**가 여전히 사용된다는 점이 중요하다. 즉, **"QKD로 키를 안전하게 전달하고, 그 키로 AES를 돌린다"**는 하이브리드 구조가 표준이다.

```text
[기존 패러다임 vs 양자 패러다임 비교]

[Legacy PKI]                                    [Quantum-Safe Era]
  +-----------+        +-----------+              +----------------+        +-----------+
  |   Alice   | <----> |  Public   |              |     Alice      | <====> |   Bob     |
  | (Client)  |  RSA   | Channel   |              |   (QKD Tx)     | Fiber  | (QKD Rx)  |
  +-----------+ Enc/Dec+----------+               +----------------+ Quantum +-----------+
       |                        |                  |   |                Channel  |
       |   취약점:              |                  |   v                          |
       |   - Shor 알고리즘     |                  | +--------+  Classical  +---+  |
       |   - HNDL 공격         |                  | |QBER <==|==============>|Err|
       |                       |                  | | 11% ?  |   Channel   |Cor| |
       +-----------------------+                  | +--------+             +---+ |
                                                 |   ||                       ||
                                                 |   vv                       vv
                                                 | +--------+              +---------+
                                                 | | Privacy|              |  PQC    |
                                                 | | Amp +  |              | ML-KEM  |
                                                 | | AES-GCM|              | ML-DSA  |
                                                 | +--------+              +---------+
                                                 |    하이브리드 운용 (실무 표준)
                                                 +----------------------------+
```

| 위협/요구 | 기존 RSA/ECC | QKD 기반 |
| :--- | :--- | :--- |
| 보안 기반 | 계산 복잡성 (수학적 추정) | 물리 법칙 (수학적 증명) |
| 양자 컴퓨터 내성 | ❌ (Shor 알고리즘) | ✅ (이론적 완전 내성) |
| HNDL 공격 대응 | ❌ (저장된 데이터 미래 해독) | ✅ (도청 시점부터 탐지) |
| 키 분배 안전성 | 수치에 의존 (RSA-2048 ≈ 112bit) | 정보이론적 (ITS) |
| 구현 복잡도 | 낮음 (SW only) | 매우 높음 (단일광자 검출기) |
| 전송 거리 | 무제한 (네트워크) | 광섬유 100~500km / 위성 2000km+ |

- **📢 섹션 요약 비유**: "보물상자 자물쇠를 매일 새로운 조합으로 바꿔 전달해야 한다고 상상해보자. 기존 방식은 '이 조합은 1억 자릿수라 풀기 어렵다'는 *희망 사항*에 의존하지만, QKD는 *누군가 상자를 들여다보는 순간 내용물이 변하는 마법의 봉투*를 사용해, 도둑이 열었는지 여부를 즉시 알 수 있다."

---

## Ⅱ. 아키텍처 및 핵심 원리

QKD 시스템은 **단일 광자 수준의 양자 채널(Quantum Channel)**과 **고전적 인증 채널(Classical Authenticated Channel)** 두 가지로 구성된다. 양자 채널은 광섬유(1550nm telecom band) 또는 자유공간(Free-space)이며, 고전 채널은 별도 통신(인터넷, 무선)이다. 고전 채널은 반드시 **인증(Authentication)**되어야 하며(예: 사전 공유된 MAC 키 또는 디지털 서명), 도청은 허용되지만 변조는 불가능해야 한다.

### BB84 프로토콜 (Bennett-Brassard 1984)

가장 대표적인 **Prepare-and-Measure** 방식의 QKD 프로토콜로, 단일 광자의 **편광(Polarization)** 또는 **위상(Phase)**에 4가지 상태를 매핑한다.

```text
[BB84 양자 상태 인코딩 - 직교 베이스 vs 대각 베이스]

     Z-Basis (Rectilinear)            X-Basis (Diagonal)
     ------------------              ------------------
     Bit 0 = |0> (0°  수직)         Bit 0 = |+> (45°  ↗)
     Bit 1 = |1> (90° 수평)         Bit 1 = |-> (135° ↖)

     ⟋ |0>     |1> ⟍                 ⟋ |+>       |-> ⟍
     ^              ->                 ↗              ↖
     0°             90°               45°            135°

     + 같은 Z-Basis로 측정해야만 비트가 일치
     + 다른 Basis로 측정 시 50% 확률로 무작위 결과
     + 도청자(Eve)가 임의 Basis로 측정 시 25% 에러율 유발
```

**BB88/BB84 8단계 프로세스 (Shor-Preskill Security Proof 기반):**

| 단계 | 명칭 | 동작 | 산출물 |
|:---:|:---|:---|:---|
| 1 | **Quantum Transmission** | Alice가 각 비트에 대해 Z/X 베이스를 50% 확률로 선택해 단일 광자 전송 | 양자 신호 (예: 10⁹ 광자/초) |
| 2 | **Measurement** | Bob도 Z/X 베이스를 50% 확률로 독립 선택 측정 | Raw Key (오류 포함) |
| 3 | **Sifting** | 공개 채널로 베이스 정보 교환 후, 동일 베이스 비트만 유지 | Sifted Key (≈ 50% 축소) |
| 4 | **Parameter Estimation** | 샘플 비트 공개 비교로 QBER 산출, 도청 정도 추정 | QBER 통계량 |
| 5 | **Information Reconciliation** | Cascade/LDPC/Polar Code로 불일치 비트 정정 | Reconciled Key |
| 6 | **Error Verification** | Universal Hash (예: SHA-256, Toeplitz)로 정정 완전성 검증 | Verified Key |
| 7 | **Privacy Amplification** | Eve가 얻었을 정보량만큼 키 압축 (Toeplitz 행렬) | Final Secret Key |
| 8 | **Authentication** | MAC 태그 검증으로 고전 채널 변조 차단 | Mutual Auth 완료 |

**E91 (Ekert 1991) - Entanglement-Based 프로토콜:**

EPR 페어(|Φ⁺> = (|00>+|11>)/√2)를 Alice/Bob에 분배하고, **CHSH 부등식 위반(S=2√2)**을 검증해 도청을 탐지한다. Bell inequality 위반이 깨지지 않을 만큼 안전하다는 **Device-Independent QKD(DI-QKD)**의 이론적 토대가 되었다.

**B92, SARG04, Decoy-State, MDI-QKD, TF-QKD, CV-QKD** 등 다양한 변형 프로토콜이 있으며, 각기 다른 물리 계, 공격 모델, 거리/속도 트레이드오프를 가진다.

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **단일 광자원 (SPDC/Herriott Cell)** | Alice 측에서 1회 1광자 방출 | 약결맞음광(SPDC) 또는 감쇠 레이저(Weak Coherent Pulse, WCP), **decoy state**로 PNS 공격 방어 |
| **광자 편광/위상 변조기** | 양자 정보 인코딩 | LiNbO₃ 위상 변조기, Pockels cell (수십 MHz 변조) |
| **양자 채널** | 광자 전송 매체 | 단일모드 광섬유(SMF-28) **손실 0.2~0.3 dB/km @1550nm**, 자유공간 2000km+(목자 위성) |
| **단일 광자 검출기 (SPD)** | Bob 측에서 광자 검출 | InGaAs/InP **APD(Gated/ Free-running, dark count < 100 Hz)** 또는 **SNSPD(NbN, 1550nm 효율 80%+, dark count < 100 Hz, jitter < 100 ps)** |
| **고전 인증 채널** | Sifting/Error Correction 정보 교환 | TLS 1.3 + 사전공유 MAC 키 또는 양자 키 자체로 인증 (Bootstrapping) |
| **Post-processing Unit** | 키 정제/증폭 | FPGA/ASIC 구현, Cascade (양방향), LDPC(비대칭), Polar Code, **Toeplitz 해시** |
| **QBER 분석기** | 도청 정량화 | 이론 임계치 BB84: **11%** (Shor-Preskill), **20%** (B92) 초과 시 키 폐기 |
| **Quantum Repeater (선택)** | 장거리 연결 | 양자 메모리 + Entanglement Swapping, 현재 R&D 단계 (수~수십 노트 fidelity) |

**주요 양자 공격과 방어 메커니즘:**

| 공격 기법 | 원리 | 방어 기법 |
| :--- | :--- | :--- |
| **Intercept-Resend (IR)** | Eve가 광자 측정 후 재전송 -> 25% 에러 | QBER 모니터링 (4% 통계 검출) |
| **PNS (Photon Number Splitting)** | 다광자 펄스에서 1개 도청 | Decoy-State Protocol (Y. Zhao 2003), GP-NQRD |
| **Detector Blinding** | APD를 선형 모드로 강제 조작 | Measurement-Device-Independent QKD (MDI-QKD) |
| **Trojan Horse** | 광자 반사 신호로 모듈러 설정 추출 | 광アイソレータ, 모니터링 검출기 |
| **Side-Channel (Timing/Wavelength)** | 부수 정보 누출 | Spectral/Polarization Filtering, Calibration |
| **Collective/Coherent Attack** | 양자 메모리 기반 통합 공격 | Shor-Preskill 증명 (Universal Composable Security) |

**거리 한계와 Quantum Repeater의 필요성:**

광섬유 100km 이상에서 손실이 약 20dB(100배), 200km에서 40dB(10,000배)이므로 **Secret Key Rate(SKR)**가 기하급수적으로 감소한다. 이를 해결하기 위한 핵심 기술이 **Quantum Repeater**이며, entanglement swapping과 양자 메모리(Quantum Memory: Rb vapor, diamond NV center, rare-earth ion)를 사용한다. 그러나 양자 메모리의 coherence time이 현재 수 ms 수준에 불과해 실용화에는 아직 10년 이상 소요될 전망(202
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 597 / 800

<- **이전**: [596. 위성 인터넷 LEO 저궤도 통신](/knowledge-base/studynote/06_ict_convergence/uncategorized/596_satellite_internet_leo_low_earth_orbit/)
**다음**: [598. 양자 컴퓨팅 큐빗 양자 우위](/knowledge-base/studynote/06_ict_convergence/uncategorized/598_quantum_computing_qubit_quantum_supremacy/) ->

---
