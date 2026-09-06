class Solution:
    def simplifyPath(self, path: str) -> str:
        
        stack = []

        for section in path.split("/"):
            if section == '..':
                if stack:
                    stack.pop()
            elif section not in ('','.'):
                stack.append(section)
        
        return "/" + "/".join(stack)
