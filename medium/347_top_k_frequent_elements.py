# 347. Top K Frequent Elements
# Difficulty: Medium
# Link: https://leetcode.com/problems/top-k-frequent-elements
# Date: 07/02/2025

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        freqMap = {}
        freqList = [[] for _ in range(len(nums))]

        for i in nums:
            freqMap[i] = freqMap.get(i, 0) + 1


        # use 0 based indexing for freq
        for num, freq in freqMap.items():
            freqList[freq - 1].append(num)

        retArray = []
        for i in range(len(freqList) - 1, -1, -1):
            for j in range(len(freqList[i])):
                retArray.append(freqList[i][j])

            if len(retArray) == k:
                return retArray