# Problem: 217. Contains Duplicate
# Difficulty: Easy
# Link: https://leetcode.com/problems/contains-duplicate
# Date: 06/30/2025

class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        return len(set(nums)) < len(nums)