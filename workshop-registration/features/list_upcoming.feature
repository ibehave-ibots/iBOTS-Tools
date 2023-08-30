Feature: (9) List all upcoming workshops

    @skip
    Scenario: (1) Do not list past workshops

    @skip
    Scenario: (2) Provide the right registration summary (registration link, number of approved and waiting registrants, number of free spots) of upcoming workshops
    
    Scenario Outline: (1) List upcoming workshops created by any member in the team
        Given Mohammad has an upcoming workshop <Mohammad> and Sangeetha has an upcoming workshop <Sangeetha>
        When the user checks upcoming workshops
        Then they see a list containing workshops <Mohammad> and <Sangeetha>

        Examples:
            | Mohammad | Sangeetha |
            | A  | B |
            | C  | D |
            | A,B | D |

    @skip
    Scenario: (1) List all the upcoming workshops main details (registration link, title, date)

    @skip
    Scenario: (2) Do not list non-workshop meetings

    @skip
    Scenario: (2) Do not list non-host meetings