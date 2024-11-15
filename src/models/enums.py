from enum import Enum


class TournamentFormat(str, Enum):
   SINGLE_ELIMINATION = "single elimination"
   ROUND_ROBIN = "round robin"


class MatchFormat(str, Enum):
   MR15 = "MR15"
   MR12 = "MR12"


class Stage(str, Enum):
   GROUP_STAGE = "group stage"  # For Round Robin - MR12
   ROUND_OF_16 = "round of 16"  # For Single Elimination - MR15
   QUARTER_FINAL = "quarter final"  # For Single Elimination - MR15
   SEMI_FINAL = "semi final"  # For Single Elimination - MR15
   FINAL = "final"  # For both - MR15


class Role(str, Enum):
   ADMIN = "admin"
   PLAYER = "player"
   DIRECTOR = "director"
   USER = "user"