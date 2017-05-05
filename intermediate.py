import utils


class Operation:
    def __init__(self, op, ra, rb, d):
        self.op = op
        self.ra = ra
        self.rb = rb
        self.d = d

    def __int__(self):
        if isinstance(self.d, int):
            return (self.op << 14) + (self.ra << 11) + (self.rb << 8) + self.d
        else:
            return (self.op << 14) + (self.ra << 11) + (self.rb << 8) + int(self.d)

    def __str__(self):
        return 'Operation(op={0:02b}, ra={1:03b}, rb={2:03b}, d={3:08b})'.format(
            self.op, self.ra, self.rb, self.d
        )

class RelativeLine:
    def __init__(self, distance):
        self.distance = distance

    def __str__(self):
        return 'RelativeLine(distance={0})'.format(self.distance)

    def __int__(self):
        return utils.sign_ext(self.distance)

class Label:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'Label(name={0})'.format(self.name)

    def __eq__(self, other):
        return str(self) == str(other)
