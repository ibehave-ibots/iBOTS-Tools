Feature: (9) List all upcoming workshops

    @skip
    Scenario: (1) Do not list past workshops

    @skip
    Scenario: (2) Provide the right registration summary (registration link, number of approved and waiting registrants, number of free spots) of upcoming workshops
    
    Scenario Outline: (1) List workshops created by any member in the team
        Given Mohammad has an workshop <Mohammad> and Sangeetha has an workshop <Sangeetha>
        When the user checks upcoming workshops
        Then they see a list containing workshops <Mohammad> and <Sangeetha>

        Examples:
            | Mohammad | Sangeetha |
            | A  | B |
            | C  | D |
            | A,B | D |

    Scenario Outline: (1) List all workshops main details (registration link, title, date)
        Given one workshop with registration link "<link>", title "<title>", and date "<date>"
        When the user checks upcoming workshops
        Then they see workshops' details ("<link>", "<title>", "<date>")

        Examples:
            | link | title | date |
            | https://workshop-register.com/upcoming1 | Introduction to Python | 2023-09-15 |
            | https://workshop-register.com/upcoming2 | Intro to Rust | 2025-10-01 |


    Scenario: List all workshops' main details (registration link, title, date)
        Given the following workshops exist:
            | link                                   | title              | date       |
            | https://workshop-register.com/upcoming1 | Introduction to Python | 2023-09-15 |
            | https://workshop-register.com/upcoming2 | Intro to Rust       | 2025-10-01 |
        When the user checks upcoming workshops
        Then they see the following workshops' details:
            | link                                   | title              | date       |
            | https://workshop-register.com/upcoming1 | Introduction to Python | 2023-09-15 |
            | https://workshop-register.com/upcoming2 | Intro to Rust       | 2025-10-01 |


    @skip
    Scenario: () List only upcoming workshops, not past ones.


    @skip
    Scenario: (2) Do not list non-workshop meetings

    @skip
    Scenario: (2) Do not list non-host meetings