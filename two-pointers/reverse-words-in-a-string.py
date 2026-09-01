class Solution:
    def reverseWords(self, s: str) -> str:
        cleaned_str = s.strip()

        split_str = cleaned_str.split()

        reversed_str = reversed(split_str)
        
        complete_str = " ".join(reversed_str)

        return complete_str

