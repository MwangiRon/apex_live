import { useState, useEffect } from 'react';
import type { TrackInfo } from '../types/telemetry.types';
import { api } from '../services/api-client';

export function useTrackInfo() {
  const [trackInfo, setTrackInfo] = useState<TrackInfo | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api.getTrackInfo()
      .then(setTrackInfo)
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  return { trackInfo, loading, error };
}