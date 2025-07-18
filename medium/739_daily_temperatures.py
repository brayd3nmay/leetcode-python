# Problem: 739. Daily Temperatures
# Difficulty: Medium
# Link: https://leetcode.com/problems/daily-temperatures/
# Date: 07/18/2025

from typing import List

class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        stack = []
        res = [0] * len(temperatures)

        for i, n in enumerate(temperatures):
            while stack and n > stack[-1][1]:
                index, num = stack.pop()
                res[index] = i - index

            stack.append((i, n))

        return res