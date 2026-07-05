---
title: 예외 처리 및 오류 복구 (Exception Handling)
date: 2026-07-05
tags: [cspe-software]
weight: 156
---

## Ⅰ. 개요
| 구분 | 내용 |
|---|---|
| 정의 | 프로그램 실행 중 발생하는 비정상적 상황을 감지하고 제어 흐름을 분리하는 기법 |
| 필요성 | 예기치 못한 종료 방지(Robustness), 오류 처리 로직과 비즈니스 로직의 분리 |
| 출제 의도 | 예외 전파(Propagation), try-catch-finally 구조, 트랜잭션 복구 이해 |

## Ⅱ. 구성요소
```text
try {
  // 위험한 코드 (Dangerous Work)
} catch (SpecificException e) {
  // 대응 로직 (Repair/Log)
} finally {
  // 필수 정리 (Resource Release)
}
```
| 구성요소 | 설명 | 비유 |
|---|---|---|
| 예외 객체 | 발생한 오류의 종류와 상세 정보를 담은 데이터 | 사고 경위서 |
| 핸들러 | 예외를 포착하여 처리하는 전용 코드 블록 | 사고 대책 본부 |
| 콜 스택 언와인딩 | 예외 발생 시 적절한 catch를 찾을 때까지 스택 역추적 | 상급 부대 보고 |
> 요약: 예외 처리는 '사고 발생 -> 보고 -> 수습'의 체계적인 단계를 거침.

## Ⅲ. 절차
```text
Error Occurs -> Create Exception Obj -> Throw -> [Stack Unwinding] -> Catch?
      |                                              |                 |
      +------- (No Handler) <--- Terminate App <-----+----- (Yes) -----+
                                                           |
                                                    Run Handler Code
```
1. 예외 발생: 런타임이 0 나누기, Null 참조 등 비정상 상황 감지 및 객체 생성.
2. 예외 던지기(Throw): 현재 실행 흐름을 중단하고 예외 객체를 런타임 시스템에 전달.
3. 전파 및 탐색: 현재 함수에 핸들러가 없으면 호출한 상위 함수로 거슬러 올라가며 검색.
4. 처리 및 재개: 일치하는 catch 블록을 실행하고, finally 구문 통과 후 실행 계속.
> 요약: 적절한 처리기가 없을 경우 시스템은 강제 종료되므로 전파 관리가 중요함.

## Ⅳ. 문제점
- 예외 처리 남용 시 프로그램 실행 경로가 복잡해져 가독성 및 유지보수성 저하.
- catch 블록 내에서 자원 해제를 누락할 경우 리소스 누수(Resource Leak) 발생.

## Ⅴ. 개선방안
- Checked Exception과 Unchecked Exception을 구분하여 명시적 예외 처리 강제.
- Try-with-resources 문법을 활용하여 파일/소켓 등 자원의 자동 닫기 보장.

## Ⅵ. 전망
- 복구 지향 프로그래밍: 오류 발생 시 이전 안전한 상태로 자동 롤백하는 체크포인트 기술.
- AI 자가 치유(Self-healing): 발생한 예외 로그를 분석하여 자동으로 패치를 적용하는 지능형 런타임.
