class RandomizedSet:

    def __init__(self):
        self.nums =[]
        self.value_to_index = {}

    def insert(self, val: int) -> bool:
        if val in self.value_to_index:
            return False
        
        self.value_to_index[val] = len(self.nums)
        self.nums.append(val)
        return True

    def remove(self, val: int) -> bool:
        if val not in self.value_to_index:
            return False
        
        removal_index = self.value_to_index[val]
        self.nums[removal_index] = self.nums[-1]

        self.value_to_index[self.nums[-1]] = removal_index

        self.nums.pop()
        del self.value_to_index[val]

        return True

    def getRandom(self) -> int:
        return random.choice(self.nums)


# Your RandomizedSet object will be instantiated and called as such:
# obj = RandomizedSet()
# param_1 = obj.insert(val)
# param_2 = obj.remove(val)
# param_3 = obj.getRandom()
