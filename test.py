import area_construction as ac
import visuals_construction as vs

if __name__ == '__main__':
    a = ac.LineArea()
    a.run_simulation(10,1)
    b = ac.LineArea()
    b.run_simulation(11, 1)

    # vs.test()

    print('success')
