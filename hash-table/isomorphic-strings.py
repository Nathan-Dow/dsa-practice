class Solution:
    def isIsomorphic(self, s: str, t: str) -> bool:
   
        setS = set()
        setT = set()

        for i in range(len(s)):
            setS.add(s[i])
        
        for j in range(len(s)):
            setT.add(t[j])

        if len(setS) != len(setT):
            return False

        checker = {}

        for k in range(len(s)):
            if s[k] not in checker:
                checker[s[k]] = t[k]
            elif checker[s[k]] != t[k]:
                return False


        return True
