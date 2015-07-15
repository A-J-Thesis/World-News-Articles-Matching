# -*- coding: utf-8 -*-
# Project:  World News Articles Matching
# File:     ProgressBar.py
# Authors:  Jason Papapanagiotakis, Aris Kotsomitopoulos
# Github:   https://github.com/A-J-Thesis/World-News-Arcticles-Matching

import time
import sys
import math

class ProgressBar:

    def __init__(self,max_size=36):
        ProgressBar.max_size = max_size
        ProgressBar.tick = 20.0/max_size
        ProgressBar.progress_counter = 0.0
        ProgressBar.counter = 0
        spaces = ' ' * 20
        hashes = '█' * 0
        sys.stdout.write("\rPercent: ┃{0}┃{1}%".format(hashes + spaces, 0))
        sys.stdout.flush()

    def update(self):
        ProgressBar.counter += 1
        if ProgressBar.counter == ProgressBar.max_size:
            hashes = '█' * 20
            spaces = ' ' * 0
            sys.stdout.write("\rPercent: ┃{0}┃{1}%".format(hashes + spaces, 100))
            print
            print "Finished Successfully!"
            sys.stdout.flush()
            return
        elif ProgressBar.counter >= ProgressBar.max_size:
            return
            
        ProgressBar.progress_counter += ProgressBar.tick
        hashes = '█' * int(ProgressBar.progress_counter)
        spaces = ' ' * (20 - int(ProgressBar.progress_counter))
        percentage = int(round(ProgressBar.progress_counter * 5))
        sys.stdout.write("\rPercent: ┃{0}┃{1}%".format(hashes + spaces, percentage))
        sys.stdout.flush()
        return

class SupportBar:
    
    def __init__(self):
        SupportBar.counter = 0
        
    def increase(self):
        SupportBar.counter += 1
        
    def init(self):
        SupportBar.counter = 0
        
    def get(self):
        return SupportBar.counter
