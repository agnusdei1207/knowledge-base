---
title: "CXL·메모리풀링 (Compute Express Link / Memory Pooling)"
date: "2026-06-30"
weight: 83
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> CXL(Compute Express Link)은 PCIe 물리계층 위에서 캐시 일관성을 제공하는 개방형 인터커넥트이며, 메모리풀링(Memory Pooling)은 여러 호스트가 공유 메모리 풀을 동적으로 할당받는 분리형 메모리 기술이다.

## Ⅱ. 구성요소 / 원리
- 3대 프로토콜: CXL.io(PCIe 호환), CXL.cache(일관성), CXL.mem(메모리 확장)
- 디바이스 유형: Type1(가속기), Type2(가속기+메모리), Type3(메모리 확장)
- 메모리풀링: 다수 서버가 풀에서 필요량만 할당(Disaggregation)
- 메모리 계층 확장 및 스태틱·다이내믹 용량 공유

## Ⅲ. 흐름도 / 구조
```text
[CPU]─CXL.mem─[Memory Pool]─CXL.mem─[CPU]
                  │
   여러 호스트가 풀에서 동적 할당/회수
   (Stranded Memory 제거, 일관성 유지)
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 메모리 용량 확장·공유, 자원 활용률 향상 |
| 장점 | 캐시 일관성, 동적 풀링, TCO 절감 |
| 한계 | 접근 지연 증가, 스위치·생태계 성숙 필요 |

## Ⅴ. 기술사적 적용
- 메모리 분리(Disaggregation)로 데이터센터 메모리 효율화
- PIM·HBM과 결합한 메모리 중심 아키텍처
- LLM 등 대용량 메모리 워크로드의 용량 한계 극복
