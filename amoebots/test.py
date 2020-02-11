import node_construction as nc
import visual_construction as vc
import datetime as dt

if __name__ == '__main__':
    time = dt.datetime.now().time()
    n = nc.NodeManager()
    x = 100
    n.create_cluster(x=x)
    v = vc.GridVisualClass()
    v.create_grid(n.plot())
    v.show_fig()
    time2 = dt.datetime.now().time()
    print('success')
    print(f'it took {dt.datetime.combine(dt.date.today(), time2)-dt.datetime.combine(dt.date.today(), time)} to create {n.get_number_of_nodes()}')