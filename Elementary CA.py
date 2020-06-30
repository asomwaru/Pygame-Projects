RULES = [0,1,0,1,1,0,1,0][::-1]

def check_rules(curr_arr:list) -> list:
    new_arr = [0 for _ in range(len(curr_arr))]

    for x in range(len(curr_arr)):
        left = (x - 1) % (len(curr_arr))
        center = x
        right = (x + 1) % (len(curr_arr))

        bits = [curr_arr[left], curr_arr[center], curr_arr[right]]
        index = int("".join([str(y) for y in bits]), 2)

        new_arr[x] = RULES[index]

    return new_arr

def display_board(arr:list):
    for x in arr:
        print(" ".join(['#' if y == 1 else '.' for y in x]))

def write_to_text(arr:list):
    with open('triangle.txt', 'w') as fh:
        for x in arr:
            fh.write(" ".join(['#' if y == 1 else '.' for y in x]) + '\n')

def main():
    size = 75
    triangle = [[0]*size]
    triangle[0][int(size/2)] = 1

    for x in range(size):
        current = check_rules(triangle[x])
        triangle.append(current)

    display_board(triangle)

if __name__ == '__main__':
    main()