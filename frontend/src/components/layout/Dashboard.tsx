import { TrackCanvas } from '../track/TrackCanvas';
import { TelemetryHUD } from '../telemetry/TelemetryHUD';
import { TrackInfoCard } from '../track/TrackInfoCard';
import { SpeedGauge } from '../telemetry/SpeedGauge';
import { SessionStats } from '../telemetry/SessionStats';
import { useTelemetry } from '../../hooks/useTelemetry';
import { useTrackInfo } from '../../hooks/useTrackInfo';
import { Header } from './Header';

export function Dashboard() {
  const { telemetryHistory, latestData, isConnected } = useTelemetry(200);
  const { trackInfo, loading: trackLoading } = useTrackInfo();

  if (trackLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-nitrous border-t-transparent rounded-full animate-spin mx-auto mb-4" />
          <div className="data-mono text-gray-400">INITIALIZING SYSTEMS...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-asphalt">
      <Header isConnected={isConnected} trackName={trackInfo?.name} />

      {/* Brutalist Asymmetric Grid */}
      <div className="max-w-[1920px] mx-auto p-6">
        <div className="grid grid-cols-12 gap-4">
          {/* Left Sidebar - Track Info & Stats */}
          <div className="col-span-12 lg:col-span-3 space-y-4">
            {trackInfo && <TrackInfoCard trackInfo={trackInfo} />}
            <SessionStats telemetryHistory={telemetryHistory} latestData={latestData} />
          </div>

          {/* Main Track View - 70% viewport dominance */}
          <div className="col-span-12 lg:col-span-6">
            <div className="glass rounded-lg p-6 h-[600px]">
              <div className="flex items-center justify-between mb-4">
                <h2 className="font-telemetry text-sm text-nitrous tracking-wider">
                  TRACK MAP
                </h2>
                <div className="data-mono text-xs text-gray-400">
                  {telemetryHistory.length} DATA POINTS
                </div>
              </div>
              <TrackCanvas telemetryData={telemetryHistory} latestData={latestData} />
            </div>
          </div>

          {/* Right Sidebar - Live Data */}
          <div className="col-span-12 lg:col-span-3 space-y-4">
            {latestData?.motion?.speed !== undefined && (
              <SpeedGauge speed={latestData.motion.speed} />
            )}
            <TelemetryHUD data={latestData} isConnected={isConnected} />
          </div>
        </div>
      </div>
    </div>
  );
}