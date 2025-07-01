# Problem: 49. Group Anagrams
# Difficulty: Medium
# Link: https://leetcode.com/problems/group-anagrams
# Date: 07/01/2025

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        groups = defaultdict(list)

        for s in strs:
            chars = [0] * 26

            for c in s:
                chars[ord(c) - ord('a')] += 1

            groups[tuple(chars)].append(s)

        return list(groups.values()) 