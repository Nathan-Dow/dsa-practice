class Solution:
    def canJump(self, nums: List[int]) -> bool:

        if len(nums) == 1 and (nums[0] == 0): 
            return True

        #check if non startable
        if (nums[0] == 0):
            return False
        
        # we just need to check the farthest possible traversable point
        max_traversable = nums[0]

        for i in range(1, len(nums)):
            if (nums[i] == 0) and (max_traversable == i) and (i != len(nums)-1):
                return False

            new_max = nums[i] + i

            if new_max > max_traversable:
                max_traversable = new_max

        return True
