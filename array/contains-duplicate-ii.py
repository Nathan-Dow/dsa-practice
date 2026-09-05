class Solution:
    def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:
        window_check = set()

        for index, number in enumerate(nums):
            if number in window_check:
                return True
            
            window_check.add(number)

            if len(window_check) > k:
                window_check.remove(nums[index - k])

        return False
