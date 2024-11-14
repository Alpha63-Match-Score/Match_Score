from enum import Enum


class TournamentFormat(str, Enum):
   SINGLE_ELIMINATION = "single elimination"
   ROUND_ROBIN = "round robin"

class MatchFormat(str, Enum):
   MR15 = "MR15"
   MR12 = "MR12"

class Stage(str, Enum):
   GROUP_STAGE = "group stage"  # For Round Robin
   ROUND_OF_16 = "round of 16"  # For Single Elimination
   QUARTER_FINAL = "quarter final"  # For Single Elimination
   SEMI_FINAL = "semi final"  # For Single Elimination
   FINAL = "final"  # For both

