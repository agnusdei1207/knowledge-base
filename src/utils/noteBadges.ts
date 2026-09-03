import type { NoteStatus, NoteBadgeData } from '../types/note';

/**
 * 출제 상태 문자열을 시맨틱한 NoteStatus('기출' | '미출')로 정규화합니다.
 */
export function normalizeNoteStatus(rawStatus?: string | null): NoteStatus | undefined {
  if (!rawStatus) return undefined;
  const trimmed = rawStatus.trim();
  if (trimmed === '기출') return '기출';
  if (trimmed === '미출' || trimmed === '미출제') return '미출';
  // 불리언이나 기타 truthy 값 대응
  if (trimmed.length > 0) return '미출';
  return undefined;
}

/**
 * 출제 예상 확률 수치를 10~100 범위로 정규화합니다.
 */
export function normalizeNotePriority(rawPriority?: number | string | null): number | undefined {
  if (rawPriority === undefined || rawPriority === null || rawPriority === '') return undefined;
  const num = typeof rawPriority === 'number' ? rawPriority : Number(String(rawPriority).replace(/[^0-9]/g, ''));
  if (Number.isNaN(num)) return undefined;
  return Math.min(100, Math.max(0, num));
}

/**
 * 우선순위(10~100)에 따른 CSS 클래스명을 산출합니다.
 */
export function getPriorityClass(priority: number): string {
  const bucket = Math.min(100, Math.max(10, Math.floor(priority / 10) * 10));
  return `priority-badge priority-${bucket}`;
}

/**
 * "기출 · 70%", "미출 • 50%", "기출", "70%" 등 통합 표기된 뱃지 텍스트를 구조화된 데이터로 파싱합니다.
 */
export function parseNoteBadgeText(text?: string | null): NoteBadgeData {
  if (!text) return {};
  const trimmed = text.trim();

  // "기출 · 70%" 또는 "미출 • 50%" 패턴
  const combinedMatch = trimmed.match(/^(기출|미출|미출제)\s*[·•\-/]\s*(\d+)%?$/);
  if (combinedMatch) {
    return {
      status: normalizeNoteStatus(combinedMatch[1]),
      priority: normalizeNotePriority(combinedMatch[2]),
    };
  }

  // "기출" 또는 "미출" 단독
  if (/^(기출|미출|미출제)$/.test(trimmed)) {
    return {
      status: normalizeNoteStatus(trimmed),
    };
  }

  // "70%" 또는 "예상 70%" 단독
  const priorityMatch = trimmed.match(/(?:예상\s*)?(\d+)%/);
  if (priorityMatch) {
    return {
      priority: normalizeNotePriority(priorityMatch[1]),
    };
  }

  return {};
}
