---
title: "Cloud KMS Key Management Encryption Service"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 KMS는 FIPS 140-2/3 검증 HSM 내부에서 KEK(Key Encryption Key)를 중앙 집중 관리하고, 평문 DEK(Data Encryption Key)를 Envelope Encryption 패턴으로 발급·암호화하여 실제 데이터 암복호화에 사용함으로써, 키의 평문 노출 없이 무제한 확장으로 데이터 평문 암호화를 가능케 하는 Key-as-a-Service 제어 평면(Control Plane)이다.
> 2. **가치**: AWS KMS 기준 월 1 USD/CMK·20,000 요청 무료, KMS-GenerateDataKey 1회 호출로 GB급 객체까지 처리 가능하여 KMS 자체를 데이터 평문에 노출하지 않음(데이터 평문은 애플리케이션/SDK가 복호화 후 메모리 처리). 자동 키 회전(每年 1회), 256비트 AES-GCM, IAM·KeyPolicy·Grant 3중 접근제어, CloudTrail을 통한 모든 키 사용 API 감사 추적으로 FIPS·PCI-DSS·ISMS-P·개인정보보호법 준수 비용을 수동 HSM 대비 90% 이상 절감한다.
> 3. **판단 포인트**: (a) 단일 리전 vs 멀티 리전 키(Primary/Multi-Region Replica) 선택, (b) CMK 대 AWS/AWS 관리 키(KMS 없이 무비용인 S3 SSE-S3, EBS 기본 암호화)와의 비용 트레이드오프, (c) 자동 회전 vs 사용자 지정 회전 정책(키 1년 vs 컨폼 요구 90일), (d) 봉투 암호화 시 CMK 임포트(ImportMaterial, EXTERNAL) vs HSM 백킹(CloudHSM/EKM), (e) 하이브리드 클라우드에서 BYOK(평문 1회 노출) ↔ HYOK(EKM/외부 HSM, 평문 미노출) ↔ External Key Store(키를 외부 Vault로 유지) 결정이 보안·비용·성능 축에서 결정적 트레이드오프를 형성한다.

---

## Ⅰ. 개요 및 필요성

클라우드 환경에서 데이터는 객체 스토리지(S3, GCS, Azure Blob), 블록 스토리지(EBS, Managed Disk), 관계형 DB(RDS, Cloud SQL, Azure SQL), 컨테이너 시크릿, SaaS 메일/문서, 그리고 전송 중 네트워크 구간에 산재한다. 전통적인 온프레미스 HSM(Thales Luna, Utimaco, AWS CloudHSM Classic 등) 기반 키 관리 체계는 ① 물리적 격리실 운영, ② FIPS 140-2 Level 3 인증 디바이스 유지보수, ③ 키 수명주기·감사 로깅·백업·DR 절차의 전수 수작업, ④ 애플리케이션-키-스토리지 간 N:N 직접 결합이라는 4대 한계를 가졌다. 클라우드 KMS는 이 모든 제어를 **API와 IAM 정책**으로 평준화하고, 키 평문은 **고객이 절대 직접 보지 못하도록 봉투 암호화(Envelope Encryption)** 구조로 캡슐화하여, "키는 누가, 어떻게, 어디서, 얼마나 자주 사용하는가"라는 4W1H 통제 문제를 결정론적으로 해결한다.

특히 **KMS 평문 키는 절대 네트워크를 통해 외부로 전송되지 않는다**는 점이 기존 파일 기반 키 관리(KMIP, PKCS#11) 대비 결정적 차이이다. 클라우드 KMS는 다음을 보장한다:
- **키 평문은 오직 FIPS 140-2/3 검증 HSM의 메모리에서만 존재** -> 일반 EC2/VM의 RAM·디스크에 평문 KEK가 노출되지 않음
- **GenerateDataKey/Decrypt API만 노출** -> 평문 DEK는 SDK로 반환되어 1회성 사용 후 폐기
- **모든 호출은 CloudTrail/Azure Activity Log에 기록** -> 누가, 어떤 리소스에, 어떤 컨텍스트에서 키를 썼는지 변조 불가능 감사
- **자동 회전(Key Rotation) + 별칭(Alias) + 버전(Version)** -> 키 교체 시 애플리케이션 무중단

```text
   [기존 온프레미스 HSM 모델]                          [클라우드 KMS + 봉투 암호화 모델]

  App --+                                         App ---+
        +-- 직접 연결(N:N 결합, IP/Port/인증서)            |      +-- AWS-KMS --- FIPS 140-2 L3 HSM
  App --+                                              +--API--+   (Key Policy + IAM)
        |                                              |      +-- GenerateDataKey(DEK_plain, DEK_wrapped)
  App --+                                         App ---+           |
   |                                                   |              v
   v                                                   |   DEK_wrapped(->S3 헤더 메타데이터 저장)
 HSM Cluster -- 키 평문 보관                              |   DEK_plain (메모리에서만 잠시 존재, 객체 암복호화 후 폐기)
   |                                                   |              |
   v                                                   v              v
 감사 로그(수동 syslog)                              S3에 저장: <EncryptedObject, DEK_wrapped, IV/AuthTag>
                                                       |              |
                                                       +-- 다운로드 시: KMS Decrypt(DEK_wrapped)->DEK_plain->복호화
```

전통적 HSM은 **데이터 평문이 HSM 내부로 흘러들어와야 암복호화**하므로 네트워크·메모리·I/O 대역폭이 HSM의 처리량에 종속된다. 반면 클라우드 KMS는 **키만 HSM이 관리하고, 데이터 평문은 애플리케이션 측에서 처리**하므로 KMS 처리량 한계(예: AWS KMS 5,500 req/s/리전, 1MB 페이로드 한도)에서 벗어나 페타바이트급 데이터도 무제한 암복호화가 가능하다. 이 비대칭이 바로 "KMS는 키 관리를 위한 것이지, 데이터 암복호화 도구가 아니다"라는 격언의 근거이며, 시험에서 빈번히 출제되는 판단 지점이다.

- **📢 섹션 요약 비유**: 기존 HSM이 "은행 금고(보안 최고) + 직접 주거래(처리량 한정)"를 겸하던 시대였다면, 클라우드 KMS는 "키만 지키는 금고(HSM)"와 "데이터는 외부 창고(S3, EBS)에서 처리하는 분업 체계"를 만든 것이다. 은행은 도장만 찍고(Sign/Decrypt), 실제 화물은 물류센터가 움직인다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 KMS는 논리적으로 **제어 평면(Control Plane, KMS API/정책)**과 **데이터 평면(Data Plane, 암호화 연산)**이 분리되어 있다. 제어 평면은 키 생성·회전·정책·IAM 바인딩을 다루고, 데이터 평면은 Encrypt/Decrypt/GenerateDataKey/Re-encrypt 같은 Cryptographic Operation을 처리한다. 모든 데이터 평면 호출은 호출자 인증(Caller) -> 키 정책 평가 -> HSM 내부 키 사용 권한 검증 -> 연산 -> 감사 로그 기록의 5단계를 거친다.

```text
                  [제어 평면: 키 수명주기]
   +------------------------------------------------------------+
   |  CreateKey / DescribeKey / EnableKey / DisableKey           |
   |  ScheduleKeyDeletion (7~30 대기) / CancelKeyDeletion         |
   |  PutKeyPolicy / CreateAlias / TagResource                   |
   |  EnableKeyRotation (자동 365일) / RotateKeyOnDemand         |
   |  ImportKeyMaterial (EXTERNAL ORIGIN) / DeleteImportedKeyMat |
   |  CreateReplicateKey (Multi-Region)                          |
   +------------------------------------------------------------+
                              |
                              v
                  [정책 평가 엔진: 3중 게이트]
   +------------------------------------------------------------+
   |  Gate1: IAM 정책(누가: Principal)                            |
   |  Gate2: KMS Key Policy(누가+어떤 동작: kms:Encrypt 등)       |
   |  Gate3: Grant(임시 위임: kms:GrantConstraints + RetiringPrincipal)|
   |  -> 세 정책이 모두 Allow여야 통과(AND 결합)                     |
   +------------------------------------------------------------+
                              |
                              v
                  [데이터 평면: 암호화 연산]
   +------------------------------------------------------------+
   |  Encrypt(plaintext, KeyId, AAD)         -- AAD로 컨텍스트 바인딩|
   |  Decrypt(ciphertextBlob)                -- 메타데이터에서 KeyId |
   |  GenerateDataKey(KeyId, KeySpec)        -- 평문+암호문 DEK 반환|
   |  GenerateDataKeyWithoutPlaintext        -- 암호문만 (저장 전용)|
   |  Re-encrypt(ciphertext, destKeyId)      -- 키 교체 시 평문 미노출|
   |  Sign/Verify (비대칭/HSM 비대칭 키, Asymmetric Spec 지원)       |
   |  GetPublicKey (비대칭 키의 공개키 회수)                          |
   +------------------------------------------------------------+
                              |
                              v
                [HSM (FIPS 140-2/3 Level 3)]
   +------------------------------------------------------------+
   |  Symmetric: AES-256-GCM, AES-256-CBC+Hmac                  |
   |  Asymmetric: RSA-2048/3072/4096, ECC P-256/384/521,         |
   |              SM2(중국), ML-DSA(양자내성)                      |
   |  HMAC key, RAW key(SecretString 용)                         |
   |  키 평문은 HSM 메모리에서만 잠시 존재, 영구 저장 X             |
   +------------------------------------------------------------+
                              |
                              v
                [감사: CloudTrail/Azure Monitor/GCP Audit Logs]
                            100% 호출 기록, 변조 불가능
```

### 봉투 암호화(Envelope Encryption) 상세 흐름

데이터 평문(GB 단위) -> DEK(AES-256) 평문으로 1회 암복호화 -> DEK 자체는 DEK_Plain으로 KMS에 Encrypt 요청 -> KMS는 HSM 내부 KEK로 DEK_Plain을 wrap -> DEK_Wrapped(CiphertextBlob) 반환 -> DEK_Wrapped는 데이터 메타데이터(예: S3 객체의 `x-amz-meta-x-amz-key`, 객체 헤더, DynamoDB 항목 attribute, EBS 볼륨의 `EncryptionContext`)에 저장. 복호화 시 KMS에 DEK_Wrapped를 보내면 HSM이 KEK로 unwrap 후 DEK_Plain을 반환, 애플리케이션이 데이터 평문 복호화 -> 메모리에서 즉시 폐기. **DEK_Plain은 네트워크로도 디스크로도 영구 저장되지 않는다**는 점이 봉투 암호화의 보안 핵심이다.

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **KEK (Key Encryption Key)** | CMK(Customer Master Key)라고도 함. DEK를 wrap/unwrap하는 최상위 키. 평문은 HSM 내부에만 존재 | AWS KMS의 `Customer master keys` (CMK), Azure Key Vault의 `Key`, GCP Cloud KMS의 `KeyRing/Key/CryptoKeyVersion`에 매핑. KMS_ALGORITHM = AES-256-GCM(대칭), RSA-OAEP(비대칭 KEK) 등. 키 회전 시 KEK Version만 새로 생성, Alias는 동일 -> 클라이언트 코드 무변경 |
| **DEK (Data Encryption Key)** | 실제 사용자 데이터(파일·객체·DB 레코드·디스크 블록)를 암복호화하는 작업 키. 평문은 메모리·디스크 어디에도 영구 저장되지 않음 | `GenerateDataKey(KeySpec=AES_256)` 호출로 (Plaintext, CiphertextBlob) 쌍을 1회 수신 -> Plaintext로 데이터 암복호화 -> CiphertextBlob는 데이터와 함께 저장. 데이터마다 고유 DEK 사용 -> 1 DEK 유출이 다른 데이터에 영향 X(키 분리성, key separation) |
| **HSM (Hardware Security Module)** | KEK 평문을 저장하고 모든 wrap/unwrap을 수행하는 FIPS 인증 경량암호화 디바이스 | AWS CloudHSM(클러스터 3AZ, FIPS 140-2 L3), Azure Dedicated HSM(Thales Luna Network HSM A790), GCP Cloud HSM. KMS는 HSM을 내부적으로 호출하지만 고객은 HSM API에 직접 접근 불가. CloudHSM Custom Key Store 사용 시 고객이 HSM 클러스터를 직접 관리하면서 KMS API로 노출 가능 |
| **정책 엔진 (Policy Engine)** | 키 사용 권한을 3중(또는 4중)으로 평가 | ① IAM(Principal 자격증명), ② KMS Key Policy(리소스 기반, kms:Action 목록), ③ Grant(임시 위임 토큰, RetiringPrincipal로 회수 가능), ④ VPC Endpoint Policy + KMS Condition Key(`kms:EncryptionContext:`, `aws:CalledVia`, `kms:ViaService`). 모든 게이트가 Allow여야 통과. 익명 호출(IAM 없는)은 Key Policy만으로 평가 |

### 비대칭 키 및 양자내성 알고리즘

클라우드 KMS는 대칭 KEK 외에 **비대칭 키 페어**도 관리한다. AWS KMS 기준 `KeyUsage = ENCRYPT_DECRYPT`(RSA-OAEP, AES-KW로 wrap) 또는 `SIGN_VERIFY`(RSA-PSS, ECDSA P-256/P-384/P-521, Ed25519) 두 용도. 비대칭 키는 공개키(`GetPublicKey`)를 외부로 배포하고, **개인키는 HSM 내부에 영구 저장**되어 외부 유출이 원천 차단된다. 2024년 기준 AWS KMS·Azure Key Vault·GCP Cloud KMS 모두 양자내성 알고리즘을 지원하기 시작: AWS는 `ML-DSA`(Module-Lattice, FIPS 204), Azure는 `ML-KEM`/`ML-DSA`(preview), GCP는 `ML-KEM-768`(post-quantum TLS용) 출시. 시험에서는 **HSM 평문 노출 원천 차단 + 양자내성 알고리즘 도입**을 한 묶음으로 자주 출제한다.

### 키 회전(Key Rotation) 메커니즘

- **자동 회전**: AWS KMS는 365일마다 새 Key Material 생성, Alias는 그대로 유지, 내부적으로 `KeyId + Version` 추적 -> `GetKeyRotationStatus`로 모니터링, 비활성화 가능.
- **수동 회전**: `RotateKeyOnDemand` 또는 신규 CMK 생성 + Alias 교체(블루-그린).
- **임포트 키(EXTERNAL)**: 자동 회전 불가. 고객이 자체 키 수명주기 관리(90일 등 정책).
- **회전 시나리오**: 새 DEK는 새 KEK 버전으로 wrap, 기존 객체의 DEK_Wrapped는 그대로(과거 KEK 버전으로 unwrap 가능), 신규 데이터만 새 KEK로 wrap -> 점진적 마이그레이션.
- **회전 후 보존 기간**: AWS KMS는 이전 키 무기한 보존(비활성화·삭제 명시 전까지), Azure는 `Enabled: true` 유지, GCP는 `CryptoKeyVersion` 별도 `Destroy` 명시 전까지 보존.

### Encryption Context (AAD, Additional Authenticated Data)

KMS Encrypt/Decrypt 호출 시 `EncryptionContext = {"department":"finance", "userId":"u-001"}` 형태로 임의 키-값 쌍을 넘기면, AES-GCM의 AAD 영역에 바인딩되어 **복호화 시 동일한 Context를 제시해야만 평문 복원 가능**하다. 이는 우발적 키 재사용·교차 사용자 키 혼선 공격을 막는 결정적 통제 수단이다. S3 SSE-KMS는 객체 ARN을 자동으로 Context로 바인딩하므로, **다른 버킷에 ciphertextBlob이 복사되어도 복호화 불가** -> 키와 데이터의 1:1 결합 보장.

- **📢 섹션 요약 비유**: KEK는 "시계 태엽"이고 DEK는 "현실에서 쓰는 손목시계"이다. 태엽(KEK 평문)은 공장 금고(HSM)에서 절대 나오지 않고, 손목시계(DEK)는 태엽으로 감아 여러 개 찍어내(GenerateDataKey) 사람마다 나눠주며, 시계가 고장나도 태엽만 돌리면 새 시계를 찍어낼 수 있다(
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 436 / 800

<- **이전**: [435. 클라우드 IAM 역할 정책 최소 권한](/studynote/13_cloud_architecture/06_exam_summary/435_cloud_iam_role_policy_least_privilege/)
**다음**: [437. 클라우드 WAF 웹 방화벽 DDoS 보호](/studynote/13_cloud_architecture/06_exam_summary/437_cloud_waf_web_firewall_ddos_protection/) ->

---
