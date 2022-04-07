# [Py Chess Tk](https://github.com/TriForMine/py-chess-tk)
A chess game written in python with tk

![Preview](https://i.imgur.com/sFCSYrZ.png)

This project was made for a university project.

## Features
- Showing the board with pieces
- Show a preview of the movements that are possible.
- Moving pieces.
- Capturing pieces
- Turn by turn with a second player
- Detect checkmate
- Playing against a basic bot using [minimax algorithm](https://towardsdatascience.com/how-a-chess-playing-computer-thinks-about-its-next-move-8f028bd0e7b1) and [alpha-beta pruning](https://www.chessprogramming.org/Alpha-Beta).
- Configuration menu, with restart, bot or 2 players, bot difficulty.

## What is missing
This project only includes the basis of chess.<br/>
- And doesn't contain everything like **Pawn Promotion, Castling, Passant**.<br/>
- It also doesn't contain any save/load board system, neither algebraic notation.<br/>
- It will not warn about any illegal moves.

## Check and Checkmate detection
The project implements a basic detection for check and checkmate.<br/>
But it might not be perfect and not always detect them.<br/>
Be aware of this if you want to play the game.

## Unstable
Be aware that this project is just a demo of what Tkinter and Python can do. <br/>
It will probably contain bugs and doesn't detect everything correctly.<br/>

## Bot
The project implements a really simple bot using the minimax algorithm.<br/>
This bot is not optimized and not really good. <br/>

> You shouldn't try using a big depth for the bot, or it will really be slow.

## Will this project be updated in the future?
No, this project was made for a university project, and I will not maintain it as I work on other big projects.

If you want to contribute feel free to open a pull request.

## Why Tkinter?
This was the requirements for that project.

## Where does the images' comes from?
The project uses the following [images](https://commons.m.wikimedia.org/wiki/Category:SVG_chess_pieces) which are under Creative Commons license.

## Thanks
- [CorentinGS](https://github.com/CorentinGS) for suggesting some ideas and improvements to the project.
