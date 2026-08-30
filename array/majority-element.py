import math

class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        crit_value = len(nums) // 2

        number_dict = {}
        max_val = 0

        winning = 0 

        for i in range(len(nums)):
            number_dict[nums[i]] = number_dict.get(nums[i], 0) + 1

            if (number_dict.get(nums[i])) > max_val:
                max_val = number_dict.get(nums[i])
                winning = nums[i]
        return winning
