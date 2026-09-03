class Solution:
    def maxArea(self, height: List[int]) -> int:
        bound1 = 0 
        bound2 = len(height) - 1

        max_area = 0
        while (bound1 != bound2):
            width = bound2 - bound1 
            temp_area = width * min(height[bound1], height[bound2])
        
            if temp_area > max_area:
                max_area = temp_area

            if (height[bound1] <= height[bound2]):
                bound1 += 1
            else:
                bound2 -= 1

        return max_area
