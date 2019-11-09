import time
import numpy as np
import numexpr as ne

if __name__ == "__main__":
    start_time = time.time()
    num1 = [i for i in range(10000)] #speed test
    num2 = [i for i in range(10000)] #speed test
    res = 0
    for x in num1:
        for y in num2:
            res = res + x + y
    print(res)

    all_time = time.time() - start_time
    print("Execution time:{0} [sec]".format(all_time))
