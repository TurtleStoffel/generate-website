def is_sorted(list):
    return all(a <= b for a, b in zip(list, list[1:]))

def flatten(list: list[list[any]]):
    return [item for sublist in list for item in sublist]