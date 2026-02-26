import type { TrackInfo } from '../../types/telemetry.types';
import { MapPin, TrendingUp } from 'lucide-react';

interface TrackInfoCardProps {
  trackInfo: TrackInfo;
}

export function TrackInfoCard({ trackInfo }: TrackInfoCardProps) {
  return (
    <div className="glass rounded-lg p-4 border-l-4 border-drs">
      <div className="flex items-start justify-between mb-3">
        <div>
          <h2 className="font-telemetry text-lg text-white tracking-wide">
            {trackInfo.name}
          </h2>
          <div className="flex items-center gap-2 mt-1">
            <MapPin className="w-4 h-4 text-gray-400" />
            <span className="text-sm text-gray-400">{trackInfo.location}</span>
          </div>
        </div>
        <div className="text-right">
          <div className="text-2xl font-bold text-drs">{trackInfo.length_km}</div>
          <div className="text-xs text-gray-500">KILOMETERS</div>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-3 data-mono text-xs">
        <div>
          <div className="text-gray-500 mb-1">TURNS</div>
          <div className="text-white font-semibold">{trackInfo.turns}</div>
        </div>
        <div>
          <div className="text-gray-500 mb-1">LAYOUT</div>
          <div className="text-white">{trackInfo.dimensions.width_meters}m × {trackInfo.dimensions.height_meters}m</div>
        </div>
      </div>

      {/* Notable Corners */}
      {trackInfo.notable_corners && trackInfo.notable_corners.length > 0 && (
        <div className="mt-4 pt-3 border-t border-gray-800">
          <div className="text-gray-500 text-xs mb-2 flex items-center gap-2">
            <TrendingUp className="w-3 h-3" />
            NOTABLE CORNERS
          </div>
          <div className="space-y-1">
            {trackInfo.notable_corners.map((corner, idx) => (
              <div key={idx} className="text-xs text-gray-400 flex items-center gap-2">
                <span className="text-nitrous font-semibold">T{corner.turn}</span>
                <span>{corner.name}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}