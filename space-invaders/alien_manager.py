import turtle
import random
import time

# Define a more detailed alien shape
alien_shape = [
    (6.0, -10),    # Bottom left leg
    (3.0, -5),     # Left leg to body
    (0.0, -10),    # Left arm base
    (3.0, -15),    # Left arm tip
    (0.0, -10),    # Back to left arm base
    (-3.0, -5),    # Left side of body
    (-9.0, -5),    # Left side of head
    (-12.0, -8),   # Left antenna base
    (-15.0, -10),  # Left antenna tip
    (-12.0, -5),   # Back to head
    (-15.0, 0),    # Top of head
    (-12.0, 5),    # Right side of head
    (-12.0, 8),    # Right antenna base
    (-15.0, 10),   # Right antenna tip
    (-12.0, 5),    # Back to head
    (-9.0, 5),     # Right side of body
    (0.0, 10),     # Right arm base
    (3.0, 15),     # Right arm tip
    (0.0, 10),     # Back to right arm base
    (3.0, 5),      # Right leg to body
    (6.0, 10),     # Bottom right leg
    (3.0, 0),      # Bottom center of body
    (6.0, -10),    # Close the shape
]
# Do NOT register the shape here! It will be registered in main.py after screen is created.

COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]

class AlienManager(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.all_aliens = []
        self.direction = 1  # 1 for right, -1 for left
        self.speed = 2
        self.direction_changes = 0
        self.shoot_timer = time.time()

    def create_aliens(self, level):
        start_x = -350
        start_y = 200
        alien_width = 2
        alien_height = 1
        rows = 5
        columns = 7

        for row in range(rows):
            for column in range(columns):
                new_alien = turtle.Turtle("alien")  # Use custom alien shape
                color_index = (level - 1) % len(COLORS)
                new_alien.color(COLORS[color_index])
                new_alien.shapesize(stretch_wid=alien_height, stretch_len=alien_width)
                new_alien.penup()
                x_position = start_x + (column * (alien_width * 20 + 25))
                y_position = start_y - (row * (alien_height * 20 + 25))
                new_alien.goto(x_position, y_position)
                self.all_aliens.append(new_alien)

    def remove_alien(self, alien):
        if alien in self.all_aliens:
            alien.hideturtle()
            self.all_aliens.remove(alien)

    def reset_aliens(self):
        for alien in self.all_aliens:
            alien.hideturtle()
        self.all_aliens.clear()
        from level_manager import LevelManager
        level_manager = LevelManager()  # Temporary instance to get level
        self.create_aliens(level_manager.level)

    def move_aliens(self):
        for alien in self.all_aliens:
            x, y = alien.position()
            x += self.speed * self.direction
            alien.goto(x, y)

        # Check boundaries and change direction
        min_x = min(alien.xcor() for alien in self.all_aliens)
        max_x = max(alien.xcor() for alien in self.all_aliens)
        if min_x < -350 or max_x > 350:
            self.direction *= -1
            self.direction_changes += 1
            if self.direction_changes >= 6:
                for alien in self.all_aliens:
                    x, y = alien.position()
                    y -= 20
                    alien.goto(x, y)
                self.direction_changes = 0

    def shoot_bullet(self, bullet_manager):
        # Shoot every 1 second
        current_time = time.time()
        if current_time - self.shoot_timer >= 1 and self.all_aliens:
            shooter = random.choice(self.all_aliens)
            x, y = shooter.position()
            bullet_manager.create_bullet(x, y - 20)  # Bullet starts below alien
            self.shoot_timer = current_time