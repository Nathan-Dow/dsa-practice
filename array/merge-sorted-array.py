class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """

        tracker = m
        for i in range(n):
            nums1[tracker] = nums2[i]
            tracker += 1
        
        nums1.sort()
        
