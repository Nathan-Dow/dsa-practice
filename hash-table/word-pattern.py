class Solution:
    def wordPattern(self, pattern: str, s: str) -> bool:
        words = s.split()

        if len(pattern) != len(words):
            return False

        setP = set(pattern)
        setW = set(words)
        
        if len(setP) != len(setW):
            return False

        checker = {}

        for k in range(len(pattern)):
            if pattern[k] not in checker:
                checker[pattern[k]] = words[k]
            elif checker[pattern[k]] != words[k]:
                return False

        return True
