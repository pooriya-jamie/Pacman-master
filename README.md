# AI algorithms for Pacman

## Intro
[The Pacman Projects](http://ai.berkeley.edu/project_overview.html) by the [University of California, Berkeley](http://berkeley.edu/).

Special Thanks to Davide Liu for sharing this project (https://github.com/davide97l/Pacman)

![Animated gif pacman game](http://ai.berkeley.edu/images/pacman_game.gif)

Start a game with the command and move the agents using ASWD keyboard buttons or arrow keys:
```
python pacman.py
```
You can see the list of all options and their default values via:
```
python pacman.py -h
```

## Multi-Agent algorithms
- MinimaxAgent: an adversarial search agent implementing minimax algorithm
```
$ python pacman.py -p MinimaxAgent -l minimaxClassic -a depth=4
```
- AlphaBetaAgent: an adversarial search agent implementing minimax algorithm with alpha-beta pruning to more efficiently explore the minimax tree.
```
$ python pacman.py -p AlphaBetaAgent -l openClassic -a depth=2
```

## Search algorithms
- DeepSearch: a deep search algorithm to find the best possible path given an evaluation function, it si faster than minimax but doesn't keep into considerations ghosts
```
$ python pacman.py -l trickyClassic -p DeepSearchAgent -a depth=6 evalFn=evaluationFunction
```
