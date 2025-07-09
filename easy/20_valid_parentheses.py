# Problem: 20. Valid Parentheses
# Difficulty: Easy
# Link: https://leetcode.com/problems/valid-parentheses/description/
# Date: 07/09/2025

class Solution:
    def isValid(self, s: str) -> bool:
        brackets = []

        for c in s:
            if (c == '('
                or c == '{'
                or c == '['):
                brackets.append(c)
            else:
                curr = brackets.pop()
                if ((c != ')' and curr == '(')
                    or (c != '}' and curr == '{')
                    or (c != ']' and curr == '[')):
                    return False

        return True