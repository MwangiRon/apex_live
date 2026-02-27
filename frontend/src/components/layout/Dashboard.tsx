import { useState, useEffect } from 'react';
import { TrackCanvas } from '../track/TrackCanvas';
import { TelemetryHUD } from '../telemetry/TelemetryHUD';
import { TrackInfoCard } from '../track/TrackInfoCard';
import { SpeedGauge } from '../telemetry/SpeedGauge';
import { SessionStats } from '../telemetry/SessionStats';
import { FlagIndicator } from '../track/FlagIndicator';
import { CarList } from '../race-control/CarList';
import { useTelemetry } from '../../hooks/useTelemetry';
import { useTrackInfo } from '../../hooks/useTrackInfo';
import { Header } from './Header';
import type { Car } from '../../types/car.types';
import type { TelemetryData } from '../../types/telemetry.types';
import { useTrackLayout } from '../../hooks/useTrackLayout';

export function Dashboard() {
  const { telemetryHistory, latestData, isConnected, currentFlag, sessionState } = useTelemetry(200);
  const { trackInfo, loading: trackLoading } = useTrackInfo();
  const { trackLayout, loading: trackLayoutLoading } = useTrackLayout();
  const [registeredCars, setRegisteredCars] = useState<Map<string, Car>>(new Map());
  const [latestTelemetryByDevice, setLatestTelemetryByDevice] = useState<Map<string, TelemetryData>>(new Map());
  const [carColors, setCarColors] = useState<Map<string, { primary: string; secondary: string }>>(new Map());

  // Group telemetry by device and track latest per car
  useEffect(() => {
    const telemetryMap = new Map<string, TelemetryData>();
    
    telemetryHistory.forEach(data => {
      telemetryMap.set(data.device_id, data);
    });
    
    setLatestTelemetryByDevice(telemetryMap);
  }, [telemetryHistory]);

  // Extract car colors from registered cars
  useEffect(() => {
    const colorMap = new Map<string, { primary: string; secondary: string }>();
    
    registeredCars.forEach((car, deviceId) => {
      colorMap.set(deviceId, {
        primary: car.team_colors.primary,
        secondary: car.team_colors.secondary
      });
    });
    
    setCarColors(colorMap);
  }, [registeredCars]);

  // Auto-register cars when they send telemetry
  useEffect(() => {
    if (!sessionState) return;
    
    sessionState.active_cars.forEach(deviceId => {
      if (!registeredCars.has(deviceId)) {
        // Create placeholder car entry
        // In production, this should fetch from API
        const carNumber = registeredCars.size + 1;
        const placeholderCar: Car = {
          device_id: deviceId,
          car_number: carNumber,
          driver_name: `Driver ${carNumber}`,
          team: 'red_bull',
          team_colors: {
            primary: '#1E41FF',
            secondary: '#FFFFFF',
            name: 'Oracle Red Bull Racing'
          }
        };
        
        setRegisteredCars(prev => new Map(prev).set(deviceId, placeholderCar));
      }
    });
  }, [sessionState, registeredCars]);

 if (trackLoading || trackLayoutLoading) {
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
          {/* Left Sidebar - Track Info, Cars & Stats */}
          <div className="col-span-12 lg:col-span-3 space-y-4">
            {trackInfo && <TrackInfoCard trackInfo={trackInfo} />}
            
            {/* Flag Indicator */}
            {currentFlag && <FlagIndicator flagState={currentFlag} />}
            
            {/* Car List */}
            <CarList cars={registeredCars} latestTelemetry={latestTelemetryByDevice} />
            
            <SessionStats telemetryHistory={telemetryHistory} latestData={latestData} />
          </div>

          {/* Main Track View - 70% viewport dominance */}
          <div className="col-span-12 lg:col-span-6">
            <div className="glass rounded-lg p-6 h-[600px]">
              <div className="flex items-center justify-between mb-4">
                <h2 className="font-telemetry text-sm text-nitrous tracking-wider">
                  TRACK MAP
                </h2>
                <div className="flex items-center gap-4">
                  <div className="data-mono text-xs text-gray-400">
                    {registeredCars.size} CARS
                  </div>
                  <div className="data-mono text-xs text-gray-400">
                    {telemetryHistory.length} DATA POINTS
                  </div>
                </div>
              </div>
              <TrackCanvas 
  telemetryData={telemetryHistory} 
  latestData={latestData}
  currentFlag={currentFlag}
  carColors={carColors}
  trackLayout={trackLayout}
/>
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