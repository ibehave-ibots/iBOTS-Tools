Feature: Play a "Ding" on Every change to the Score


Scenario Outline: teams get a ding every interval
    Given the interval setting for <team> is set to <interval>
    And that <team> already had <old-points> points
    When the <team> gets <now-points> points
    Then the <team> ding sound should be <status>

    Examples:
        |  team    | old-points   | now-points  |  status  |  interval |
        |  team-1  | 0            | 0           |  off     |  3        |
        |  team-1  | 0            | 2           |  off     |  3        |
        |  team-1  | 2            | 3           |  on      |  3        |
        |  team-1  | 3            | 5           |  off     |  3        |
        |  team-1  | 3            | 6           |  on      |  3        |
        |  team-1  | 3            | 8           |  on      |  3        |
        |  team-1  | 4            | 10          |  on      |  3        |
        |  team-1  | 5            | 6           |  on      |  3        |
        |  team-2  | 0            | 0           |  off     |  4        |
        |  team-2  | 0            | 2           |  off     |  4        |
        |  team-2  | 2            | 3           |  off     |  4        |
        |  team-2  | 3            | 5           |  on      |  4        |
        |  team-2  | 3            | 6           |  on      |  4        |
        |  team-2  | 3            | 8           |  on      |  4        |
        |  team-2  | 4            | 10          |  on      |  4        |
        |  team-2  | 5            | 6           |  off     |  4        |
