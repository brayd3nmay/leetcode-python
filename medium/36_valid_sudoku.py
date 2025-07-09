# Problem: 36. Valid Sudoku
# Difficulty: Medium
# Link: https://leetcode.com/problems/valid-sudoku
# Date: 07/09/2025

class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        rows = defaultdict(set)
        cols = defaultdict(set)
        sub_boxes = defaultdict(set)

        for r in range(9):
            for c in range(9):
                curr = board[r][c]
                if curr == '.':
                    continue
                elif curr in rows[r] or curr in cols[c] or curr in sub_boxes[(r // 3, c // 3)]:
                    return False
                else:
                    rows[r].add(curr)
                    cols[c].add(curr)
                    sub_boxes[(r // 3, c // 3)].add(curr)

        return True