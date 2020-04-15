from amoebot.grid.trigrid import TriangularGrid
from amoebot.elements.node.manager import NodeManager
from amoebot.elements.bot.manager import BotManager
from time import perf_counter

def main():
        grid_size_x = 128
        grid_size_y = 128

        t1 = perf_counter()

        grid = TriangularGrid(grid_size_x, grid_size_y)
        grid_points = grid.get_grid()

        node_manager = NodeManager(points=grid_points)
        node_manager.grid_builder()
        
        node_list = node_manager._get_node_list()
        n_bots = node_manager.get_num_nodes() // 3
        
        bot_manager = BotManager()
        
        bot_manager.random_bot_placement(number_of_bots=n_bots, 
                                         node_list=node_list)

        round = 0
        while True:
            # next to review and optimize below #
            status = bot_manager.activate_mf()
            # status = bot_manager.activate_si()
            
            if status:
                break
            
            round += 1
            
            if not round%10:
                print(f"Round {round} completed")
            
            # if round > 15:
            #     break

        t2 = perf_counter()

        print(f"{t2-t1} seconds and {round} rounds")

if __name__ == "__main__": main()