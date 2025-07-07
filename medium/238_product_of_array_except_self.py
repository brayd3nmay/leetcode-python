# Problem: 238. Product of Array Except Self
# Difficulty: Medium
# Link: https://leetcode.com/problems/product-of-array-except-self
# Date: 07/07/2025

class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        ans = [1] * len(nums)

        pre = 1
        for i in range(len(nums)):
            ans[i] *= pre
            pre *= nums[i]

        post = 1
        for j in range(len(nums) - 1, -1, -1):
            ans[i] *= post
            post *= nums[i]

        return ans