export interface TeamColor {
  primary: string;
  secondary: string;
  name: string;
}

export interface Car {
  device_id: string;
  car_number: number;
  driver_name: string;
  team: string;
  team_colors: TeamColor;
}

export const F1_TEAMS: Record<string, TeamColor> = {
  red_bull: { primary: '#1E41FF', secondary: '#FFFFFF', name: 'Oracle Red Bull Racing' },
  ferrari: { primary: '#FF2800', secondary: '#FFFFFF', name: 'Scuderia Ferrari HP' },
  mercedes: { primary: '#C0C0C0', secondary: '#00A19B', name: 'Mercedes-AMG PETRONAS F1 Team' },
  mclaren: { primary: '#FF8700', secondary: '#000000', name: 'McLaren Mastercard F1 Team' },
  aston_martin: { primary: '#006F62', secondary: '#FDE100', name: 'Aston Martin Aramco F1 Team' },
  alpine: { primary: '#0090FF', secondary: '#FF5F9E', name: 'BWT Alpine F1 Team' },
  williams: { primary: '#005AFF', secondary: '#FFFFFF', name: 'Atlassian Williams F1 Team' },
  racing_bulls: { primary: '#FFFFFF', secondary: '#2B6EB2', name: 'Visa Cash App Racing Bulls F1 Team' },
  audi: { primary: '#C0C0C0', secondary: '#D10000', name: 'Audi Revolut F1 Team' },
  haas: { primary: '#FFFFFF', secondary: '#E60000', name: 'TGR Haas F1 Team' },
  cadillac: { primary: '#000000', secondary: '#FFFFFF', name: 'Cadillac F1 Team' },
};