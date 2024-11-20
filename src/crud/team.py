from typing import Type
from uuid import UUID

from dns.e164 import query
from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from starlette.status import HTTP_400_BAD_REQUEST
from src.utils import validators as v
from src.models import Tournament, Match, Team
from src.models.team import Team
from src.schemas.schemas import TeamListResponse, TeamCreate, UserResponse, TeamDetailedResponse
from src.utils import validators as v
from src.utils.pagination import PaginationParams


def get_teams(db: Session,
              pagination: PaginationParams,
              search: str | None = None) -> TeamListResponse:

    query = db.query(Team).order_by(Team.name.asc())

    filters = []

    if search:
        filters.append(Team.name.ilike(f"%{search}%"))

    if filters:
        query = db.query(Team).filter(*filters)

    query = query.offset(pagination.offset).limit(pagination.limit)

    db_teams = query.all()
    return [convert_db_to_team_list_response(db_team) for db_team in db_teams]

def create_team( db: Session, team: TeamCreate, current_user: UserResponse)-> TeamListResponse:
    # v.team_exists(db, team_name=team.name)
    v.director_or_admin(current_user)

    db_team = Team(
        name=team.name,
        logo=team.logo,
 )

    db.add(db_team)
    db.commit()
    db.refresh(db_team)

    return convert_db_to_team_list_response(db_team)

def get_team(db: Session, team_id: UUID) -> TeamDetailedResponse:
    db_team = v.team_exists(db, team_id=team_id)

    stats = {
        "tournaments_played": set(),
        "tournaments_won": 0,
        "tournament_win_loss_ratio": {"ratio": 0.0, "won": 0, "played": 0},
        "matches_played": 0,
        "matches_won": 0,
        "match_win_loss_ratio": {"ratio": 0.0, "wins": 0, "losses": 0},
        "most_often_played_opponent": None,
        "best_opponent": None,
        "worst_opponent": None

    }

    matches = db.query(Match).filter(
        (Match.team1_id == team_id) | (Match.team2_id == team_id)
    ).all()

    opponent_stats = {}

    for match in matches:
        stats["matches_played"] += 1
        stats["tournaments_played"].add(match.tournament_id)

        if match.winner_team_id == team_id:
            stats["matches_won"] += 1

        opponent_id = match.team2_id if match.team1_id == team_id else match.team1_id
        opponent_name = match.team2.name if match.team1_id == team_id else match.team1.name

        if opponent_id not in opponent_stats:
            opponent_stats[opponent_id] = {"wins": 0,
                                           "losses": 0,
                                           "games": 0,
                                           "opponent_name": opponent_name}

        opponent_stats[opponent_id]["games"] += 1
        if match.winner_team_id == team_id:
            opponent_stats[opponent_id]["wins"] += 1
        else:
            opponent_stats[opponent_id]["losses"] += 1

    if matches:
        stats["tournaments_played"] = len(stats["tournaments_played"])
        stats["tournaments_won"] = sum(1 for match in matches if match.winner_team_id == team_id and match.stage == 'FINAL')

    if opponent_stats:
        stats["most_often_played_opponent"] = max(opponent_stats, key=lambda k: opponent_stats[k]["games"])
        stats["best_opponent"] = max(opponent_stats,
                                     key=lambda k: opponent_stats[k]["wins"] / opponent_stats[k]["games"])
        stats["worst_opponent"] = min(opponent_stats,
                                      key=lambda k: opponent_stats[k]["losses"] / opponent_stats[k]["games"])

    stats["match_win_loss_ratio"]["wins"] = stats["matches_won"]
    stats["match_win_loss_ratio"]["losses"] = stats["matches_played"] - stats["matches_won"]
    stats["match_win_loss_ratio"]["ratio"] = stats["matches_won"] / stats["matches_played"] if stats[
                                                                                                   "matches_played"] > 0 else 0.0

    stats["tournament_win_loss_ratio"]["won"] = stats["tournaments_won"]
    stats["tournament_win_loss_ratio"]["played"] = stats["tournaments_played"]
    stats["tournament_win_loss_ratio"]["ratio"] = stats["tournaments_won"] / stats["tournaments_played"] if stats[
                                                                                                                "tournaments_played"] > 0 else 0.0

    return convert_db_to_team_detailed_response(db_team, matches, stats)

def convert_db_to_team_detailed_response(
        db_team: Type[Team],
        matches: list[Type[Match]],
        stats: dict
) -> TeamDetailedResponse:
    return TeamDetailedResponse(
        id=db_team.id,
        name=db_team.name,
        logo=db_team.logo,
        players=db_team.players,
        matches=matches,
        tournament_id=db_team.tournament_id,
        prize_cuts=db_team.prize_cuts,
        team_stats=stats
    )

def convert_db_to_team_list_response(
        db_team: Type[Team]
) -> TeamListResponse:
    return TeamListResponse(
        id=db_team.id,
        name=db_team.name,
        logo=db_team.logo,
    )


def create_teams_lst_for_tournament(
        db: Session,
        team_names: list[str],
        tournament_id: UUID
) -> None:

    teams = []
    for name in team_names:
        v.team_exists(db, team_name=name)
        db_team = db.query(Team).filter(Team.name == name).first()

        if db_team.tournament_id is not None:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=f"Team '{db_team.name}' already participates in another tournament")

        if len(db_team.players) < 5:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Team must have at least 5 players")

        teams.append(db_team)

    for db_team in teams:
        db_team.tournament_id = tournament_id


def leave_top_teams_from_robin_round(
        db_tournament: Type[Tournament],
) -> None:

    team_stats = {}
    for match in db_tournament.matches:
            if match.winner_team_id not in team_stats:
                team_stats[match.winner_team] = 0
            team_stats[match.winner_team] += 1

    top_scores = sorted(team_stats.values(), reverse=True)[:2]

    best_teams = []
    for team, score in team_stats.items():
        if score in top_scores:
            best_teams.append(team)
        else:
            team.tournament_id = None