from collections import defaultdict

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        grouping = defaultdict(list)

        for string in strs:
            sorted_key = "".join(sorted(string))

            grouping[sorted_key].append(string)

        return list(grouping.values())
