import turtle



class BulletManager(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.player_bullets = []
        self.alien_bullets = []
        self.bullet_speed = 5

    def set_bullet_speed(self, speed):
        self.bullet_speed = speed

    def create_bullet(self, x, y, is_player_bullet=False, angle=90):
        bullet = turtle.Turtle("square")  # Revert to square shape
        bullet.color("green" if is_player_bullet else "red")
        bullet.shapesize(stretch_wid=0.2, stretch_len=0.5)
        bullet.penup()
        bullet.goto(x, y)
        bullet.setheading(angle)
        if is_player_bullet:
            self.player_bullets.append(bullet)
        else:
            self.alien_bullets.append(bullet)

    def move_bullets(self):
        # Move player bullets (straight up)
        for bullet in self.player_bullets[:]:
            x, y = bullet.position()
            y += self.bullet_speed
            bullet.goto(x, y)
            if y > 300:
                bullet.hideturtle()
                self.player_bullets.remove(bullet)

        # Move alien bullets (straight down)
        for bullet in self.alien_bullets[:]:
            x, y = bullet.position()
            y -= self.bullet_speed
            bullet.goto(x, y)
            if y < -300:
                bullet.hideturtle()
                self.alien_bullets.remove(bullet)

    def remove_bullet(self, bullet, is_player_bullet=False):
        bullet.hideturtle()
        if is_player_bullet and bullet in self.player_bullets:
            self.player_bullets.remove(bullet)
        elif not is_player_bullet and bullet in self.alien_bullets:
            self.alien_bullets.remove(bullet)

    def clear_bullets(self):
        for bullet in self.player_bullets + self.alien_bullets:
            bullet.hideturtle()
        self.player_bullets.clear()
        self.alien_bullets.clear()
