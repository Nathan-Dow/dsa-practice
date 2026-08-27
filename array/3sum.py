class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        answers = []

        nums.sort()

        for i, a in enumerate(nums):
            if i > 0 and a == nums[i-1]:
                continue

            l = i + 1
            r = len(nums) - 1

            while l < r:
                cur_sum = a + nums[l] + nums[r]

                if (cur_sum < 0):
                    l += 1
                elif (cur_sum > 0):
                    r -= 1
                else: 
                    answers.append([a, nums[l], nums[r]])
                    l += 1
                    while nums[l] == nums[l-1] and l < r:
                        l+= 1
                    
        return answers


        
