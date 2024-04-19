import collections
import re
from typing import Collection


class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        if not set(magazine).issuperset(set(ransomNote)):
            return False

        for i in set(ransomNote):
            if ransomNote.count(i) > magazine.count(i):
                return False

        return True


if __name__ == "__main__":
    r = input("Enter ransom note: ")
    m = input("Enter magazine: ")
    sol = Solution()
    print(sol.canConstruct(r, m))
