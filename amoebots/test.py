import amoebots.node_construction as nc
import amoebots.visual_construction as vc
import amoebots.bot_construction as bc
import math
import random as rd
import time
import os
import psutil


def create_grid_test():
    t1 = time.process_time()
    n = nc.NodeManager()
    x = 15
    y = 13
    n.create_cluster(x=x, y=y)
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

def MT_create_grid_with_random_bots_and_movement_test():
    """
    Notes: remember to add bots data first, then run simulation, and lastly add frames.

    :return:
    """
    t1 = time.perf_counter()
    n = nc.NodeManager()
    x = 3
    y = 3
    n.create_cluster(x=x, y=y)
    nodes = n.get_node_array()
    rd.shuffle(nodes)
    b = bc.BotManager()
    number_of_bots = math.ceil(n.get_number_of_nodes() * (1 / 3))
    b.mass_add_bots(number_of_bots=number_of_bots, nodes=nodes)
    # for i in range(number_of_bots):
    #     b.add_bots(node=nodes[i], id=i)
    # print(f"{b.get_bots()}")
    positions = b.get_positions()
    v = vc.GridVisualClass()
    v.create_bots(positions)
    # b.activate(rounds=10, turns=1)
    b.bot_threads(rounds=200, turns=None)
    plot = n.plot()
    # positions = b.get_positions()
    points = n.get_points()
    paths = b.get_paths()
    t2 = time.perf_counter()
    this_process = psutil.Process(os.getpid())
    print(f"This is the time it takes to produce data {t2-t1}, using this much memory {this_process.memory_info().rss} bytes")
    # v = vc.GridVisualClass()
    # v.create_bots(positions)
    v.create_grid(plot)
    v.create_nodes(points)
    # b.activate(rounds=20, turns=1)

    v.create_frames(paths)
    v.create_figure()
    v.show_fig()
    print("success")

def create_grid_with_random_bots_and_movement_test():
    """
    Notes: remember to add bots data first, then run simulation, and lastly add frames.

    :return:
    """
    t1 = time.perf_counter()
    n = nc.NodeManager()
    x = 15
    y = 13
    n.create_cluster(x=x, y=y)
    nodes = n.get_node_array()
    rd.shuffle(nodes)
    b = bc.BotManager()
    number_of_bots = math.ceil(n.get_number_of_nodes() * (1 / 3))
    b.mass_add_bots(number_of_bots=number_of_bots, nodes=nodes)
    # for i in range(number_of_bots):
    #     b.add_bots(node=nodes[i], id=i)
    # print(f"{b.get_bots()}")
    positions = b.get_positions()
    v = vc.GridVisualClass()
    v.create_bots(positions)
    b.activate(rounds=200, turns=1)
    # b.bot_threads(rounds=200, turns=None)
    plot = n.plot()
    # positions = b.get_positions()
    points = n.get_points()
    paths = b.get_paths()
    t2 = time.perf_counter()
    this_process = psutil.Process(os.getpid())
    print(f"This is the time it takes to produce data {t2-t1}, using this much memory {this_process.memory_info().rss} bytes")
    # v = vc.GridVisualClass()
    # v.create_bots(positions)
    v.create_grid(plot)
    v.create_nodes(points)
    # b.activate(rounds=20, turns=1)

    v.create_frames(paths)
    v.create_figure()
    v.show_fig()
    print("success")

def create_grid_with_random_bots_test():
    t1 = time.process_time()
    n = nc.NodeManager()
    x = 15
    y = 13
    n.create_cluster(x=x, y=y)
    nodes = n.get_node_array()
    rd.shuffle(nodes)
    b = bc.BotManager()
    number_of_bots = math.ceil(n.get_number_of_nodes() * (1 / 3))
    b.mass_add_bots(number_of_bots=number_of_bots, nodes=nodes)
    positions = b.get_positions()
    v = vc.GridVisualClass()
    v.create_bots(positions)
    plot = n.plot()
    points = n.get_points()
    t2 = time.process_time()
    this_process = psutil.Process(os.getpid())
    print(f"This is the time it takes to produce data {t2 - t1}, using this much memory {this_process.memory_info().rss} bytes")
    v.create_grid(plot)
    v.create_nodes(points)
    v.create_figure()
    v.show_fig()




if __name__ == '__main__':
    # create_grid_test()
    # scan_for_spaces_test()
    # create_grid_with_random_bots_test()
    # create_grid_with_random_bots_and_movement_test()
    # MT_create_grid_with_random_bots_and_movement_test()
    pass

