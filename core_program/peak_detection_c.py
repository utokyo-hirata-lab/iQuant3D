import time
import numpy as np
import cython_code

if __name__ == "__main__":
    start_time = time.time()

    num1 = [i for i in range(10000)]
    num2 = [i for i in range(10000)]

    res = cython_code.cy_peak_detect(np.array(num1), np.array(num2))
    print(res)

    all_time = time.time() - start_time
    print("Execution time:{0} [sec]".format(all_time))
