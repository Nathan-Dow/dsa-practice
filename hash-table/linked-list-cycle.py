# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
      
        check_set = set()

        current = head

        while current is not None:
            if current not in check_set:
                check_set.add(current)
            else:
                return True
            current = current.next
        return False
