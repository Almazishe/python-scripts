from typing import List



def sumOddLengthSubarrays(arr: List[int]) -> int:
    result = 0
    length = len(arr)

    for count in range(1, length + 1, 2):
        end = count
        start = 0
        while end <= length:
            result += sum(arr[start:end])
            start += 1
            end += 1 
            
    return result


def main():
    print([1,4,2,5,3], " -> ",sumOddLengthSubarrays([1,4,2,5,3]))
    print([1,2], " -> ",sumOddLengthSubarrays([1,2]))
    print([10,11,12], " -> ",sumOddLengthSubarrays([10,11,12]))


if __name__ == '__main__':
    main()