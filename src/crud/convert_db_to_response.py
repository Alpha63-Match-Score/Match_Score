from typing import Type

from src.models import Match, Player, PrizeCut, Team, Tournament
from src.schemas.schemas import (
    MatchDetailResponse,
    MatchListResponse,
    PlayerDetailResponse,
    PlayerListResponse,
    PrizeCutResponse,
    TeamDetailedResponse,
    TeamListResponse,
    TournamentDetailResponse,
    TournamentListResponse,
)


def convert_db_to_match_response(db_match: Match | Type[Match]) -> MatchDetailResponse:
    return MatchDetailResponse(
        id=db_match.id,
        match_format=db_match.match_format,
        start_time=db_match.start_time,
        is_finished=db_match.is_finished,
        stage=db_match.stage,
        team1_id=db_match.team1_id,
        team2_id=db_match.team2_id,
        team1_score=db_match.team1_score,
        team2_score=db_match.team2_score,
        winner_id=db_match.winner_team_id,
        tournament_id=db_match.tournament_id,
        team1_name=db_match.team1.name,
        team2_name=db_match.team2.name,
        team1_logo=db_match.team1.logo,
        team2_logo=db_match.team2.logo,
        tournament_title=db_match.tournament.title,
    )


def convert_db_to_match_list_response(
    db_match: Match | Type[Match],
) -> MatchListResponse:
    return MatchListResponse(
        id=db_match.id,
        match_format=db_match.match_format,
        start_time=db_match.start_time,
        is_finished=db_match.is_finished,
        stage=db_match.stage,
        team1_id=db_match.team1_id,
        team2_id=db_match.team2_id,
        team1_score=db_match.team1_score,
        team2_score=db_match.team2_score,
        winner_id=db_match.winner_team_id,
        tournament_id=db_match.tournament_id,
    )


def convert_db_to_player_list_response(db_player: Type[Player]) -> PlayerListResponse:
    team_name = db_player.team.name if db_player.team else None
    user_email = db_player.user.email if db_player.user else None
    return PlayerListResponse(
        id=db_player.id,
        username=db_player.username,
        first_name=db_player.first_name,
        last_name=db_player.last_name,
        country=db_player.country,
        avatar=db_player.avatar,
        user_email=user_email,
        team_name=team_name,
        game_win_ratio=f"{db_player.won_games / db_player.played_games * 100:.0f}%" if db_player.played_games > 0 else "0%"
    )


def convert_db_to_player_detail_response(
    db_player: Type[Player], tournament_title: str | None
) -> PlayerDetailResponse:
    team_name = db_player.team.name if db_player.team else None
    user_email = db_player.user.email if db_player.user else None
    return PlayerDetailResponse(
        id=db_player.id,
        username=db_player.username,
        first_name=db_player.first_name,
        last_name=db_player.last_name,
        country=db_player.country,
        avatar=db_player.avatar,
        user_email=user_email,
        team_name=team_name,
        game_win_ratio=f"{db_player.won_games / db_player.played_games * 100:.0f}%" if db_player.played_games > 0 else "0%",
        current_tournament_title=tournament_title,

    )


def convert_db_to_prize_cut_response(
    db_prize: PrizeCut | Type[PrizeCut],
) -> PrizeCutResponse:

    return PrizeCutResponse(
        id=db_prize.id,
        place=db_prize.place,
        prize_cut=db_prize.prize_cut,
        tournament_id=db_prize.tournament_id,
        tournament_name=db_prize.tournament.title,
        team_id=db_prize.team_id,
        team_name=db_prize.team.name if db_prize.team else None,
    )


def convert_db_to_team_detailed_response(
    db_team: Type[Team], matches: list[Type[Match]], stats: dict
) -> TeamDetailedResponse:
    return TeamDetailedResponse(
        id=db_team.id,
        name=db_team.name,
        logo=db_team.logo,
        players=db_team.players,
        matches=[convert_db_to_match_list_response(match) for match in matches],
        tournament_id=db_team.tournament_id,
        prize_cuts=[
            convert_db_to_prize_cut_response(prize_cut)
            for prize_cut in db_team.prize_cuts
        ],
        team_stats=stats,
    )


def convert_db_to_team_list_response(db_team: Type[Team]) -> TeamListResponse:
    return TeamListResponse(
        id=db_team.id,
        name=db_team.name,
        logo=db_team.logo,
        game_win_ratio=f"{db_team.won_games / db_team.played_games * 100:.0f}%" if db_team.played_games > 0 else "0%"
    )


def convert_db_to_tournament_list_response(
    db_tournament: Tournament | Type[Tournament],
) -> TournamentListResponse:

    return TournamentListResponse(
        id=db_tournament.id,
        title=db_tournament.title,
        tournament_format=db_tournament.tournament_format,
        start_date=db_tournament.start_date,
        end_date=db_tournament.end_date,
        current_stage=db_tournament.current_stage,
        number_of_teams=len(db_tournament.teams),
    )


def convert_db_to_tournament_response(
    db_tournament: Tournament | Type[Tournament],
) -> TournamentDetailResponse:

    return TournamentDetailResponse(
        id=db_tournament.id,
        title=db_tournament.title,
        tournament_format=db_tournament.tournament_format,
        start_date=db_tournament.start_date,
        end_date=db_tournament.end_date,
        current_stage=db_tournament.current_stage,
        number_of_teams=len(db_tournament.teams),
        matches_of_current_stage=[
            convert_db_to_match_list_response(db_match)
            for db_match in db_tournament.matches
            if db_match.stage == db_tournament.current_stage
        ],
        teams=[
            convert_db_to_team_list_response(db_team) for db_team in db_tournament.teams
        ],
        prizes=[
            convert_db_to_prize_cut_response(db_prize)
            for db_prize in db_tournament.prize_cuts
        ],
    )
