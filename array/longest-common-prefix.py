class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        if not strs:
            return ""

        initialPrefix = strs[0]

        for i in range(1, len(strs)):
            currentWord = strs[i]

            while not currentWord.startswith(initialPrefix):
                initialPrefix = initialPrefix[:-1]

                if not initialPrefix:
                    return ""
        
        return initialPrefix
            
