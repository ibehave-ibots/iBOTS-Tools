Feature: Play a "Ding" on Every change to the Score


Scenario Outline: teams made less than set number of commits for a ding 
    Given we've already detected <prev-commits> from <team>
    And the interval setting for <team> is set to <interval>
    And now <team> has <now-commits> total commits
    When the scores are calculated
    Then there is <ding> a <team> ding sound

    Examples:
        |  team    | prev-commits | now-commits |  ding  |  interval |
        |  team-1  | 0            | 0           |  not   |  3        |
        |  team-1  | 0            | 2           |  not   |  3        |
        |  team-1  | 2            | 3           |  yes   |  3        |
        |  team-1  | 3            | 5           |  not   |  3        |
        |  team-1  | 3            | 6           |  yes   |  3        |
        |  team-1  | 3            | 8           |  yes   |  3        |
        |  team-1  | 4            | 10          |  yes   |  3        |
        |  team-1  | 5            | 6           |  yes   |  3        |
        |  team-2  | 0            | 0           |  not   |  4        |
        |  team-2  | 0            | 2           |  not   |  4        |
        |  team-2  | 2            | 3           |  not   |  4        |
        |  team-2  | 3            | 5           |  yes   |  4        |
        |  team-2  | 3            | 6           |  yes   |  4        |
        |  team-2  | 3            | 8           |  yes   |  4        |
        |  team-2  | 4            | 10          |  yes   |  4        |
        |  team-2  | 5            | 6           |  no    |  4        |
