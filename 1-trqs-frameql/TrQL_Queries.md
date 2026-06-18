# TrQL Queries Explained

## Dataset 2_6 — Cars on a straight road moving vertically

### Q1: Cars present for at least 100 frames
```
SELECT (a: type=car) WHERE duration(a.x1>0, 100)
```
Finds all cars that stay in the scene for 100+ frames. Filters out short-lived detections or flickering objects.

---

## Dataset 2_8 — Cars moving horizontally, some parked

### Q2: Stationary cars in top-left
```
SELECT (a: type=car) WHERE duration(a.x1<400 AND a.y1<300, 100)
```
Finds parked cars in the top-left region. x1<400 means left side, y1<300 means top. 100+ frames means they're stationary.

### Q3: Stationary cars on left AND right
```
SELECT (car:) WHERE duration(car.x1<400 OR car.x1>1300 AND car.y1<300, 100)
```
Same as Q2 but uses OR to also include parked cars on the right side (x1>1300). Covers both sides of the road.

---

## Dataset 2_9 — Cars in lanes, people walking

### Q4: Cars that took the left lane
```
SELECT (a: ) WHERE duration(a.x1<780, 10) THEN duration(a.x2>800, 10)
```
Finds cars that were first on the left (x1<780) and THEN moved to the right (x2>800). This detects lane-changing behavior — car going from left side to right side.

### Q5: Left lane — remove false positives
```
SELECT (a: ) WHERE duration(a.x1<780, 10) THEN duration(a.x2>800, 100)
```
Same as Q4 but increased duration to 100 frames. Cars just passing through get filtered out, only actual lane-changers remain.

### Q6: Pairs of cars close together
```
SELECT (c1:, c2:) WHERE duration(c1.y1>c2.y1-30 AND c1.y1<c2.y1+30, 20)
```
Finds two cars whose y-coordinates are within 30 pixels for 20+ frames. They're moving together at similar height in the frame.

### Q7: Close pairs — near camera only
```
SELECT (c1:, c2:) WHERE duration(c1.y1>c2.y1-30 AND c1.y1<c2.y1+30 AND c1.y1>400 AND c2.y1>400, 20)
```
Same as Q6 but added y1>400 to exclude far-away cars. Near the camera y-values are higher. So only finds close pairs that are actually near.

### Q8: People walking side by side
```
SELECT (a: type=person, b: type=person) WHERE duration(b.x1 < a.x1 + 120 AND b.x1 > a.x1, 120)
```
Finds two people whose x-coordinates are within 120 pixels for 120+ frames. They're walking together at similar horizontal position.

### Q9: People walking together through the middle of street
```
SELECT (a: type=person, b: type=person) WHERE
DURATION(a.y1<200 AND b.y1<200, 1)
THEN
DURATION(a.x1 > 700 AND a.x1 < 1300 AND b.x1>700 AND b.x1<1200 AND b.x1 < a.x1 + 120 AND b.x1 > a.x1, 500)
THEN
DURATION(a.y1>800 AND b.y1>800, 1)
```
Three stages: (1) Start at top of frame (y1<200), (2) Walk through middle of street (x between 700-1300) side by side for 500 frames, (3) Reach bottom of frame (y1>800). Finds people who walked together from top to bottom through the middle.
