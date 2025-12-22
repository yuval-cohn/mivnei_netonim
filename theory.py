from AVLTree import AVLTree
import random

def array_to_tree(iter):
    tree = AVLTree()
    total_cost = 0
    for item in iter:
        total_cost += tree.finger_insert(item, item)[2]
    return total_cost


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


def test_average_array_costs(array_create_func, reps=1):
    for i in range(1, 6):
        cost = 0
        for j in range(reps):
            array = array_create_func(300*2**i)
            random.shuffle(array)
            cost += array_to_tree(array)/reps
        print(i, cost)

def test_average_switches_array(array_create_func, reps=1):
    for i in range(1,6):
        switches = 0
        for j in range(reps):
            switches += count_switchest(array_create_func(300*2**i))/reps
        print(i, switches)

def mix_neighbors(array):
    index_list = list(range(len(array)))
    for i in range(len(array) -1):
        if random.choice(["mix", "dont mix"]) == "mix":
            a = index_list[i+1]
            index_list[i+1] = index_list[i]
            index_list[i] = a
    mixed_array = [array[i] for i in index_list]
    return mixed_array



#
def test(test_func):
    print("================sorted===============")
    test_func(generate_sorted_array, 1)
    print("===============reverse sorted=========")
    test_func(generate_reverse_sorted_array, 1)
    print("===============random=================")
    test_func(generate_random_sorted_array, 20)
    print("===============neighbor===============")
    test_func(generate_mix_neighbors_sorted_array, 20)


def count_switchest(array):
    counter = 0
    for i in range(len(array)-1):
        for j in range(i+1, len(array)):
            if array[i] > array[j]:
                counter += 1

    return counter

def test1():
    test(test_average_array_costs)

def test2():
    test(test_average_switches_array)

test2()
