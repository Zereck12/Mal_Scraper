""" 
PyJaC Competition Submission

Prompts: Create a mathematical-operations-guesser
possibly, combine with web scraping later

Valid operations include; +, -, /, *, ()

We'll just consider the (4): +, -, /, * (for now)
"""

from itertools import combinations_with_replacement
from typing import Tuple, List


OPS = ['+', '-', '/', '*']


def ask_input() -> Tuple:
    """ Asks the user for the numbers 
    and the result """
    print("========== MATH OPERATION GUESSER ========")
    seq = input("Enter sequence of numbers: ").split(',')
    result = input("Enter the result: ")
    print(f"Sequence: {seq}, Result: {result}")
    
    try:
        return [int(i) for i in seq], int(result)
    except ValueError: 
        return ask_input()


def combine(nums: List[int], ops: List[str]) -> str:
    """ Return the expression where the <nums>
    and <ops> are combined"""
    ans = ""
    for i in range(len(ops)):
        ans += str(nums[i]) + ops[i]
    ans += str(nums[len(nums)-1])
    return ans


def try_all_combs(nums: List[int], result: int) -> str:
    """ Try out all the different combinations """
    
    for comb in combinations_with_replacement(OPS, len(nums) - 1):
        expr = combine(nums, comb)
        if eval(expr) == result:
            return expr
    return ""


if __name__ == '__main__':
    
    nums, result = ask_input()
    
    ans = try_all_combs(nums, result)
    if ans:
        print(ans)
    else:
        print("[No answer found!]")
    