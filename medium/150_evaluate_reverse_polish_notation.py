# Problem: 150. Evaluate Reverse Polish Notation
# Difficulty: Medium
# Link: https://leetcode.com/problems/evaluate-reverse-polish-notation
# Date: 07/18/2025

class Solution:
    def recursiveEvalRPN(self, tokens: List[str]) -> int:
        def dfs():
            token = tokens.pop()

            if token not in '+-*/':
                return int(token)

            right = dfs()
            left = dfs()

            if token == '+':
                return left + right
            elif token == '-':
                return left - right
            elif token == '*':
                return left * right
            else:
                return int(left/right)
        
        return dfs()

    def stackEvalRPN(self, tokens: List[str]) -> int:
        stack = []

        for token in tokens:
            if token == '+':
                stack.append(stack.pop() + stack.pop())
            elif token == '-':
                b = stack.pop()
                a = stack.pop()

                stack.append(a - b)
            elif token == '*':
                stack.append(stack.pop() * stack.pop())
            elif token == '/':
                b = stack.pop()
                a = stack.pop()

                stack.append(int(a / b))
            else:
                stack.append(int(token))

        return stack[0]