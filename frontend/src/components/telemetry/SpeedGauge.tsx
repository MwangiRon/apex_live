import { useEffect, useRef } from 'react';

interface SpeedGaugeProps {
  speed: number;
  maxSpeed?: number;
}

export function SpeedGauge({ speed, maxSpeed = 350 }: SpeedGaugeProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const radius = 80;

    // Clear
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Background arc
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
    ctx.lineWidth = 12;
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, 0.75 * Math.PI, 2.25 * Math.PI);
    ctx.stroke();

    // Speed arc
    const speedPercentage = Math.min(speed / maxSpeed, 1);
    const endAngle = 0.75 * Math.PI + speedPercentage * 1.5 * Math.PI;

    const gradient = ctx.createLinearGradient(0, 0, canvas.width, 0);
    gradient.addColorStop(0, '#00D2FF');
    gradient.addColorStop(0.5, '#00FF39');
    gradient.addColorStop(1, '#FF1E23');

    ctx.strokeStyle = gradient;
    ctx.lineWidth = 12;
    ctx.lineCap = 'round';
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, 0.75 * Math.PI, endAngle);
    ctx.stroke();

    // Speed text
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 36px "Archivo Black"';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(Math.round(speed).toString(), centerX, centerY);

    ctx.fillStyle = '#888888';
    ctx.font = '12px "Inter"';
    ctx.fillText('km/h', centerX, centerY + 25);
  }, [speed, maxSpeed]);

  return (
    <div className="glass rounded-lg p-4 flex flex-col items-center">
      <div className="text-xs text-gray-500 mb-2 font-telemetry tracking-wider">VELOCITY</div>
      <canvas ref={canvasRef} width={200} height={200} className="gpu-accelerated" />
    </div>
  );
}