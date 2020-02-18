import area_construction as ac
import visuals_construction as vs

# if __name__ == '__main__':
#     a = ac.LineArea()
#     a.run_simulation(5,3, wireless=True)
#     # b = ac.LineArea()
#     # b.run_simulation(11, 1)
#
#     # vs.test()
#     vs.show()
#
#     print('success')

# testing threading
import concurrent.futures as cf
import math
import time

primes = range(100000)


def is_prime(n):
    if n % 2 == 0:
        return

    sqrt_n = int(math.floor(math.sqrt(n)))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
    return True


def main():
    with cf.ThreadPoolExecutor(max_workers=6) as executor:
        for number, prime in zip(primes, executor.map(is_prime, primes)):
            pass


def main2():
    for number, prime in zip(primes, map(is_prime, primes)):
        pass


def main3():
    with cf.ProcessPoolExecutor(max_workers=6) as executor:
        for number, prime in zip(primes, executor.map(is_prime, primes)):
            pass


if __name__ == '__main__':
    t1 = time.process_time()
    main()
    t2 = time.process_time()
    t3 = time.process_time()
    main2()
    t4 = time.process_time()
    t5 = time.process_time()
    main3()
    t6 = time.process_time()

    print(f'{t2 - t1} vs {t4 - t3} vs {t6-t5}')
