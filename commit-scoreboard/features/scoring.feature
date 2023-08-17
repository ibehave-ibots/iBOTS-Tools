Feature: Calculate Score based on Number of Relative Commits

Background: Working from a certain branch
    Given the reference is the "main" branch

Scenario: A single Team makes 3 commits
    Given a team has made 3 commits on the "team-1" branch
    When the scores are calculated
    Then "team-1" is shown to have a score of 3

Scenario: Two teams make different numbers of commits
    Given a team has made 7 commits on the "team-1" branch
    And a team has made 5 commits on the "team-4" branch
    When the scores are calculated
    Then "team-1" is shown to have a score of 7
    And "team-4" is shown to have a score of 5


