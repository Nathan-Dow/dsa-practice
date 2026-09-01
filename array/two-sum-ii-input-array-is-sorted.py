class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        visited ={}

        for i in range(len(numbers)):
            to_find = target - numbers[i]

            if to_find in visited:
                return [visited[to_find] + 1, i + 1]
            else:
                visited[numbers[i]] = i 
         
    
