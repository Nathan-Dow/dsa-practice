class Solution:
    def isHappy(self, n: int) -> bool:

        result = 0
        test = n

        result_set = set()

        while result != 1:

            digits = [int(d) for d in str(test)]

            sum_temp = 0
            for number in digits:
                sum_temp += (number ** 2)
                print(sum_temp)
            
            result = sum_temp
            test = result
            if (result in result_set):
                return False
            else:
                result_set.add(result)

            

        return True
