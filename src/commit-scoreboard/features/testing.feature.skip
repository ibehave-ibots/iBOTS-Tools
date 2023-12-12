@skip
Feature: Check if a branch's script is working

Background: Working from a certain branch
    Given the reference is the "main" branch


Scenario: A team' project isn't working.
    Given the "coolkids" branch's code is failing to run
    When the scores are calculated
    But "coolkids" has a status of "broken"


Scenario: A team' project isn't working.
    Given the "coolkids" branch's code is running successfully
    When the scores are calculated
    But "coolkids" has a status of "working"