# Problem: 128. Longest Consecutive Sequence
# Difficulty: Medium
# Link: https://leetcode.com/problems/longest-consecutive-sequence
# Date: 07/09/2025

class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        num_set = set(nums)
        longest = 0

        for i in num_set:
            if i - 1 not in num_set:
                length = 1
                while i + length in num_set:
                    length += 1
                longest = max(longest, length)

        return longest