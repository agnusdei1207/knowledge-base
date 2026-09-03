export type NoteStatus = '기출' | '미출';

export interface NoteExtraMetadata {
  question_no?: string;
  source_status?: string;
  source_history?: string;
  priority?: number;
  priority_note?: string;
}

export interface NoteBadgeData {
  status?: NoteStatus;
  priority?: number;
}
