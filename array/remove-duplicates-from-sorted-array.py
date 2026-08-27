class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        numbers = set()

        for i in range(len(nums)):
            numbers.add(nums[i])
        
        new_nums = list(numbers)
        new_nums.sort()
        
        for j in range(len(new_nums)):
            nums[j] = new_nums[j]

        return len(new_nums)
