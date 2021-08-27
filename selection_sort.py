def selection_sort(lst: list) -> tuple:
    """Sort lst into ascending order using the selection sort, and return the
    number of element comparisons and swaps performed while sorting.

    >>> a_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    >>> selection_sort(a_list)
    (55, 0)
    >>> a_list
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


    >>> a_list = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    >>> selection_sort(a_list)
    (55, 5)
    >>> a_list
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    """
    num_comparisons = 0
    num_swaps = 0

    for i, item in enumerate(lst):
        min_idx = len(lst) - 1
        for j in range(i, len(lst)):
            num_comparisons += 1
            if lst[j] < lst[min_idx]:
                min_idx = j
        if min_idx != i:
            num_swaps += 1
            lst[min_idx], lst[i] = lst[i], lst[min_idx]

    return num_comparisons, num_swaps