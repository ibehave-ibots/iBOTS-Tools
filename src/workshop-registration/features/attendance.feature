@attendance
Feature: Make Attandance Table
 
    Scenario: Two people attend 2 sessions
        Given participants attended workshop 1 with the following events:
            |  Name  | Email        | Session | Arrived | Departed |
            | Alice  |	a@alice.com | Day1    | 12:00   | 15:30    |
            | Alice  |	a@alice.com | Day2    | 12:00   | 19:30    |
            | Bob    |	b@bob.com   | Day1    | 12:00   | 17:30    |
            | Bob    |	b@bob.com   | Day2    | 12:00   | 20:30    |
        When the attendance table is built for workshop 1
        Then the user sees
            |  Name  | Email        | Day1 | Day2 |
            | Alice  |	a@alice.com | 3.5  | 7.5  | 
            | Bob    |	b@bob.com   | 5.5  | 8.5  |
    
    @skip
    Scenario: One person changes name during the sessions, email is the same
        Given participants attended workshop 1 with the following events:
            |  Name  | Email        | Session | Arrived | Departed |
            | Alice  |	a@alice.com | Day1    | 12:00   | 15:30    |
            | Alicia |	a@alice.com | Day1    | 15:30   | 19:30    |
        When the attendance table is built for workshop 1
        Then the user sees
            |  Name         | Email         | Day1 |
            | Alice, Alicia |	a@alice.com | 7.5  | 
    
    @skip
    Scenario: One person changes name between sessions, email is the same
        Given participants attended workshop 1 with the following events:
            |  Name  | Email        | Session | Arrived | Departed |
            | Alice  |	a@alice.com | Day1    | 12:00   | 15:30    |
            | Alicia |	a@alice.com | Day2    | 15:30   | 19:30    |
        When the attendance table is built for workshop 1
        Then the user sees
            |  Name         | Email         | Day1 | Day2 |
            | Alice, Alicia |	a@alice.com | 3.5  | 4    |

    @skip
    Scenario: Someone shows up to the first and third session, not the second.
        Given participants attended workshop 1 with the following events:
            |  Name  | Email        | Session | Arrived | Departed |
            | Alice  |	a@alice.com | Day1    | 12:00   | 15:30    |
            | Alice  |	a@alice.com | Day3    | 15:30   | 19:30    |
            | Bob    |	b@alice.com | Day1    | 12:00   | 15:30    |
            | Bob    |	b@alice.com | Day2    | 15:30   | 19:30    |
            | Bob    |	b@alice.com | Day3    | 15:30   | 19:30    |
        When the attendance table is built for workshop 1
        Then the user sees
            |  Name         | Email         | Day1 | Day2 | Day3 |
            | Alice         |	a@alice.com | 3.5  | 0    | 4    |
            | Bob           |	b@alice.com | 3.5  | 4    | 4    |