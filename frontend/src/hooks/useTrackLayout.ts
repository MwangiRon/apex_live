import { useState, useEffect } from 'react';
import type { TrackLayout } from '../services/api-client';
import { api } from '../services/api-client';

export function useTrackLayout() {
  const [trackLayout, setTrackLayout] = useState<TrackLayout | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api.getTrackLayout()
      .then(setTrackLayout)
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  return { trackLayout, loading, error };
}