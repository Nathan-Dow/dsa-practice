class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:

        memory = {}
        for i in range(len(magazine)):
            memory[magazine[i]] = memory.get(magazine[i], 0) + 1

        for j in range(len(ransomNote)):
            if ransomNote[j] not in memory or memory[ransomNote[j]] == 0:
                return False
            
            memory[ransomNote[j]] -= 1
        

        return True
