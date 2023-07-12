Feature: Give attendance of participants for a course on Zoom

    Scenario: User gets attendance from a Zoom meeting
        Given the ID from a Zoom meeting where Nick, Sangeetha, and Oliver were present, and they were present for 191, 182, and 156 minutes, respectively
        When you ask for attendance report
        Then we see that Nick, Sangeetha, and Oliver were present
        And they were present for 191, 182, and 156 minutes, respectively

    Scenario: User gets number of participants of a Zoom meeting
        Given the ID from a Zoom meeting where there were 3 participants
        When you ask for attendance report
        Then you get that the number of participants is 3

    Scenario: User gets attendance from a Zoom meeting from a recurring meeting
        Given the Zoom meeting ID "iJmk+imDQmugWQGtDIyRvg=="
        When you ask for attendance report
        Then you get the names of the participants
        And the durations for which they were present

    Scenario: User gets number of participants of a Zoom meeting from a recurring meeting
        Given the Zoom meeting ID "iJmk+imDQmugWQGtDIyRvg=="
        When you ask for attendance report
        Then you get that the number of participants is 3

