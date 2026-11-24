import random
import math
import time

def botanical_conflict_demo():
    print("This line directly conflicts with the PR branch!")
    return "FORCED_CONFLICT_FROM_AYUSH"

def play_music():
    print("music is playing")

class Banana:
    """Represents a banana entity that can be eaten by an apple."""
    def __init__(self, x=0, y=0, energy_value=25):
        self.x = x
        self.y = y
        self.energy_value = energy_value
        self.is_eaten = False

    def __repr__(self):
        return f"Banana(x={self.x}, y={self.y}, energy={self.energy_value}, eaten={self.is_eaten})"


class Apple:
    """Represents an apple entity that actively hunts and eats bananas."""
    def __init__(self, x=0, y=0, energy=100):
        self.x = x
        self.y = y
        self.energy = energy
        self.bananas_eaten_count = 0

    def move_towards(self, target_x, target_y, step=1.0):
        """Moves the apple towards a target coordinate by a given step size."""
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.hypot(dx, dy)
        if distance <= step:
            self.x = target_x
            self.y = target_y
        else:
            self.x += (dx / distance) * step
            self.y += (dy / distance) * step

    def eat(self, banana: Banana):
        """Consumes a banana, increasing energy and tracking count."""
        if not banana.is_eaten:
            banana.is_eaten = True
            self.energy += banana.energy_value
            self.bananas_eaten_count += 1
            return True
        return False

    def __repr__(self):
        return f"Apple(x={self.x:.1f}, y={self.y:.1f}, energy={self.energy}, eaten_count={self.bananas_eaten_count})"


class AppleBananaSimulation:
    """Simulation engine where an apple hunts and eats multiple bananas."""
    def __init__(self, width=20, height=10):
        self.width = width
        self.height = height
        self.apple = Apple(x=float(width // 2), y=float(height // 2), energy=100)
        self.bananas = [
            Banana(x=random.uniform(0, width), y=random.uniform(0, height), energy_value=random.randint(15, 40))
            for _ in range(5)
        ]

    def get_nearest_uneaten_banana(self):
        uneaten = [b for b in self.bananas if not b.is_eaten]
        if not uneaten:
            return None
        return min(uneaten, key=lambda b: math.hypot(b.x - self.apple.x, b.y - self.apple.y))

    def step(self):
        """Performs a single simulation step."""
        target = self.get_nearest_uneaten_banana()
        if not target:
            return False  # No more bananas

        # Move towards target banana
        self.apple.move_towards(target.x, target.y, step=1.5)

        # Check collision / eating distance
        distance = math.hypot(target.x - self.apple.x, target.y - self.apple.y)
        if distance < 0.5:
            self.apple.eat(target)

        return True

    def run(self, max_steps=50):
        """Runs the simulation until all bananas are eaten or max steps reached."""
        steps = 0
        while steps < max_steps:
            active = self.step()
            if not active:
                break
            steps += 1
        return self.apple.bananas_eaten_count
