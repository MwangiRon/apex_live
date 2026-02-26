import type { TelemetryData } from '../../types/telemetry.types';
import { Activity, Thermometer, Gauge } from 'lucide-react';

interface SessionStatsProps {
  telemetryHistory: TelemetryData[];
  latestData: TelemetryData | null;
}

export function SessionStats({ telemetryHistory, latestData }: SessionStatsProps) {
  const speeds = telemetryHistory
    .map(t => t.motion?.speed)
    .filter((s): s is number => s !== undefined);

  const maxSpeed = speeds.length > 0 ? Math.max(...speeds) : 0;
  const avgSpeed = speeds.length > 0 ? speeds.reduce((a, b) => a + b, 0) / speeds.length : 0;

  const gForces = telemetryHistory
    .map(t => Math.sqrt(
      Math.pow(t.motion?.acceleration_x || 0, 2) +
      Math.pow(t.motion?.acceleration_y || 0, 2)
    ));

  const maxGForce = gForces.length > 0 ? Math.max(...gForces) : 0;

  return (
    <div className="grid grid-cols-1 gap-3">
      {/* Max Speed */}
      <div className="glass rounded-lg p-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-nitrous/10 flex items-center justify-center">
            <Gauge className="w-5 h-5 text-nitrous" />
          </div>
          <div className="flex-1">
            <div className="text-xs text-gray-500 mb-1">MAX SPEED</div>
            <div className="font-telemetry text-2xl text-white">
              {maxSpeed.toFixed(0)} <span className="text-sm text-gray-400">km/h</span>
            </div>
          </div>
        </div>
      </div>

      {/* Avg Speed */}
      <div className="glass rounded-lg p-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-drs/10 flex items-center justify-center">
            <Activity className="w-5 h-5 text-drs" />
          </div>
          <div className="flex-1">
            <div className="text-xs text-gray-500 mb-1">AVG SPEED</div>
            <div className="font-telemetry text-2xl text-white">
              {avgSpeed.toFixed(0)} <span className="text-sm text-gray-400">km/h</span>
            </div>
          </div>
        </div>
      </div>

      {/* Max G-Force */}
      <div className="glass rounded-lg p-4">
        <div className="flex items-center gap-3">
          <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
            maxGForce > 3 ? 'bg-championship/10' : 'bg-gray-700/10'
          }`}>
            <Activity className={`w-5 h-5 ${maxGForce > 3 ? 'text-championship' : 'text-gray-400'}`} />
          </div>
          <div className="flex-1">
            <div className="text-xs text-gray-500 mb-1">MAX G-FORCE</div>
            <div className="font-telemetry text-2xl text-white">
              {maxGForce.toFixed(2)} <span className="text-sm text-gray-400">g</span>
            </div>
          </div>
        </div>
      </div>

      {/* Engine Temp */}
      {latestData?.sensors?.temperature_engine && (
        <div className="glass rounded-lg p-4">
          <div className="flex items-center gap-3">
            <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
              latestData.sensors.temperature_engine > 100 ? 'bg-championship/10' : 'bg-gray-700/10'
            }`}>
              <Thermometer className={`w-5 h-5 ${
                latestData.sensors.temperature_engine > 100 ? 'text-championship' : 'text-gray-400'
              }`} />
            </div>
            <div className="flex-1">
              <div className="text-xs text-gray-500 mb-1">ENGINE TEMP</div>
              <div className="font-telemetry text-2xl text-white">
                {latestData.sensors.temperature_engine.toFixed(0)} <span className="text-sm text-gray-400">°C</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Data Points */}
      <div className="glass rounded-lg p-4">
        <div className="text-xs text-gray-500 mb-2">SESSION DATA</div>
        <div className="data-mono text-sm text-white">
          {telemetryHistory.length} <span className="text-gray-400">points logged</span>
        </div>
      </div>
    </div>
  );
}