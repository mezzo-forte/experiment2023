dummy_dict = {"a":"1 2 3", "b":"5 1 3"}
for i in dummy_dict.values():
    # listed = list(dummy_dict.values())
    if "1" in i:
        print('a')
        break
    else:
        print('b')