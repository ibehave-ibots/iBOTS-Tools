Feature: Simple Addition

    The calculator can do plus, minus, multiply, and divide.

    Scenario Outline: Addition of Integers
        Given I have the number <first>
        And I also have the number <second>
        When I use the addition operator on them
        Then I see the result is <result>

        Examples:
            | first | second | result |
            | 8 | 9 | 17 |
            | 2 | 5 | 7 |
            | -5 | 19 | 14 | 

    Scenario Outline: Subtraction of Integers
        Given I have the number <first>
        And I also have the number <second>
        When I use the subtraction operator on them
        Then I see the result is <result>

        Examples:
            | first | second | result |
            | 8 | 9 | -1 |
            | 2 | 5 | -3 |
            | -5 | 19 | -24 | 
        

        
