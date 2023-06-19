class Elevators:
    def __init__(self, floor, number):
        self.floor = floor
        self.number = number

    def stats(self):
        print(f'{self.number} lift is on {self.floor} floor')


first = Elevators(1, "1")
second = Elevators(3, "2")
third = Elevators(8, "3")


def button(where, lifts):
    minimal = [10, None]
    for lift in lifts:
        # print(f'|{where} - {lift.floor}| < {minimal[0]}')
        if abs(where - lift.floor) < minimal[0]:
            minimal[0], minimal[1] = abs(where - lift.floor), lift
    print(f"Lift number {minimal[1].number} is the nearest, so it goes to {where} floor")
    minimal[1].floor = where
    if not check_first_floor(lifts):
        button(1, [i for i in lifts if i != minimal[1]])


def check_first_floor(lifts):
    on_first = 0
    for lift in lifts:
        if lift.floor == 1:
            on_first += 1
    if not on_first:
        print('First floor is empty!')
        return False
    else:
        return True


# Test
for lift in [first, second, third]:
    lift.stats()
print()

button(2, [first, second, third])  # Calling lift from 2 floor

print()
for lift in [first, second, third]:
    lift.stats()
