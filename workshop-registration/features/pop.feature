Feature: Get registrants contact info

    Scenario: Contacting Students.  For a given workshop, list name and email of all approved registrants

    Scenario: General Info.  For a given workshop, list name and email of all registrants by registration status

    Scenario: Contact Database. List name and email of all registrants of all past workshops regardless of their registration status

Feature: Approve or reject registrants

    Scenario: (SSM) For a given workshop and registration status, list all registrants with details (name, email, research group, date of registration, questions with answers)

    Scenario: For a given workshop, if a registrant's email was approved for a past workshop with the same title mark the registration with the coresponding past workshop id(s)

    Scenario: (SSM) For a given workshop, change the status of a waitlisted registrant to approved or rejected

    Scenario: For a given workshop, change an accepted registrant to cancelled.

Feature: List all upcoming workshops

    Scenario: Do not list past workshops

    Scenario: (SM) Provide the right registration summary (registration link, number of approved and waiting registrants, number of free spots) of workshops

    Scenario Outline: (M) List workshops created by any member in the team

    Scenario Outline: List single workshop main details (registration link, title, date)

    Scenario: (SM) List multiple workshops' main details (registration link, title, date)

    Scenario: (M) Do not list non-workshop meetings

    Scenario: Do not list non-host meetings