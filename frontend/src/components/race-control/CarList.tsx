import { TelemetryData } from '../../types/telemetry.types';
import { Car } from '../../types/car.types';
import { Activity } from 'lucide-react';

interface CarListProps {
  cars: Map<string, Car>;
  latestTelemetry: Map<string, TelemetryData>;
}

export function CarList({ cars, latestTelemetry }: CarListProps) {
  const sortedCars = Array.from(cars.values()).sort((a, b) => a.car_number - b.car_number);

  return (
    <div className="glass rounded-lg p-4">
      <h3 className="font-telemetry text-sm text-nitrous tracking-wider mb-3">
        ACTIVE CARS
      </h3>

      <div className="space-y-2">
        {sortedCars.map((car, index) => {
          const telemetry = latestTelemetry.get(car.device_id);
          const isActive = telemetry !== undefined;

          return (
            <div
              key={car.device_id}
              className="bg-asphalt-light rounded-lg p-3 border-l-4 transition-all"
              style={{ 
                borderColor: car.team_colors.primary,
                animationDelay: `${index * 50}ms`
              }}
            >
              <div className="flex items-center gap-3">
                {/* Car Number */}
                <div 
                  className="w-10 h-10 rounded-lg flex items-center justify-center font-telemetry text-lg"
                  style={{ 
                    backgroundColor: car.team_colors.primary + '20',
                    color: car.team_colors.primary
                  }}
                >
                  {car.car_number}
                </div>

                {/* Driver Info */}
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-semibold text-white truncate">
                    {car.driver_name}
                  </div>
                  <div className="text-xs text-gray-500 truncate">
                    {car.team_colors.name}
                  </div>
                </div>

                {/* Status */}
                <div className="flex items-center gap-2">
                  {isActive ? (
                    <>
                      <Activity className="w-4 h-4 text-drs animate-pulse" />
                      <span className="data-mono text-xs text-drs">LIVE</span>
                    </>
                  ) : (
                    <span className="data-mono text-xs text-gray-600">OFFLINE</span>
                  )}
                </div>
              </div>

              {/* Telemetry Quick View */}
              {telemetry && (
                <div className="mt-2 pt-2 border-t border-gray-800 grid grid-cols-3 gap-2 data-mono text-xs">
                  <div>
                    <span className="text-gray-500">Speed:</span>
                    <span className="text-white ml-1">{telemetry.motion?.speed?.toFixed(0) || 'N/A'}</span>
                  </div>
                  <div>
                    <span className="text-gray-500">Pos:</span>
                    <span className="text-white ml-1">
                      {telemetry.position.normalized_x?.toFixed(0)},{telemetry.position.normalized_y?.toFixed(0)}
                    </span>
                  </div>
                  <div>
                    <span className="text-gray-500">Temp:</span>
                    <span className="text-white ml-1">
                      {telemetry.sensors?.temperature_engine?.toFixed(0) || 'N/A'}°C
                    </span>
                  </div>
                </div>
              )}
            </div>
          );
        })}

        {sortedCars.length === 0 && (
          <div className="text-center py-8 text-gray-500 text-sm">
            No cars registered in session
          </div>
        )}
      </div>
    </div>
  );
}