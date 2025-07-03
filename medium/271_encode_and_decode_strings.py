# Problem: 271. Encode and Decode Strings
# Difficulty: Medium
# Link: https://leetcode.com/problems/encode-and-decode-strings
# Date: 07/02/2025

class Solution:

    def encode(self, strs: List[str]) -> str:
        encoded = ''
        for s in strs:
            encoded += str(len(s)) + s + ','

        return encoded

    def decode(self, s: str) -> List[str]:
        slist = []

        while len(s) > 0:
            slist.append(s[1:int(s[0]) + 1])
            s = s[int(s[0]) + 2:]

        return slist