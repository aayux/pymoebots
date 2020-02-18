import node_construction as nc
import visual_construction as vc
import time

if __name__ == '__main__':
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