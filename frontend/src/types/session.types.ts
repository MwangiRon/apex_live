export enum FlagType {
  GREEN = 'green',
  YELLOW = 'yellow',
  DOUBLE_YELLOW = 'double_yellow',
  RED = 'red',
  BLUE = 'blue',
  BLACK = 'black',
  CHEQUERED = 'chequered',
}

export enum TrackSector {
  SECTOR_1 = 'sector_1',
  SECTOR_2 = 'sector_2',
  SECTOR_3 = 'sector_3',
}

export interface FlagState {
  flag_type: FlagType;
  full_course: boolean;
  affected_sectors: TrackSector[];
  timestamp: string;
  message?: string;
}

export interface SessionState {
  session_id: string;
  session_type: string;
  active_cars: string[];
  current_flag: FlagState;
  lap_count: number;
  session_time_remaining?: number;
}

export interface WebSocketMessage {
  type: 'connection' | 'telemetry' | 'flag_change' | 'session_update';
  data: any;
  timestamp?: string;
}