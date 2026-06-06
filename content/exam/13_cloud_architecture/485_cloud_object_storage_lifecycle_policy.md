---
title: "Cloud Object Storage Lifecycle Policy"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 객체 스토리지(Amazon S3, Azure Blob, GCS, NCP Object Storage)에서 객체(Object) 단위로 생성 시점·마지막 접근 시점·버전 상태를 트리거 조건으로 삼아 스토리지 클래스를 자동 전이(Transition)·만료(Expiration)·미완료 멀티파트 청소(AbortIncompleteMultipartUpload)하는 **선언적 규칙 엔진(Declarative Rule Engine)** 이며, XML/JSON 기반 Lifecycle Configuration으로 표현된다.
> 2. **가치**: 액세스 빈도가 시간에 따라 급격히 변하는 워크로드(로그, 백업, 미디어, AI 학습 데이터셋)에서 **월 스토리지 비용을 평균 60~85% 절감**하며, 수동 데이터 마이그레이션 운영 부담을 0에 수렴시키고 GDPR/PCI-DSS 등 데이터 보존 및 삭제 의무를 코드로 자동 이행 가능하게 한다.
> 3. **판단 포인트**: (a) 액세스 패턴 분석의 정확도 vs 정책 복잡도 트레이드오프, (b) 버저닝·Replication·Object Lock과의 상호작용 규칙 숙지, (c) 최소 스토리지 기간(Minimum Storage Duration) 및 최소 청구 가능 객체 크기(Minimum Billable Object Size)로 인한 조기 전이 역효과, (d) 마지막 접근 시간(Last Access Time) 추적의 모니터링 비용까지 종합한 TCO 산정.

---

## Ⅰ. 개요 및 필요성

클라우드 객체 스토리지는 페타바이트~엑사바이트급 비정형 데이터를 무제한 확장 가능한 단일 네임스페이스(Bucket/Container)에 보관한다. 그러나 모든 객체가 동일한 성능·내구성·비용을 요구하지는 않는다. 로그 파일은 7~30일간 빈번히 조회되지만 1년 후에는 법적 보존 목적 외에는 거의 접근되지 않고, AI 학습용 원시 데이터는 학습 1회 후 수년간 콜드 상태로 머문다. 이러한 **시간-의존적 액세스 패턴(Temporal Access Pattern)** 을 무시하고 단일 스토리지 클래스에 두는 것은 클라우드 비용 최적화의 가장 큰 손실 요인이다.

기존 온프레미스 환경의 **계층적 스토리지 관리(HSM, Hierarchical Storage Management)** 는 Tivoli Storage Manager, NetApp DataFabric, EMC Data Domain 등이 파일 단위로 LTO 테이프 라이브러리·디스크 간 자동 마이그레이션을 수행했지만, 정책이 워크로드와 결합되어 있고 적용 범위(수 TB~수십 TB)와 라이선스 비용이 한계였다. 클라우드 객체 스토리지는 **정책을 데이터 자체의 메타데이터(태그, 프리픽스)와 분리**하여, 버킷 단위·프리픽스 단위·태그 단위로 수백만 객체에 대해 일관되게 적용할 수 있는 **데이터-정책-인프라 분리(Decoupling)** 모델을 제공한다.

```text
+----------------------------------------------------------------------+
|         클라우드 객체 스토리지 수명주기 정책 (Lifecycle Policy)        |
|                  +--------------------------+                       |
|                  |   Bucket / Container      |                       |
|                  |   "log-archive-2026"      |                       |
|                  +--------------------------+                       |
|                                 |                                    |
|    +----------------+-----------+--------------+-----------------+  |
|    v                v           v              v                 v  |
|  /raw/          /processed/   /tmp/        /backup/          /dl/  |
|  (원본 로그)     (ETL 결과)   (임시)        (DB 덤프)     (딥러닝) |
|    |                |           |              |                 |  |
|    v                v           v              v                 v  |
| +--------+    +--------+   +--------+    +--------+       +--------+|
| | Day 0  |    | Day 0  |   | Day 0  |    | Day 0  |       | Day 0  ||
| |S3 Std  |---->|S3 Std  |   |S3 Std  |    |S3 Std  |       |S3 Std  ||
| +----+---+    +----+---+   +---+----+    +----+---+       +----+---+|
|      | D+30        | D+30     | D+1          | D+7           | D+30|
|      v             v          v              v                v   |
| +--------+    +--------+   +--------+    +--------+       +--------+
| |S3 IA   |    |S3 IA   |   |  Expire |    |Glacier |       |Glacier |
| | (1Z-IA |    |        |   |  즉시   |    |Instant |       | Deep   |
| | 가능)  |    |        |   |  삭제   |    |Retriev.|       |Archive |
| +----+---+    +----+---+   +--------+    +----+---+       +----+---+
|      | D+90        | D+180                    | D+90           | 1Y
|      v             v                          v                v
| +--------+    +--------+                 +---------+      +--------+
| |Glacier |    |Glacier |                 |Glacier  |      |  만료  |
| |Flexible|    | Deep   |                 |  Deep   |      | (정책) |
| |Retriev.|    |Archive |                 | Archive |      +--------+
| +--------+    +--------+                 +---------+
|
| Legend:  S3 Standard (고가·고성능) -> IA (저가·빈도낮음)
|          -> Glacier (초저가·아카이브) -> Expiration (소멸)
+----------------------------------------------------------------------+
```

**왜 필요한가? — Before vs After**

| 항목 | Before (단일 클래스) | After (Lifecycle 적용) |
|---|---|---|
| 1PB 로그 5년 보관 비용 (예시) | $23K/월 (S3 Standard) | $3.1K/월 (D+30 IA, D+90 Glacier) — **86% 절감** |
| 데이터 삭제 누락 리스크 | 수동 스크립트·사람 의존 | Expiration 규칙으로 자동 삭제·감사 로그 자동 생성 |
| 컴플라이언스 증적 | 별도 거버넌스 시스템 필요 | Object Lock·Lifecycle 결합으로 WORM 자동화 |
| 운영 부담 | 야간 배치로 수동 마이그레이션 | 이벤트 기반·서버리스 자동 처리 |

- **📢 섹션 요약 비유**: 수명주기 정책은 **도서관의 사서(司書)** 와 같다. 신간은 대출대에, 1년 지난 책은 지하 서고로, 10년 지난 학술지는 자동 폐기하거나 마이크로필름으로 보내듯, **데이터의 ‘나이’** 와 ‘이용 빈도’를 기준으로 보관 위치를 자동 재배치하는 시스템이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

수명주기 정책은 **평가 엔진(Policy Evaluation Engine)** 이 객체의 메타데이터(생성일, Last-Modified, Last-Accessed, Version ID, 태그, 크기)와 사전 정의된 규칙을 매시간(또는 S3의 경우 하루 1회) 비교하여 액션을 실행하는 구조다. 정책은 **Bucket 단위**로 부착되며, **최대 1,000개 규칙** 까지 등록 가능하다(AWS S3 기준, GCP/Naver는 유사).

### 정책 구조 (AWS S3 Lifecycle Configuration)

```text
LifecycleConfiguration
|
+-- Rule[1]  (ID="log-tiering", Status=Enabled)
|    +-- Filter
|    |    +-- Prefix  = "raw/"
|    |    +-- Tag     = {Key=Project, Value=ecommerce}
|    +-- Transition[1]   Days=30  -> StorageClass=STANDARD_IA
|    +-- Transition[2]   Days=90  -> StorageClass=GLACIER_IR
|    +-- Transition[3]   Days=365 -> StorageClass=DEEP_ARCHIVE
|    +-- Expiration                Days=2555 (≈7년)
|    +-- AbortIncompleteMultipartUpload  DaysAfterInitiation=7
|
+-- Rule[2]  (ID="temp-cleanup", Status=Enabled)
|    +-- Filter  Prefix="tmp/"
|    +-- Expiration  Days=1
|
+-- Rule[3]  (ID="noncurrent-cleanup", Status=Enabled)
|    +-- Filter  Prefix=""
|    +-- NoncurrentVersionExpiration        NoncurrentDays=30
|    +-- NoncurrentVersionTransition[1]     NoncurrentDays=15 -> IA
|    +-- NoncurrentVersionTransition[2]     NoncurrentDays=60 -> Glacier
|    +-- ExpiredObjectDeleteMarker          true
|
+-- Rule[4]  (ID="size-based-rule", Status=Enabled)
     +-- Filter
     |    +-- ObjectSizeGreaterThan = 131072   (128KB)
     |    +-- ObjectSizeLessThan    = 5368709120 (5GB)
     +-- Transition  Days=0 -> INTELLIGENT_TIERING
```

### 데이터 흐름 및 평가 알고리즘

```text
[ Object Upload / Last-Access Event ]
              |
              v
   +----------------------+
   |  Metadata Ingestion  |  (Prefix, Tags, LastModified, Size, VersionId)
   +----------+-----------+
              |
              v
   +----------------------------------------------+
   |  Policy Evaluation Engine  (주기: S3=24h,    |
   |  Azure=24h, S3 Intelligent-Tiering=실시간)   |
   +----------+-----------------------------------+
              |
              |  for each rule R:
              |    if (object satisfies R.Filter):
              |      evaluate Age-based conditions
              |      (Days from LastModified, NoncurrentDays)
              |      -----------------------+
              |                             v
              |       +--------------------------------------+
              |       | Action Execution (비동기, 분산 처리)   |
              |       |  • Transition: storage class 변경     |
              |       |  • Expiration: 객체 영구 삭제         |
              |       |  • AbortMultipart: 미완료 업로드 취소 |
              |       +----------------+---------------------+
              |                        v
              |       +--------------------------------------+
              |       | S3 Storage Lens / Cost Explorer       |
              |       | -> 메트릭 발행·비용 집계              |
              |       +--------------------------------------+
              v
   +----------------------------------------------+
   | CloudTrail / Audit Log  (정책 변경·적용 이력)|
   +----------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Policy Document (XML/JSON)** | 선언적 규칙 저장소 | `LifecycleConfiguration` 리소스; AWS는 S3 API `PutBucketLifecycleConfiguration`, Azure는 `Management Policy` (REST PUT), GCP는 `Lifecycle Rule` (`gcloud storage buckets update`) |
| **Filter (필터)** | 적용 대상 객체 식별 | `Prefix` (경로) / `Tag` (Key-Value) / `ObjectSizeGreater/LessThan` / `And` 연산자 조합. 빈 Prefix는 버킷 전체. |
| **Transition Action** | 스토리지 클래스 이동 | `Days` 또는 `Date` 트리거. 최소 보관 기간(S3 IA=30일, Glacier IR=90일, Deep Archive=180일) 미달 시 미리 전이 불가. |
| **Expiration Action** | 객체 영구 삭제 | `Days=0` 가능. 버전 관리 시 `DeleteMarker` 생성 또는 `ExpiredObjectDeleteMarker=true`로 비관리 마커 정리. |
| **NoncurrentVersion** | 비현재 버전 처리 | 버저닝 활성화 시에만 동작. `NoncurrentDays`로 이전 버전의 별도 수명 관리. |
| **AbortIncompleteMultipartUpload** | 미완료 멀티파트 정리 | `DaysAfterInitiation` (권장 7일). 미종료 시 스토리지 과금·데이터 누수 방지. |

### 핵심 파라미터 및 알고리즘

**1. 트리거 시점 결정 알고리즘**
- **Time-based (Days)**: `TriggerDate = ObjectCreationDate + Days`. S3는 UTC 자정 기준 평가.
- **Date-based**: `YYYY-MM-DD` 형식 절대 시점. 1회성 일괄 마이그레이션에 유리.

**2. 최소 보관 기간(Minimum Storage Duration) — 비용 역효과 방지 핵심**
| 스토리지 클래스 | 최소 보관 기간 | 최소 청구 가능 객체 크기 | 비고 |
|---|---|---|---|
| S3 Standard-IA | 30일 | 128KB | 30일 이전 전이/삭제 시 잔여 일수 요금 |
| S3 One Zone-IA | 30일 | 128KB | 단일 AZ, AZ 장애 시 데이터 손실 |
| S3 Glacier Instant Retrieval | 90일 | 128KB | 밀리초 단위 검색 |
| S3 Glacier Flexible Retrieval | 90일 | 40KB | 1분~12시간 검색 |
| S3 Glacier Deep Archive | 180일 | 40KB | 12~48시간 검색 |
| Azure Cool | 30일 | — | LRS/GRS 모두 동일 |
| Azure Archive | 180일 | — | 온라인 검색 불가, 우선 순위 해제 가능 |

**3. Last Access Time (LAT) 추적**
S3 Standard-IA·IA·One Zone-IA는 **Last Access Time** 기반으로 과금 모델이 진화했다(2024년 기준). 모니터링 자동화를 위한 LAT 추적 옵션은 **추적 활성화 시 IA 클래스 과금 약 2~3% 상승**하며, Lifecycle 자체와는 별개로 운영된다.

**4. 동시성·일관성 보장**
- 평가 엔진은 **Eventually Consistent** 모델: 정책 변경 후 최대 48시간(S3 기준) 이내 모든 객체에 반영.
- Transition 중 객체는 **두 클래스 모두에 일시적 과금** 발생 가능 (S3 기준 transition 작업이 24시간 미만일 때도 1일 요금 이중 청구).

- **📢 섹션 요약 비유**: 수명
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 485 / 800

<- **이전**: [484. DNS 기반 글로벌 로드 밸런싱 GSLB](/studynote/13_cloud_architecture/06_exam_summary/484_dns_based_global_load_balancing_gslb/)
**다음**: [486. 클라우드 블록 스토리지 EBS 디스크](/studynote/13_cloud_architecture/06_exam_summary/486_cloud_block_storage_ebs_disk/) ->

---
