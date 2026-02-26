import { Radio, Wifi, WifiOff } from 'lucide-react';

interface HeaderProps {
  isConnected: boolean;
  trackName?: string;
}

export function Header({ isConnected, trackName }: HeaderProps) {
  return (
    <header className="glass border-b border-gray-800 sticky top-0 z-50">
      <div className="max-w-[1920px] mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-nitrous to-drs flex items-center justify-center">
              <Radio className="w-6 h-6 text-asphalt" />
            </div>
            <div>
              <h1 className="font-telemetry text-xl text-white tracking-wider">
                FORMULA GRID
              </h1>
              <div className="text-xs text-gray-400 data-mono">
                LIVE TELEMETRY SYSTEM
              </div>
            </div>
          </div>

          {/* Track Info */}
          {trackName && (
            <div className="hidden md:block">
              <div className="text-xs text-gray-500 mb-1">ACTIVE CIRCUIT</div>
              <div className="font-semibold text-white">{trackName}</div>
            </div>
          )}

          {/* Connection Status */}
          <div className="flex items-center gap-3">
            <div className={`flex items-center gap-2 px-4 py-2 rounded-lg ${
              isConnected ? 'bg-drs/10' : 'bg-championship/10'
            }`}>
              {isConnected ? (
                <Wifi className="w-4 h-4 text-drs" />
              ) : (
                <WifiOff className="w-4 h-4 text-championship" />
              )}
              <span className={`data-mono text-xs font-semibold ${
                isConnected ? 'text-drs' : 'text-championship'
              }`}>
                {isConnected ? 'LIVE' : 'OFFLINE'}
              </span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}