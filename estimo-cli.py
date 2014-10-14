# -*- coding: utf-8 -*-

from estimo import Estimo
import argparse

parser = argparse.ArgumentParser(description='steamgifts.com client')
parser.add_argument('-s', '--scan', const='scan', default='play', nargs='?', dest='operation',
                    help='Scan the webpage and choose what games you want')
parser.add_argument('-f', '--full', const=True, default=False, nargs='?',
                    help='Work on all pages, not just on the first one (frontpage - page 1)')
parser.add_argument('-d', '--debug', const=True, default=False, nargs='?',
                    help='Show the browser window')
estimo = Estimo()
argss = parser.parse_args()
if argss.operation == 'scan':
    games = estimo.scan(argss.full, argss.debug)
    for game in games:
        decision = raw_input("New game found: '" + game + "'. Do you want to " +
                             " automatically access its giveaways (y/n/q)?")
        if decision == 'y':
            estimo.settings.add_game(game, 1)
        elif decision == 'n':
            estimo.settings.add_game(game, 0)
        else:
            break
    estimo.settings.save()
else:
    games = estimo.subscribe(argss.full, argss.debug)
    for game in games:
        print(game)
