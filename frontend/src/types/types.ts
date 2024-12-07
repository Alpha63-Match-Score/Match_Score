export interface Tournament {
  id: string
  title: string
  tournament_format: string
  start_date: string
  end_date: string
  current_stage: string
  number_of_teams: number
}

export interface Request {
  id: string;
  email: string;
  request_type: string;
  status: string;
  request_date: string;
  response_date: string | null;
  admin_id: string | null;
  username: string | null;
}

export interface Player {
  id: string;
  username: string;
  first_name: string;
  last_name: string;
  country: string;
  user_email: string;
  team_name: string;
  avatar: string | null;
  game_win_ratio: string;
  current_tournament_title: string | null;
}

export interface Team {
  id: string
  name: string
}

export interface FilterOption {
  text: string
  value: string
}

export interface FilterValues {
  period: string | null
  status: string | null
  format: string | null
}

