from plot import Grid
from node_manager import NodeManager

import node_manager as nm
import bot_manager as bm
import plot as pt
import time




if __name__ == "__main__":
    grid_size_x = 128
    grid_size_y = 128

    t1 = time.perf_counter()
    for _ in range(1):
        grid = Grid(grid_size_x, grid_size_y)
        grid.create_triangular_grid()
        node_manager = NodeManager()
        node_manager.initialize()
        plotted_points = grid.get_grid()
        node_manager.set_plotted_points(plotted_points=plotted_points)

        node_manager.create_node_structure()
        number_of_bots = node_manager.get_number_nodes()//3
        bot_manager = bm.BotManager()
        bot_manager.random_bot_placement(number_of_bots=number_of_bots,node_list=node_manager.get_node_list())
        round = 0
        while True:
            status = bot_manager.activate_si()
            if status:
                break
            round += 1
            if not round%10:
                print(f"Round {round} completed")
    t2 = time.perf_counter()
    print(f"it took {t2-t1} seconds and {round} rounds to run this program ")
    print("success")