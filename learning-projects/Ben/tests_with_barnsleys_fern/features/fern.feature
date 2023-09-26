Feature: calculate the points of a Barnsley fern

    Scenario: give the first point of the fern 
        Given no points have been generated
        When the fern is created
        Then the first point is (0,0)


    Scenario: calculate the second point of the fern 
        Given only a first point exists
        When the next point is calculated
        Then the fern consists of two points

    Scenario: generate 10 points of the fern
        Given only a first point exists
        When 10 points of the fern are calculated
        Then the fern consists of 10 calculated points