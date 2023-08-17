Feature: Calculate Score based on Number of Relative Commits

Scenario: 
    Given the "team-1" branch is 3 commits ahead of the reference "main" branch
    When the scores are calculated for teams "team1"
    Then "team-1" is shown to have a score of 3

@skip
Scenario: Two teams make different numbers of commits
    Given a team has made 7 commits on the "team-1" branch
    And a team has made 5 commits on the "team-4" branch
    When the scores are calculated
    Then "team-1" is shown to have a score of 7
    And "team-4" is shown to have a score of 5


