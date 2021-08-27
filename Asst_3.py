import random
import matplotlib.pyplot as plt
import pandas as pd
import os


from bubble_sort import bubble_sort
from heapsort import heapsort
from merge_sort import merge_sort
from selection_sort import selection_sort


class TestComplexity:
    """
    Class for testing sorting algorithms
    to measure its behaviour as n increases
    exponentially by 10
    """

    # FIXME: focus on error handling later
    def __init__(self, max_num_elements: int, increment: int, functions: list, function_names: list):
        """
        Constructor for TestComplexity
        :param max_num_elements:   int, max number of element in list
        :param increment    int, increment of number of elements in list
        :param functions:   list, list of functions to test
        :param function_names:  list, function names

        Protocol:
            Function indices:
            - bubble -> 0
            - heap -> 1
            - merge -> 2
            - selection -> 3

            Order indices:
            - Sorted -> 0
            - Reverse -> 1
            - Random -> 2

            Data index:
            - Comparison -> 0
            - Swap -> 1

        There will be 24 data columns.
        Data column = f_index * 6 + s_index * 2 + d_index
        """
        if max_num_elements <= 0:
            raise ValueError("Invalid n value. Input integer greater than or equal to 1")
        self.sorting_algorithms = functions
        self.algorithm_names = function_names
        self.max_num_elements = max_num_elements
        self.increment = increment
        self.column_names = self._generate_column_names()
        self.data = None

    def _build_ascending_list(self, n: int) -> list:
        """
        Builds a ascending list of length n
        with elements from 0..n-1
        :param n:   int, length of list and range of elements
        :return:    list, ascending list of length n

        >>> lst = build_ascending_list(10)
        >>> lst
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        """
        return [i for i in range(n)]

    def _build_descending_list(self, n: int) -> list:
        """
        Builds a descending list of length n
        from (n-1)..0
        :param n:   int, length of list and range of elements
        :return:    list, descending list of length n

        >>> lst = build_descending_list(10)
        >>> lst
        [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
        """
        return [i for i in range(n - 1, -1, -1)]

    def _build_random_list(self, n: int) -> list:
        """
        Builds a random list of length n
        with elements between 0..n-1
        :param n:   int, length of list and range of elements
        :return:    list, random list of length n

        >>> lst = build_random_list(10)
        >>> lst
        """
        # TODO: select random number generator that is fast
        #   - Consider the computational cost of certain random number generators
        #   - Focus on optimization once you finish the most of the work
        return [random.randint(0, n - 1) for i in range(n)]

    def _generate_column_names(self) -> list:
        """
        Generates DataFrame column names
        :return:    list, column names

        >>> test = TestComplexity(10, [bubble_sort, heapsort], ["bubble_sort", "heapsort"])
        >>> test._generate_column_names()
        """

        order_names = ["Sorted", "Reverse", "Random"]
        data_names = ["Comparisons", "Swaps"]

        # FIXME: check if this works
        column_names = ["Num items"]
        column_names += [algorithm + "-" + order + "-" + data for algorithm in self.algorithm_names for order in
                         order_names for data in data_names]

        return column_names

    def run_tests(self):
        """
        Runs tests.
        :return:    DataFrame, experiment results

        >>> test = TestComplexity(10, 1, [bubble_sort, heapsort], ["bubble_sort", "heapsort"])
        >>> test.run_tests()

        """
        # expected to be a 2d array
        results = []

        for i in range(0, self.max_num_elements + 1, self.increment):
            print("Testing for n = {}".format(i))
            results += [self._run_iteration(i)]

        results = pd.DataFrame(results, columns=self.column_names)
        self.data = results
        return results

    def _run_iteration(self, n: int) -> list:
        """
        Runs an iteration of tests
        :param n:   int, number of elements in test lists
        :return:    list, results for each test

        >>> test = TestComplexity(10, [bubble_sort], ["bubble_sort"])
        >>> test._run_iteration(1)

        >>> test = TestComplexity(10, [bubble_sort, merge_sort], ["bubble_sort", "merge_sort"])
        >>> test._run_iteration(2)
        """
        sorted_list = self._build_ascending_list(n)
        reverse_list = self._build_descending_list(n)
        random_list = self._build_random_list(n)

        list_options = [sorted_list, reverse_list, random_list]
        results = [n]

        # FIXME: Can it be re-factored in a Pythonic way
        # FIXME: add multithreading?
        #   - every 10k gets a thread?
        for i in range(len(self.sorting_algorithms)):
            for j in range(3):
                comparisons, swaps = self.sorting_algorithms[i](list_options[j][:])
                results.append(comparisons)
                results.append(swaps)

        return results

    def plot_data(self):
        """
        Plots data.
        """
        # TODO: make different plotting settings?
        if self.data is None:
            raise InterruptedError("Run tests first!")

        dirname = "Results - Max " + str(self.max_num_elements) + " - Inc " + str(self.increment)
        if not os.path.isdir(dirname):
            # Create Figures directory if it does not exist
            os.mkdir(dirname)

        num_rows = len(self.sorting_algorithms)
        num_columns = 2

        # plt.subplot(num_rows, num_columns, 1)
        # num_items = self.data['Num items']
        # max_offset = len(self.sorting_algorithms) * 6

        for algo_index in range(0, len(self.sorting_algorithms)):
            # Draw comparison graph
            # min_offset = i * 6 + 1  # +1 because of the num_items column
            self._generate_subplots(algo_index, dirname)

        print("The plots will be located in directory {}".format(dirname))
        plt.show()

    def _generate_subplots(self, algo_index, dirname):
        """
        Generates subplots for an algorithm's test results

        :param algo_index:  int, algorithm index
        :param dirname:     str, directory name
        """
        # suplots are at algo_index * 2 and algo_index * 2 + 1
        algorithm_name = self.algorithm_names[algo_index]
        num_items_col = data['Num items']
        plt.figure(algo_index)
        figure = plt.gcf()

        # Comparison subplot
        plt.subplot(2, 2, 1)
        plt.xlabel("Number of items")
        plt.ylabel("Number of comparisons")
        plt.title("Number of items vs number of comparisons in " + algorithm_name)
        for i in range(0, 5, 2):
            plot_name = self.column_names[algo_index * 6 + i + 1]
            plt.plot(num_items_col, self.data[plot_name], label=plot_name)
        plt.grid()
        plt.legend()

        # Swaps subplot
        plt.subplot(2, 2, 2)
        plt.xlabel("Number of items")
        plt.ylabel("Number of swaps")
        plt.title("Number of items vs number of swaps in " + algorithm_name)
        for i in range(1, 6, 2):
            plot_name = self.column_names[algo_index * 6 + i + 1]
            plt.plot(num_items_col, self.data[plot_name], label=plot_name)
        plt.grid()
        plt.legend()

        figure.set_size_inches(16, 12)
        plt.savefig(dirname + '/Figure{}.png'.format(algo_index), dpi=120)

    def export_data(self):
        """
        Exports test result data to excel.
        """
        if self.data is None:
            raise InterruptedError("Run tests first!")

        dirname = "Results - Max " + str(self.max_num_elements) + " - Inc " + str(self.increment)
        # dirname = "Output - Max " + str(self.max_num_elements) + " - Inc " + str(self.increment)
        if not os.path.isdir(dirname):
            # Create Output directory if it does not exist
            os.mkdir(dirname)
        print("The experiment data will be located in directory {} in an excel file.".format(dirname))
        self.data.to_excel(dirname + "/output.xlsx")


# ENGINEERING ASSUMPTION: The marking TA will have bubble_sort.py,
# merge_sort.py, selection_sort.py, and heapsort.py in the same directory


if __name__ == "__main__":
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    functions = [bubble_sort, heapsort, merge_sort, selection_sort]
    function_names = ["bubble_sort", "heap_sort", "merge_sort", "selection_sort"]

    print("---RUNNING TESTS----")
    test = TestComplexity(2500, 100, functions, function_names)
    data = test.run_tests()
    test.export_data()
    print(data)

    # plot data
    print("NOTE: if the window that opens is blank, resize it to show the plots")
    test.plot_data()

    # TODO: make method that plots the results from the random lists
    #   - Compare the worst cases (hence, Big O) of each algorithm
    """
    # Plot the worst-cases for each algorithm
    worst_bubble = data['bubble_sort-Reverse-Comparisons']
    worst_heap = data['heap_sort-Sorted-Comparisons']
    worst_merge = data['merge_sort-Random-Comparisons']
    worst_selection = data['selection_sort-Random-Comparisons']
    num_items = data['Num items']

    plt.figure(10)
    figure = plt.gcf()
    plt.xlabel("Number of items")
    plt.ylabel("Number of comparisons")
    plt.title("Number of comparisons vs the number of items for the worst-cases of bubble sort," +
              "heap sort, merge sort, and selection sort")
    plt.plot(num_items, worst_bubble, label='bubble_sort-Reverse-Comparisons')
    plt.plot(num_items, worst_heap, label='heap_sort-Sorted-Comparisons')
    plt.plot(num_items, worst_merge, label='merge_sort-Random-Comparisons')
    plt.plot(num_items, worst_selection, label='selection_sort-Random-Comparisons')
    plt.grid()
    plt.legend()
    figure.set_size_inches(16, 12)
    plt.savefig('worst_case_comparison.png', dpi=120)
    plt.show()
    """
