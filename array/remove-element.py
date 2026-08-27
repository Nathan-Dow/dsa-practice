class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
       
        placer = 0

        for i in range(len(nums)):
            if nums[i] != val:
                nums[placer] = nums[i]
                placer += 1
        
    
        return placer
