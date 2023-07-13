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


    Scenario: User gets mark of whether each attendee was present for at least 80% of the sessions of a workshop
        Given the uuid for a Zoom meeting where the participants Nick, Sangeetha, and Oliver were present, and they were present for 191, 182, and 156 minutes, respectively
        When you ask for attendance report
        Then you get attendance mark for Nick, Sangeetha, and Oliver

    Scenario: Get emails of all participants
        Given the uuid for a Zoom meeting where the participants Nick, Sangeetha, and Oliver were present
        When you ask for participant contact details
        Then you get names as Nick, Sangeetha, and Oliver
        And their email addresses

    Scenario: Get meeting date
        Given the ID for a Zoom meeting from '2023-07-03T07:30:00Z'
        When you ask for meeting details
        Then you get the date of meeting as '2023-07-03'

    Scenario: Get meeting title
        Given the ID for a Zoom meeting for Mouseflow refactoring
        When you ask for meeting details
        Then you get the title of the meeting

    Scenario: Get meeting description
        Given the ID for a Zoom meeting for Mouseflow refactoring
        When you ask for meeting details
        Then you get the agenda of the meeting

    Scenario: List planned start and end times of a meeting
        Given the ID for a Zoom meeting starting at '2023-07-03T07:30:00Z'
        And 150 minutes of planned duration
        When you ask for meeting details
        Then you get the start time as '7:30:00'
        And end time as '10:00:00'

    Scenario: List all Session Meetings IDs of a Workshop Meeting ID
        Given the ID for a past zoom meeting with 1 sessions
        When you ask for meeting details
        Then you get the uuid of the session

    Scenario: Get name and email of all registrants
        Given the ID for a zoom meeting with registrants Test Name 1, Test Name 2, Test Name 3
        When you ask for registrants details
        Then you get names as Test Name 1, Test Name 2, Test Name 3
        And emails as astrophysics12@gmail.com, sangeetha.nk94@gmail.com, an.sangeetha@gmail.com

    Scenario: User gets a mark of attendance for each session of a workshop, whether they were present at least 75% or not.
    Scenario: <if student changes name mid-session, it doesn't affect their attendance or number of participants>
    Scenario: <if a student joins from two different devices, it doesn't increase their participation>
    Scenario: List Meeting IDs over a period of time

    Scenario: User gets Excel file with attendances from each session of a workshop, including daily marks (yes or no) and course mark (yes or no)
