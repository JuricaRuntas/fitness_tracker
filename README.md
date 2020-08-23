# Fitness Tracker

## Main Functionality -> It tracks your fitness progress

What is fitness progress?

* Improvement of fitness goals such as:
1. Being able to lift more weight (STRENGTH GAINS)
2. Losing body fat, getting leaner (MUSCLE DEFINITION)

How can one fitness individual track their fitness progress?
1. STRENGTH GAINS:
* Make notes of weight lifted after every workout (BIG LIFTS)
* BIG LIFTS -> bench, squat, deadlift, military press, barbell rows etc.
* Any kind of variation of big lifts is also considered as big lift e.g. front squats, sumo deadlift etc.
* Use charts and graphs to visualize their progress
* Track their workouts, track exercises they perform, how many reps and sets, weight etc. 
* By tracking their workouts, they can see what made them stronger over time and what didn't have any significant impact

2. MUSCLE DEFINITION:
* Track weight loss, set goal weight
* Track calorie intake
* How much cardio does a person do in a week?
* Use charts and graphs to visualize weight progress, calorie intake

### Features (functionalities):
1. STRENGTH GAINS:
* Notes for amount of weight lifted for every big lift
* Workout tracker that tracks exercises, sets and reps, rest...
* 1 rep max calculator
* Graphs and charts for visualization
* Strength calculator that works based on your bodyweight and lifting standards

2. MUSCLE DEFINITION:
* Notes for tracking weight loss, ability to set goal weight
* Calorie tracker, nutrition/food API??
* Body fat calculator, example: https://www.calculator.net/body-fat-calculator.html
* Graphs and charts for visualization

### How to actually make this?
App consists of several different "pages"/layouts:
* "Homepage" or main page
* Weight lifting notes layout
* Workout tracker layout
* Layout for 1 rep max calculator
* Weight loss notes layout
* Calorie tracker layout
* Body fat calculator layout
* Layout for graphs and charts visualization

## Homepage
* Contains navigation to other layouts, e.g. buttons that will "render"/"switch" to selected layout when clicked
* Some other relevant info

## Weight lifting notes:
* User can pick from some list of exercises they want to track/make an entry
* For each exercise they can enter weight lifted at particular day/workout
* They can also enter number of reps performed with that weight

## Workout tracker
* CRUD type notes
* User needs to be able to store exercises
* For each exercise, user needs to be able to store how many sets and reps they performed, name of exercise, rest between sets, duration of exercise (cardio)
* Notes should look and work like some sort of calendar so user can store workout(s) for each day of the week
* User can also create "template workout program" that can repeat every week or so

## 1 rep max calculator
* User enters their heaviest lift and number of reps
* Calculator outputs their estimated 1 rep max, and recommended progression towards that max
* Progression -> format of progression should look something like:  | *set* | *percetange* | *weight* | *reps* | *rest* |
* e.g. | 3 | ~70% | 120 | 5 | ~ 3min |

## Weight loss notes
* User needs to be able to store their current weight and set their goal weight
* After every day user can enter their current weight

## Calorie tracker
* User can track their meals
* Possible food API that can be used for food database
* User can track their calories which are calculated

## Body fat calculator
* Implement something like https://www.calculator.net/body-fat-calculator.html
* BFP formulas on page above

## Graphs and charts visualization
* Graphs and charts will display progress and statistics
* Possible graphs:
1. Weight progression over time for each big lift
2. Estimated 1 rep max for each big lift over time
3. Weight loss/gain over time
4. If there are "template workout programs" we can do graph like graph #1 and show weight progression over time for each workout program on one graph (e.g. different colored lines, each line represents one workout program)
