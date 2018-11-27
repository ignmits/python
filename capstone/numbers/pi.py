'''
    Enter a number and have the program generate PI up to that many decimal places.
    Keep a limit to how far the program will go.
'''
import system

system.clear()

precision_range = 15

print('Welcome to pi precision program')

while True:
    try:
        precision = int(input('\nPlease enter precision for the value pi (0-{}) : '\
                .format(precision_range)))
        if precision < 0 or precision > precision_range:
            print('Please enter precision value in range')
            continue
        else:
            print('pi = {0:1.{prec}f}'.format(22/7, prec=precision))
            break
    except TypeError:
        print('Please enter a valid input')
        continue
