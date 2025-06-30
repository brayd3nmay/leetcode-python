# Problem: 1. Two Sum
# Difficulty: Easy
# Link: https://leetcode.com/problems/two-sum/
# Date: 06/30/2025

from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        prev = {}

        for i, n in enumerate(nums):
            diff = target - n
            if diff in prev:
                return [i, prev[diff]]
            prev[n] = i

        return []