def unique(lst):
    unique_lst = []
    for item in lst:
        if item not in unique_lst:
            unique_lst.append(item)

    return unique_lst

def forall(fn, lst):
    for item in lst:
        if not fn(lst):
            return False

    return True
