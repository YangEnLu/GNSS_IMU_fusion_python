def find_str(string:str, substring:str):
    index = 0
    indices = []
    while index < len(string):
        index = string.find(substring, index)
        if index == -1:
            break
        indices.append(index)
        index += 1
    return indices