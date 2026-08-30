class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        two_club = 1

        counter = 1
        revised = 0
        for original in range(1, len(nums)):
            # revised != original means change in number, therefore we reset to 1
            # else, we bump to 2
            # if counter already 2 then original increment

            if (nums[revised] != nums[original]): 
                counter = 1
                revised += 1
                nums[revised] = nums[original]   
                two_club += 1
            elif counter == 2:
                pass
            else: 
                revised += 1
                counter += 1
                nums[revised] = nums[original]
                two_club += 1
        return two_club
                
