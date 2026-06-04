+++
title = "280. 동형 암호 연산 데이터 프라이버시 보존 (Homomorphic Encryption Computation Privacy)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 평문 연산 $f(x)$에 대해 $\mathrm{Eval}(pk, f, \mathrm{Enc}(x)) = \mathrm{Enc}(f(x))$을 만족하는 준동형(Homomorphism) 성질을 갖는 공개키 암호로, 복호화 권한 없는 제3자가 암호문 상태에서 산술/논리 회로를 평가 가능하며, Gentry의 2009년 FHE 구성 이후 LWE/RLWE 격자 난제에 기반한 BGV·BFV·CKKS·TFHE 스킴으로 실용화되었다.
> 2. **가치**: 데이터를 평문으로 복호화하지 않고도 연산을 수행하므로, 클라우드 MLaaS·연합학습·의료 유전체 분석·금융 신용평가에서 "데이터는 암호화된 채로 이동·집계·추론"이 가능하여 GDPR/개인정보보호법 제29조(안전조치의무) 및 EU AI Act의 학습데이터 최소 노출 원칙을 기술적으로 충족하며, Microsoft SEAL/OpenFHE 기준 128-bit 보안 레벨에서 평균 오버헤드는 평문 대비 1,000~10,000배 수준이다.
> 3. **판단 포인트**: (1) 정확도 vs 노이즈 예산(Noise Budget) trade-off에서 CKKS는 부동소수점 근사 연산에 유리하고 BFV는 정수 산술·통계 집계에 강하며, (2) Bootstrapping 비용(TFHE 기준 10~50ms/gate, CKKS 기준 수십 초) vs Leveled FHE 깊이 한계 선택, (3) MPC·ZKP·TEE(Intel SGX/TDX)·DP(Differential Privacy)와의 하이브리드 아키텍처 설계가 실무 핵심 의사결정 포인트다.

---

## Ⅰ. 개요 및 필요성

클라우드 컴퓨팅과 데이터 외부화(Outsourcing)가 보편화되면서, 데이터 소유자(Data Owner)는 자신의 민감 평문(plaintext)을 클라우드 제공자(CSP)에게 노출하지 않은 채로 데이터 처리·분석·ML 추론을 위탁해야 하는 *두 마리 토끼*의 요구가 발생했다. 전통적 암호화는 *저장 시점(At-Rest)* 과 *전송 시점(In-Transit)* 만 보호하며, *사용 시점(In-Use)* 데이터는 평문으로 존재해야만 연산이 가능했다. 이 보안 공백을 메우기 위해 2009년 Craig Gentry는 최초의 **완전준동형암호(Fully Homomorphic Encryption, FHE)** 구성(Based on Ideal Lattice)을 STOC에서 발표했고, 이후 LWE(Learning with Errors)·RLWE(Ring-LWE) 난제에 기반한 2세대(BGV, BFV), 3세대(GSW, FHEW, TFHE), 4세대(CKKS) 스킴으로 발전해왔다.

```text
[기존 암호화 패러다임 vs FHE 패러다임 비교]

   기존 (Confidential Computing 미적용)         FHE 적용
   +------------------------------+         +------------------------------+
   | Client                      |         | Client                       |
   |  |  평문(PII/의료데이터)     |         |  | Enc_K(p) = ct              |
   |  v                          |         |  v                           |
   | +----+ TLS  +----------+   |         | +----+  TLS  +-------------+ |
   | |Enc |------->| Cloud    |   |         | |Enc |------->|  FHE Cloud  | |
   | | ct |       | [Dec]    |   |         | | ct |       |  Eval(f,ct) | |
   | |    |<-------|  평문처리 |   |         | | ct'|<-------|  ct'        | |
   | |Dec | 결과  | [Enc]    |   |         | |Dec | 결과  |  (No Dec!)  | |
   | +----+       +----------+   |         | +----+       +-------------+ |
   +------------------------------+         +------------------------------+
        ❌ 평문 노출 구간 존재                ✅ 평문 노출 0 (End-to-End)
        ❌ 내부자/하이퍼바이저 위협             ✅ CSP가 봐도 암호문
```

**필요성의 기술적 배경**:
- **규제 환경**: GDPR Art.32(Technical Safeguards), HIPAA Security Rule, 한국 개인정보보호법 제29조(안전조치) 및 EU AI Act 고위험군(High-Risk) 시스템의 학습 데이터 프라이버시 요건
- **MLaaS(ML-as-a-Service) 위협 모델**: 입력 프롬프트/유전체 데이터/재무제표가 API 호출 시 평문 노출되는 P1 공격 표면
- **데이터 협업**: 멀티 파티 연합학습(Federated Learning)에서 중간 기울기(gradient)가 Membership Inference Attack에 취약 -> 암호문 집계가 근본 해법
- **양자 내성**: FHE는 NIST PQC 표준화(Kyber, Dilithium)와 동일한 RLWE/LWE 가정에 기반하므로 *Post-Quantum Cryptography* 측면에서도 미래 안전성 확보

- **📢 섹션 요약 비유**: FHE는 "금이 가루 상태로 잠긴 상태에서 요리사가 맛을 보지 않고도 레시피 대로 볶음·간을 맞추는 것"과 같다. 요리사(클라우드)는 재료의 원형을 알 수 없지만, 손님(데이터 소유자)이 시식할 때 정확한 맛이 나온다.

---

## Ⅱ. 아키텍처 및 핵심 원리

동형암호는 평문 공간 $\mathcal{M}$에 대한 두 연산 $\boxplus, \boxdot$과 암호문 공간 $\mathcal{C}$에 대한 두 연산 $\oplus, \odot$가 다음을 만족하는 준동형 사상(homomorphism)을 구성한다.

$$\mathrm{Dec}_k(\mathrm{Enc}_k(m_1) \oplus \mathrm{Enc}_k(m_2)) = m_1 \boxplus m_2$$
$$\mathrm{Dec}_k(\mathrm{Enc}_k(m_1) \odot \mathrm{Enc}_k(m_2)) = m_1 \boxdot m_2$$

**핵심 메커니즘 — 노이즈(Noise) 관리**: LWE/RLWE 기반 FHE의 모든 평문은 작은 오차항 $e \leftarrow \chi$와 함께 $b = a \cdot s + e + \Delta \cdot m$ 형태로 임베딩된다. 연산이 누적될수록 노이즈가 팽창(특히 곱셈에서 *연산 깊이* $d$에 대해 대략 $O(B^d)$로 폭증)하여, 노이즈가 평문 임계값 $\Delta/2$를 초과하면 복호화 실패가 발생한다. 이를 해결하는 두 전략이 **Leveled FHE**(미리 깊이를 가정해 파라미터 산정)와 **Bootstrapping**(노이즈가 찬 암호문을 *동형적으로* 재암호화하여 노이즈 리셋)이다.

```text
[FHE 연산 파이프라인 및 노이즈 진화]

   Client (Data Owner)               FHE Cloud                Key Owner
   ---------------------             -----------              ----------
   ① GenParams(λ=128, d=10)
   ② KeyGen() -> {pk, sk, evk}
   ③ m₁, m₂, m₃ -> Encoding        +--------------+
       (plaintext modulus p)       |   Ring:      |
   ④ ct_i = Enc(pk, m_i)           |   R = Z_q[x] |
   ⑤ Upload: ct₁, ct₂, ct₃ -------->|              |
       + evk (bootstrapping key)    |  Eval(f, cts)|
                                   |              |
                                   |  ct₁ ⊕ ct₂  |  <--- Addition: 노이즈 add
                                   |       |      |      (성장률 낮음, +1)
                                   |       v      |
                                   |  res ⊗ ct₃  |  <--- Multiplication: 노이즈 ×²
                                   |       |      |      (성장률 높음, -> O(B²))
                                   |       v      |
                                   |  Level v     |
                                   |   +-----+    |
                                   |   |Boot |    |  <--- Refresh: ct -> ct' (noise->0)
                                   |   |strap|    |      Homomorphic Decryption
                                   |   +-----+    |      using encrypted sk
                                   +------+-------+
                                          v
   ⑥ Download: ct_result <------- Result ciphertext
   ⑦ Dec(sk, ct_result) -> f(m₁,m₂,m₃) ✅ 평문 복구
   (CSP는 절대 sk 접근 불가)
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **KeyGen 모듈** | 비밀키/공개키/평가키 생성 | Ring-LWE 샘플링 $s, a \in R_q$, 오차 $\chi$에서 $pk = (a, b = a\cdot s + e)$; `evk`(Bootstrapping Key)는 $s$의 암호화된 비트를 Galois Key $\sigma$와 함께 포함 |
| **Encoder/Encryptor** | 평문 임베딩 및 암호화 | BFV: 정수 $m \in \mathbb{Z}_t$를 $p \cdot m$으로 스케일링 후 $R_q$에 임베딩. CKKS: 복소수 $z$를 $\Delta \cdot z$로 스케일링(근사 오차 허용). TFHE: 비트 단위 TLWE 샘플링 |
| **Evaluator** | 암호문 회로 평가 | NTT(Number Theoretic Transform) 기반 다항식 곱셈 $\mathcal{O}(n \log n)$, Modular Reduction(Rescale/ModSwitch), Relinearization(2차->1차 암호문 압축), Rotation(Galois 자동자) |
| **Bootstrapper** | 노이즈 리프레시 | TFHE: $\sim$10–50ms/gate, *Programmable Bootstrapping*(PBS)으로 LUT 평가 동시 수행. CKKS: *CKKS Bootstrap* (Cheon et al. 2018, 30–60s/refresh), *stC*·*pbs-stc* 최적화로 5–10s 단축 |
| **Decryptor** | 평문 복원 | $\tilde{m} = (b - a \cdot s) \bmod q$, $\Delta$로 나눈 후 rounding: $m = \lfloor \tilde{m} / \Delta \rceil$ |

**스킴별 세부 파라미터와 트레이드오프**:

| 스킴 | 평문 공간 | 노이즈 관리 | 대표 라이브러리 | Bootstrapping 비용 | 적합 워크로드 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **BGV** (Brakerski–Gentry–Vaikuntanathan, 2011) | 정수 $\mathbb{Z}_p$ | Modulus Switching | HElib, OpenFHE | 수십 초 | 정수 산술, Boolean 회로 |
| **BFV** (Fan–Vercauteren, 2012) | 정수 $\mathbb{Z}_p$ | Modulus Switching (RNS) | Microsoft SEAL, OpenFHE | 수십 초 (낮은 depth) | 정수 통계, 행렬 연산 |
| **CKKS** (Cheon–Kim–Kim–Song, 2017) | 부동소수 근사 | Rescaling (Fixed Manual Scale) | HEAAN, OpenFHE, Lattigo, Concrete-ML | 5–60초 (현실적) | 머신러닝, 통계, 신호처리 |
| **TFHE** (Chillotti et al., 2016) | 비트/메시지 | Programmable Bootstrapping | TFHE-rs, Concrete | 10–50ms | Boolean 회로, lookup table, 임의 깊이 |
| **FHEW** (Ducas–Micciancio, 2015) | 비트 | Gate Bootstrapping | OpenFHE(이전 PALISADE) | 30–100ms | 빠른 Boolean gate |
| **GSW** (Gentry–Sahai–Waters, 2013) | 비트 | Matrix 형태 (Gadget) | (주로 이론) | – | 이론 분석, TFHE 전신 |

**보안성**: Ring-LWE는 이상 격자(Ideal Lattice)上の SVP(Shortest Vector Problem) 어려움에 환원되며, 128-bit 보안을 위해 $n=2^{14}$, $q \approx 2^{900}$, 오차 분포 $\sigma \approx 3.2$ (Gaussian) 사용(OpenFHE `HEStd_128_classic`). NIST PQC Kyber와 유사한 가정이라 양자 컴퓨터에 내성.

- **📢 섹션 요약 비유**: FHE 노이즈 예산은 "물컵에 담긴 진흙탕 물"과 같다. 한 번 쓸 때마다 진흙이 조금씩 쌓이고(노이즈 증가), 곱셈은 폭포수(급격한 누적)다. Bootstrapping은 "물컵을 통째로 깨끗한 정수기로 갈아 끼우는" 작업이며, 이게 FHE의 가장 비싼 비용이다.

---

## Ⅲ. 비교 및 연결

**FHE vs 다른 Privacy-Enhancing Technologies(PETs)**

| 구분 | FHE (동형암호) | MPC/SMC (다자 안전계산) | ZKP (영지식증명) | TEE (Trusted Execution Env) | DP (차등프라이버시) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **핵심 원리** | 암호문 상에서 회로 평가 | 비밀분할 + 다자 프로토콜 | NP-문제를 영지식으로 증명 | 하드웨어 격리(Enclave) 내 평문 연산 | 결과에 노이즈 인가 |
| **연산 모델** | 단일 서버(Offload) | 다수 서버(Active/Honest) | Prover/Verifier | CPU/GPU Enclave | 통계 쿼리 |
| **연산 깊이** | 무제한(Bootstrap), 단 비용 큼 | 무제한(Round별 통신) | 회로 크기에 비례 | 평문 수준(매우 빠름) | 무제한 |
| **성능 오버헤드** | 1,000–10,000× | 100–1,000× (통신 병목) | 100× (Prove), 1ms (Verify) | 1–10% (HW 지원 시) | 1× (단 정확도 손실) |
| **신뢰 가정** | Ring-LWE 격자 난제 | 소수 정직(Semi-honest) 가정 | 계산/통계적 가정 | HW 제조사(Intel/AMD/ARM) | 데이터 분포 사전지식 |
| **출력 형태** | 암호문(원본 형태) | 공유(shares) | 단일 비트/문 | 평문(Enclave 내부) | 노이즈 첨가 결과 |
| **통신 비용** | 1-RTT(비대칭) | n-Party ≥ O(n) | 1-RTT(증명전송) | 0-RTT(원격인증) | 없음 |
| **대표 구현** | OpenFHE, SEAL, Lattigo, Zama TFHE-rs | MP-SPDZ, CrypTen, SecretFlow | snarkjs, gnark, Halo2, Plonky3 | Intel SGX/TDX, AMD SEV-SNP, ARM CCA | Opacus, TensorFlow Privacy |
| **적합 시나리오** | 단일 CSP 위탁 ML·DB | 다자 분산 데이터셋 | 블록체인·검증 | 일반 워크로드(범용) | 통계 공개/공공데이터 |
| **한계** | Bootstrapping 비용, 메모리 폭증 |
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 280 / 300

<- **이전**: [279. 차등 프라이버시 노이즈 주입 엡실론 보장 (Differential Privacy Noise Injection Epsilon)](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/279_differential_privacy/)
**다음**: [281. 데이터 주권 국경간 이전 규제 (Data Sovereignty Cross-border Transfer Regulation)](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/281_data_sovereignty/) ->

---
