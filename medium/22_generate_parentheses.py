# Problem: 22. Generate Parentheses
# Difficulty: Medium
# Link: https://leetcode.com/problems/generate-parentheses/
# Date: 07/18/2025

from typing import List

class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        stack = []
        res = []

        def backtrack(openC, closedC):
            if openC == closedC == n:
                res.append(''.join(stack))

                return

            if openC < n:
                stack.append('(')
                backtrack(openC + 1, closedC)
                stack.pop()

            if closedC < openC:
                stack.append(')')
                backtrack(openC, closedC + 1)
                stack.pop()

        backtrack(0,0)
        return res