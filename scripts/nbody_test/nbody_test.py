#!/usr/bin/env python3
import sys

DELTA = 0.2

def check_numbers(numbers):
    num_cnt = len(numbers[0])

    for lst in numbers:
        if len(lst) != num_cnt:
            print("Unexpected numbers")

    for num in range(num_cnt):
        ref_num = numbers[0][num]
        for lst in numbers:
            if abs(lst[num] - ref_num) > DELTA:
                print("ERROR DETECTED")
                print(lst[num], ref_num)
                return False

    print("PASSED")
    return True


def main(files):
    file_descriptors = list()

    for fl in files:
        try:
            file_descriptors.append(open(fl, 'r'))
        except:
            print("Problem opening file " + fl)

    numbers = list()

    for fd in file_descriptors:
        array = list()
        for line in fd:
            line_floats = [float(x) for x in line.split()]
            for num in line_floats:
                array.append(num)

        numbers.append(array)

    check_numbers(numbers)

    for fd in file_descriptors:
        fd.close()


if __name__ == "__main__":
    main(sys.argv[1:])
