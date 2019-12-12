# lift_simulation
Remember such a project when I was still in the university. The work I submitted wasn't great if I recall correctly. It would be fun to redo it now.

### Run the program with `python program.py`


```python
if __name__ == '__main__':
    planner = Planner(5, 1)
    while True:
        lvl_from = int(input())
        lvl_to = int(input())
        Person(lvl_from, lvl_to, planner)
```


To test the program, I instanced a planner with 5 levels (**_from level 0 to level 4_**) and 1 lift.
Below is the console output when I add a passenger who goes from level 1 to level 2.
```
PS D:\gh\lift_simulation> python .\program.py
1
2
New Passenger from 1 to 2
######
current direction: 1 ; current location: 0.1
######
current direction: 1 ; current location: 0.2
######
current direction: 1 ; current location: 0.30000000000000004
######
current direction: 1 ; current location: 0.4
######
current direction: 1 ; current location: 0.5
######
current direction: 1 ; current location: 0.6
######
current direction: 1 ; current location: 0.7
######
current direction: 1 ; current location: 0.7999999999999999
######
current direction: 1 ; current location: 0.8999999999999999
######
current direction: 1 ; current location: 1
before passengers going 1 get IN, passenger count: 0
after passengers going 1 get IN, passenger count: 1
######
current direction: 1 ; current location: 1.1
######
current direction: 1 ; current location: 1.2000000000000002
######
current direction: 1 ; current location: 1.3000000000000003
######
current direction: 1 ; current location: 1.4000000000000004
######
current direction: 1 ; current location: 1.5000000000000004
######
current direction: 1 ; current location: 1.6000000000000005
######
current direction: 1 ; current location: 1.7000000000000006
######
current direction: 1 ; current location: 1.8000000000000007
######
current direction: 1 ; current location: 1.9000000000000008
######
current direction: 1 ; current location: 2
at level 2
before passengers get OUT, passenger count: 1
after passengers get OUT, passenger count: 0
```

---

## Further development

- [ ] The Cart's `move()` function can be optimized, now there are lots of repeated code.
- [ ] Add more planner logic to handle the situation when there are more than 1 lift.
- [x] To end the program with any input other than a digit number. (End the threading.)
- [ ] Fix the bug in **4febbc0**.