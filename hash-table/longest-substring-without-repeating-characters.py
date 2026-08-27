class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        
        if not s:
            return 0
    
        max_length = 0
        start_index = 0
        
        last_seen = {}

        for end_index, char in enumerate(s):
            
            if char in last_seen and last_seen[char] >= start_index:
                start_index = last_seen[char] + 1
            
   
            last_seen[char] = end_index

            current_length = end_index - start_index + 1
            max_length = max(max_length, current_length)
            
        return max_length
