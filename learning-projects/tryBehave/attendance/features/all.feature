Feature: Get Attendance

Scenario: Single-Session Attendance for Single-Attendance Events
    Given session ABCD, where Nick at dg@email.com arrived at 10h00 and left at 11h29
    When the teacher asks for the attendance report for session ABCD
    Then they see that dg@email.com attended for 89 minutes


Scenario: Single-Session Attendance for Single-Attendance Events
    Given session ABCD, where Nick at dg@email.com arrived at <10h00> and left at 11h29
    When the teacher asks for the attendance report for session ABCD
    Then they see that Nick attended for 89 minutes