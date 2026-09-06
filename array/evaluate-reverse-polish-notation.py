class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        OPERANDS = ['+', '-', '*', '/']
        stack = []

        def evaluate(num1: int, op: str, num2: int) -> int:
            if (op == '+'):
                return num1 + num2
            elif (op == '-'):
                return num1 - num2
            elif (op == '*'):
                return num1 * num2
            else :
                return int(num1 / num2)


        for i in tokens:
            if i not in OPERANDS:
                #numbers
                stack.append(int(i))
            else:
                #operations
                second_n = stack.pop()
                first_n = stack.pop()

                result = evaluate(first_n, i, second_n)
    
                stack.append(result)
        return stack.pop()
        
