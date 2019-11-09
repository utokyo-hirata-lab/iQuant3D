cimport numpy as np

cdef extern from "peak_detection.h":
    np.int64_t c_peak_detect(np.int64_t *num1, np.int64_t *num2, np.int64_t size_a, np.int64_t size_b)

def cy_peak_detect(np.ndarray[np.int64_t, ndim=1] num1, np.ndarray[np.int64_t, ndim=1] num2):
    return c_peak_detect(&num1[0], &num2[0], len(num1), len(num2))
