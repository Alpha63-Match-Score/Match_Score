from src.models.team import Team
from src.schemas.team import TeamListResponse


def get_teams():
    raise NotImplementedError

def convert_db_to_team_list_response(
        db_team: Team
) -> TeamListResponse:
    return TeamListResponse(
        id=db_team.id, name=db_team.name,
        logo=db_team.logo,
    )