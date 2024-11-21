from typing import Type
from uuid import UUID

from src.models import Tournament, Match, Team
from src.models.team import Team
from src.schemas.schemas import TeamListResponse, TeamCreate, UserResponse, TeamDetailedResponse, TeamUpdate
from src.utils import validators as v
from src.utils.pagination import PaginationParams

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST


def get_teams(
    db: Session, pagination: PaginationParams, search: str | None = None
) -> TeamListResponse:

    query = db.query(Team).order_by(Team.name.asc())

    filters = []

    if search:
        filters.append(Team.name.ilike(f"%{search}%"))

    if filters:
        query = db.query(Team).filter(*filters)

    query = query.offset(pagination.offset).limit(pagination.limit)

    db_teams = query.all()
    return [convert_db_to_team_list_response(db_team) for db_team in db_teams]


def create_team(
    db: Session, team: TeamCreate, current_user: UserResponse
) -> TeamListResponse:
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


def update_team(db: Session, team_id: UUID, team: TeamUpdate, current_user: UserResponse) -> TeamListResponse:
    db_team = v.team_exists(db, team_id=team_id)
    v.director_or_admin(current_user)

    db_team.name = team.name
    db_team.logo = team.logo

    db.commit()
    db.refresh(db_team)

    return convert_db_to_team_list_response(db_team)


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

def convert_db_to_team_list_response(db_team: Type[Team]) -> TeamListResponse:
    return TeamListResponse(
        id=db_team.id,
        name=db_team.name,
        logo=db_team.logo,
    )


def create_teams_lst_for_tournament(
    db: Session, team_names: list[str], tournament_id: UUID
) -> None:

    teams = []
    for name in team_names:
        db_team = db.query(Team).filter(Team.name == name).first()

        if db_team is None:
            new_team = Team(name=name)
            db.add(new_team)
            db.flush()
            teams.append(new_team)
        else:
            if db_team.tournament_id is not None:
                raise HTTPException(
                    status_code=HTTP_400_BAD_REQUEST,
                    detail=f"Team '{db_team.name}' already participates in another tournament",
                )

            teams.append(db_team)

    for db_team in teams:
        db_team.tournament_id = tournament_id


def leave_top_teams_from_robin_round(db, db_tournament: Tournament) -> None:
    team_stats = {}
    for team in db_tournament.teams:
        team_stats[team] = {
            "points": 0,
            "wins": 0,
            "score_difference": 0,
            "total_score": 0,
        }

    for match in db_tournament.matches:
        team1 = match.team1
        team2 = match.team2

        team_stats[team1]["total_score"] += match.team1_score
        team_stats[team2]["total_score"] += match.team2_score

        team_stats[team1]["score_difference"] += match.team1_score - match.team2_score
        team_stats[team2]["score_difference"] += match.team2_score - match.team1_score

        winner = team1 if match.winner_team_id == team1.id else team2
        team_stats[winner]["points"] += 2
        team_stats[winner]["wins"] += 1

    sorted_teams = sorted(
        team_stats.keys(),
        key=lambda t: (
            team_stats[t]["points"],
            team_stats[t]["wins"],
            team_stats[t]["score_difference"],
            team_stats[t]["total_score"],
        ),
        reverse=True,
    )

    for team in sorted_teams[2:]:
        team.tournament_id = None

    db.flush()
