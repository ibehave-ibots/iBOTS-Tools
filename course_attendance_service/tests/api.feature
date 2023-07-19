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

    Scenario: Get emails of all participants
        Given the uuid for a Zoom meeting where the participants Nick, Sangeetha, and Oliver were present
        When you ask for attendance details
        Then you get their email addresses

    Scenario: Get meeting date
        Given the ID for a Zoom meeting from '2023-07-03T07:30:00Z'
        When you ask for meeting details
        Then you get the date of meeting as '2023-07-03'

    Scenario: List Meeting IDs over a period of time
        Given the ID of the user with Zoom meeting on '2023-07-18' created by Sangeetha
        When you ask for meeting details
        Then you get [82619942883] as meeting ID

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
        When you ask for registrants contact details
        Then you get names as Test Name 1, Test Name 2, Test Name 3
        And emails as astrophysics12@gmail.com, sangeetha.nk94@gmail.com, an.sangeetha@gmail.com

    Scenario: User gets mark of whether each attendee was present for at least 80% of the sessions of a workshop
        Given the ID for a zoom meeting with Nick, Sangeetha, and Oliver as participants
        When you ask for attendance report
        Then you get a report with names
        And attendance of workshop

    Scenario: Users changing their display name doesn't affect attendance duration measuremen nor the number of participants
        Given the ID for a zoom meeting with where Nick <dg@gmail.com> was present for 10 minutes, then left, and NickDG <dg@gmail.com> was present for 20 minutes afterwards
        When you ask for the attendance report
        Then you see that someone named both Nick and NickDG <dg@gmail.com> was present for 30 minutes
        And the number of participants was 1

    Scenario:
        Given the ID for a zoom meeting where Nick <dg@gmail.com> and Nick's Phone <dg@gmail.com> was simultaneously present for 20 minutes
        When you ask for the attendance report
        Then you see that someone named both Nick and Nick's Phonse was present for 20 minutes

    Scenario: Get details of all registrants
        Given the ID for a zoom meeting with registrants Test Name 1, Test Name 2, Test Name 3, Test Name 4, Test Name 5
        When you ask for registrants details
        Then you get names as Test Name 1, Test Name 2, Test Name 3, Test Name 4, Test Name 5
        And emails as tn1@gmail.com, tn2@gmail.com, tn3@gmail.com, tn4@gmail.com, tn5@gmail.com
        And affiliations as A, B, A, C, D

    Scenario: User gets Excel file with attendances from each session of a workshop, including daily marks (yes or no) and course mark (yes or no)
