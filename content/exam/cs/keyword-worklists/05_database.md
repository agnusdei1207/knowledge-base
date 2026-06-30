---
title: "05 데이터베이스 기출-grounded 키워드 워크리스트"
date: "2026-06-30"
tags:
  - "exam-keywords"
  - "cspe"
  - "keyword-worklist"
weight: 5
---

# 05 데이터베이스 기출-grounded 키워드 워크리스트 (목표 ~80개)
> 출처: 120~138회 컴퓨터시스템응용기술사 기출 대조 + content/exam/cs/keyword_list.md + frequency.md + keyword-universe.md + 출제 전망.

## 챕터: 02_modeling_normalization
001. 3단계 스키마(ANSI/SPARC)
002. 데이터 독립성
003. 키(슈퍼/후보/기본/대체/외래)
004. 무결성(개체/참조/도메인) [출제:128,134회]
005. ER 모델
006. 함수적 종속(부분/이행)
007. 이상현상(삽입/삭제/갱신)
008. 정규화(1NF~BCNF/4NF/5NF)
009. 무손실분해
010. 반정규화
011. 논리/물리설계

## 챕터: 03_relational_model
012. 조인(Inner/Outer/Cross/Self)
013. 서브쿼리
014. 윈도우함수
015. 뷰/구체화뷰
016. 인덱스(B+Tree/해시/비트맵/클러스터드/결합)
017. 옵티마이저(RBO/CBO)
018. 실행계획
019. 조인기법(NL/Sort-Merge/Hash)
020. 선택도·카디널리티
021. 파티셔닝(Range/Hash/List)
022. 힌트
023. 바인드변수
024. B-Tree vs LSM-Tree 비교 (B-Tree vs LSM-Tree) [출제:137회]
025. 커버링 인덱스 (Covering Index)
026. 구체화 뷰 갱신 (Materialized View Refresh)
027. 쿼리 재작성 (Query Rewrite)
028. 복합 인덱스 선두 컬럼 (Composite Index Leading Column) [출제:125,134회]

## 챕터: 04_transactions_concurrency
029. ACID [출제:129,131회]
030. 트랜잭션 상태전이
031. 병행수행 문제(Lost Update/Dirty Read/Phantom)
032. 직렬가능성
033. 락(S/X-Lock)
034. 2PL(Strict/Rigorous)
035. 타임스탬프 순서
036. 낙관적 제어
037. MVCC
038. 격리수준(4단계)
039. Redo/Undo
040. WAL
041. 체크포인트
042. ARIES
043. 교착상태(Wait-Die/Wound-Wait) [출제:131,132,134,136회]
044. 대기그래프
045. 스냅샷 격리 (Snapshot Isolation)

## 챕터: 05_distributed_nosql_newsql
046. 분산DB 투명성
047. 데이터분할(수평/수직)
048. 복제(동기/비동기·Master-Slave)
049. 2PC/3PC
050. Saga
051. CAP/PACELC
052. BASE·결과적일관성
053. Raft/Paxos
054. Split Brain
055. NoSQL 4모델(KV/Document/Column/Graph) [출제:137회]
056. 샤딩·샤드키
057. 일관된 해싱
058. NewSQL(Spanner)
059. HTAP
060. LSM-Tree [출제:137회]
061. CDC
062. 클라우드 DB RDS Aurora DynamoDB (Cloud Database Service)
063. DynamoDB 일관성 모델 (DynamoDB Consistency Model)
064. 분산 합의 리더 선출 (Distributed Consensus Leader Election) [출제:138회]
065. 분산 데이터베이스 투명성 (Distributed Database Transparency)

## 챕터: 06_dw_olap_trends
066. DW 4특징
067. 데이터마트·ODS
068. ETL/ELT
069. OLTP vs OLAP
070. OLAP연산(롤업/드릴다운/슬라이스/다이스/피벗)
071. 스타/스노우플레이크 스키마
072. 데이터레이크·레이크하우스 [출제:137회]
073. 스키마 온 리드/라이트
074. 벡터DB·임베딩
075. 유사도검색(코사인/L2)
076. ANN/HNSW
077. RAG [출제:135,136,137,138회]
078. TDE·데이터마스킹
079. SQL 인젝션
080. 데이터 레이크하우스 Delta Iceberg (Lakehouse) [출제:137회]
081. 벡터 인덱스 HNSW (Vector Index HNSW)

> 생성 기준: 총 81개. 목표 수는 시험 출제 가능성 기준의 운영 상한이며, 지엽 키워드는 제외한다.
