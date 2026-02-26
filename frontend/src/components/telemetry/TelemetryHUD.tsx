import type { TelemetryData } from '../../types/telemetry.types';

interface TelemetryHUDProps {
  data: TelemetryData | null;
  isConnected: boolean;
}

export function TelemetryHUD({ data, isConnected }: TelemetryHUDProps) {
  if (!data) {
    return (
      <div className="glass rounded-lg p-4 border-l-4 border-championship">
        <div className="data-mono text-sm text-gray-400">
          NO TELEMETRY DATA
        </div>
      </div>
    );
  }

  return (
    <div className="glass rounded-lg p-4 border-l-4 border-nitrous">
      {/* Header */}
      <div className="flex items-center justify-between mb-3">
        <h3 className="font-telemetry text-xs text-nitrous tracking-wider">
          LIVE TELEMETRY
        </h3>
        <div className="flex items-center gap-2">
          <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-drs animate-pulse' : 'bg-championship'}`} />
          <span className="data-mono text-xs text-gray-400">
            {isConnected ? 'CONNECTED' : 'OFFLINE'}
          </span>
        </div>
      </div>

      {/* Raw Data Grid */}
      <div className="grid grid-cols-2 gap-3 data-mono text-xs">
        {/* Device ID */}
        <div className="col-span-2 pb-2 border-b border-gray-800">
          <div className="text-gray-500 mb-1">DEVICE_ID</div>
          <div className="text-nitrous font-semibold">{data.device_id}</div>
        </div>

        {/* Position */}
        <div>
          <div className="text-gray-500 mb-1">LAT</div>
          <div className="text-white">{data.position.latitude.toFixed(6)}</div>
        </div>
        <div>
          <div className="text-gray-500 mb-1">LON</div>
          <div className="text-white">{data.position.longitude.toFixed(6)}</div>
        </div>

        {/* Normalized Coordinates */}
        <div>
          <div className="text-gray-500 mb-1">NORM_X</div>
          <div className="text-drs font-semibold">
            {data.position.normalized_x?.toFixed(2) || 'N/A'}
          </div>
        </div>
        <div>
          <div className="text-gray-500 mb-1">NORM_Y</div>
          <div className="text-drs font-semibold">
            {data.position.normalized_y?.toFixed(2) || 'N/A'}
          </div>
        </div>

        {/* Motion Data */}
        {data.motion && (
          <>
            <div>
              <div className="text-gray-500 mb-1">SPEED</div>
              <div className="text-white font-semibold">
                {data.motion.speed?.toFixed(1) || 'N/A'} <span className="text-gray-500">km/h</span>
              </div>
            </div>
            <div>
              <div className="text-gray-500 mb-1">HEADING</div>
              <div className="text-white">
                {data.motion.heading?.toFixed(1) || 'N/A'}°
              </div>
            </div>

            {/* G-Forces */}
            <div>
              <div className="text-gray-500 mb-1">G_LAT</div>
              <div className={`font-semibold ${Math.abs(data.motion.acceleration_x || 0) > 2 ? 'text-championship' : 'text-white'}`}>
                {data.motion.acceleration_x?.toFixed(2) || 'N/A'}g
              </div>
            </div>
            <div>
              <div className="text-gray-500 mb-1">G_LONG</div>
              <div className={`font-semibold ${Math.abs(data.motion.acceleration_y || 0) > 2 ? 'text-championship' : 'text-white'}`}>
                {data.motion.acceleration_y?.toFixed(2) || 'N/A'}g
              </div>
            </div>
          </>
        )}

        {/* Sensors */}
        {data.sensors && (
          <>
            <div>
              <div className="text-gray-500 mb-1">ENG_TEMP</div>
              <div className={`font-semibold ${(data.sensors.temperature_engine || 0) > 100 ? 'text-championship' : 'text-white'}`}>
                {data.sensors.temperature_engine?.toFixed(1) || 'N/A'}°C
              </div>
            </div>
            <div>
              <div className="text-gray-500 mb-1">AMB_TEMP</div>
              <div className="text-white">
                {data.sensors.temperature_ambient?.toFixed(1) || 'N/A'}°C
              </div>
            </div>
          </>
        )}

        {/* Timestamp */}
        <div className="col-span-2 pt-2 border-t border-gray-800">
          <div className="text-gray-500 mb-1">TIMESTAMP</div>
          <div className="text-gray-400 text-[10px]">
            {new Date(data.timestamp).toLocaleTimeString('en-US', { 
              hour12: false,
              hour: '2-digit',
              minute: '2-digit',
              second: '2-digit',
              fractionalSecondDigits: 3
            })}
          </div>
        </div>
      </div>
    </div>
  );
}