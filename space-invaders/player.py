import turtle
from turtle import Turtle

class Player(Turtle):
    def __init__(self):
        super().__init__()
        self._create_rocket_shape()
        self.shape("rocket")  # Use custom rocket shape
        self.color("white")
        self.shapesize(stretch_wid=1.0, stretch_len=1.5)  # Adjusted proportions
        self.speed('fastest')
        self.penup()
        self.goto(0, -250)
        self.setheading(90)  # Pointing upwards
        self.moving_left = False
        self.moving_right = False
        self.bullet_cooldown = 0  # Cooldown counter

    def _create_rocket_shape(self):
        """Create a more detailed rocket shape"""
        screen = turtle.Screen()
        rocket = turtle.Shape("compound")
        
        # Main rocket body (triangle)
        body = ((0, 15), (-8, -15), (8, -15))
        rocket.addcomponent(body, "white", "gray")
        
        # Cockpit window (diamond shape)
        window = ((-3, 5), (0, 8), (3, 5), (0, 2))
        rocket.addcomponent(window, "cyan", "blue")
        
        # Rocket flames
        flames = ((-5, -15), (0, -25), (5, -15))
        rocket.addcomponent(flames, "red", "orange")
        
        # Side fins
        left_fin = ((-8, -5), (-12, -15), (-8, -15))
        right_fin = ((8, -5), (12, -15), (8, -15))
        rocket.addcomponent(left_fin, "white", "gray")
        rocket.addcomponent(right_fin, "white", "gray")
        
        screen.register_shape("rocket", rocket)

    def move(self):
        """Move the player based on movement flags"""
        if self.moving_left and self.xcor() > -350:
            self.setx(self.xcor() - 10)  # Slightly slower movement
        if self.moving_right and self.xcor() < 350:
            self.setx(self.xcor() + 10)
        
        # Update cooldown
        if self.bullet_cooldown > 0:
            self.bullet_cooldown -= 1

    def start_going_left(self):
        self.moving_left = True

    def start_going_right(self):
        self.moving_right = True

    def stop_going_left(self):
        self.moving_left = False

    def stop_going_right(self):
        self.moving_right = False

    def shoot(self, bullet_manager, num_bullets=1):
        """Create bullets with cooldown management"""
        if self.bullet_cooldown > 0:
            return False
            
        x, y = self.position()
        if num_bullets == 1:
            bullet_manager.create_bullet(x, y + 20, is_player_bullet=True, angle=90)
        else:
            # Spread bullets with 8px spacing for better visual
            total_width = (num_bullets - 1) * 8
            start_x = x - total_width / 2
            for i in range(num_bullets):
                bullet_x = start_x + i * 8
                bullet_manager.create_bullet(bullet_x, y + 20, is_player_bullet=True, angle=90)
        
        # Set cooldown (10 frames)
        self.bullet_cooldown = 10
        return True