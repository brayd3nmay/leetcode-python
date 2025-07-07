# Problem: 238. Product of Array Except Self
# Difficulty: Medium
# Link: https://leetcode.com/problems/product-of-array-except-self
# Date: 07/07/2025

class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        pre, post = [1] * len(nums), [1] * len(nums)

        for i, n in enumerate(nums):
            pre[i] = n * pre[i - 1]

        for i, n in enumerate(reversed(nums)):
            post[i] = n * post[i - 1]

        post = list(reversed(post))

        ans, i = [], 0
        while i < len(nums):
            if i == 0:
                ans.append(post[i + 1])
            elif i == len(nums) - 1:
                ans.append(pre[i - 1])
            else:
                ans.append(pre[i - 1] * post[i + 1])
            
            i += 1

        return ans