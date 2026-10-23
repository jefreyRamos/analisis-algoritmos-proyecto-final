from .bucket_sort import bucket_sort
from .counting_sort import counting_sort
from .radix_sort import radix_sort

ALGORITMOS = {
    "Counting Sort": counting_sort,
    "Radix Sort": radix_sort,
    "Bucket Sort": bucket_sort,
}
