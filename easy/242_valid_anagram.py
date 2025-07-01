# Problem: 242. Valid Anagram
# Difficulty: Easy
# Link: https://leetcode.com/problems/valid-anagram
# Date: 06/30/2025

class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False

        str1, str2 = {}, {}

        for i in range(len(s)):
            str1[s[i]] = 1 + str1.get(s[1], 0)
            str2[t[i]] = 1 + str2.get(t[1], 0)

        return str1 == str2