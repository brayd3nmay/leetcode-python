# Problem: 271. Encode and Decode Strings
# Difficulty: Medium
# Link: https://leetcode.com/problems/encode-and-decode-strings
# Date: 07/03/2025

class Solution:

    def encode(self, strs: List[str]) -> str:
        encoded = ""
        for s in strs:
            encoded += str(len(s)) + "$" + s
    
        return encoded

    def decode(self, s: str) -> List[str]:
        res, i = [], 0
    
        while i < len(s):
            j = i

            while s[j] != "$":
                j += 1
                
            length = int(s[i:j])
            i = j + 1
            j = i + length
            res.append(s[i:j])
            i = j

        return res