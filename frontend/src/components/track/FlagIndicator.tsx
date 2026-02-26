import type { FlagState } from '../../types/session.types';
import { FlagType } from '../../types/session.types';
import type { WebSocketMessage } from '../types/session.types';
import { AlertCircle, Flag, X, CheckCircle } from 'lucide-react';

interface FlagIndicatorProps {
  flagState: FlagState | null;
}

export function FlagIndicator({ flagState }: FlagIndicatorProps) {
  if (!flagState) return null;

  const getFlagConfig = (flagType: FlagType) => {
    switch (flagType) {
      case FlagType.GREEN:
        return {
          color: 'bg-drs',
          textColor: 'text-drs',
          icon: CheckCircle,
          label: 'GREEN FLAG',
          description: 'Racing',
        };
      case FlagType.YELLOW:
        return {
          color: 'bg-yellow-500',
          textColor: 'text-yellow-500',
          icon: AlertCircle,
          label: 'YELLOW FLAG',
          description: 'Caution',
        };
      case FlagType.DOUBLE_YELLOW:
        return {
          color: 'bg-yellow-500',
          textColor: 'text-yellow-500',
          icon: AlertCircle,
          label: 'DOUBLE YELLOW',
          description: 'No overtaking',
        };
      case FlagType.RED:
        return {
          color: 'bg-championship',
          textColor: 'text-championship',
          icon: X,
          label: 'RED FLAG',
          description: 'Session stopped',
        };
      case FlagType.BLUE:
        return {
          color: 'bg-blue-500',
          textColor: 'text-blue-500',
          icon: Flag,
          label: 'BLUE FLAG',
          description: 'Let faster car pass',
        };
      default:
        return {
          color: 'bg-gray-500',
          textColor: 'text-gray-500',
          icon: Flag,
          label: 'FLAG',
          description: '',
        };
    }
  };

  const config = getFlagConfig(flagState.flag_type);
  const Icon = config.icon;

  return (
    <div className={`glass rounded-lg p-4 border-l-4 border-${config.color.replace('bg-', '')}`}>
      <div className="flex items-start gap-3">
        <div className={`w-12 h-12 rounded-full ${config.color} bg-opacity-20 flex items-center justify-center flex-shrink-0`}>
          <Icon className={`w-6 h-6 ${config.textColor}`} />
        </div>
        
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-1">
            <h3 className={`font-telemetry text-sm ${config.textColor} tracking-wider`}>
              {config.label}
            </h3>
            {!flagState.full_course && (
              <span className="text-xs px-2 py-0.5 rounded bg-gray-800 text-gray-400">
                SECTOR SPECIFIC
              </span>
            )}
          </div>
          
          <p className="text-xs text-gray-400 mb-2">{config.description}</p>
          
          {!flagState.full_course && flagState.affected_sectors.length > 0 && (
            <div className="data-mono text-xs text-gray-500 mb-2">
              Sectors: {flagState.affected_sectors.map(s => s.toUpperCase()).join(', ')}
            </div>
          )}
          
          {flagState.message && (
            <div className="text-sm text-white bg-asphalt-light rounded px-3 py-2">
              {flagState.message}
            </div>
          )}
          
          <div className="data-mono text-[10px] text-gray-600 mt-2">
            {new Date(flagState.timestamp).toLocaleTimeString('en-US', {
              hour12: false,
              hour: '2-digit',
              minute: '2-digit',
              second: '2-digit',
            })}
          </div>
        </div>
      </div>
    </div>
  );
}