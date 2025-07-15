# Problem: 20. Valid Parentheses
# Difficulty: Easy
# Link: https://leetcode.com/problems/valid-parentheses/description/
# Date: 07/09/2025

class Solution:
    def isValid(self, s: str) -> bool:
        brackets = {')': '(', ']': '[', '}': '{'}

        inputStack = []

        for c in s:
            if c in brackets:
                if len(inputStack) == 0 or brackets[c] != inputStack.pop():
                    return False
            else:
                inputStack.append(c)

        return len(inputStack) == 0