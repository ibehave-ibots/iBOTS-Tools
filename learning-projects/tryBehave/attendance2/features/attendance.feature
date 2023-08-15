Feature: Attendance reporting

    Scenario: list all attendees of a session
        Given a session id for a session where Nick and Sangeetha attended
        When the user asks for attendees for that session
        Then they see names of Nick and Sangeetha