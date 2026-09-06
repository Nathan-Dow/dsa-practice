"""
# Definition for a Node.
class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random
"""

class Solution:
    def copyRandomList(self, head: 'Optional[Node]') -> 'Optional[Node]':
        if not head:
            return None

        old_to_new = {None: None}

        # Create all clone nodes without wiring any pointers
        curr = head
        while curr:
            old_to_new[curr] = Node(curr.val)
            curr = curr.next

        curr = head
        while curr:
            clone = old_to_new[curr]
            clone.next = old_to_new[curr.next]        
            clone.random = old_to_new[curr.random]    
            curr = curr.next

        # Return the clone of the head node
        return old_to_new[head]
            

        
