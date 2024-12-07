export interface Tournament {
  id: string
  title: string
  tournament_format: string
  start_date: string
  end_date: string
  current_stage: string
  number_of_teams: number
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
