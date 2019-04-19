
number_of_dishes = 5

def get_list_of_dishes():
    a = number_of_dishes
    list_of_dishes = [str(i + 1) for i in range(a)]
    return list_of_dishes

if __name__ == '__main__':
    get_list_of_dishes()
