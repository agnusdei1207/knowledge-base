#!/usr/bin/env python3
"""
ASCII 박스 도식 정렬 수정기

코드 블록(```text / ```) 안에서 박스 문자(│┐┘)로 끝나는 줄들의
display width를 통일하여 정렬 깨짐을 해결한다.

원리:
  한글은 터미널에서 2칸 폭인데 1칸 문자(영문/공백)와 혼용하면
  오른쪽 경계(│)가 들쭉날쭉 밀린다.
  → 각 박스 블록에서 "기준 폭(=빈 줄 또는 ┌/└ 줄의 폭)"을 잡고,
    나머지 줄의 오른쪽 경계 직전 공백을 가감하여 맞춘다.
"""

import os
import re
import sys
import unicodedata
from pathlib import Path


def display_width(s: str) -> int:
    """문자열의 터미널 표시 폭 (한글=2, 영문/공백/기호=1)."""
    w = 0
    for c in s:
        if unicodedata.east_asian_width(c) in ('F', 'W'):
            w += 2
        else:
            w += 1
    return w


# 오른쪽 경계로 쓰이는 박스 문자
RIGHT_BORDER = set('│┐┘┤╗╝║╣')
LEFT_BORDER = set('│┌└├╔╚║╠')
TOP_BOTTOM = set('┌┐└┘─╔╗╚╝═')


def is_box_line(line: str) -> bool:
    """박스 도식 줄인지 (왼쪽 또는 오른쪽에 박스 문자가 있는 줄)."""
    stripped = line.strip()
    if not stripped:
        return False
    return any(c in RIGHT_BORDER or c in LEFT_BORDER or c in TOP_BOTTOM for c in stripped)


def find_right_border_char(line: str) -> tuple:
    """줄 끝에서 오른쪽 경계 박스 문자의 위치를 찾는다.
    Returns: (before_border, border_char, after_border) or None
    """
    rstripped = line.rstrip('\n\r')
    if not rstripped:
        return None

    last_char = rstripped[-1]
    if last_char in RIGHT_BORDER:
        # 경계 문자 앞의 공백을 찾는다
        before = rstripped[:-1]
        return (before, last_char, '')

    return None


def fix_box_block(lines: list) -> list:
    """박스 도식 블록 내 줄들의 오른쪽 경계를 정렬한다."""

    # 1. 오른쪽 경계가 있는 줄 식별
    border_info = []
    for i, line in enumerate(lines):
        result = find_right_border_char(line.rstrip('\n'))
        if result:
            border_info.append((i, result))

    if len(border_info) < 2:
        return lines  # 경계 줄이 2개 미만이면 박스가 아님

    # 2. 기준 폭 결정: ┌ 또는 └ 줄의 display width를 기준으로 삼음
    #    (이 줄들은 보통 ─ 반복이라 한글 없이 정확함)
    reference_width = None
    for i, (before, border, _) in border_info:
        full = before + border
        if '┌' in full or '└' in full or '╔' in full or '╚' in full:
            reference_width = display_width(full)
            break

    if reference_width is None:
        # ┌/└ 줄이 없으면 공백만 있는 줄 (│       │) 기준
        for i, (before, border, _) in border_info:
            full = before + border
            if before.rstrip() == before.rstrip().split('│')[0].rstrip() if '│' in before else True:
                # 내용이 거의 없는 줄 (공백만)
                content_after_left = before.lstrip()
                if content_after_left and content_after_left[0] in LEFT_BORDER:
                    remaining = content_after_left[1:]
                    if remaining.strip() == '':
                        reference_width = display_width(full)
                        break

    if reference_width is None:
        # 최후 수단: 모든 경계 줄의 최소 폭
        widths = [display_width(before + border) for _, (before, border, _) in border_info]
        reference_width = min(widths)

    # 3. 각 줄의 오른쪽 공백을 조절하여 기준 폭에 맞춤
    result = list(lines)
    for i, (before, border, _) in border_info:
        current_full = before + border
        current_width = display_width(current_full)

        if current_width == reference_width:
            continue  # 이미 맞음

        # before에서 경계 직전 공백을 찾아 조절
        # 내용 부분과 trailing 공백 분리
        content_part = before.rstrip(' ')
        trailing_spaces = len(before) - len(content_part)

        content_width = display_width(content_part)
        # 필요한 총 폭 = reference_width
        # border 폭 = 1 (박스 문자는 항상 1칸)
        needed_spaces = reference_width - content_width - 1

        if needed_spaces < 0:
            # 내용 자체가 기준 폭을 초과 → 공백 1개만 남김
            needed_spaces = 1

        new_line = content_part + ' ' * needed_spaces + border
        result[i] = new_line

    return result


def process_file(filepath: str, dry_run: bool = False) -> bool:
    """파일 내 코드 블록의 ASCII 박스 도식을 정렬한다."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    new_lines = []
    in_code_block = False
    code_block_lines = []
    changed = False

    for line in lines:
        stripped = line.strip()

        if stripped.startswith('```'):
            if in_code_block:
                # 코드 블록 끝 → 블록 내용 처리
                has_box = any(is_box_line(l) for l in code_block_lines)
                if has_box:
                    fixed = fix_box_block(code_block_lines)
                    if fixed != code_block_lines:
                        changed = True
                        code_block_lines = fixed
                new_lines.extend(code_block_lines)
                new_lines.append(line)
                code_block_lines = []
                in_code_block = False
            else:
                in_code_block = True
                new_lines.append(line)
        elif in_code_block:
            code_block_lines.append(line)
        else:
            new_lines.append(line)

    # 코드 블록이 닫히지 않은 경우
    if code_block_lines:
        new_lines.extend(code_block_lines)

    if changed:
        new_content = '\n'.join(new_lines)
        if not dry_run:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
        return True
    return False


def main():
    dry_run = '--dry-run' in sys.argv
    verbose = '--verbose' in sys.argv or '-v' in sys.argv

    target_dir = 'content/cspe/'
    if len(sys.argv) > 1 and not sys.argv[1].startswith('-'):
        target_dir = sys.argv[1]

    fixed_count = 0
    total_count = 0

    for root, dirs, files in os.walk(target_dir):
        for fname in sorted(files):
            if not fname.endswith('.md'):
                continue
            filepath = os.path.join(root, fname)
            total_count += 1
            try:
                was_fixed = process_file(filepath, dry_run=dry_run)
                if was_fixed:
                    fixed_count += 1
                    if verbose:
                        prefix = '[DRY-RUN] ' if dry_run else ''
                        print(f'{prefix}FIXED  {filepath}')
            except Exception as e:
                print(f'ERROR  {filepath}: {e}', file=sys.stderr)

    mode = 'DRY-RUN' if dry_run else 'APPLIED'
    print(f'\n[{mode}] {fixed_count}/{total_count} files {"would be " if dry_run else ""}fixed')


if __name__ == '__main__':
    main()
