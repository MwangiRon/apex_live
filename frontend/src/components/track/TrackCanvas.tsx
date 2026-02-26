import { useEffect, useRef, useState } from 'react';
import { TelemetryData } from '../../types/telemetry.types';
import { FlagState, FlagType, TrackSector } from '../../types/session.types';

interface TrackCanvasProps {
  telemetryData: TelemetryData[];
  latestData: TelemetryData | null;
  currentFlag: FlagState | null;
  carColors: Map<string, { primary: string; secondary: string }>;
}

export function TrackCanvas({ telemetryData, latestData, currentFlag, carColors }: TrackCanvasProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [flashState, setFlashState] = useState(false);

  // Flash animation for flags
  useEffect(() => {
    if (!currentFlag) return;

    let interval: NodeJS.Timeout;

    if (currentFlag.flag_type === FlagType.YELLOW || 
        currentFlag.flag_type === FlagType.DOUBLE_YELLOW ||
        currentFlag.flag_type === FlagType.RED) {
      
      interval = setInterval(() => {
        setFlashState(prev => !prev);
      }, 500); // Flash every 500ms
    } else if (currentFlag.flag_type === FlagType.GREEN) {
      // Green flag flash sequence (3 flashes then stop)
      let flashCount = 0;
      interval = setInterval(() => {
        setFlashState(prev => !prev);
        flashCount++;
        if (flashCount >= 6) {
          clearInterval(interval);
          setFlashState(false);
        }
      }, 300);
    }

    return () => {
      if (interval) clearInterval(interval);
      setFlashState(false);
    };
  }, [currentFlag?.flag_type, currentFlag?.timestamp]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const width = canvas.width;
    const height = canvas.height;

    // Clear canvas
    ctx.fillStyle = '#0D0D0D';
    ctx.fillRect(0, 0, width, height);

    // Draw grid
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
    ctx.lineWidth = 1;
    for (let i = 0; i <= 10; i++) {
      const x = (i / 10) * width;
      const y = (i / 10) * height;
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, height);
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(width, y);
      ctx.stroke();
    }

    // Draw sector boundaries
    drawSectorBoundaries(ctx, width, height);

    // Draw flag state overlays
    if (currentFlag && flashState) {
      drawFlagOverlay(ctx, width, height, currentFlag);
    }

    // Draw track boundary (ghost track)
    ctx.strokeStyle = 'rgba(0, 210, 255, 0.2)';
    ctx.lineWidth = 3;
    ctx.strokeRect(50, 50, width - 100, height - 100);

    // Group telemetry by device_id
    const telemetryByDevice = new Map<string, TelemetryData[]>();
    telemetryData.forEach(data => {
      if (!telemetryByDevice.has(data.device_id)) {
        telemetryByDevice.set(data.device_id, []);
      }
      telemetryByDevice.get(data.device_id)!.push(data);
    });

    // Draw each car's trail and position
    telemetryByDevice.forEach((deviceData, deviceId) => {
      const colors = carColors.get(deviceId) || { primary: '#00D2FF', secondary: '#00FF39' };
      drawCarTrail(ctx, deviceData, width, height, colors);
      
      // Draw current position for this car
      const currentPosition = deviceData[deviceData.length - 1];
      if (currentPosition?.position.normalized_x && currentPosition?.position.normalized_y) {
        drawCarMarker(ctx, currentPosition, width, height, colors);
      }
    });

  }, [telemetryData, latestData, currentFlag, flashState, carColors]);

  function drawSectorBoundaries(ctx: CanvasRenderingContext2D, width: number, height: number) {
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
    ctx.lineWidth = 2;
    ctx.setLineDash([5, 5]);

    // Sector 1 | Sector 2 boundary (x = 400)
    const sector1Boundary = (400 / 1000) * width;
    ctx.beginPath();
    ctx.moveTo(sector1Boundary, 0);
    ctx.lineTo(sector1Boundary, height);
    ctx.stroke();

    // Sector 2 | Sector 3 boundary (x = 700)
    const sector2Boundary = (700 / 1000) * width;
    ctx.beginPath();
    ctx.moveTo(sector2Boundary, 0);
    ctx.lineTo(sector2Boundary, height);
    ctx.stroke();

    ctx.setLineDash([]);

    // Sector labels
    ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
    ctx.font = 'bold 12px Inter';
    ctx.fillText('S1', 20, 30);
    ctx.fillText('S2', sector1Boundary + 20, 30);
    ctx.fillText('S3', sector2Boundary + 20, 30);
  }

  function drawFlagOverlay(
    ctx: CanvasRenderingContext2D, 
    width: number, 
    height: number, 
    flag: FlagState
  ) {
    let overlayColor: string;

    switch (flag.flag_type) {
      case FlagType.YELLOW:
      case FlagType.DOUBLE_YELLOW:
        overlayColor = 'rgba(234, 179, 8, 0.15)';
        break;
      case FlagType.RED:
        overlayColor = 'rgba(255, 30, 35, 0.2)';
        break;
      case FlagType.GREEN:
        overlayColor = 'rgba(0, 255, 57, 0.1)';
        break;
      default:
        return;
    }

    if (flag.full_course) {
      // Full course flash
      ctx.fillStyle = overlayColor;
      ctx.fillRect(0, 0, width, height);
    } else {
      // Sector-specific flash
      flag.affected_sectors.forEach(sector => {
        const bounds = getSectorBounds(sector, width, height);
        ctx.fillStyle = overlayColor;
        ctx.fillRect(bounds.x, bounds.y, bounds.width, bounds.height);
      });
    }
  }

  function getSectorBounds(sector: TrackSector, width: number, height: number) {
    switch (sector) {
      case TrackSector.SECTOR_1:
        return { x: 0, y: 0, width: (400 / 1000) * width, height };
      case TrackSector.SECTOR_2:
        return { x: (400 / 1000) * width, y: 0, width: (300 / 1000) * width, height };
      case TrackSector.SECTOR_3:
        return { x: (700 / 1000) * width, y: 0, width: (300 / 1000) * width, height };
      default:
        return { x: 0, y: 0, width, height };
    }
  }

  function drawCarTrail(
    ctx: CanvasRenderingContext2D, 
    deviceData: TelemetryData[], 
    width: number, 
    height: number,
    colors: { primary: string; secondary: string }
  ) {
    if (deviceData.length < 2) return;

    ctx.strokeStyle = colors.primary + '40'; // 25% opacity
    ctx.lineWidth = 2;
    ctx.beginPath();

    deviceData.forEach((data, index) => {
      if (!data.position.normalized_x || !data.position.normalized_y) return;
      
      const x = (data.position.normalized_x / 1000) * width;
      const y = (data.position.normalized_y / 1000) * height;

      if (index === 0) {
        ctx.moveTo(x, y);
      } else {
        ctx.lineTo(x, y);
      }
    });

    ctx.stroke();
  }

  function drawCarMarker(
    ctx: CanvasRenderingContext2D,
    data: TelemetryData,
    width: number,
    height: number,
    colors: { primary: string; secondary: string }
  ) {
    const x = (data.position.normalized_x! / 1000) * width;
    const y = (data.position.normalized_y! / 1000) * height;

    // Outer pulse (team primary color)
    ctx.fillStyle = colors.primary + '33'; // 20% opacity
    ctx.beginPath();
    ctx.arc(x, y, 20, 0, Math.PI * 2);
    ctx.fill();

    // Middle pulse
    ctx.fillStyle = colors.primary + '80'; // 50% opacity
    ctx.beginPath();
    ctx.arc(x, y, 12, 0, Math.PI * 2);
    ctx.fill();

    // Core (team secondary color)
    ctx.fillStyle = colors.secondary;
    ctx.beginPath();
    ctx.arc(x, y, 6, 0, Math.PI * 2);
    ctx.fill();

    // Direction indicator
    if (data.motion?.heading) {
      const heading = (data.motion.heading * Math.PI) / 180;
      const lineLength = 30;
      const endX = x + Math.cos(heading - Math.PI / 2) * lineLength;
      const endY = y + Math.sin(heading - Math.PI / 2) * lineLength;

      ctx.strokeStyle = colors.primary;
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.moveTo(x, y);
      ctx.lineTo(endX, endY);
      ctx.stroke();
    }
  }

  return (
    <canvas
      ref={canvasRef}
      width={800}
      height={600}
      className="w-full h-full gpu-accelerated"
      style={{ imageRendering: 'crisp-edges' }}
    />
  );
}