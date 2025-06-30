# Problem: 217. Contains Duplicate
# Difficulty: Easy
# Link: https://leetcode.com/problems/contains-duplicate
# Date: 06/30/2025

class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        prev = set()

        for i in nums:
            if i in prev:
                return True
            prev.add(i)

        return False