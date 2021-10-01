from colorama import init, Fore, Back, Style
from termcolor import colored, cprint

###### Class To Use Colors #########

class color :
    warning = lambda x: cprint(x, 'red', attrs=["bold"])
    main = lambda x: cprint(x, 'yellow', attrs=["bold"])
    prompt = lambda x: cprint(x, 'green', attrs=["blink"])
    success = lambda x: cprint(x, 'blue', attrs=["bold"])



