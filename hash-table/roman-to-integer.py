class Solution:
    def romanToInt(self, s: str) -> int:

        counter = 0
        temp_sign = 1
        for i in range(len(s)):
            
            if (i < len(s) - 1):
                if (s[i] == 'I'):
                    if (s[i+1] == 'V') or (s[i+1] == 'X'):
                        temp_sign = -1
                
                elif (s[i] == 'X'):
                    if (s[i+1] == 'L') or (s[i+1] == 'C'):
                        temp_sign = -1
              
                elif (s[i] == 'C'):
                    if (s[i+1] == 'D') or (s[i+1] == 'M'):
                        temp_sign = -1
             
                    
            match s[i]:
                case 'I':
                    counter += (1 * temp_sign)
                case 'V':
                    counter += 5
                case 'X':
                    counter += (10 * temp_sign)
                case 'L':
                    counter += 50
                case 'C':
                    counter += (100 * temp_sign)
                case 'D':
                    counter += 500
                case 'M':
                    counter += 1000

            temp_sign = 1

        return counter
