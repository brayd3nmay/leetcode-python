# Problem: 242. Valid Anagram
# Difficulty: Easy
# Link: https://leetcode.com/problems/valid-anagram
# Date: 06/30/2025

class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        str1 = {}
        str2 = {}

        for c in s:
            if c not in str1:
                str1[c] = 1
            else:
                str1[c] = str1[c] + 1

        for c in t:
            if c not in str2:
                str2[c] = 1
            else:
                str2[c] = str2[c] + 1

        return str1 == str2