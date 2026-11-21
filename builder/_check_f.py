import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from problems_f import DATA

def ns(i):
    g = {}
    exec(DATA[i]["code"], g)
    return g["Solution"]()

assert ns(138).rob([1, 2, 3, 1]) == 4
assert ns(138).rob([2, 7, 9, 3, 1]) == 12
assert ns(139).wordBreak("leetcode", ["leet", "code"]) is True
assert ns(139).wordBreak("applepenapple", ["apple", "pen"]) is True
assert ns(139).wordBreak("catsandog", ["cats", "dog", "sand", "and", "cat"]) is False
assert ns(140).coinChange([1, 2, 5], 11) == 3
assert ns(140).coinChange([2], 3) == -1
assert ns(141).lengthOfLIS([10, 9, 2, 5, 3, 7, 101, 18]) == 4
assert ns(141).lengthOfLIS([7, 7, 7, 7, 7]) == 1
assert ns(142).minimumTotal([[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]]) == 11
assert ns(142).minimumTotal([[-10]]) == -10
assert ns(143).minPathSum([[1, 3, 1], [1, 5, 1], [4, 2, 1]]) == 7
assert ns(143).minPathSum([[1, 2, 3], [4, 5, 6]]) == 12
assert ns(144).uniquePathsWithObstacles([[0, 0, 0], [0, 1, 0], [0, 0, 0]]) == 2
assert ns(144).uniquePathsWithObstacles([[0, 1], [0, 0]]) == 1
assert ns(144).uniquePathsWithObstacles([[1]]) == 0
assert ns(145).longestPalindrome("babad") in ("bab", "aba")
assert ns(145).longestPalindrome("cbbd") == "bb"
assert ns(146).isInterleave("aabcc", "dbbca", "aadbbcbcac") is True
assert ns(146).isInterleave("aabcc", "dbbca", "aadbbbaccc") is False
assert ns(146).isInterleave("", "", "") is True
assert ns(147).minDistance("horse", "ros") == 3
assert ns(147).minDistance("intention", "execution") == 5
assert ns(148).maxProfit([3, 3, 5, 0, 0, 3, 1, 4]) == 6
assert ns(148).maxProfit([1, 2, 3, 4, 5]) == 4
assert ns(149).maxProfit(2, [2, 4, 1]) == 2
assert ns(149).maxProfit(2, [3, 2, 6, 5, 0, 3]) == 7
assert ns(150).maximalSquare([["1", "0", "1", "0", "0"], ["1", "0", "1", "1", "1"], ["1", "1", "1", "1", "1"], ["1", "0", "0", "1", "0"]]) == 4
assert ns(150).maximalSquare([["0", "1"], ["1", "0"]]) == 1
print("problems_f: all tests passed")
