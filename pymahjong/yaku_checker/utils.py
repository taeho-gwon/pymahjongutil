def is_three_color_index(idx1: int, idx2: int, idx3: int):
    if idx1 >= 27 or idx2 >= 27 or idx3 >= 27:
        return False
    if idx1 == idx2 or idx2 == idx3 or idx3 == idx1:
        return False
    return idx1 % 9 == idx2 % 9 == idx3 % 9
