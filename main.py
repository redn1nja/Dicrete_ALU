'''
A module for matplotlib animated vizualization of the CA
'''

from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
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

    fig = plt.figure(figsize=(8, 6))
    fig.add_axes((0.05, 0.1, 0.1, 0.8))
    fig.add_axes((0.2, 0.1, 0.6, 0.8))
    fig.add_axes((0.85, 0.1, 0.04, 0.8))
    ax = fig.get_axes()

    states = [[grid[i, j].state if grid[i, j] else np.nan for j in range(
        grid.shape[1])] for i in range(grid.shape[0])]
    states = np.ma.array(states, mask=np.isnan(states))

    ax[0].clear()
    ax[0].set_frame_on(False)
    ax[0].set_axis_off()
    ax[0].text(0, 0.9, f"Births: {ca.total_births}")
    ax[0].text(0, 0.8, f"Deaths: {ca.total_deaths}")

    cmap = LinearSegmentedColormap.from_list(
        'ru-ua', ((1, 0, 0), (0, 0, 1)), N=5)
    cmap.set_bad((1, 1, 1), np.nan)

    mappable = ax[1].imshow(states, cmap=cmap)
    ax[1].set_title('Language Spread Simulation. Step 1')

    cbar = fig.colorbar(mappable=mappable, cax=ax[2], ticks=[i for i in range(5)])
    cbar.set_ticks([0.4 + 0.8 * i for i in range(5)],
                   labels=['active ru', 'passive ru',
                           'surzhyk', 'passive ua', 'active ua'])

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

        step = int(ax[1].get_title().split(' ')[-1]) + 1
        ax[1].clear()
        ax[1].imshow(states, cmap=cmap)
        ax[1].set_title(f'Language Spread Simulation. Step {step}')

        ax[0].clear()
        ax[0].set_axis_off()
        ax[0].text(0, 0.9, f"Births: {ca.total_births}")
        ax[0].text(0, 0.8, f"Deaths: {ca.total_deaths}")

    anim = FuncAnimation(fig, animation, frames=iterate(),
                         interval=100, repeat=False)
    plt.show()


if __name__ == '__main__':
    main()
