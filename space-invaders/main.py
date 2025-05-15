import time
from turtle import Screen, Terminator
from player import Player
from alien_manager import AlienManager, alien_shape
from bullet_manager import BulletManager
from level_manager import LevelManager
import tkinter as tk
from tkinter import messagebox

def close_game():
    screen.bye()
    root.destroy()

def reset_game(player, alien_manager, bullet_manager, level_manager):
    # Reset player position
    player.goto(0, -250)
    # Reset aliens
    alien_manager.reset_aliens()
    # Reset bullets
    bullet_manager.clear_bullets()
    # Reset bullet speed to initial value for level 1
    bullet_manager.set_bullet_speed(level_manager.get_bullet_speed())
    # Reset level
    level_manager.reset_level()

root = tk.Tk()
root.withdraw()
screen = Screen()
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.title("Space Invaders")
screen.tracer(0)

# Register the custom shapes on the correct screen
screen.register_shape("alien", tuple(alien_shape))


# Initialize game objects
alien_manager = AlienManager()
bullet_manager = BulletManager()
level_manager = LevelManager()
alien_manager.create_aliens(level_manager.level)  # Pass initial level
player = Player()

screen.listen()
screen.onkeypress(player.start_going_left, "Left")
screen.onkeyrelease(player.stop_going_left, "Left")
screen.onkeypress(player.start_going_right, "Right")
screen.onkeyrelease(player.stop_going_right, "Right")

game_is_on = True
player_shoot_timer = time.time()
try:
    while game_is_on:
        alien_manager.move_aliens()
        alien_manager.shoot_bullet(bullet_manager)
        bullet_manager.move_bullets()
        player.move()

        # Automatic player shooting
        current_time = time.time()
        if current_time - player_shoot_timer >= 0.5:
            num_bullets = level_manager.get_num_bullets()
            player.shoot(bullet_manager, num_bullets)
            player_shoot_timer = current_time

        # Collision detection: Player bullets hitting aliens
        for bullet in bullet_manager.player_bullets[:]:
            for alien in alien_manager.all_aliens[:]:
                if bullet.distance(alien) < 20:
                    bullet_manager.remove_bullet(bullet, is_player_bullet=True)
                    alien_manager.remove_alien(alien)
                    break

        # Collision detection: Alien bullets hitting player
        player_hit = False
        for bullet in bullet_manager.alien_bullets[:]:
            if player.distance(bullet) < 20:
                bullet_manager.remove_bullet(bullet, is_player_bullet=False)
                # Show game over messagebox
                response = messagebox.askyesno("Game Over", "You were hit by an alien bullet!\nWould you like to start again?")
                if response:  # Yes: Start again
                    reset_game(player, alien_manager, bullet_manager, level_manager)
                else:  # No: Exit
                    game_is_on = False
                    close_game()
                    player_hit = True
                    break
        if player_hit:
            break  # Exit the while loop immediately to prevent screen.update()

        # Collision detection: Player bullets hitting alien bullets
        for player_bullet in bullet_manager.player_bullets[:]:
            for alien_bullet in bullet_manager.alien_bullets[:]:
                if player_bullet.distance(alien_bullet) < 15:  # Smaller distance for bullet-to-bullet collision
                    bullet_manager.remove_bullet(player_bullet, is_player_bullet=True)
                    bullet_manager.remove_bullet(alien_bullet, is_player_bullet=False)
                    break  # Stop checking this player bullet against other alien bullets

        # Check for level completion
        if game_is_on and not alien_manager.all_aliens:
            level_manager.next_level()
            alien_manager.create_aliens(level_manager.level)  # Pass current level
            bullet_manager.clear_bullets()
            bullet_manager.set_bullet_speed(level_manager.get_bullet_speed())

        if game_is_on:
            time.sleep(0.016)
            screen.update()

except Terminator:
    # Handle the case where the user closes the window manually
    game_is_on = False
    root.destroy()

screen.mainloop()
