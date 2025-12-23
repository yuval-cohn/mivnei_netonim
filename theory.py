import random

from AVLTree import AVLTree


def array_to_tree(iter)-> tuple[AVLTree, int]:
    tree = AVLTree()
    total_cost = 0
    for item in iter:
        total_cost += tree.finger_insert(item, item)[2]
    return tree, total_cost


def generate_sorted_array(length):
    return list(range(length))


def generate_reverse_sorted_array(length):
    return list(range(length, 0, -1))


def generate_random_sorted_array(length):
    array = generate_sorted_array(length)
    random.shuffle(array)
    return array


def generate_mix_neighbors_sorted_array(length):
    array = generate_sorted_array(length)
    mixed_array = mix_neighbors(array)
    return mixed_array


def test_average_array_costs(array_create_func, scale, reps=1):
    for i in range(1, scale + 1):
        cost = 0
        for j in range(reps):
            array = array_create_func(300 * 2 ** i)
            random.shuffle(array)
            cost += array_to_tree(array)[1] / reps
        print(i, cost)


def test_average_switches_array(array_create_func, scale, reps=1):
    for i in range(1, scale + 1):
        switches = 0
        for j in range(reps):
            switches += count_switchest(array_create_func(300 * 2 ** i)) / reps
        print(i, switches)


def test_search_array_average_cost(array_create_func, scale, reps=1):
    for i in range(scale+1):
        cost = 0
        for j in range(reps):
            array = array_create_func(300*2**i)
            item_to_search = random.choice(array)
            tree = array_to_tree(array)[0]
            cost += tree.finger_search(item_to_search)[1] / reps
        print(i, cost)



def mix_neighbors(array):
    index_list = list(range(len(array)))
    for i in range(len(array) - 1):
        if random.choice(["mix", "dont mix"]) == "mix":
            a = index_list[i + 1]
            index_list[i + 1] = index_list[i]
            index_list[i] = a
    mixed_array = [array[i] for i in index_list]
    return mixed_array


#
def test(test_func, scale, regular_test_reps, random_test_reps):
    print("================sorted===============")
    test_func(generate_sorted_array, scale, regular_test_reps)
    print("===============reverse sorted=========")
    test_func(generate_reverse_sorted_array, scale, regular_test_reps)
    print("===============random=================")
    test_func(generate_random_sorted_array, scale, random_test_reps)
    print("===============neighbor===============")
    test_func(generate_mix_neighbors_sorted_array, scale, random_test_reps)


def count_switchest(array):
    counter = 0
    for i in range(len(array) - 1):
        for j in range(i + 1, len(array)):
            if array[i] > array[j]:
                counter += 1

    return counter


def test1():
    test(test_average_array_costs, 5, 1, 20)


def test2():
    test(test_average_switches_array, 5, 1, 20)

def test3():
    test(test_search_array_average_cost, 5, 20, 20)

test3()
