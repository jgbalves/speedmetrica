Feature: Calculate a lap time using a point-mass model
    Scenario: Calculating the radius of an entire track
        Given the following track file with presented channels
            |File Name|Speed Channel|Lateral Acceleration Channel|
            ||||
        When I provide the car information with file and car 
            | File Name | Plot Name |
            | car_1.csv | Car 1     |
        Then It plots the presented information
            | Plot Name | X Axis   | Y Axis |
            | Plot 1    | Distance | Speed  |

