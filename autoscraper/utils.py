def unique(item_list):	
    unique_list = []	
    for item in item_list:	
        if item not in unique_list:	
            unique_list.append(item)	
    return unique_list


def forall(fn, lst):
    for item in lst:
        if not fn(lst):
            return False

    return True
