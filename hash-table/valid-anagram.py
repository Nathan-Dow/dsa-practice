class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        
        counter = {}

        for char in s:
            counter[char] = counter.get(char, 0) + 1
        
        for check in t:
            if check not in counter:
                return False
            
            counter[check] = counter.get(check, -1) - 1

        for key, value in counter.items():
            if value != 0:
                return False

        return True
