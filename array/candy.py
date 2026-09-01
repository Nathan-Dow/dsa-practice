class Solution:
    def candy(self, ratings: List[int]) -> int:
        amount = 0

        sum_array = [1] * len(ratings)

        if len(ratings) == 0:
            return 0
        if len(ratings )== 1:
            return 1
        
        #left pass
        for i in range(1, len(ratings)):
            if (ratings[i-1] < ratings[i]):
                sum_array[i] = sum_array[i-1] + 1

        #right pass
        for j in range(len(ratings)-2, -1, -1):
            if (ratings[j] > ratings[j+1]):
                sum_array[j] = max(sum_array[j], sum_array[j + 1] + 1)

        for k in range(len(sum_array)):
            amount += sum_array[k]
        
        return amount


