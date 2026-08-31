class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        left_storage = []
        right_storage = []

        left_storage.append(nums[0])
        right_storage.append(nums[-1])

        for i in range(1, len(nums)-1):
            left_storage.append(nums[i] * left_storage[i-1])

        nums.reverse()
        for j in range(1, len(nums)-1):
            right_storage.append(nums[j] * right_storage[j-1])

        answer = []
        right_storage.reverse()

        for k in range(len(nums)):
            if k == 0:
                answer.append(right_storage[0])
            elif k == len(nums)-1:
                answer.append(left_storage[-1])
            else: 
                answer.append(left_storage[k-1] * right_storage[k]) 
        
        return answer

