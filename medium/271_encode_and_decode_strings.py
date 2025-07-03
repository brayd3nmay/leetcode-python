# Problem: 271. Encode and Decode Strings
# Difficulty: Medium
# Link: https://leetcode.com/problems/encode-and-decode-strings
# Date: 07/02/2025

class Solution:

    def encode(self, strs: List[str]) -> str:
        encoded = ''
        for s in strs:
            encoded += s + ','

        return encoded

    def decode(self, s: str) -> List[str]:
        slist = []

        while len(s) > 0:
            end = s.find(',')
            slist.append(s[0:end])
            s = s.replace(slist[-1],'')
            s = s.replace(',','', 1)

        return slist