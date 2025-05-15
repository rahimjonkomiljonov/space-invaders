from turtle import Turtle


class LevelManager(Turtle):
    def __init__(self):
        super().__init__()
        self.level = 1
        self.base_bullet_speed = 5
        self.speed_increment = 0.5  # Speed increase per level
        self.color("white")
        self.penup()
        self.hideturtle()
        self.goto(-380, 260)
        self.update_level()

    def update_level(self):
        self.clear()
        self.write(f"Level: {self.level}", align="left", font=("Courier", 18, "normal"))

    def next_level(self):
        self.level += 1
        self.update_level()

    def get_bullet_speed(self):
        return self.base_bullet_speed + (self.level - 1) * self.speed_increment

    def get_num_bullets(self):
        return (self.level - 1) // 3 + 1  # +1 bullet every 3 levels

    def reset_level(self):
        self.level = 1
        self.clear()
        self.update_level()