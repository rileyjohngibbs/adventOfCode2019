with open("input.txt", "r") as f:
    input_text = f.read()
low = int(input_text.split("-")[0])
high = int(input_text.split("-")[1])

def passes(num):
    strnum = str(num).zfill(6)
    for i in range(5):
        if strnum[i] > strnum[i+1]:
            return False
    if not any(strnum[i] == strnum[i+1] for i in range(5)):
        return False
    return True

print(len([x for x in range(low, high+1) if passes(x)]))

def passes2(num):
    strnum = str(num).zfill(6)
    for i in range(5):
        if strnum[i] > strnum[i+1]:
            return False
    if not any(strnum[i] == strnum[i+1] and (i == 0 or strnum[i-1] != strnum[i]) and (i == 4 or strnum[i+2] != strnum[i]) for i in range(5)):
        return False
    return True

print(len([x for x in range(low, high+1) if passes2(x)]))
