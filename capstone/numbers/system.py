'''
    THIS IS TO CALL UBUNTU / LINUX SYSTEM CALLS
'''
import os
import platform

def clear():
    '''
        CLEAR SCREEN FOR LINUX / UNIX
    '''
    if platform.system() == 'Linux':
        os.system("clear")
