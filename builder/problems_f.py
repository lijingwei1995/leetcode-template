# -*- coding: utf-8 -*-
"""题解数据 138-150：一维 / 多维动态规划。"""

DATA = {
    138: {
        "statement": "你是一个专业的小偷，计划偷窃沿街的房屋。每间房内的现金为非负整数，相邻房屋装有互相连通的防盗系统，如果两间相邻的房屋在同一晚被闯入，系统会自动报警。求在不触动报警的情况下，一晚能够偷窃到的最高金额。",
        "examples": [
            {"input": "nums = [1,2,3,1]", "output": "4"},
            {"input": "nums = [2,7,9,3,1]", "output": "12"},
        ],
        "approach": "每个房屋只有“偷”与“不偷”两种选择，且只与前两间房的状态有关，是线性 DP 的信号。dp[i] 表示前 i 间房的最大金额：不偷第 i 间为 dp[i-1]，偷则为 dp[i-2]+nums[i]。变化点在于用两个滚动变量保存前两项，省掉数组。",
        "code": """class Solution:
    def rob(self, nums):
        prev, cur = 0, 0
        for x in nums:
            prev, cur = cur, max(cur, prev + x)   # 变化点: 偷当前房要跳过前一间
        return cur""",
        "time": "O(n)",
        "space": "O(1)",
        "pitfalls": [
            "prev 与 cur 的更新必须同时完成，否则会用到已覆盖的值",
            "只有一间房时答案就是它本身，空数组返回 0",
            "金额非负，但不要假设一定能偷到所有正数房屋",
        ],
    },
    139: {
        "statement": "给定字符串 s 和字符串列表 wordDict 作为字典，判断 s 是否可以被空格拆分为一个或多个字典中出现的单词。字典中的单词可以重复使用。",
        "examples": [
            {"input": "s = \"leetcode\", wordDict = [\"leet\",\"code\"]", "output": "true"},
            {"input": "s = \"applepenapple\", wordDict = [\"apple\",\"pen\"]", "output": "true"},
        ],
        "approach": "问题可以拆成“前 i 个字符是否可拆分”的子问题，是布尔型完全背包。dp[i] 为真表示前缀 s[:i] 可拆分；枚举最后一段的起点 j，只要 dp[j] 为真且 s[j:i] 在字典中，dp[i] 就为真。变化点在于内层枚举的是“最后一段”的起点。",
        "code": """class Solution:
    def wordBreak(self, s, wordDict):
        words = set(wordDict)
        n = len(s)
        dp = [False] * (n + 1)
        dp[0] = True
        for i in range(1, n + 1):
            for j in range(i):                      # 变化点: 枚举最后一段的起点
                if dp[j] and s[j:i] in words:
                    dp[i] = True
                    break
        return dp[n]""",
        "time": "O(n²)（子串比较另计）",
        "space": "O(n)",
        "pitfalls": [
            "dp[0] 必须为 True，表示空前缀天然可拆分",
            "单词可以重复使用，不需要 used 数组",
            "字典要转成 set，否则 in 查询会退化",
        ],
    },
    140: {
        "statement": "给定不同面额的硬币 coins 和总金额 amount，计算凑成总金额所需的最少硬币个数。如果没有任何组合能凑成该金额，返回 -1。每种硬币的数量是无限的。",
        "examples": [
            {"input": "coins = [1,2,5], amount = 11", "output": "3"},
            {"input": "coins = [2], amount = 3", "output": "-1"},
        ],
        "approach": "每种硬币可用无限次，是典型的完全背包求最小值。dp[j] 表示凑出金额 j 的最少硬币数，转移为 dp[j] = min(dp[j], dp[j-coin]+1)。变化点在于容量正序遍历以允许重复使用硬币，以及用 amount+1 代替无穷大避免溢出。",
        "code": """class Solution:
    def coinChange(self, coins, amount):
        INF = amount + 1
        dp = [INF] * (amount + 1)
        dp[0] = 0
        for coin in coins:
            for j in range(coin, amount + 1):        # 变化点: 完全背包正序遍历
                dp[j] = min(dp[j], dp[j - coin] + 1)
        return -1 if dp[amount] == INF else dp[amount]""",
        "time": "O(amount × 硬币种数)",
        "space": "O(amount)",
        "pitfalls": [
            "dp 其余位置要初始化为无穷大，不能初始化为 0",
            "金额为 0 时答案是 0，不是 -1",
            "容量必须正序遍历，倒序会退化成 0-1 背包",
        ],
    },
    141: {
        "statement": "给定整数数组 nums，找到其中最长严格递增子序列的长度。子序列由数组派生而来，删除（或不删除）元素而不改变其余元素顺序。",
        "examples": [
            {"input": "nums = [10,9,2,5,3,7,101,18]", "output": "4"},
            {"input": "nums = [7,7,7,7,7]", "output": "1"},
        ],
        "approach": "“以第 i 个元素结尾的最长递增子序列”只依赖更小的下标，适合线性 DP。dp[i] 表示以 nums[i] 结尾的 LIS 长度，内层枚举 j < i 且 nums[j] < nums[i] 转移。变化点在于答案不是 dp[n-1]，而是所有 dp[i] 的最大值。",
        "code": """class Solution:
    def lengthOfLIS(self, nums):
        if not nums:
            return 0
        dp = [1] * len(nums)
        for i in range(len(nums)):
            for j in range(i):                       # 变化点: 只从更小的前驱转移
                if nums[j] < nums[i]:
                    dp[i] = max(dp[i], dp[j] + 1)
        return max(dp)""",
        "time": "O(n²)",
        "space": "O(n)",
        "pitfalls": [
            "要求严格递增，判断必须是 nums[j] < nums[i] 而不是 <=",
            "答案是 max(dp)，不是 dp[-1]",
            "可用贪心 + 二分把时间复杂度优化到 O(n log n)",
        ],
    },
    142: {
        "statement": "给定一个三角形 triangle，找出自顶向下的最小路径和。每一步只能移动到下一行中相邻的结点上，即从 (i,j) 只能移到 (i+1,j) 或 (i+1,j+1)。",
        "examples": [
            {"input": "triangle = [[2],[3,4],[6,5,7],[4,1,8,3]]", "output": "11"},
            {"input": "triangle = [[-10]]", "output": "-10"},
        ],
        "approach": "路径只能向下且相邻，状态落在三角形的每个位置，是网格 DP 的变体。自底向上更简单：dp[j] 表示从底层走到当前层第 j 个位置的最小和，转移为当前值加上下一层相邻两格的最小值。变化点在于遍历方向与相邻下标。",
        "code": """class Solution:
    def minimumTotal(self, triangle):
        dp = triangle[-1][:]
        for i in range(len(triangle) - 2, -1, -1):   # 变化点: 自底向上
            for j in range(len(triangle[i])):
                dp[j] = triangle[i][j] + min(dp[j], dp[j + 1])
        return dp[0]""",
        "time": "O(n²)",
        "space": "O(n)",
        "pitfalls": [
            "自顶向下需要处理边界，自底向上无需特判",
            "若自底向上，dp 初始化为最后一行而不是第一行",
            "相邻位置是下一层的 j 与 j+1",
        ],
    },
    143: {
        "statement": "给定一个包含非负整数的 m × n 网格 grid，请找出一条从左上角到右下角的路径，使得路径上的数字总和为最小。每次只能向下或者向右移动一步。",
        "examples": [
            {"input": "grid = [[1,3,1],[1,5,1],[4,2,1]]", "output": "7"},
            {"input": "grid = [[1,2,3],[4,5,6]]", "output": "12"},
        ],
        "approach": "只能向右或向下，说明每个格子的最优值只来自上方或左方，是标准网格 DP。用一维滚动数组：dp[j] 在更新前代表上方，dp[j-1] 代表左方。变化点在于第一行与第一列的初始化，以及原地复用数组。",
        "code": """class Solution:
    def minPathSum(self, grid):
        m, n = len(grid), len(grid[0])
        dp = [0] * n
        dp[0] = grid[0][0]
        for j in range(1, n):
            dp[j] = dp[j - 1] + grid[0][j]           # 变化点: 第一行只能从左边来
        for i in range(1, m):
            dp[0] += grid[i][0]                      # 变化点: 第一列只能从上边来
            for j in range(1, n):
                dp[j] = min(dp[j], dp[j - 1]) + grid[i][j]
        return dp[-1]""",
        "time": "O(mn)",
        "space": "O(n)",
        "pitfalls": [
            "第一行与第一列没有两个方向可选，必须单独初始化",
            "更新 dp[j] 时，它尚未被覆盖，代表的是上一行同列的值",
            "m 或 n 为 1 时仍要正确返回路径和",
        ],
    },
    144: {
        "statement": "一个机器人位于 m × n 网格的左上角，每次只能向下或向右移动一步。网格中有障碍物（1 表示障碍，0 表示空位），求从左上角到右下角的不同路径数。",
        "examples": [
            {"input": "obstacleGrid = [[0,0,0],[0,1,0],[0,0,0]]", "output": "2"},
            {"input": "obstacleGrid = [[0,1],[0,0]]", "output": "1"},
        ],
        "approach": "没有障碍时是组合数 / 网格 DP；有障碍后只需把障碍格的方案数置 0。dp[j] 滚动表示到达当前行第 j 列的不同路径数，转移为上方 dp[j] 加左方 dp[j-1]。变化点在于障碍判断与起点障碍。",
        "code": """class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid):
        n = len(obstacleGrid[0])
        dp = [0] * n
        dp[0] = 1 if obstacleGrid[0][0] == 0 else 0
        for i in range(len(obstacleGrid)):
            for j in range(n):
                if obstacleGrid[i][j] == 1:
                    dp[j] = 0                       # 变化点: 障碍格方案清零
                elif j > 0:
                    dp[j] += dp[j - 1]              # 变化点: 累加左方方案
        return dp[-1]""",
        "time": "O(mn)",
        "space": "O(n)",
        "pitfalls": [
            "起点或终点有障碍时直接无解，代码需能自然处理",
            "第一行某个障碍之后的格子方案数都应为 0",
            "dp[j] += dp[j-1] 依赖本行已更新的左邻格，遍历顺序不能反",
        ],
    },
    145: {
        "statement": "给定一个字符串 s，找到 s 中最长的回文子串。如果存在多个长度相同的答案，返回任意一个即可。",
        "examples": [
            {"input": "s = \"babad\"", "output": "\"bab\"（或 \"aba\"）"},
            {"input": "s = \"cbbd\"", "output": "\"bb\""},
        ],
        "approach": "回文可以看成“首尾字符相同，且内部子串也是回文”，适合区间 DP。dp[i][j] 表示 s[i:j+1] 是否回文，转移依赖 dp[i+1][j-1]，因此 i 必须从后往前遍历。变化点在于长度小于 2 的区间直接为真。",
        "code": """class Solution:
    def longestPalindrome(self, s):
        n = len(s)
        dp = [[False] * n for _ in range(n)]
        start, best = 0, 1
        for i in range(n - 1, -1, -1):
            for j in range(i, n):
                if s[i] == s[j] and (j - i < 2 or dp[i + 1][j - 1]):  # 变化点: 单字符或内部回文
                    dp[i][j] = True
                    if j - i + 1 > best:
                        best = j - i + 1
                        start = i
        return s[start:start + best]""",
        "time": "O(n²)",
        "space": "O(n²)",
        "pitfalls": [
            "i 必须从后往前遍历，否则 dp[i+1][j-1] 还没计算",
            "长度为 1 和 2 的子串要特殊判断，避免访问越界",
            "中心扩展法可用 O(1) 空间达到同样复杂度",
        ],
    },
    146: {
        "statement": "给定三个字符串 s1、s2 和 s3，判断 s3 是否由 s1 和 s2 交错组成。交错的定义是 s1 和 s2 的字符按原顺序交替出现，但同一字符串内部字符的相对顺序不能改变。",
        "examples": [
            {"input": "s1 = \"aabcc\", s2 = \"dbbca\", s3 = \"aadbbcbcac\"", "output": "true"},
            {"input": "s1 = \"aabcc\", s2 = \"dbbca\", s3 = \"aadbbbaccc\"", "output": "false"},
        ],
        "approach": "s3 的每个前缀都由 s1 的某个前缀和 s2 的某个前缀拼成，状态是二维的，但可以滚动成一维。dp[j] 表示用 s1 的前 i 个字符和 s2 的前 j 个字符能否拼出 s3 的前 i+j 个字符。变化点在于当前字符既可能来自 s1，也可能来自 s2。",
        "code": """class Solution:
    def isInterleave(self, s1, s2, s3):
        m, n = len(s1), len(s2)
        if m + n != len(s3):
            return False
        dp = [False] * (n + 1)
        dp[0] = True
        for j in range(1, n + 1):
            dp[j] = dp[j - 1] and s2[j - 1] == s3[j - 1]   # 变化点: 只取 s2 的前缀
        for i in range(1, m + 1):
            dp[0] = dp[0] and s1[i - 1] == s3[i - 1]
            for j in range(1, n + 1):
                from_s1 = dp[j] and s1[i - 1] == s3[i + j - 1]
                from_s2 = dp[j - 1] and s2[j - 1] == s3[i + j - 1]
                dp[j] = from_s1 or from_s2              # 变化点: 两个来源任一可达
        return dp[n]""",
        "time": "O(mn)",
        "space": "O(n)",
        "pitfalls": [
            "先判断长度，长度不匹配直接返回 False",
            "滚动数组中 dp[j] 更新前代表上一行，dp[j-1] 代表当前行左邻",
            "s1 或 s2 为空时，另一个必须与 s3 完全相同",
        ],
    },
    147: {
        "statement": "给你两个单词 word1 和 word2，请返回将 word1 转换成 word2 所使用的最少操作数。允许的操作有插入一个字符、删除一个字符、替换一个字符。",
        "examples": [
            {"input": "word1 = \"horse\", word2 = \"ros\"", "output": "3"},
            {"input": "word1 = \"intention\", word2 = \"execution\"", "output": "5"},
        ],
        "approach": "两个字符串的前缀之间的编辑距离只依赖更短前缀，是经典字符串 DP。dp[i][j] 表示 word1 前 i 个字符转成 word2 前 j 个字符的最少操作数：末字符相同则继承左上，否则在删、增、替换中取最小加一。变化点在于滚动数组保存左上角。",
        "code": """class Solution:
    def minDistance(self, word1, word2):
        m, n = len(word1), len(word2)
        dp = list(range(n + 1))
        for i in range(1, m + 1):
            prev = dp[0]
            dp[0] = i
            for j in range(1, n + 1):
                temp = dp[j]
                if word1[i - 1] == word2[j - 1]:
                    dp[j] = prev                        # 变化点: 末字符相同，无需操作
                else:
                    dp[j] = min(dp[j], dp[j - 1], prev) + 1  # 变化点: 删 / 增 / 替换
                prev = temp
        return dp[n]""",
        "time": "O(mn)",
        "space": "O(n)",
        "pitfalls": [
            "dp[0] 要初始化为 i，表示把前 i 个字符全部删除",
            "prev 必须在覆盖 dp[j] 之前保存，它代表左上角",
            "两个空串的编辑距离为 0",
        ],
    },
    148: {
        "statement": "给定一个数组 prices，它的第 i 个元素是一支给定股票第 i 天的价格。你最多可以完成两笔交易（买一次卖一次算一笔），但不能同时持有多笔股票。求能获得的最大利润。",
        "examples": [
            {"input": "prices = [3,3,5,0,0,3,1,4]", "output": "6"},
            {"input": "prices = [1,2,3,4,5]", "output": "4"},
        ],
        "approach": "每天只关心“第几次买入 / 卖出后”的收益，是股票状态机 DP。用 buy1、sell1、buy2、sell2 四个状态滚动：第二次买入要使用第一次卖出后的利润。变化点在于交易次数的顺序不能颠倒。",
        "code": """class Solution:
    def maxProfit(self, prices):
        buy1 = buy2 = -float('inf')
        sell1 = sell2 = 0
        for p in prices:
            buy1 = max(buy1, -p)                 # 变化点: 第一次买入
            sell1 = max(sell1, buy1 + p)         # 变化点: 第一次卖出
            buy2 = max(buy2, sell1 - p)          # 变化点: 第二次买入使用第一次利润
            sell2 = max(sell2, buy2 + p)
        return sell2""",
        "time": "O(n)",
        "space": "O(1)",
        "pitfalls": [
            "buy 状态初始化为负无穷，sell 初始化为 0",
            "更新顺序必须是 buy1 → sell1 → buy2 → sell2",
            "最多两笔交易，可以少于两笔，sell2 天然包含这种情况",
        ],
    },
    149: {
        "statement": "给定数组 prices 和整数 k，其中 prices[i] 是某支股票第 i 天的价格。你最多可以完成 k 笔交易，求能获得的最大利润。注意不能同时参与多笔交易。",
        "examples": [
            {"input": "k = 2, prices = [2,4,1]", "output": "2"},
            {"input": "k = 2, prices = [3,2,6,5,0,3]", "output": "7"},
        ],
        "approach": "在股票状态机 DP 上增加交易次数维度：buy[j] 表示最多 j 笔交易时持股的最大收益，sell[j] 表示不持股。每天先更新买入再更新卖出。变化点在于 k 很大时，k 超过 n/2 会退化为无限次交易，需单独处理避免超时。",
        "code": """class Solution:
    def maxProfit(self, k, prices):
        if not prices or k == 0:
            return 0
        n = len(prices)
        if k >= n // 2:                       # 变化点: 次数足够多，退化为无限次交易
            return sum(max(0, prices[i] - prices[i - 1]) for i in range(1, n))
        buy = [-float('inf')] * (k + 1)
        sell = [0] * (k + 1)
        for p in prices:
            for j in range(1, k + 1):         # 变化点: 枚举交易次数
                buy[j] = max(buy[j], sell[j - 1] - p)
                sell[j] = max(sell[j], buy[j] + p)
        return sell[k]""",
        "time": "O(nk)（k 过大时 O(n)）",
        "space": "O(k)",
        "pitfalls": [
            "k 大于等于 n/2 时应走无限次交易的贪心分支",
            "buy 数组初始化为负无穷，sell 初始化为 0",
            "第二次买入要基于 sell[j-1]，不是 sell[j]",
        ],
    },
    150: {
        "statement": "在一个由 '0' 和 '1' 组成的二维矩阵内，找到只包含 '1' 的最大正方形，并返回其面积。",
        "examples": [
            {"input": "matrix = [[\"1\",\"0\",\"1\",\"0\",\"0\"],[\"1\",\"0\",\"1\",\"1\",\"1\"],[\"1\",\"1\",\"1\",\"1\",\"1\"],[\"1\",\"0\",\"0\",\"1\",\"0\"]]", "output": "4"},
            {"input": "matrix = [[\"0\",\"1\"],[\"1\",\"0\"]]", "output": "1"},
        ],
        "approach": "以 (i,j) 为右下角的最大正方形边长，取决于左、上、左上三个位置的最小值加一，是网格 DP。用一维滚动数组时用 prev 保存左上角。变化点在于输入是字符 '1'，以及返回的是面积而不是边长。",
        "code": """class Solution:
    def maximalSquare(self, matrix):
        m, n = len(matrix), len(matrix[0])
        dp = [0] * (n + 1)
        best = 0
        for i in range(1, m + 1):
            prev = 0
            for j in range(1, n + 1):
                temp = dp[j]
                if matrix[i - 1][j - 1] == '1':
                    dp[j] = min(dp[j], dp[j - 1], prev) + 1   # 变化点: 左 / 上 / 左上取最小再加一
                    best = max(best, dp[j])
                else:
                    dp[j] = 0                                  # 变化点: 遇到 0 归零
                prev = temp
        return best * best""",
        "time": "O(mn)",
        "space": "O(n)",
        "pitfalls": [
            "matrix 的元素是字符 '1'，不是整数 1",
            "prev 保存的是左上角的值，必须在覆盖前取出",
            "最终返回 best * best（面积），不是边长",
        ],
    },
}
