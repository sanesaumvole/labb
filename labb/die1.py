from random import randint

class Die:
    """A class representing a single die."""
    
    def __init__(self, num_sides=6):
        """Assume a six-sided die."""
        self.num_sides = num_sides
        
    def roll(self):
        """"Return a random value between 1 and number of sides."""
        return randint(1, self.num_sides)

class AsymmetricDie(Die):
    """A class representing an asymmetric die."""
    
    def __init__(self, num_sides=6):
        super().__init__(num_sides)
        
    def roll(self):
        """Return a random value between 1 and number of sides, with probability proportional to its face value."""
        return randint(1, self.num_sides)

die_1 = Die(8)  # N = n + 3, n = 5
die_2 = AsymmetricDie(8)  

results = []
for roll_num in range(1000):
    result = die_1.roll() + die_2.roll()
    results.append(result)
