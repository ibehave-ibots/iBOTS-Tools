Feature: Calculate Score based on Number of Relative Commits

Scenario Outline: A team is ahead of a branch by different amounts: 
    Given the <team> branch is <commits> commits ahead of the reference <ref> branch
    When the scores are calculated for teams <team> against reference branch <ref>
    Then <team> is shown to have a score of <score>

    Examples:
        | team | ref | commits | score |
        | team-1 | main | 3 | 3 |
        | team-4 | dev | 6 | 6 |




