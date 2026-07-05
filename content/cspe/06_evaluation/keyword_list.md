---
title: "Keyword List"
date: "2026-07-05"
tags:
  - "cspe-evaluation"
weight: 50
---
<컴퓨터 시스템 평가 키워드 목록 (60제)>
컴퓨터시스템응용기술사 시험 출제동향 기반으로 엄선한 컴퓨터 시스템 평가 핵심 키워드입니다.

---

## 1. 시스템 성능 평가 및 벤치마크 (10개)
1. 시스템 성능 지표 (System KPI TPS Response Time) — TPS·응답시간·처리량·가용성 등 시스템 핵심 성능 지표 [출제:120,131,133,137회]
2. 응답 시간 분해 (Response Time Decomposition) — 서비스 시간과 대기 시간으로 구분하여 응답 시간 분석
3. 처리율·대역폭 (Throughput Bandwidth) — 단위 시간당 처리 건수 및 데이터 전송 용량 측정
4. 병목 분석 (Bottleneck Analysis) — 시스템 성능 저하 원인이 되는 병목 구간 식별·해소 기법
5. 성능 테스트 (Performance Testing Types) — 부하·스트레스·소크·스파이크 등 테스트 유형별 목적과 방법 [출제:131회]
6. TPS 계산 (TPS Calculation) — 동시 사용자 수와 응답 시간 기반 TPS 산출 공식 [출제:131회]
7. APM 애플리케이션 성능 관리 (Application Performance Management) — 애플리케이션 레벨 성능 모니터링·진단·최적화 [출제:137회]
8. CPU 이용률·메모리 사용률 측정 (CPU Memory Utilization) — 하드웨어 자원 사용률 측정 및 임계치 관리
9. 벤치마크 (Benchmark SPEC TPC LINPACK) — SPEC·TPC·LINPACK 등 표준 벤치마크 도구와 활용
10. BMT 벤치마크 테스트 방법론 (BMT Methodology) — 제품 비교·선정을 위한 BMT 수행 절차와 기준 [출제:123,127,129회]

## 2. 가용성 및 신뢰성 (17개)
11. 시스템 신뢰성 지표 (Reliability Metrics MTBF MTTR) — MTBF·MTTR·MTTF 기반 신뢰성 정량 평가 [출제:120,137회]
12. 가용성 계산 (Availability Calculation) — 99.9% vs 99.99% 등 가용성 등급별 허용 중단 시간 산출 [출제:120회]
13. SLA 서비스 수준 협약 (Service Level Agreement) — 서비스 제공자와 이용자 간 품질 수준 합의 [출제:123,137회]
14. SLO·SLI (Service Level Objective Indicator) — 서비스 수준 목표치와 측정 지표 정의 [출제:137회]
15. 오류 예산 (Error Budget) — SLO 기반 허용 가능한 장애 시간 예산 관리 [출제:137회]
16. 고가용성 설계 (High Availability Architecture) — Active-Active·Active-Standby 구성 방식 [출제:130,137회]
17. 단일 장애점 SPOF 제거 (SPOF Elimination) — 시스템 내 SPOF 식별 및 이중화를 통한 제거 [출제:137회]
18. 장애 복구 전략 (Disaster Recovery Site) — 핫·웜·콜드 사이트 유형별 복구 전략 [출제:136회]
19. RTO·RPO 정의·측정 (RTO RPO) — 목표 복구 시간·목표 복구 시점 설정 기준 [출제:121회]
20. Split Brain·쿼럼 (Split Brain Quorum) — 클러스터 분리 시 데이터 정합성 보장 메커니즘 [출제:126회]
21. 자동 페일오버·페일백 (Auto Failover Failback) — 장애 감지 시 자동 전환 및 원복 프로세스 [출제:137회]
22. 결함 허용 시스템 (Fault-Tolerant System) — 부분 장애 시에도 서비스를 지속하는 시스템 설계
23. 이중화 구성 (Redundancy Configuration) — N+1·2N·2N+1 이중화 방식별 특징과 적용
24. 신뢰성 성장 모델 (Reliability Growth Model) — 테스트 반복에 따른 신뢰성 향상 추이 모델링 [출제:122회]
25. FTA 결함 나무 분석 (Fault Tree Analysis) — 최상위 사건으로부터 원인을 역추적하는 하향식 분석 [출제:128회]
26. ETA 이벤트 나무 분석 (Event Tree Analysis) — 초기 사건에서 결과를 추적하는 상향식 분석 [출제:128회]
27. FMEA 고장 모드 영향 분석 (FMEA Failure Mode Effect Analysis) — 잠재적 고장 모드와 시스템 영향도 사전 분석

## 3. 성능 모델링 (3개)
28. 큐잉 이론 (Queuing Theory) — M/M/1·M/M/c 모델을 활용한 대기 시간·서비스율 분석 [출제:131회]
29. 리틀의 법칙 (Little's Law) — 시스템 내 평균 체류량 = 도착률 × 평균 체류 시간 관계식
30. 암달의 법칙 (Amdahl's Law) — 병렬화 가능 비율에 따른 성능 향상 한계 산출 [출제:132회]
31. 구스탑슨의 법칙 (Gustafson's Law) — 문제 크기 확장 시 병렬 처리 성능 향상 모델
32. 성능 모델링 (Performance Modeling) — 분석 모델과 시뮬레이션을 활용한 성능 예측 기법
33. 하드웨어 규모 산정 지침 (HW Sizing TPS-based) — TPS 기반 서버·스토리지 용량 산정 방법 [출제:126,129회]

## 4. 모니터링 및 관측 (3개)
34. 프로파일링·핫스팟 분석 (Profiling Hotspot Analysis) — 코드 실행 경로별 자원 소비 집중 구간 분석
35. 용량 계획 (Capacity Planning) — 성장률·피크 예측 기반 인프라 용량 사전 확보 전략
36. 정보시스템 성능 관리 방법론 (IS Performance Management) — 정보시스템 전반의 성능 측정·분석·개선 체계

## 5. 소프트웨어 품질 (10개)
37. 소프트웨어 품질 모델 ISO/IEC 25010 (ISO 25010) — 8대 품질 특성과 하위 특성 체계 [출제:120,128회]
38. 품질 특성 (Quality Characteristics) — 기능 적합성·성능 효율성·호환성·보안성 등 세부 정의 [출제:120회]
39. 소프트웨어 품질 평가 시험 TTA (TTA SW Quality Test) — TTA 인증 기반 SW 품질 시험 절차 [출제:126,134회]
40. 결함 밀도·결함 제거율 (Defect Density Removal Rate) — 코드 규모 대비 결함 수 및 제거 효율 측정 [출제:122회]
41. 테스트 커버리지 (Test Coverage) — 구문·분기·MC/DC 등 커버리지 기준과 측정 방법 [출제:136회]
42. 소프트웨어 신뢰도 성장 모델 (SW Reliability Growth Model) — SW 결함 발견·수정에 따른 신뢰도 향상 모델
43. 기능점수 FP 기반 생산성 측정 (FP Productivity) — 기능점수 산정을 통한 개발 생산성 평가 [출제:126회]
44. 코드 복잡도 (Cyclomatic Complexity) — 맥케이브 순환 복잡도 기반 코드 품질 정량 측정
45. 정적 분석 결과 해석 (Static Analysis Result Interpretation) — 정적 분석 도구 결과의 해석 및 조치 방법 [출제:128회]
46. ATAM 아키텍처 트레이드오프 분석 (ATAM) — 아키텍처 품질 속성 간 트레이드오프 평가 방법 [출제:121,131회]

## 6. 데이터센터 평가 (5개)
47. 데이터센터 TIA-942 등급 (TIA-942 Tier Rating) — Tier 1~4 등급별 인프라 요구사항 및 가용성 [출제:129회]
48. 전력 사용 효율 PUE (PUE Power Usage Effectiveness) — 데이터센터 총 전력 대비 IT 장비 전력 비율 [출제:138회]
49. 물 사용 효율 WUE (WUE Water Usage Effectiveness) — 데이터센터 냉각 등에 사용되는 물 효율 지표 [출제:138회]
50. 냉각 효율 (Cooling Efficiency CUE ERE) — CUE·ERE 등 냉각 관련 에너지 효율 지표
51. 그린 데이터센터 설계 기준 (Green Data Center Design) — 친환경 데이터센터 설계·운영 평가 기준 [출제:138회]

## 7. IT 거버넌스 및 감리 (7개)
52. 정보 시스템 감리 절차 (Information System Audit Procedure) — 정보시스템 구축·운영의 독립적 검증 절차 [출제:120,121,123,126회]
53. 감리 유형 (Audit Types) — 착수·중간·완료·상주 감리 유형별 목적과 수행 시점 [출제:120,121회]
54. 감리 점검 항목 (Audit Checklist) — 공공사업 기준 감리 점검 항목 및 평가 기준 [출제:120,121회]
55. AI 개발 사업 감리 특수 점검 (AI Development Audit) — AI 사업 특성을 반영한 감리 점검 항목 [출제:130,133,135회]
56. 지능정보기술 감리 (Intelligent IT Audit) — 빅데이터·클라우드 등 지능정보 사업 감리 기준 [출제:134회]
57. 클라우드 서비스 감리 (Cloud Service Audit) — 클라우드 전환·운영 사업의 감리 특수 점검 [출제:128,132,136회]
58. CSAP 클라우드 보안 인증 평가 (CSAP Assessment) — 클라우드 보안 인증 등급 및 평가 기준 [출제:129,136회]

## 8. 서비스 연속성 및 디지털 성숙도 (3개)
59. IT 서비스 연속성 관리 ITSCM (IT Service Continuity Management) — 재해·장애 시 IT 서비스 지속을 위한 관리 체계 [출제:136회]
60. 디지털 서비스 성숙도 모형 평가 (Digital Service Maturity Evaluation) — 디지털 전환 수준 진단·평가 프레임워크 [출제:138회]
