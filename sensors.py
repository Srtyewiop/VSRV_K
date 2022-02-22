import datetime


def clamp(num, min_value, max_value):
    return max(min(num, max_value), min_value)


class Aquarium:
    first_time = datetime.timedelta(hours=0)
    second_time = datetime.timedelta(hours=0)
    third_time = datetime.timedelta(hours=0)
    isError = False

    def set_index(self, x):
        self._index = x

    def get_index(self):
        return self._index

    def set_state(self, x):
        self._open = x

    def get_state(self):
        return self._open

    def get_mass(self):
        return self._tank_food_mass

    def set_mass(self, x):
        if x < 0.00000001:
            self._tank_food_mass = 0.0
            print(f"tank {self.get_index()} is empty!")
        else:
            self._tank_food_mass = x

    def check_state_and_decrease_mass(self, mass, delta):
        if self.isError:
            return False
        if self.get_state():
            self.set_mass(self.get_mass()-((mass/15)*delta))
            return True
        else:
            return False

    def check_time(self, time):
        if self.isError:
            print('aquarium ', self.get_index(), ' is in error state! ', time)
            return
        deltatime1 = self.first_time + datetime.timedelta(seconds=5)
        deltatime2 = self.second_time + datetime.timedelta(seconds=5)
        deltatime3 = self.third_time + datetime.timedelta(seconds=5)
        if (self.first_time == time or self.second_time == time or self.third_time == time) and not(self.get_state()):
            self.set_state(True)
            print('tank ', self.get_index(), ' opened at ', time, ' mass: ', self.get_mass())
        if (deltatime1 == time or deltatime2 == time or deltatime3 == time) and (self.get_state()):
            self.set_state(False)
            print('tank ', self.get_index(), ' closed at ', time, ' mass: ', self.get_mass())

    def check_errors(self):
        if self.first_time == self.second_time or self.first_time == self.third_time:
            self.isError = True
        if self.second_time == self.third_time:
            self.isError = True
