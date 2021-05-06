# https://leetcode.com/problems/count-the-number-of-consistent-strings/

from typing import List


def countConsistentStrings(allowed: str, words: List[str]) -> int:
    allowed_set = set(list(allowed))

    count = 0

    for word in words:
        word_set = set(list(word))
        if len(word_set.difference(allowed_set)) == 0:
            count += 1


    return count
        


def main():
    print(countConsistentStrings(allowed="ab", words=["ad","bd","aaab","baa","badab"]))
    print(countConsistentStrings(allowed="abc", words=["a","b","c","ab","ac","bc","abc"]))


if __name__ == '__main__':
    main()