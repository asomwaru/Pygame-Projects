RULES = [1,0,0,1,0,1,1,0][::-1]

def bin2dec(num:str):
    total = 0

    for i,x in enumerate(num[::-1]):
        if x == '1':
            total += (2**i)

    return total

def check_rules(curr_arr:list) -> list:
    new_arr = [0 for _ in range(len(curr_arr))]

    for x in range(len(curr_arr)):
        left = (x - 1) % (len(curr_arr))
        center = x
        right = (x + 1) % (len(curr_arr))

        bits = [curr_arr[left], curr_arr[center], curr_arr[right]]
        index = bin2dec("".join([str(y) for y in bits]))

        print("".join([str(y) for y in bits]), index)
        new_arr[x] = RULES[index]

    return new_arr

def display_board(arr:list):
    for x in arr:
        print(" ".join(['#' if y == 1 else '.' for y in x]))

def main():
    size = 25
    triangle = [[0]*size]
    triangle[0][int(size/2)] = 1

    for x in range(15):
        current = check_rules(triangle[x])
        triangle.append(current)

    display_board(triangle)

if __name__ == '__main__':
    main()