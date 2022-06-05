'''
A module for matplotlib animated vizualization of the CA
'''

from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patches as mpatches
from cellular_automaton import CellularAutomaton
import numpy as np


def main():
    grid_size = tuple(map(int, input("Enter grid size (e.g. 160 90): ").split()))
    ua_percentage = float(input("Enter percentage of Ukrainian speakers (e.g 0.3): "))
    age_dist = tuple(map(float, input("Enter respective percentages of youth and adults (e.g 0.3 0.5): ").split()))
    fill = float(input("Enter fill percentage of the grid (e.g 0.8): "))
    print("Plotting..")
    ca = CellularAutomaton(*grid_size, ua_percentage, *age_dist, fill)
    grid = ca.get_grid()

    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)

    cmap = LinearSegmentedColormap.from_list(
        'ru-ua', ((1, 0, 0), (0, 0, 1)), N=5)

    states = [[grid[i, j].state if grid[i, j] else np.nan for j in range(
        grid.shape[1])] for i in range(grid.shape[0])]

    states = np.ma.array(states, mask=np.isnan(states))

    cmap.set_bad((1, 1, 1), np.nan)

    mappable = ax.imshow(states, cmap=cmap)

    ax.set_title('Language Spread Simulation. Step 1')

    cbar = fig.colorbar(mappable=mappable, ax=ax, ticks=[i for i in range(5)])

    cbar.set_ticks([0.4 + 0.8 * i for i in range(5)],
                   labels=['active ru speaker', 'passive ru speaker',
                           'surzhyk-speaking', 'pasive ua speaker',
                           'active ua speaker'])

    def check_monotonic(grid):
        return all((j is None or j.state == 4) for row in grid for j in row) or\
                all((j is None or j.state == 0) for row in grid for j in row)

    def iterate() -> iter:
        while not check_monotonic(ca.get_grid()):
            ca.evolve()
            if check_monotonic(ca.get_grid()):
                print('End of the Simulation! The Society Became Monotonic!')
                return None
            yield ca.get_grid()
        

    def animation(grid):
        states = [[grid[i, j].state if grid[i, j] else np.nan for j in range(
            grid.shape[1])] for i in range(grid.shape[0])]

        states = np.ma.array(states, mask=np.isnan(states))

        death_patch = mpatches.Patch(label=f"Deaths: {ca.total_deaths}")
        birth_patch = mpatches.Patch(label=f"Births: {ca.total_births}")

        leg = None
        leg = fig.legend(handles=[birth_patch, death_patch])

        step = int(ax.get_title().split(' ')[-1]) + 1
        ax.clear()
        ax.imshow(states, cmap=cmap)
        ax.set_title(f'Language Spread Simulation. Step {step}')

    anim = FuncAnimation(fig, animation, frames=iterate(),
                         interval=0, repeat=False)
    plt.show()


if __name__ == '__main__':
    main()
