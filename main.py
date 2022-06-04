'''
A module for matplotlib animated vizualization of the CA
'''

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from cellular_automaton import CellularAutomaton
import numpy as np


def main():
    ca = CellularAutomaton(30, 30, 0.6, 0.3, 0.3, 0.5)
    grid = ca.get_grid()

    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
    cmap = LinearSegmentedColormap.from_list('ru-ua', ((1, 0, 0), (0, 0, 1)), N=5)
    states = [[grid[i,j].state if grid[i,j] else np.nan for j in range(grid.shape[1])] for i in range(grid.shape[0])]
    states = np.ma.array(states, mask=np.isnan(states))
    cmap.set_bad((1, 1, 1), np.nan)
    mappable = ax.imshow(states, cmap=cmap)
    cbar = fig.colorbar(mappable=mappable, ax=ax, ticks=[i for i in range(5)])
    cbar.set_ticks([0.4 + 0.8 * i for i in range(5)], 
        labels=['active ru speaker','passive ru speaker','surzhyk-speaking','pasive ua speaker','active ua speaker'])
    plt.show()

    

if __name__ == '__main__':
    main()