Feature: Approve or reject registrants

    Scenario: For a given workshop, list all approved registrants with details (name, email, research group, date of registration)

        Given a workshop with the following registrants
            | name    | status       | email          | group       | date         |
            | alice   | approved     | a@alice.com    | Group A     | 2023-09-12   |
            | betty   | waitlisted   | b@betty.com    | Group B     | 2023-09-13   |
            | cathy   | approved     | c@cathy.com    | Group A     | 2023-09-14   |
            | denis   | rejected     | d@denis.com    | Group C     | 2023-09-15   |
            | eve     | waitlisted   | e@eve.com      | Group B     | 2023-09-16   |
            | ford    | approved     | f@ford.com     | Group A     | 2023-09-17   |
            | gemma   | rejected     | g@gemma.com    | Group C     | 2023-09-18   |
            | henry   | approved     | h@henry.com    | Group A     | 2023-09-19   |
        When the user checks for a list of approved registrants
        Then they see the following registrants summary
            | name    | email          | group       | date         |
            | alice   | a@alice.com    | Group A     | 2023-09-12   |
            | cathy   | c@cathy.com    | Group A     | 2023-09-14   |
            | ford    | f@ford.com     | Group A     | 2023-09-17   |
            | henry   | h@henry.com    | Group A     | 2023-09-19   |
