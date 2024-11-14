from enum import Enum


class TournamentFormat(str, Enum):
   SINGLE_ELIMINATION = "single_elimination"
   ROUND_ROBIN = "round_robin"