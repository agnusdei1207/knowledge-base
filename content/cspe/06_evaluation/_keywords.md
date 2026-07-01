---
title: "컴퓨터 시스템 평가 키워드 워크리스트"
date: "2026-07-01"
tags:
  - "cspe-keywords"
weight: 1
---

# 6. 컴퓨터 시스템 평가 출제동향 키워드 (목표 60개)

> 출처: 120~138회 기출 + frequency.md + 공식 8대영역 + 전망. CS(개인 학습용)·keyword_list.md 미사용.

## 성능 평가 (Performance Evaluation)

001. 시스템 성능 지표 — TPS·응답시간·처리량·가용성 (System KPI TPS Response Time) [출제:120,131,133,137회]
002. 응답 시간 분해 — 서비스 시간·대기 시간 (Response Time Decomposition)
003. 처리율·대역폭 (Throughput Bandwidth)
004. 병목 분석 (Bottleneck Analysis)
005. 큐잉 이론 — M/M/1·M/M/c (Queuing Theory) [출제:131회]
006. 리틀의 법칙 (Little's Law)
007. 암달의 법칙 — 병렬화 한계 (Amdahl's Law) [출제:132회]
008. 구스탑슨의 법칙 (Gustafson's Law)
009. 성능 테스트 — 부하·스트레스·소크·스파이크 (Performance Testing Types) [출제:131회]
010. TPS 계산 — 동시 사용자·응답 시간 공식 (TPS Calculation) [출제:131회]
011. APM 애플리케이션 성능 관리 (Application Performance Management) [출제:137회]
012. CPU 이용률·메모리 사용률 측정 (CPU Memory Utilization)
013. 하드웨어 규모 산정 지침 — TPS 기반 (HW Sizing TPS-based) [출제:126,129회]
014. 벤치마크 — SPEC·TPC·LINPACK (Benchmark SPEC TPC LINPACK)
015. BMT 벤치마크 테스트 방법론 (BMT Methodology) [출제:123,127,129회]
016. 프로파일링·핫스팟 분석 (Profiling Hotspot Analysis)
017. 성능 모델링 — 분석 모델·시뮬레이션 (Performance Modeling)

## 신뢰성·가용성 (Reliability & Availability)

018. 시스템 신뢰성 지표 — MTBF·MTTR·MTTF (Reliability Metrics MTBF MTTR) [출제:120,137회]
019. 가용성 계산 — 99.9% vs 99.99% (Availability Calculation) [출제:120회]
020. SLA 서비스 수준 협약 (Service Level Agreement) [출제:123,137회]
021. SLO·SLI (Service Level Objective Indicator) [출제:137회]
022. 오류 예산 Error Budget (Error Budget) [출제:137회]
023. 고가용성 설계 — Active-Active·Active-Standby (High Availability Architecture) [출제:130,137회]
024. 단일 장애점 SPOF 제거 (SPOF Elimination) [출제:137회]
025. 장애 복구 전략 — 핫·웜·콜드 사이트 (Disaster Recovery Site) [출제:136회]
026. RTO·RPO 정의·측정 (RTO RPO) [출제:121회]
027. Split Brain·쿼럼 (Split Brain Quorum) [출제:126회]
028. 자동 페일오버·페일백 (Auto Failover Failback) [출제:137회]
029. 결함 허용 시스템 (Fault-Tolerant System)
030. 이중화 구성 — N+1·2N·2N+1 (Redundancy Configuration)
031. 신뢰성 성장 모델 (Reliability Growth Model) [출제:122회]
032. FTA 결함 나무 분석 (Fault Tree Analysis) [출제:128회]
033. ETA 이벤트 나무 분석 (Event Tree Analysis) [출제:128회]
034. FMEA 고장 모드 영향 분석 (FMEA Failure Mode Effect Analysis)

## 소프트웨어 품질 평가 (SW Quality Evaluation)

035. 소프트웨어 품질 모델 ISO/IEC 25010 (ISO 25010) [출제:120,128회]
036. 품질 특성 — 기능 적합성·성능 효율성·호환성·보안성 (Quality Characteristics) [출제:120회]
037. 소프트웨어 품질 평가 시험 TTA (TTA SW Quality Test) [출제:126,134회]
038. 결함 밀도·결함 제거율 (Defect Density Removal Rate) [출제:122회]
039. 테스트 커버리지 — 구문·분기·MC/DC (Test Coverage) [출제:136회]
040. 소프트웨어 신뢰도 성장 모델 (SW Reliability Growth Model)
041. 기능점수 FP 기반 생산성 측정 (FP Productivity) [출제:126회]
042. 코드 복잡도 — 맥케이브 순환 복잡도 (Cyclomatic Complexity)
043. 정적 분석 결과 해석 (Static Analysis Result Interpretation) [출제:128회]
044. ATAM 아키텍처 트레이드오프 분석 (ATAM) [출제:121,131회]

## 데이터센터·시스템 감리 (DC & Audit)

045. 데이터센터 TIA-942 등급 — Tier 1~4 (TIA-942 Tier Rating) [출제:129회]
046. 전력 사용 효율 PUE (PUE Power Usage Effectiveness) [출제:138회]
047. 물 사용 효율 WUE (WUE Water Usage Effectiveness) [출제:138회]
048. 냉각 효율 — CUE·ERE (Cooling Efficiency CUE ERE)
049. 그린 데이터센터 설계 기준 (Green Data Center Design) [출제:138회]
050. 정보 시스템 감리 절차 (Information System Audit Procedure) [출제:120,121,123,126회]
051. 감리 유형 — 착수·중간·완료·상주 감리 (Audit Types) [출제:120,121회]
052. 감리 점검 항목 — 공공사업 기준 (Audit Checklist) [출제:120,121회]
053. AI 개발 사업 감리 특수 점검 (AI Development Audit) [출제:130,133,135회]
054. 지능정보기술 감리 — 빅데이터·클라우드 (Intelligent IT Audit) [출제:134회]
055. 클라우드 서비스 감리 (Cloud Service Audit) [출제:128,132,136회]
056. CSAP 클라우드 보안 인증 평가 (CSAP Assessment) [출제:129,136회]
057. 정보시스템 성능 관리 방법론 (IS Performance Management)
058. 용량 계획 — 성장률·피크 예측 (Capacity Planning)
059. IT 서비스 연속성 관리 ITSCM (IT Service Continuity Management) [출제:136회]
060. 디지털 서비스 성숙도 모형 평가 (Digital Service Maturity Evaluation) [출제:138회]
