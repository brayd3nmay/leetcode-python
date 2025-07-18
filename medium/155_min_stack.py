# Problem: 155. Min Stack
# Difficulty: Medium
# Link: https://leetcode.com/problems/min-stack
# Date: 07/18/2025

class MinStack:

    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val: int) -> None:
        self.stack.append(val)

        if len(self.min_stack) == 0:
            self.min_stack.append(val)
        else:
            for i in range(len(self.min_stack)):
                if val < self.min_stack[i]:
                    self.min_stack.insert(i, val)

                    break
                elif i == len(self.min_stack) - 1:
                    self.min_stack.append(val)


    def pop(self) -> None:
        temp = self.stack.pop()

        for n in self.min_stack:
            if n == temp:
                self.min_stack.remove(n)

    def top(self) -> int:
        return self.stack[len(self.stack) - 1]
        

    def getMin(self) -> int:
        return self.min_stack[0]
    

# Your MinStack object will be instantiated and called as such:
# obj = MinStack()
# obj.push(val)
# obj.pop()
# param_3 = obj.top()
# param_4 = obj.getMin()