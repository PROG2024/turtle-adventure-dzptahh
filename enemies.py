"""
The enemies module is responsible for defining enemy classes with various
behaviours.  It also contains logic to make enemies show up in the game at
certain points in time.
"""
import abc
import random
from abc import ABC

from gamelib import GameElement
import turtle_adventure


class Enemy(GameElement):
    """
    Define an enemy for the Turtle's adventure game with specific behaviors
    """

    # * Implement __init__()
    # * Implement all methods required by the GameElement abstract class
    # * Define enemy's update logic in the update() method
    # * Check whether the player hits this enemy, then call the method
    #   game_over_lose() in TurtleAdventureGame

    def __init__(self, game: "turtle_adventure.TurtleAdventureGame", size: int, color: str):
        super().__init__(game)
        self.__game = game
        self.__size = size
        self.__color = color
        # self.__speed = speed
        self.x: int
        self.y: int
        self.cont_x, self.cont_y = self.set_range()

    def create(self) -> None:
        # self.__id = canvas.create_oval(0, 0, size, size, fill=color)
        self.__id = self.canvas.create_oval(100, 100, 100 + self.__size, 100 + self.__size, fill=self.__color)

    def update(self) -> None:
        x1, x2 = self.x - self.__size / 2, self.x + self.__size / 2
        y1, y2 = self.y - self.__size / 2, self.y + self.__size / 2
        if x1 <= self.__game.player.x <= x2 and y1 <= self.__game.player.y <= y2:
            self.__game.game_over_lose()
        self.x += self.cont_x
        self.y += self.cont_y
        if self.x > 800:
            self.cont_x = - self.cont_x
        if self.y > 500:
            self.cont_y = - self.cont_y
        if self.x < 0:
            self.cont_x = -self.cont_x
        if self.y < 0:
            self.cont_y = -self.cont_y

    def set_range(self):
        x2 = random.randint(-3, 3)
        y2 = random.randint(-3, 3)
        return x2, y2

    def render(self) -> None:
        self.canvas.coords(self.__id,
                           self.x - self.__size / 2,
                           self.y - self.__size / 2,
                           self.x + self.__size / 2,
                           self.y + self.__size / 2)

    def delete(self) -> None:
        self.canvas.delete(self.__id)


class EnemyGenerator:
    """
    An EnemyGenerator instance is responsible for creating enemies of various
    kinds and scheduling them to appear at certain points in time.
    """

    # insert code to generate enemies based on the given game level; call
    # TurtleAdventureGame's add_enemy() method to add one enemy into the game
    # at a time.
    #
    # Hint: the 'game' parameter is a tkinter's frame, so it's after()
    # method can be used to schedule some future events.

    def __init__(self, game: "turtle_adventure.TurtleAdventureGame", level: int):
        self.__game: "turtle_adventure.TurtleAdventureGame" = game
        self.__level: int = level

        # example
        self.__game.after(100, self.create_enemy)

    def create_enemy(self):
        color = ["#FCDFA6", "#5CA4A9", "#F4ACB7", "#4464AD"]
        size = [30, 45, 60]
        # normal
        for i in range(7):
            new_enemy = Enemy(self.__game, random.choice(size), random.choice(color))
            new_enemy.x = random.randint(1, 550)
            new_enemy.y = random.randint(1, 550)
            self.__game.add_enemy(new_enemy)
        # chasing
        for i in range(2):
            chase = ChasingEnemy(self.__game, 20, "#fef9ef")
            chase.x = random.randint(1, 550)
            chase.y = random.randint(1, 550)
            self.__game.add_enemy(chase)
        # fencing
        fence = FencingEnemy(self.__game, 20, "#cbf3f0")
        fence.x = self.__game.home.x + 30
        fence.y = self.__game.home.y + 30
        self.__game.add_enemy(fence)
        # door
        door = DoorEnemy(self.__game, 60, "#5c4742")
        door.x = 400
        door.y = 250
        self.__game.add_enemy(door)


class ChasingEnemy(Enemy):
    """Chasing the turtle"""

    def __init__(self, game: "turtle_adventure.TurtleAdventureGame", size: int, color: str):
        super().__init__(game, size, color)
        self.__game = game
        self.__size = size
        self.__color = color
        # self.__speed = speed
        self.x: int
        self.y: int

    def update(self) -> None:
        if self.x < self.__game.player.x:
            self.x += 2
        if self.y < self.__game.player.y:
            self.y += 2
        if self.x > self.__game.player.x:
            self.x -= 2
        if self.y > self.__game.player.y:
            self.y -= 2
        x1, x2 = self.x - self.__size / 2, self.x + self.__size / 2
        y1, y2 = self.y - self.__size / 2, self.y + self.__size / 2
        if x1 <= self.__game.player.x <= x2 and y1 <= self.__game.player.y <= y2:
            self.__game.game_over_lose()

    def create(self) -> None:
        self.__id = self.canvas.create_oval(100, 100, 100 + self.__size, 100 + self.__size, fill=self.__color)

    def render(self) -> None:
        self.canvas.coords(self.__id,
                           self.x - self.__size / 2,
                           self.y - self.__size / 2,
                           self.x + self.__size / 2,
                           self.y + self.__size / 2)

    def delete(self) -> None:
        self.canvas.delete(self.__id)


class FencingEnemy(Enemy):
    """Fencing around house"""

    def __init__(self, game: "turtle_adventure.TurtleAdventureGame", size: int, color: str):
        super().__init__(game, size, color)
        self.__game = game
        self.__size = size
        self.__color = color
        # self.__speed = speed
        self.x: int
        self.y: int
        self.count = 0

    def update(self) -> None:
        self.count += 1
        x1, x2 = self.x - self.__size / 2, self.x + self.__size / 2
        y1, y2 = self.y - self.__size / 2, self.y + self.__size / 2
        if x1 <= self.__game.player.x <= x2 and y1 <= self.__game.player.y <= y2:
            self.__game.game_over_lose()
        if self.count <= 60:
            self.x -= 1
        elif self.count <= 120:
            self.y -= 1
        elif self.count <= 180:
            self.x += 1
        elif self.count <= 240:
            self.y += 1
        else:
            self.count = 0

    def create(self) -> None:
        self.__id = self.canvas.create_oval(100, 100, 100 + self.__size, 100 + self.__size, fill=self.__color)

    def render(self) -> None:
        self.canvas.coords(self.__id,
                           self.x - self.__size / 2,
                           self.y - self.__size / 2,
                           self.x + self.__size / 2,
                           self.y + self.__size / 2)

    def delete(self) -> None:
        self.canvas.delete(self.__id)


class DoorEnemy(Enemy):
    """Move up and down, slowly"""

    def __init__(self, game: "turtle_adventure.TurtleAdventureGame", size: int, color: str):
        super().__init__(game, size, color)
        self.__game = game
        self.__size = size
        self.__color = color
        # self.__speed = speed
        self.x: int
        self.y: int
        self.cont_x, self.cont_y = self.set_range()

    def update(self) -> None:
        x1, x2 = self.x - self.__size / 2, self.x + self.__size / 2
        y1, y2 = self.y - self.__size / 2, self.y + self.__size / 2
        if x1 <= self.__game.player.x <= x2 and y1 <= self.__game.player.y <= y2:
            self.__game.game_over_lose()
        self.y += self.cont_y
        if self.y > 500:
            self.cont_y = - self.cont_y
        if self.y < 0:
            self.cont_y = -self.cont_y

    def create(self) -> None:
        self.__id = self.canvas.create_rectangle(100, 100, 100 + self.__size, 100 + self.__size, fill=self.__color)

    def render(self) -> None:
        self.canvas.coords(self.__id,
                           self.x - self.__size / 2,
                           self.y - self.__size / 2,
                           self.x + self.__size / 2,
                           self.y + self.__size / 2)

    def set_range(self):
        x2 = random.randint(-3, 3)
        y2 = random.randint(-3, 3)
        return x2, y2

    def delete(self) -> None:
        self.canvas.delete(self.__id)
