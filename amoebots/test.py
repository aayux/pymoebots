import amoebots.node_construction as nc
import amoebots.visual_construction as vc
import amoebots.bot_construction as bc
import random as rd
import time


def create_grid_test():
    t1 = time.process_time()
    n = nc.NodeManager()
    x = 1000
    n.create_cluster(x=x)
    v = vc.GridVisualClass()
    v.create_grid(n.plot())
    v.show_fig()
    print('success')
    t2 = time.process_time()
    print(f'it took {t2-t1} to create {n.get_number_of_nodes()}')

def scan_for_spaces_test():
    """
    tests scan_for_spaces_test method for bots

    :return:
    """
    choices = ['right', 'bottom right', 'bottom left', 'left', 'top left', 'top right']
    bot = bc.Bot()
    bot.toggle_debug()
    bot.set_head_node(nc.Node())
    on_or_off = [0, 1]
    for i in range(6):
        occupied = rd.choice(on_or_off)
        if occupied:
            print(f"{choices[i]} is occupied")
            bot.get_head().set_node(choices[i], nc.Node())
            bot.get_head().get_node(choices[i]).toggle_debug()
            bot.get_head().get_node(choices[i]).toggle_occupied()
        else:
            bot.get_head().set_node(choices[i], nc.Node())
    bot.engine()
    result = bot.scan_for_spaces()
    print(f"{result[0]} is how many agents found, {result[1]} is a list of space end-points")


if __name__ == '__main__':
    # create_grid_test()
    scan_for_spaces_test()

