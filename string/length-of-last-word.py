class Solution:
    def lengthOfLastWord(self, s: str) -> int:

        count = 0
        cleaned_string = s.strip()

        for i in range(len(cleaned_string)-1, -1, -1):
            print(cleaned_string[i])
            if (cleaned_string[i] == " "):
                return count
            elif (cleaned_string[i] != " "):
                count += 1

        return count
        
