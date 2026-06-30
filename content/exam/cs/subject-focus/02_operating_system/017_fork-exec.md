---
title: "fork·exec (Process Creation)"
date: "2026-06-30"
weight: 17
tags:
  - "exam-cspe-operating-system"
---

## Ⅰ. 정의
> fork()는 호출 프로세스를 복제해 자식 프로세스를 생성하고, exec()는 자식의 주소공간을 새 프로그램 이미지로 덮어쓰는 UNIX 프로세스 생성 메커니즘.

## Ⅱ. 구성요소 / 원리
- fork(): 부모 PCB·주소공간 복제, 자식에 새 PID 부여
- 반환값: 부모는 자식 PID, 자식은 0(분기 판별 근거)
- exec() 계열: 현재 이미지를 새 실행파일로 교체(PID 유지)
- 부모-자식: 동일 코드 시작, 별도 주소공간(COW로 효율화)
- wait(): 부모가 자식 종료 상태 수거(좀비 방지)

## Ⅲ. 흐름도 / 구조
```text
 Parent ---fork()---> [Parent] (pid>0) ---wait()---> 수거
                  \--> [Child]  (pid==0)
                         |
                       exec("prog")  --> 주소공간 교체
                         |
                       new program 실행 --> exit()
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 프로세스 복제·프로그램 교체의 직교적 분리 |
| 장점 | fork/exec 분리로 fd 조정 등 유연한 제어 가능 |
| 한계 | 복제 비용(COW로 완화), exec 실패 시 처리 필요 |

## Ⅴ. 기술사적 적용
- 셸의 명령 실행: fork 후 자식이 exec로 명령 적재
- fork-exec 사이에서 표준입출력 리다이렉션·파이프 연결
- 대비: Windows는 CreateProcess()로 생성·적재 통합 수행
