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
        Given the uuid from a Zoom meeting where Nick, Sangeetha, and Oliver were present, and they were present for 191, 182, and 156 minutes, respectively
        When you ask for attendance report
        Then we see that Nick, Sangeetha, and Oliver were present
        And they were present for 191, 182, and 156 minutes, respectively

    Scenario: User gets number of participants of a Zoom meeting from a recurring meeting
        Given the uuid from a Zoom meeting where there were 3 participants
        When you ask for attendance report
        Then you get that the number of participants is 3


    Scenario: User gets a mark of attendance for each session of a workshop, whether they were present at least 75% or not.
        Given the uuid for a Zoom meeting where the participants Nick, Sangeetha, and Oliver were present, and they were present for 191, 182, and 156 minutes, respectively
        When you ask for attendance report
        Then you get attendance mark for Nick, Sangeetha, and Oliver

    Scenario: Get meeting date
    Scenario: Get meeting title
    Scenario: Get meeting description
    Scenario: Get emails of all participants
    Scenario: Get name and email of all registrants

    Scenario: User gets mark of whether each attendee was present for at least 80% of the sessions of a workshop
    Scenario: <if student changes name mid-session, it doesn't affect their attendance or number of participants>
    Scenario: <if a student joins from two different devices, it doesn't increase their participation>
    Scenario: User gets Excel file with attendances from each session of a workshop, including daily marks (yes or no) and course mark (yes or no)
    Scenario: List Meeting IDs over a period of time
    Scenario: List all Session Meetings IDs of a Workshop Meeting ID
    Scenario: List planned start and end times of a meeting
