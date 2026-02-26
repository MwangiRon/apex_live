import { useEffect, useRef } from 'react';
import type { TelemetryData } from '../../types/telemetry.types';

interface TrackCanvasProps {
  telemetryData: TelemetryData[];
  latestData: TelemetryData | null;
}

export function TrackCanvas({ telemetryData, latestData }: TrackCanvasProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

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

    // Draw track boundary (ghost track)
    ctx.strokeStyle = 'rgba(0, 210, 255, 0.2)';
    ctx.lineWidth = 3;
    ctx.strokeRect(50, 50, width - 100, height - 100);

    // Draw telemetry trail
    if (telemetryData.length > 1) {
      ctx.strokeStyle = 'rgba(0, 210, 255, 0.4)';
      ctx.lineWidth = 2;
      ctx.beginPath();

      telemetryData.forEach((data, index) => {
        const x = ((data.position.normalized_x || 500) / 1000) * width;
        const y = ((data.position.normalized_y || 500) / 1000) * height;

        if (index === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
      });

      ctx.stroke();
    }

    // Draw car position (pulsing node)
    if (latestData?.position.normalized_x && latestData?.position.normalized_y) {
      const x = (latestData.position.normalized_x / 1000) * width;
      const y = (latestData.position.normalized_y / 1000) * height;

      // Outer pulse
      ctx.fillStyle = 'rgba(0, 255, 57, 0.2)';
      ctx.beginPath();
      ctx.arc(x, y, 20, 0, Math.PI * 2);
      ctx.fill();

      // Middle pulse
      ctx.fillStyle = 'rgba(0, 255, 57, 0.5)';
      ctx.beginPath();
      ctx.arc(x, y, 12, 0, Math.PI * 2);
      ctx.fill();

      // Core
      ctx.fillStyle = '#00FF39';
      ctx.beginPath();
      ctx.arc(x, y, 6, 0, Math.PI * 2);
      ctx.fill();

      // Direction indicator
      if (latestData.motion?.heading) {
        const heading = (latestData.motion.heading * Math.PI) / 180;
        const lineLength = 30;
        const endX = x + Math.cos(heading - Math.PI / 2) * lineLength;
        const endY = y + Math.sin(heading - Math.PI / 2) * lineLength;

        ctx.strokeStyle = '#00FF39';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.moveTo(x, y);
        ctx.lineTo(endX, endY);
        ctx.stroke();
      }
    }
  }, [telemetryData, latestData]);

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