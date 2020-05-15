# SavePepe

A game made using Pygame for ISS Assignment - 3 in Spring'20 semester, IIIT Hyderabad.

Game is based on Pepe the frog crossing a grid filled with obstacles.

Run command:

```shell
cd game/
python3 game.py
```

## Player Keys

Player 1: Up, Down, Left, Right
Player 2: W, S, A, D

All as used normally in games

## Scoring

For crossing a moving object, you get points equal to the speed of the object

For crossing a stationary object, you get 1 point

Crossing an object more than once does not refetch you points

For every second taken to cross the board, 1 point is deducted!

## Levels

On each level, the speed of the moving object is equal to the level number.

Thus, the game gets harder as it continues for a longer time!

## Winner

The winner is decided on the bases of who has more total points across all levels

## Exit
You can exit the game anytime by pressing the space bar
