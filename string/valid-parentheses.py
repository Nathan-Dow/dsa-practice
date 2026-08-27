class Solution:

         
    def isValid(self, s: str) -> bool:
        MAPPING = {")": "(", "]": "[", "}": "{"}

        stack1 = []

        for char in s:
            if char in MAPPING.values():
                stack1.append(char)
            elif char in MAPPING.keys():
                if not stack1 or MAPPING[char] != stack1[-1]:
                    return False
                else:
                    stack1.pop()
        return not stack1
            

        
