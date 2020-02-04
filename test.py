import area_construction as ac
import visuals_construction as vs

if __name__ == '__main__':
    a = ac.LineArea()
    a.run_simulation(5,101, wireless=True)
    # b = ac.LineArea()
    # b.run_simulation(11, 1)

    # vs.test()
    vs.show()

    print('success')
