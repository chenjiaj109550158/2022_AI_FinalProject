# AI-2022-Final-Project-Gobang-AI


## Enviornment
 Python 3

## Requirement
- pygame
- numpy

## Abstract
We construct the environment of gobang(五子棋), where an user can switch modes, including mumual and two different type of AI robots. One is applying minimax algorithm and the other one is applying Momte Carlo search tree.

## Guidence
Just like regular Gobang, you can place a piece on the board by clicking the mouse.
Users can press the buttons introducing below anytime to switch different modes.
(Defalut is 'MANUAL' playing black and 'MANUAL' playing white.) 
('Random' mode is used for debug)
button 'a': 'MANUAL' playing black
button 's': 'RANDOM' playing black
button 'd': 'MCTS' playing black
button 'f': 'MINIMAX' playing black
button 'h': 'MANUAL' playing white
button 'j': 'RANDOM' playing white
button 'k': 'MCTS' playing white
button 'l': 'MINIMAX' playing white

    #switch modes
        if event.key == ord('a'):
        modes_list[0] = 'MANUAL'
    if event.key == ord('s'):
        modes_list[0] = 'RANDOM'
    if event.key == ord('d'):
        modes_list[0] = 'MCTS'
    if event.key == ord('f'):
        modes_list[0] = 'MINIMAX'
    if event.key == ord('h'):
        modes_list[1] = 'MANUAL'
    if event.key == ord('j'):
        modes_list[1] = 'RANDOM'
    if event.key == ord('k'):
        modes_list[1] = 'MCTS'
    if event.key == ord('l'):
        modes_list[1] = 'MINIMAX'


[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [dill]: <https://github.com/joemccann/dillinger>
   [git-repo-url]: <https://github.com/joemccann/dillinger.git>
   [john gruber]: <http://daringfireball.net>
   [df1]: <http://daringfireball.net/projects/markdown/>
   [markdown-it]: <https://github.com/markdown-it/markdown-it>
   [Ace Editor]: <http://ace.ajax.org>
   [node.js]: <http://nodejs.org>
   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [jQuery]: <http://jquery.com>
   [@tjholowaychuk]: <http://twitter.com/tjholowaychuk>
   [express]: <http://expressjs.com>
   [AngularJS]: <http://angularjs.org>
   [Gulp]: <http://gulpjs.com>

   [PlDb]: <https://github.com/joemccann/dillinger/tree/master/plugins/dropbox/README.md>
   [PlGh]: <https://github.com/joemccann/dillinger/tree/master/plugins/github/README.md>
   [PlGd]: <https://github.com/joemccann/dillinger/tree/master/plugins/googledrive/README.md>
   [PlOd]: <https://github.com/joemccann/dillinger/tree/master/plugins/onedrive/README.md>
   [PlMe]: <https://github.com/joemccann/dillinger/tree/master/plugins/medium/README.md>
   [PlGa]: <https://github.com/RahulHP/dillinger/blob/master/plugins/googleanalytics/README.md>
