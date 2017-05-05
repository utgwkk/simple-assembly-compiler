class Operation:
    def __init__(self, op, ra, rb, d):
        self.op = op
        self.ra = ra
        self.rb = rb
        self.d = d

    def __int__(self):
        return (self.op << 14) + (self.ra << 11) + (self.rb << 8) + self.d

    def __str__(self):
        return 'Operation(op={0}, ra={1}, rb={2}, d={3})'.format(
            self.op, self.ra, self.rb, self.d
        )

class Label:
    def __init__(self, name, lineno):
        self.name = name
        self.lineno = lineno

    def __str__(self):
        return 'Label(name={0}, lineno={1})'.format(self.name, self.lineno)

class UnknownLabel(Label):
    def __init__(self, name):
        super(UnknownLabel, self).__init__(name, -1)

    def __str__(self):
        return 'UnknownLabel(name={0})'.format(self.name)
