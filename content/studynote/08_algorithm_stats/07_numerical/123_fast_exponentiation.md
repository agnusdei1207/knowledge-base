+++
title = "004. 빠른 거듭제곱 — Fast Exponentiation"
date = 2026-04-05

[taxonomies]
tags = ["studynote-algorithm-stats"]

[extra]
tags = ["studynote-algorithm-stats"]
+++

> **핵심 인사이트**
> 1. 빠른 거듭제곱(Fast Exponentiation)은 a^b를 O(log b) 번의 곱셈으로 계산 — a^b를 나이브하게 계산하면 O(b) 번 곱셈이 필요하지만, 반복 제곱법(Repeated Squaring)을 사용하면 지수를 이진수로 표현하여 O(log b)로 줄인다.
> 2. 모듈러 거듭제곱(Modular Exponentiation)이 암호학의 핵심 연산 — [RSA](/knowledge-base/studynote/09_security/03_network_security/110_rsa/) 암호화·복호화, 디피-헬만 키 교환, 밀러-라빈 소수 판별 모두 a^b mod m 계산에 의존하며, 모듈러 연산을 각 단계에 적용해야 수의 크기가 관리 가능하다.
> 3. 행렬 빠른 거듭제곱으로 피보나치를 O(log N)에 계산 — 스칼라 거듭제곱과 동일한 원리를 행렬에 적용하여 피보나치·선형 점화식을 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 시간에 계산하는 강력한 기법이다.

---

## Ⅰ. 반복 제곱법 (Repeated Squaring)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">나이브한 방법 (O(b)):</div>
<div class="kb-diagram-note">a^8 = a × a × a × a × a × a × a × a</div>
<div class="kb-diagram-note">→ 7번 곱셈 (b-1번)</div>
<div class="kb-diagram-note">반복 제곱법 원리:</div>
<div class="kb-diagram-note">a^8 = (a^4)^2 = ((a^2)^2)^2</div>
<div class="kb-diagram-note">a^1 → a^2(제곱) → a^4(제곱) → a^8(제곱)</div>
<div class="kb-diagram-note">→ 3번 곱셈 (log₂ 8 = 3)</div>
<div class="kb-diagram-note">일반화 (이진 지수):</div>
<div class="kb-diagram-note">b = 13 = 1101₂ = 8 + 4 + 1</div>
<div class="kb-diagram-note">a^13 = a^8 × a^4 × a^1</div>
<div class="kb-diagram-note">계산:</div>
<div class="kb-diagram-note">a^1 (초기값)</div>
<div class="kb-diagram-note">a^2 = (a^1)^2</div>
<div class="kb-diagram-note">a^4 = (a^2)^2</div>
<div class="kb-diagram-note">a^8 = (a^4)^2</div>
<div class="kb-diagram-note">b의 이진수 표현의 각 비트가 1인 위치의 값 곱하기</div>
<div class="kb-diagram-note">→ 곱셈 횟수 = log₂(b) + popcount(b) - 1 ≈ O(log b)</div>
<div class="kb-diagram-note">구현:</div>
<div class="kb-diagram-note">재귀 버전:</div>
<div class="kb-diagram-note">def fast_pow(a, b):</div>
<div class="kb-diagram-note">if b == 0: return 1</div>
<div class="kb-diagram-note">if b % 2 == 0:</div>
<div class="kb-diagram-note">half = fast_pow(a, b // 2)</div>
<div class="kb-diagram-note">return half * half</div>
<div class="kb-diagram-note">else:</div>
<div class="kb-diagram-note">return a * fast_pow(a, b - 1)</div>
<div class="kb-diagram-note">반복 버전 (스택 오버플로우 없음):</div>
<div class="kb-diagram-note">def fast_pow_iter(a, b):</div>
<div class="kb-diagram-note">result = 1</div>
<div class="kb-diagram-note">while b &gt; 0:</div>
<div class="kb-diagram-note">if b &amp; 1: # 현재 비트가 1이면</div>
<div class="kb-diagram-note">result *= a</div>
<div class="kb-diagram-note">a *= a # a를 제곱</div>
<div class="kb-diagram-note">b &gt;&gt;= 1 # 다음 비트로</div>
<div class="kb-diagram-note">return result</div>
<div class="kb-diagram-note">성능 비교:</div>
<div class="kb-diagram-note">a^1000000:</div>
<div class="kb-diagram-note">나이브: 999,999번 곱셈</div>
<div class="kb-diagram-note">반복 제곱: 20번 (log₂ 1,000,000 ≈ 20)</div>
<div class="kb-diagram-note">→ 50,000배 빠름</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 반복 제곱법 = 종이 접기 — 종이 한 번 접으면 2배, 두 번 4배, 10번 1024배. a^1024는 1023번 곱하기 대신 10번 제곱으로! 이진수가 핵심!

---

## Ⅱ. 모듈러 거듭제곱



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">모듈러 거듭제곱 (Modular Exponentiation):</div>
<div class="kb-diagram-note">a^b mod m 계산</div>
<div class="kb-diagram-note">나이브 문제:</div>
<div class="kb-diagram-note">a = 2, b = 1000, m = 10^9 + 7</div>
<div class="kb-diagram-note">a^b = 2^1000 = 10^301 자리 수!</div>
<div class="kb-diagram-note">→ 메모리, 처리 불가</div>
<div class="kb-diagram-note">핵심 성질:</div>
<div class="kb-diagram-note">(a × b) mod m = ((a mod m) × (b mod m)) mod m</div>
<div class="kb-diagram-note">→ 각 단계에서 mod 취하면 수의 크기를 m 이하로 유지</div>
<div class="kb-diagram-note">모듈러 거듭제곱 구현:</div>
<div class="kb-diagram-note">def mod_pow(a, b, m):</div>
<div class="kb-diagram-note">result = 1</div>
<div class="kb-diagram-note">a %= m # 초기 mod 처리</div>
<div class="kb-diagram-note">while b &gt; 0:</div>
<div class="kb-diagram-note">if b &amp; 1:</div>
<div class="kb-diagram-note">result = (result * a) % m</div>
<div class="kb-diagram-note">a = (a * a) % m</div>
<div class="kb-diagram-note">b &gt;&gt;= 1</div>
<div class="kb-diagram-note">return result</div>
<div class="kb-diagram-note"># Python 내장 함수 (더 빠름)</div>
<div class="kb-diagram-note">pow(a, b, m) # C 구현, 최적화됨</div>
<div class="kb-diagram-note">사용 사례:</div>
<div class="kb-diagram-note">RSA 암호화:</div>
<div class="kb-diagram-note">C = M^e mod n (공개키 암호화)</div>
<div class="kb-diagram-note">M = C^d mod n (개인키 복호화)</div>
<div class="kb-diagram-note">e, d, n: 수백~수천 비트</div>
<div class="kb-diagram-note">pow(M, e, n) 호출 한 번으로 처리</div>
<div class="kb-diagram-note">페르마 소정리 확인:</div>
<div class="kb-diagram-note">a^(p-1) mod p == 1 이면 p는 소수 (후보)</div>
<div class="kb-diagram-note">pow(a, p-1, p)</div>
<div class="kb-diagram-note">조합 수 mod p:</div>
<div class="kb-diagram-note">C(n, k) mod p = n! / (k! × (n-k)!) mod p</div>
<div class="kb-diagram-note">분모의 역원 = pow(k! × (n-k)!, p-2, p) (페르마 소정리)</div>
<div class="kb-diagram-note">nCr = (n! * pow(factorial(r) * factorial(n-r), p-2, p)) % p</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 모듈러 거듭제곱 = 시계 덧셈 — 2^1000을 직접 계산하면 300자리 수. 시계(mod)로 계산하면 항상 0~[11](/knowledge-base/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/) 사이. [RSA](/knowledge-base/studynote/09_security/03_network_security/110_rsa/), 소수 판별 모두 "시계 덧셈"!

---

## Ⅲ. 행렬 빠른 거듭제곱



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">행렬 빠른 거듭제곱:</div>
<div class="kb-diagram-note">스칼라 거듭제곱과 동일한 반복 제곱법을 행렬에 적용</div>
<div class="kb-diagram-note">피보나치 O(log N) 계산:</div>
<div class="kb-diagram-note">점화식:</div>
<div class="kb-diagram-note">F(n) = F(n-1) + F(n-2)</div>
<div class="kb-diagram-note">행렬 표현:</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">F(n+1)</div><div class="kb-diagram-node">1 1</div><div class="kb-diagram-note">^n</div><div class="kb-diagram-node">F(1)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">F(n)</div><div class="kb-diagram-note">=</div><div class="kb-diagram-node">1 0</div><div class="kb-diagram-note">×</div><div class="kb-diagram-node">F(0)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">1 1</div><div class="kb-diagram-note">^n = 행렬 A의 n제곱</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">1 0</div></div>
<div class="kb-diagram-note">A^n을 빠른 거듭제곱으로 계산 → O(log n)</div>
<div class="kb-diagram-note">구현:</div>
<div class="kb-diagram-note">def mat_mul(A, B, mod):</div>
<div class="kb-diagram-note">n = len(A)</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">C = [</div><div class="kb-diagram-node">0</div><div class="kb-diagram-note">*n for _ in range(n)]</div></div>
<div class="kb-diagram-note">for i in range(n):</div>
<div class="kb-diagram-note">for k in range(n):</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">if A</div><div class="kb-diagram-node">i</div><div class="kb-diagram-node">k</div><div class="kb-diagram-note">== 0: continue</div></div>
<div class="kb-diagram-note">for j in range(n):</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">C</div><div class="kb-diagram-node">i</div><div class="kb-diagram-node">j</div><div class="kb-diagram-note">= (C</div><div class="kb-diagram-node">i</div><div class="kb-diagram-node">j</div><div class="kb-diagram-note">+ A</div><div class="kb-diagram-node">i</div><div class="kb-diagram-node">k</div><div class="kb-diagram-note">* B</div><div class="kb-diagram-node">k</div><div class="kb-diagram-node">j</div><div class="kb-diagram-note">) % mod</div></div>
<div class="kb-diagram-note">return C</div>
<div class="kb-diagram-note">def mat_pow(A, p, mod):</div>
<div class="kb-diagram-note">n = len(A)</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">result = [</div><div class="kb-diagram-node">1 if i==j else 0 for j in range(n)</div><div class="kb-diagram-note">for i in range(n)]</div></div>
<div class="kb-diagram-note">while p &gt; 0:</div>
<div class="kb-diagram-note">if p &amp; 1:</div>
<div class="kb-diagram-note">result = mat_mul(result, A, mod)</div>
<div class="kb-diagram-note">A = mat_mul(A, A, mod)</div>
<div class="kb-diagram-note">p &gt;&gt;= 1</div>
<div class="kb-diagram-note">return result</div>
<div class="kb-diagram-note">def fib(n, mod=10**9+7):</div>
<div class="kb-diagram-note">if n &lt;= 1: return n</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">A = [</div><div class="kb-diagram-node">1, 1</div><div class="kb-diagram-note">,</div><div class="kb-diagram-node">1, 0</div><div class="kb-diagram-note">]</div></div>
<div class="kb-diagram-note">M = mat_pow(A, n-1, mod)</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">return M</div><div class="kb-diagram-node">0</div><div class="kb-diagram-node">0</div></div>
<div class="kb-diagram-note"># F(10^18 mod 10^9+7) 계산 가능!</div>
<div class="kb-diagram-note">응용:</div>
<div class="kb-diagram-note">선형 점화식 일반 풀이:</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">a</div><div class="kb-diagram-node">n</div><div class="kb-diagram-note">= c1*a</div><div class="kb-diagram-node">n-1</div><div class="kb-diagram-note">+ c2*a</div><div class="kb-diagram-node">n-2</div><div class="kb-diagram-note">+ ... + ck*a</div><div class="kb-diagram-node">n-k</div></div>
<div class="kb-diagram-note">→ k×k 행렬 거듭제곱으로 O(k³ log n) 해결</div>
<div class="kb-diagram-note">타일링 문제, 계단 오르기, 경로 수 계산...</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 행렬 거듭제곱 = 변환 반복 빠른 계산 — 피보나치를 100억 번 더하는 대신 행렬 변환을 33번 적용(log₂ [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)^[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) ≈ 33). F([10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)^18)도 60번 행렬 곱으로!

---

## Ⅳ. 코딩테스트 활용 패턴



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">패턴 1: 대용량 거듭제곱 mod p</div>
<div class="kb-diagram-note">문제: a^b mod (10^9+7) 계산 (b ≤ 10^18)</div>
<div class="kb-diagram-note">→ pow(a, b, 10**9+7)</div>
<div class="kb-diagram-note">패턴 2: 모듈러 역원 (Modular Inverse)</div>
<div class="kb-diagram-note">a^(p-2) mod p = a의 역원 (페르마 소정리, p는 소수)</div>
<div class="kb-diagram-note">→ pow(a, p-2, p)</div>
<div class="kb-diagram-note">패턴 3: 이항계수 mod p</div>
<div class="kb-diagram-note">C(n, k) mod p:</div>
<div class="kb-diagram-note">MOD = 10**9 + 7</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">fact =</div><div class="kb-diagram-node">1</div><div class="kb-diagram-note">* (n+1)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">for i in range(1, n+1): fact</div><div class="kb-diagram-node">i</div><div class="kb-diagram-note">= fact</div><div class="kb-diagram-node">i-1</div><div class="kb-diagram-note">* i % MOD</div></div>
<div class="kb-diagram-note">def nCr(n, k):</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">return fact</div><div class="kb-diagram-node">n</div><div class="kb-diagram-note">* pow(fact</div><div class="kb-diagram-node">k</div><div class="kb-diagram-note">, MOD-2, MOD) % MOD * pow(fact</div><div class="kb-diagram-node">n-k</div><div class="kb-diagram-note">, MOD-2, MOD) % MOD</div></div>
<div class="kb-diagram-note">패턴 4: 피보나치 n번째 (n ≤ 10^18)</div>
<div class="kb-diagram-note">행렬 거듭제곱 사용</div>
<div class="kb-diagram-note">패턴 5: 경우의 수 mod p (곱의 역원)</div>
<div class="kb-diagram-note">P(n, k) = n! / (n-k)!</div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">n</div><div class="kb-diagram-note">* pow(fact</div><div class="kb-diagram-node">n-k</div><div class="kb-diagram-note">, MOD-2, MOD) % MOD</div></div>
<div class="kb-diagram-note">주의사항:</div>
<div class="kb-diagram-note">Python pow(a, b, m)은 C 최적화됨 → 빠름</div>
<div class="kb-diagram-note">직접 구현보다 pow() 내장 우선 사용</div>
<div class="kb-diagram-note">mod 연산: 각 단계에서 취하지 않으면 수 폭발</div>
<div class="kb-diagram-note">a = 2, b = 10^18, mod 없으면:</div>
<div class="kb-diagram-note">→ 10^(3×10^17) 자리 수 → 불가능</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 코딩테스트 거듭제곱 패턴 — "큰 수 mod p" = pow(a,b,m). "모듈러 역원" = pow(a,p-2,p). "이항계수" = 팩토리얼 × 역원×역원. 3가지 패턴 암기로 80% 해결!

---

## Ⅴ. 실무 시나리오 — [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 서명 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">ECDSA 서명 검증에서의 모듈러 거듭제곱:</div>
<div class="kb-diagram-note">배경:</div>
<div class="kb-diagram-note">비트코인/이더리움: ECDSA (타원 곡선 디지털 서명)</div>
<div class="kb-diagram-note">타원 곡선 점 덧셈 + 스칼라 곱셈</div>
<div class="kb-diagram-note">내부 연산:</div>
<div class="kb-diagram-note">타원 곡선 스칼라 곱셈: k × G</div>
<div class="kb-diagram-note">(G: 생성 점, k: 개인키)</div>
<div class="kb-diagram-note">구현: 이중-덧셈 알고리즘 (Double-and-Add)</div>
<div class="kb-diagram-note">빠른 거듭제곱과 동일한 원리!</div>
<div class="kb-diagram-note">k의 이진수 표현에서:</div>
<div class="kb-diagram-note">각 비트: 0이면 2배(Double), 1이면 2배 후 덧셈(Add)</div>
<div class="kb-diagram-note">→ O(log k) 번 연산</div>
<div class="kb-diagram-note">서명 검증 과정:</div>
<div class="kb-diagram-note">1. 서명 (r, s) 수신</div>
<div class="kb-diagram-note">2. 공개키 Q = d × G (d: 개인키)</div>
<div class="kb-diagram-note">3. 검증: u1 = H(m) × s^(-1) mod p</div>
<div class="kb-diagram-note">u2 = r × s^(-1) mod p</div>
<div class="kb-diagram-note">4. R = u1 × G + u2 × Q</div>
<div class="kb-diagram-note">5. R.x == r 이면 유효</div>
<div class="kb-diagram-note">모듈러 역원:</div>
<div class="kb-diagram-note">s^(-1) mod p = pow(s, p-2, p) (페르마 소정리)</div>
<div class="kb-diagram-note">(secp256k1: p = 2^256 - 2^32 - 977)</div>
<div class="kb-diagram-note">성능:</div>
<div class="kb-diagram-note">Bitcoin 서명 검증: 수 밀리초</div>
<div class="kb-diagram-note">블록 1개 ~2000 거래 검증: 수 초</div>
<div class="kb-diagram-note">결론:</div>
<div class="kb-diagram-note">고대 반복 제곱법 → 현대 블록체인 보안의 기반</div>
<div class="kb-diagram-note">RSA 암호화, ECDSA, ECC 모두 빠른 거듭제곱 필수</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 서명 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) = 타원 곡선 도장 찍기 — 개인키(k)로 공개키(k×G) [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/). 역산 불가(이산 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 문제). [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)은 빠른 거듭제곱 덕에 수 ms. 수학이 [블록체인 보안](/knowledge-base/studynote/09_security/19_ai_advanced_security/989_blockchain_security/)!

---

## 📌 관련 개념 맵

```
빠른 거듭제곱 (Fast Exponentiation)
+-- 핵심: 반복 제곱법 O(log b)
+-- 응용
|   +-- 모듈러 거듭제곱 (a^b mod m)
|   +-- 행렬 거듭제곱 (피보나치)
|   +-- 타원 곡선 스칼라 곱 (ECDSA)
+-- 암호학 연결
|   +-- RSA 암호화/복호화
|   +-- 밀러-라빈 소수 판별
|   +-- 디피-헬만 키 교환
+-- 코딩테스트 패턴
    +-- pow(a, b, m) 내장 활용
    +-- 모듈러 역원
    +-- 이항계수 mod p
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[고대 이집트 배수법 (기원전 1600년)]
곱셈을 배로 줄이기
빠른 거듭제곱의 원형
      |
      v
[RSA 암호화 (1977)]
모듈러 거듭제곱 필수화
암호학 응용
      |
      v
[ECC (Elliptic Curve, 1985)]
타원 곡선 점 스칼라 곱
더 작은 키 + 동등 보안
      |
      v
[블록체인 ECDSA (2008~)]
비트코인 secp256k1
거래 서명 검증
      |
      v
[현재: 양자 저항 암호]
격자 기반 서명
빠른 거듭제곱 원리 계속
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 반복 제곱법 = 종이 접기 — 10번 접으면 1024배 두께. a^1024도 10번 제곱(×[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/))으로! 1000번 곱하기 대신 10번!
2. 모듈러 거듭제곱 = 시계 계산 — 큰 수를 12시간 시계로 계산. [RSA](/knowledge-base/studynote/09_security/03_network_security/110_rsa/) 암호화도 시계(mod) 안에서 거듭제곱!
3. 행렬 거듭제곱 = 피보나치 마법 — F([10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)^18)을 60번 행렬 곱으로 계산. [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)^18번 더하기 대신 60번으로!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 123 / 175

← **이전**: [003. 소수 판별 — Primality Test](/knowledge-base/studynote/08_algorithm_stats/07_numerical/122_primality_test/)
**다음**: [005. 중국인의 나머지 정리 — CRT](/knowledge-base/studynote/08_algorithm_stats/07_numerical/124_crt/) →

---
