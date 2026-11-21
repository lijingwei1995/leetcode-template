# -*- coding: utf-8 -*-
"""题解数据 1-33：数组 / 字符串、双指针、滑动窗口。"""

DATA = {
    1: {
        "statement": "给你两个按非递减顺序排列的整数数组 nums1 和 nums2，另有两个整数 m 和 n，分别表示它们中的元素数目。请你把 nums2 合并到 nums1 中，使合并后的数组同样按非递减顺序排列。最终结果不返回而是存放在 nums1 中：nums1 的初始长度为 m + n，前 m 个元素是待合并的值，后 n 个位置为 0。",
        "examples": [
            {"input": "nums1 = [1,2,3,0,0,0], m = 3, nums2 = [2,5,6], n = 3", "output": "[1,2,2,3,5,6]"},
            {"input": "nums1 = [1], m = 1, nums2 = [], n = 0", "output": "[1]"},
        ],
        "approach": "两个数组都已有序、要把 nums2 并入 nums1，是对撞双指针的信号：从后往前比较两个有效尾部，把较大者放到写入位，避免覆盖 nums1 中尚未比较的元素。三个指针 i、j、k 分别从 m-1、n-1、m+n-1 起步。变化点在于指针从尾部向前推进，以及循环结束后 nums2 若有剩余还要继续拷入。",
        "code": """class Solution:
    def merge(self, nums1, m, nums2, n):
        i, j, k = m - 1, n - 1, m + n - 1      # 变化点: 三个指针都从尾部起步，避免覆盖未比较元素
        while i >= 0 and j >= 0:
            if nums1[i] > nums2[j]:
                nums1[k] = nums1[i]
                i -= 1
            else:
                nums1[k] = nums2[j]
                j -= 1
            k -= 1
        while j >= 0:                           # 变化点: nums2 剩余元素继续拷入，nums1 剩余已在原位
            nums1[k] = nums2[j]
            j -= 1
            k -= 1""",
        "time": "O(m+n)",
        "space": "O(1)",
        "pitfalls": [
            "从前往后合并会覆盖 nums1 未比较的元素，必须从后往前写",
            "两个出口都要考虑：nums1 先用完时要把 nums2 剩余拷入，nums2 先用完则无需处理",
            "k 的初值是 m + n - 1，不是 len(nums1) - 1 之外的任意位置",
        ],
    },
    2: {
        "statement": "给你一个数组 nums 和一个值 val，你需要原地移除所有数值等于 val 的元素，并返回移除后数组的新长度。元素的顺序可以改变，你不需要考虑数组中超出新长度后面的元素。",
        "examples": [
            {"input": "nums = [3,2,2,3], val = 3", "output": "2, nums 前缀 = [2,2]"},
            {"input": "nums = [0,1,2,2,3,0,4,2], val = 2", "output": "5, nums 前缀 = [0,1,3,0,4]"},
        ],
        "approach": "要求原地删除且 O(1) 空间，是同向读写双指针的信号：read 指针扫描全部元素，write 指向下一个可写位置。nums[read] != val 时把 read 处的值写到 write 并让 write 前移。变化点只在保留条件——不等于 val 的元素全部留下，扫描结束时 write 就是新长度。",
        "code": """class Solution:
    def removeElement(self, nums, val):
        write = 0
        for read in range(len(nums)):
            if nums[read] != val:               # 变化点: 保留条件为不等于 val
                nums[write] = nums[read]
                write += 1
        return write""",
        "time": "O(n)",
        "space": "O(1)",
        "pitfalls": [
            "write 起点是 0，别初始化成 1，首个元素也可能被保留",
            "返回值是 write（新长度），不是 len(nums) 或 write + 1",
            "题目允许改变元素顺序，所以不需要交换，直接覆盖即可",
        ],
    },
    3: {
        "statement": "给你一个升序排列的数组 nums，请你原地删除重复出现的元素，使每个元素只出现一次，返回删除后数组的新长度。必须保持元素的相对顺序一致，返回后 nums 的前 k 个位置应恰好是去重后的结果。",
        "examples": [
            {"input": "nums = [1,1,2]", "output": "2, nums 前缀 = [1,2]"},
            {"input": "nums = [0,0,1,1,1,2,2,3,3,4]", "output": "5, nums 前缀 = [0,1,2,3,4]"},
        ],
        "approach": "升序数组去重且要保持相对顺序，同向读写双指针信号：write 始终指向已保留部分的末尾。nums[read] 与上一个保留值 nums[write-1] 不同时才写入。变化点在于比较对象从 val 换成“上一个保留值”，且首个元素无条件保留、write 从 1 起步。",
        "code": """class Solution:
    def removeDuplicates(self, nums):
        write = 1                               # 变化点: 首个元素必保留，write 从 1 起步
        for read in range(1, len(nums)):
            if nums[read] != nums[write - 1]:   # 变化点: 与上一个保留值比较，而不是与上一个原始值
                nums[write] = nums[read]
                write += 1
        return write""",
        "time": "O(n)",
        "space": "O(1)",
        "pitfalls": [
            "比较对象是 nums[write-1]（上一个保留值），写成 nums[read-1] 会把中间的重复也误判",
            "write 从 1 起步隐含数组非空，题目保证 1 <= len(nums)，不必额外判空",
            "超出 write 的尾部元素不用清理，题目只校验前 k 个位置",
        ],
    },
    4: {
        "statement": "给你一个升序排列的数组 nums，请你原地删除重复出现的元素，使得每个元素最多出现两次，返回删除后数组的新长度。保持相对顺序，前 k 个位置应保留每个元素最多两次的结果。",
        "examples": [
            {"input": "nums = [1,1,1,2,2,3]", "output": "5, nums 前缀 = [1,1,2,2,3]"},
            {"input": "nums = [0,0,1,1,1,1,2,3,3]", "output": "7, nums 前缀 = [0,0,1,1,2,3,3]"},
        ],
        "approach": "每个元素最多保留两次，仍是同向读写双指针：把保留条件从“与上一个保留值不同”放宽为“与上上个保留值不同”即可。write-2 位置保存的正是再往前第二个保留值。变化点在于比较 nums[write-2]，以及前两个元素必保留、write 从 2 起步。",
        "code": """class Solution:
    def removeDuplicates(self, nums):
        if len(nums) <= 2:
            return len(nums)
        write = 2                               # 变化点: 前两个元素必保留，write 从 2 起步
        for read in range(2, len(nums)):
            if nums[read] != nums[write - 2]:   # 变化点: 与上上个保留值比较，允许每个值出现两次
                nums[write] = nums[read]
                write += 1
        return write""",
        "time": "O(n)",
        "space": "O(1)",
        "pitfalls": [
            "比较对象是 nums[write-2]，错写成 nums[write-1] 会退化成每个元素只保留一次",
            "write < 2 时 write-2 下标为负会从尾部取值，长度 ≤ 2 必须先特判",
            "不能只统计次数不写回，题目要求保留结果落在数组前缀上",
        ],
    },
    5: {
        "statement": "给定一个大小为 n 的数组 nums，返回其中的多数元素。多数元素是指在数组中出现次数大于 n/2 的元素。你可以假设数组非空，且给定的数组总是存在多数元素。",
        "examples": [
            {"input": "nums = [3,2,3]", "output": "3"},
            {"input": "nums = [2,2,1,1,1,2,2]", "output": "2"},
        ],
        "approach": "求出现次数超过一半的元素，计数信号：用哈希表逐个累加每个值的出现次数。一旦某值次数超过 n//2，它就是多数元素。变化点在于边计数边检查、命中提前返回，不必等全部统计完成。",
        "code": """class Solution:
    def majorityElement(self, nums):
        freq = {}
        half = len(nums) // 2
        for x in nums:
            freq[x] = freq.get(x, 0) + 1
            if freq[x] > half:                  # 变化点: 边计数边检查，命中提前返回
                return x
        return -1""",
        "time": "O(n)",
        "space": "O(n)",
        "pitfalls": [
            "阈值是严格大于 n//2，不是大于等于",
            "题目保证多数元素必存在，末尾 return -1 只是语法兜底，不会执行",
            "若额外要求 O(1) 空间可改 Boyer–Moore 投票法，计数法空间是 O(n)",
        ],
    },
    6: {
        "statement": "给定一个整数数组 nums，将数组中的元素向右轮转 k 个位置，其中 k 是非负数。要求使用空间复杂度为 O(1) 的原地算法，不返回任何值。",
        "examples": [
            {"input": "nums = [1,2,3,4,5,6,7], k = 3", "output": "[5,6,7,1,2,3,4]"},
            {"input": "nums = [-1,-100,3,99], k = 2", "output": "[3,99,-1,-100]"},
        ],
        "approach": "要求 O(1) 空间原地轮转，信号是“三次反转”：先整体反转，再分别反转前 k 段与后 n-k 段，反转内部用对撞双指针左右交换。变化点在于 k 要先对 n 取模防止越界，以及两段反转的区间边界 [0,k-1] 与 [k,n-1]。",
        "code": """class Solution:
    def rotate(self, nums, k):
        n = len(nums)
        k %= n                                  # 变化点: k 可能大于 n，先取模
        def reverse(l, r):
            while l < r:
                nums[l], nums[r] = nums[r], nums[l]
                l += 1
                r -= 1
        reverse(0, n - 1)                       # 变化点: 先整体反转，再反转前 k 与后 n-k 两段
        reverse(0, k - 1)
        reverse(k, n - 1)""",
        "time": "O(n)",
        "space": "O(1)",
        "pitfalls": [
            "k 必须先对 n 取模，否则 k > n 时反转区间下标越界",
            "反转顺序不能乱：先整体、再前段、再后段，顺序错了结果不是右轮转",
            "k % n == 0 时三次反转互相抵消，是自然的空操作，不用特判",
        ],
    },
    7: {
        "statement": "给定一个数组 prices，它的第 i 个元素表示某支股票第 i 天的价格。你只能选择某一天买入，并在未来的某一天卖出。返回你能获得的最大利润；若无法获利则返回 0。",
        "examples": [
            {"input": "prices = [7,1,5,3,6,4]", "output": "5"},
            {"input": "prices = [7,6,4,3,1]", "output": "0"},
        ],
        "approach": "只允许一次交易，卖出日在 i 的最大利润只依赖之前日期的最低买入价，这是前缀分解信号：维护“到当前天为止的最低价”这个前缀量。每日用 price - min_price 尝试更新答案。变化点在于前缀量是滚动最小值，先更新 best 再刷新 min_price，保证卖出在买入之后。",
        "code": """class Solution:
    def maxProfit(self, prices):
        best = 0
        min_price = prices[0]
        for price in prices[1:]:
            best = max(best, price - min_price)     # 变化点: 当前价减去前缀最低价
            min_price = min(min_price, price)       # 变化点: 前缀最低价随扫描滚动更新
        return best""",
        "time": "O(n)",
        "space": "O(1)",
        "pitfalls": [
            "减数必须是“之前日期的最低价”，先更新 best 再更新 min_price 顺序不能颠倒",
            "价格一路下跌时最大利润是 0，不是负数，best 初值要设 0",
            "min_price 初值用 prices[0]，设成 0 会把“白送股票”当成合法买入",
        ],
    },
    8: {
        "statement": "给你一个整数数组 prices，其中 prices[i] 表示某支股票第 i 天的价格。每一天你可以决定是否买入或出售股票，任意一天最多只能持有一股，也可以先卖出再买入。返回你能获得的最大利润。",
        "examples": [
            {"input": "prices = [7,1,5,3,6,4]", "output": "7"},
            {"input": "prices = [1,2,3,4,5]", "output": "4"},
        ],
        "approach": "允许多次交易时，任何一段上涨区间的收益都能完整拿到，线性贪心信号：只需收集所有相邻两天的正差值。prices[i] > prices[i-1] 时把差值计入利润，下跌段直接跳过。变化点在于贪心对象是相邻差值，而不是像 I 题那样维护最低价模拟单次买卖。",
        "code": """class Solution:
    def maxProfit(self, prices):
        profit = 0
        for i in range(1, len(prices)):
            if prices[i] > prices[i - 1]:
                profit += prices[i] - prices[i - 1]     # 变化点: 收集每一段相邻上涨的差值
        return profit""",
        "time": "O(n)",
        "space": "O(1)",
        "pitfalls": [
            "只有相邻上涨才累加，把下跌差值也加进去会得到错误利润",
            "本题与 I 不同允许多次交易，不能沿用“维护最低价、只卖一次”的思路",
            "差值拆分与整段持有等价，无需真的模拟买入卖出操作",
        ],
    },
    9: {
        "statement": "给你一个非负整数数组 nums，你最初位于数组的第一个下标。数组中每个元素代表你在该位置可以跳跃的最大长度。判断你是否能够到达最后一个下标，如果能返回 true，否则返回 false。",
        "examples": [
            {"input": "nums = [2,3,1,1,4]", "output": "true"},
            {"input": "nums = [3,2,1,0,4]", "output": "false"},
        ],
        "approach": "能否到达终点只取决于“当前位置之前能跳到的最远下标”，线性贪心信号：从左到右扫描，维护 farthest = max(farthest, i + nums[i])。一旦 i 超出 farthest，说明链条断裂、无法继续前进。变化点在于扫描只需到倒数第二个位置，且 i > farthest 时立即返回 False。",
        "code": """class Solution:
    def canJump(self, nums):
        farthest = 0
        for i in range(len(nums) - 1):          # 变化点: 只扫到倒数第二个位置即可判定
            if i > farthest:                    # 变化点: 当前位置已不可达，链条断裂
                return False
            farthest = max(farthest, i + nums[i])
        return farthest >= len(nums) - 1""",
        "time": "O(n)",
        "space": "O(1)",
        "pitfalls": [
            "扫描到 len(nums)-2 即可，扫到最后一个位置反而容易把“恰好停住”误处理",
            "i > farthest 必须提前返回 False，继续更新会把不可达位置的跳跃范围混进来",
            "单元素数组 range(0) 不进循环，farthest = 0 >= 0 返回 True，天然正确",
        ],
    },
    10: {
        "statement": "给定一个长度为 n 的 0 索引整数数组 nums，初始位置为 nums[0]，每个元素代表在该位置可以跳跃的最大长度。你的目标是到达最后一个下标，返回到达它所需的最少跳跃次数。测试用例保证可以到达。",
        "examples": [
            {"input": "nums = [2,3,1,1,4]", "output": "2"},
            {"input": "nums = [2,3,0,1,4]", "output": "2"},
        ],
        "approach": "最少跳跃次数可按“每一跳覆盖的区间”分层，线性贪心信号：扫描时维护本层边界 end 与可达最远 farthest，走到边界就必须再跳一步，并把边界更新为 farthest。变化点在于“到达边界即步数加一”的时机（先更新 farthest 再计数），以及扫描停在倒数第二个位置避免多计一步。",
        "code": """class Solution:
    def jump(self, nums):
        steps, end, farthest = 0, 0, 0
        for i in range(len(nums) - 1):          # 变化点: 停在倒数第二个位置，避免终点多计一步
            farthest = max(farthest, i + nums[i])
            if i == end:                        # 变化点: 走到本层边界，必须再跳一次
                steps += 1
                end = farthest
        return steps""",
        "time": "O(n)",
        "space": "O(1)",
        "pitfalls": [
            "先更新 farthest 再判断 i == end，顺序反了会把旧边界当成新边界",
            "扫描只到 len(nums)-2，扫到终点会在最后一层多计一次跳跃",
            "题目保证可达，无需处理“end == i 且 farthest 不再前进”的死局场景",
        ],
    },
    11: {
        "statement": "给你一个整数数组 citations，其中 citations[i] 表示研究者的第 i 篇论文被引用的次数。计算并返回该研究者的 h 指数：h 代表“高引用次数”，即至少有 h 篇论文分别被引用了至少 h 次。",
        "examples": [
            {"input": "citations = [3,0,6,1,5]", "output": "3"},
            {"input": "citations = [1,3,1]", "output": "1"},
        ],
        "approach": "h 不可能超过论文总数 n，计数信号：把引用次数截断到 n，用长度 n+1 的桶统计每档引用的篇数。从高到低累加“引用至少 h 次的篇数”，首次满足 total >= h 的 h 就是答案。变化点在于超过 n 的引用统一并入最高桶，以及倒序累加时的判定条件是 total >= h。",
        "code": """class Solution:
    def hIndex(self, citations):
        n = len(citations)
        buckets = [0] * (n + 1)
        for c in citations:
            buckets[min(c, n)] += 1             # 变化点: 引用超过 n 的并入最高桶
        total = 0
        for h in range(n, 0, -1):               # 变化点: 从高到低累加“引用至少 h 次”的篇数
            total += buckets[h]
            if total >= h:
                return h
        return 0""",
        "time": "O(n)",
        "space": "O(n)",
        "pitfalls": [
            "引用次数要先 min(c, n) 截断，否则桶下标越界",
            "判定条件是 total >= h（篇数不少于引用数），写反方向会返回偏大的 h",
            "也可以排序后从大到小扫描，但计数桶法无需排序，时间 O(n)",
        ],
    },
    12: {
        "statement": "实现 RandomizedSet 类：insert(val) 在元素不存在时向集合中插入该项并返回 true，否则返回 false；remove(val) 在元素存在时移除该项并返回 true，否则返回 false；getRandom() 等概率随机返回集合中的任意一项。要求每个函数的平均时间复杂度为 O(1)。集合中每个元素最多出现一次。",
        "examples": [
            {"input": "insert(1)、remove(2)、insert(2)、getRandom()", "output": "true / false / true / 2（集合内为 [1,2]，各以 1/2 概率返回）"},
            {"input": "remove(1)、insert(2)、getRandom()", "output": "true / false / 2"},
        ],
        "approach": "要在 O(1) 内完成插入、删除与等概率随机取值，是“哈希映射 + 动态数组”的设计信号：字典负责 O(1) 定位，数组负责 O(1) 随机下标。删除时用尾元素覆盖被删位置再 pop，避免数组整体搬移。变化点在于“字典存值到下标映射 + 尾部覆盖删除”的组合，以及 getRandom 直接随机数组下标。",
        "code": """import random

class RandomizedSet:
    def __init__(self):
        self.vals = []
        self.pos = {}                           # 变化点: 哈希表存“值 -> 数组下标”

    def insert(self, val):
        if val in self.pos:
            return False
        self.pos[val] = len(self.vals)
        self.vals.append(val)
        return True

    def remove(self, val):
        if val not in self.pos:
            return False
        i = self.pos[val]
        last = self.vals[-1]                    # 变化点: 用尾元素覆盖被删位置，O(1) 删除
        self.vals[i] = last
        self.pos[last] = i
        self.vals.pop()
        del self.pos[val]
        return True

    def getRandom(self):
        return random.choice(self.vals)         # 变化点: 随机数组下标即等概率""",
        "time": "各操作平均 O(1)",
        "space": "O(n)",
        "pitfalls": [
            "删除被删值恰是尾元素时，覆盖与 pop 的顺序仍要先改 pos 再 del，否则映射残留",
            "只靠哈希表做不到 O(1) 等概率随机，必须配合数组下标",
            "本题 LeetCode 签名是 RandomizedSet 而非 Solution，提交时类名要一致",
        ],
    },
    13: {
        "statement": "给你一个整数数组 nums，返回数组 answer，其中 answer[i] 等于 nums 中除 nums[i] 之外其余各元素的乘积。题目保证任意前缀或后缀的乘积都在 32 位整数范围内。要求不使用除法，并在 O(n) 时间内完成；进阶要求额外空间复杂度为 O(1)。",
        "examples": [
            {"input": "nums = [1,2,3,4]", "output": "[24,12,8,6]"},
            {"input": "nums = [-1,1,0,-3,3]", "output": "[0,0,9,0,0]"},
        ],
        "approach": "answer[i] 等于左侧前缀乘积乘右侧后缀乘积，前缀后缀分解信号：第一遍从左往右把前缀乘积填进 answer，第二遍从右往左用滚动后缀变量乘上去。变化点在于右侧不建后缀数组、只维护一个变量，额外空间降到 O(1)，且全程不用除法。",
        "code": """class Solution:
    def productExceptSelf(self, nums):
        n = len(nums)
        answer = [1] * n
        for i in range(1, n):
            answer[i] = answer[i - 1] * nums[i - 1]     # 变化点: 先填左侧前缀乘积（不含自身）
        right = 1
        for i in range(n - 1, -1, -1):
            answer[i] *= right                          # 变化点: 再乘右侧后缀乘积（滚动变量）
            right *= nums[i]
        return answer""",
        "time": "O(n)",
        "space": "O(1)（输出数组不计入额外空间）",
        "pitfalls": [
            "禁止用除法：数组含 0 时除法直接出错，前缀后缀分解天然规避",
            "左侧前缀乘的是 nums[i-1]，注意“不含自身”的下标错位",
            "第二遍必须从右往左，且先乘 right 再更新 right，顺序颠倒会漏掉自身",
        ],
    },
    14: {
        "statement": "在一条环路上有 n 个加油站，第 i 个加油站有汽油 gas[i]，你从第 i 个加油站出发开往第 i+1 个加油站需要消耗汽油 cost[i]。油箱初始为空，且油箱容量足够大。若你能沿环路行驶一周，返回出发加油站的编号，否则返回 -1。题目保证答案唯一。",
        "examples": [
            {"input": "gas = [1,2,3,4,5], cost = [3,4,5,1,2]", "output": "3"},
            {"input": "gas = [2,3,4], cost = [3,4,3]", "output": "-1"},
        ],
        "approach": "从 A 出发到 B 抛锚，则 A、B 之间任何站点出发都无法越过 B，线性贪心信号：一遍扫描，tank 为负时把候选起点挪到 i+1 并清零 tank。能否绕环由 total（总油量 - 总花费）决定。变化点在于抛锚后起点直接跳过整段失效区间，以及最后用 total >= 0 判定无解。",
        "code": """class Solution:
    def canCompleteCircuit(self, gas, cost):
        total = tank = start = 0
        for i in range(len(gas)):
            diff = gas[i] - cost[i]
            total += diff
            tank += diff
            if tank < 0:                        # 变化点: start 到 i 抛锚，i 之前的起点全部排除
                start = i + 1
                tank = 0
        return start if total >= 0 else -1      # 变化点: 总油量不足则无解""",
        "time": "O(n)",
        "space": "O(1)",
        "pitfalls": [
            "判定无解用 total（全程累计差值），不是 tank（从当前起点算的余量）",
            "抛锚后新起点是 i + 1，写成 i 会重复尝试已证明失效的位置",
            "题目保证解唯一，找到的 start 不需要再验证一圈",
        ],
    },
    15: {
        "statement": "n 个孩子站成一排，每个孩子有一个整数评分 ratings。你需要按照以下要求给孩子们分发糖果：每个孩子至少分配到一个糖果；相邻两个孩子中评分更高的那个可以获得更多的糖果。返回你需要准备的最少糖果数目。",
        "examples": [
            {"input": "ratings = [1,0,2]", "output": "5"},
            {"input": "ratings = [1,2,2]", "output": "4"},
        ],
        "approach": "相邻约束只涉及左右两个邻居，线性贪心信号：拆成两个单向约束分别处理——从左到右保证比左邻评分高就多一颗，再从右到左保证比右邻评分高就不少于右邻加一。变化点在于第二遍必须反向扫描，并用 max 合并两次结果使两个约束同时成立。",
        "code": """class Solution:
    def candy(self, ratings):
        n = len(ratings)
        candies = [1] * n
        for i in range(1, n):                   # 变化点: 左到右处理“比左邻高”的约束
            if ratings[i] > ratings[i - 1]:
                candies[i] = candies[i - 1] + 1
        for i in range(n - 2, -1, -1):          # 变化点: 右到左处理“比右邻高”，取 max 合并
            if ratings[i] > ratings[i + 1]:
                candies[i] = max(candies[i], candies[i + 1] + 1)
        return sum(candies)""",
        "time": "O(n)",
        "space": "O(n)",
        "pitfalls": [
            "评分相等不构成约束，不要给相等评分的孩子追加糖果",
            "第二遍必须从右往左，方向反了右侧约束无法传递",
            "合并两遍结果用 max，直接覆盖会破坏第一遍已满足的约束",
        ],
    },
    16: {
        "statement": "给定 n 个非负整数表示每个宽度为 1 的柱子的高度图 height，计算按此排列的柱子，下雨之后能接多少雨水。",
        "examples": [
            {"input": "height = [0,1,0,2,1,0,1,3,2,1,2,1]", "output": "6"},
            {"input": "height = [4,2,0,3,2,5]", "output": "9"},
        ],
        "approach": "每个位置能接的水由 min(左最高, 右最高) - 自身高度决定，对撞双指针信号：left、right 从两端内移，谁矮就结算谁——另一侧必有更高的墙兜底，水位无需再确认。变化点在于维护 left_max / right_max 两个滚动最大值，先更新再结算、结算后内移。",
        "code": """class Solution:
    def trap(self, height):
        left, right = 0, len(height) - 1
        left_max = right_max = 0
        water = 0
        while left < right:
            if height[left] < height[right]:    # 变化点: 结算较矮一侧，另一侧必有高墙兜底
                left_max = max(left_max, height[left])
                water += left_max - height[left]
                left += 1
            else:
                right_max = max(right_max, height[right])
                water += right_max - height[right]
                right -= 1
        return water""",
        "time": "O(n)",
        "space": "O(1)",
        "pitfalls": [
            "结算的是“较矮的一侧”，两侧高度相等时归入 right 分支即可，不影响正确性",
            "left_max 要先更新再结算，顺序错了首根柱子会算出负水",
            "height 为空时 right = -1，循环不进入直接返回 0，不用特判",
        ],
    },
    17: {
        "statement": "罗马数字包含七种字符：I(1)、V(5)、X(10)、L(50)、C(100)、D(500)、M(1000)。通常小数字写在大数字右边表示相加，但存在六种减法形式：IV(4)、IX(9)、XL(40)、XC(90)、CD(400)、CM(900)。给定一个罗马数字字符串 s，将其转换成整数。",
        "examples": [
            {"input": "s = \"III\"", "output": "3"},
            {"input": "s = \"MCMXCIV\"", "output": "1994"},
        ],
        "approach": "罗马数字规则可完全由“当前符号值与下一个符号值的大小关系”推出，哈希映射信号：建立字符到数值的表，扫描时若当前字符值小于下一个字符值就做减法，否则做加法。变化点在于比较对象是相邻两个字符，一次遍历即可完成转换。",
        "code": """class Solution:
    def romanToInt(self, s):
        values = {"I": 1, "V": 5, "X": 10, "L": 50,
                  "C": 100, "D": 500, "M": 1000}
        total = 0
        for i, ch in enumerate(s):
            if i + 1 < len(s) and values[ch] < values[s[i + 1]]:
                total -= values[ch]             # 变化点: 小值在大值左侧时做减法
            else:
                total += values[ch]
        return total""",
        "time": "O(n)",
        "space": "O(1)",
        "pitfalls": [
            "判断依据是“当前值 < 下一个值”，只看相邻一个字符，不用回看更远",
            "减法只发生在 IV/IX/XL/XC/CD/CM 六种组合，符合上述判据即天然覆盖",
            "取 s[i+1] 前要判 i + 1 < len(s)，最后一个字符一定做加法",
        ],
    },
    18: {
        "statement": "给定一个整数 num，将其转换为对应的罗马数字表示，输入范围 1 <= num <= 3999。罗马数字由 I、V、X、L、C、D、M 七种符号及六种减法形式 IV、IX、XL、XC、CD、CM 组成。",
        "examples": [
            {"input": "num = 3749", "output": "\"MMMDCCXLIX\""},
            {"input": "num = 58", "output": "\"LVIII\""},
        ],
        "approach": "把罗马数字的 13 种符号（含 900/400/90/40/9/4 六种减法形式）从大到小排成对照表，模拟信号：每轮尽量多用最大的符号并扣减 num，直到归零。变化点在于减法形式作为独立表项参与贪心匹配，且同一符号可能连续使用（如 MMM）要用 while。",
        "code": """class Solution:
    def intToRoman(self, num):
        table = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
                 (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
                 (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
        result = []
        for value, symbol in table:             # 变化点: 13 项符号表按数值降序贪心匹配
            while num >= value:
                result.append(symbol)
                num -= value
        return "".join(result)""",
        "time": "O(1)（符号表固定 13 项）",
        "space": "O(1)",
        "pitfalls": [
            "对照表必须按数值降序，且不能漏掉 CM/XC/IX 等减法形式，否则会出现 IIII 这类非法连写",
            "同一符号可能连续使用，内层要用 while 而不是 if",
            "num 范围限定 1 到 3999，超出范围无合法表示，不必处理",
        ],
    },
    19: {
        "statement": "给你一个字符串 s，由若干单词组成，单词之间用空格字符分隔。返回字符串中最后一个单词的长度。单词是指仅由字母组成、不包含任何空格字符的最大子字符串。",
        "examples": [
            {"input": "s = \"Hello World\"", "output": "5"},
            {"input": "s = \"   fly me   to   the moon  \"", "output": "4"},
        ],
        "approach": "只需要最后一个单词，字符串扫描信号：从字符串尾部向前扫。先跳过所有尾部空格定位单词的末字符，再向左数到第一个空格或字符串开头。变化点在于两阶段反向扫描，单词长度由两次停留位置相减得到。",
        "code": """class Solution:
    def lengthOfLastWord(self, s):
        i = len(s) - 1
        while i >= 0 and s[i] == ' ':           # 变化点: 先跳过尾部空格
            i -= 1
        end = i
        while i >= 0 and s[i] != ' ':           # 变化点: 再向左数到单词起点（空格或串首）
            i -= 1
        return end - i""",
        "time": "O(n)",
        "space": "O(1)",
        "pitfalls": [
            "末尾可能有多个空格，必须先跳过再计数",
            "两个内层循环都要带 i >= 0 判断，防止越界",
            "返回值是 end - i，循环停在空格位置上时不要再加一",
        ],
    },
    20: {
        "statement": "编写一个函数来查找字符串数组中的最长公共前缀。如果不存在公共前缀，返回空字符串 \"\"。所有输入只包含小写英文字母。",
        "examples": [
            {"input": "strs = [\"flower\",\"flow\",\"flight\"]", "output": "\"fl\""},
            {"input": "strs = [\"dog\",\"racecar\",\"car\"]", "output": "\"\""},
        ],
        "approach": "公共前缀要同时约束所有字符串，字符串扫描信号：以第一个串为基准做纵向逐列比较。任一列在某串上越界或字符失配，当前列下标就是公共前缀长度。变化点在于扫描维度是“列”而非“行”，且越界判断要在取 other[i] 之前完成。",
        "code": """class Solution:
    def longestCommonPrefix(self, strs):
        for i in range(len(strs[0])):           # 变化点: 逐列纵向扫描
            ch = strs[0][i]
            for other in strs[1:]:
                if i == len(other) or other[i] != ch:   # 变化点: 先判越界再取字符
                    return strs[0][:i]
        return strs[0]""",
        "time": "O(m·n)（m 为串长，n 为串数）",
        "space": "O(1)",
        "pitfalls": [
            "判断“某串先结束”要在取 other[i] 之前，否则下标越界",
            "strs[0] 可能为空串，外层循环不进入直接返回 \"\"，天然兼容",
            "失配时返回 strs[0][:i]，不是从头拼一个新字符串",
        ],
    },
    21: {
        "statement": "给你一个字符串 s，请你反转字符串中单词的顺序。单词是由非空格字符组成的字符串，s 中可能存在前导空格、尾随空格或者单词间的多个空格。返回的结果字符串中，单词之间应当仅用单个空格分隔，且不包含任何额外的空格。",
        "examples": [
            {"input": "s = \"the sky is blue\"", "output": "\"blue is sky the\""},
            {"input": "s = \"  hello world  \"", "output": "\"world hello\""},
        ],
        "approach": "单词顺序反转且要清理多余空格，字符串扫描信号：从右往左扫，跳过空格、截取单词、按遇到顺序拼接。反向截到的单词天然就是目标顺序。变化点在于扫描方向是反向，以及拼接用 ' '.join 保证单词间恰好一个空格。",
        "code": """class Solution:
    def reverseWords(self, s):
        words = []
        i = len(s) - 1
        while i >= 0:
            while i >= 0 and s[i] == ' ':       # 变化点: 反向扫描跳过多余空格
                i -= 1
            if i < 0:
                break
            end = i
            while i >= 0 and s[i] != ' ':
                i -= 1
            words.append(s[i + 1:end + 1])      # 变化点: 反向截取的单词天然符合新顺序
        return ' '.join(words)""",
        "time": "O(n)",
        "space": "O(n)",
        "pitfalls": [
            "单词间可能连续多个空格，两段内层循环都不能漏 i >= 0 判断",
            "拼接用 ' '.join(words)，手动加空格容易产生尾随空格",
            "s[i+1:end+1] 的左端点是 i+1（i 停在空格或 -1 上），下标错一格就截错词",
        ],
    },
    22: {
        "statement": "将一个给定字符串 s 根据给定的行数 numRows，以从上往下、从左到右进行 Z 字形排列，之后再按行从左到右逐行读取，输出拼接成的字符串。例如 \"PAYPALISHIRING\" 按 3 行排列后输出 \"PAHNAPLSIIGYIR\"。",
        "examples": [
            {"input": "s = \"PAYPALISHIRING\", numRows = 3", "output": "\"PAHNAPLSIIGYIR\""},
            {"input": "s = \"PAYPALISHIRING\", numRows = 4", "output": "\"PINALSIGYAHRPI\""},
        ],
        "approach": "字符要按 Z 形落到固定行上，字符串扫描信号：按行号顺序扫字符串，行号在 0 与 numRows-1 之间往返。变化点在于行号触到首行或末行时翻转方向，numRows == 1 时 rows 只有第 0 行必须特判返回原串。",
        "code": """class Solution:
    def convert(self, s, numRows):
        if numRows == 1 or numRows >= len(s):   # 变化点: 单行时无需折叠，直接返回原串
            return s
        rows = [[] for _ in range(numRows)]
        row, going_down = 0, False
        for ch in s:
            rows[row].append(ch)
            if row == 0 or row == numRows - 1:  # 变化点: 触到首行或末行时掉头
                going_down = not going_down
            row += 1 if going_down else -1
        return ''.join(''.join(r) for r in rows)""",
        "time": "O(n)",
        "space": "O(n)",
        "pitfalls": [
            "numRows == 1 必须特判，否则翻转会写到 rows[1] 导致下标越界",
            "going_down 初值是 False，靠首行触发第一次翻转开始向下",
            "numRows >= len(s) 时每行至多一个字符，直接返回原串即可",
        ],
    },
    23: {
        "statement": "给你两个字符串 haystack 和 needle，请你在 haystack 字符串中找出 needle 字符串的第一个匹配项的下标（下标从 0 开始）。如果 needle 不是 haystack 的一部分，则返回 -1。本题约定 needle 为空字符串时返回 0。",
        "examples": [
            {"input": "haystack = \"sadbutsad\", needle = \"sad\"", "output": "0"},
            {"input": "haystack = \"leetcode\", needle = \"leeto\"", "output": "-1"},
        ],
        "approach": "在主串中找模式串首现位置，字符串扫描信号：从每个可行起点 i 出发，内层循环逐字符比对 needle，比对走满 m 个字符即命中。变化点在于外层起点只需扫到 n-m，且失配立即换下一个起点（进阶可换 KMP 把均摊降到 O(n+m)）。",
        "code": """class Solution:
    def strStr(self, haystack, needle):
        n, m = len(haystack), len(needle)
        for i in range(n - m + 1):              # 变化点: 起点最多到 n-m，防止越界
            j = 0
            while j < m and haystack[i + j] == needle[j]:
                j += 1
            if j == m:                          # 变化点: 内层走满 m 个字符即完整匹配
                return i
        return -1""",
        "time": "O(n·m)",
        "space": "O(1)",
        "pitfalls": [
            "外层范围是 range(n - m + 1)，写成 n - m 会漏掉末尾起点",
            "needle 比 haystack 长时 range 为空，直接返回 -1，无需特判",
            "KMP 是进阶写法，暴力扫描在题目数据范围内即可通过",
        ],
    },
    24: {
        "statement": "给定一个单词数组 words 和一个宽度 maxWidth，重新排版文本，使每行恰好有 maxWidth 个字符且左右两端对齐。贪心策略：每行放置尽可能多的单词；单词间空格数尽量均匀分配，无法均匀时左侧空格多于右侧；最后一行应左对齐且单词间只放一个空格，行尾补空格。",
        "examples": [
            {"input": "words = [\"This\", \"is\", \"an\", \"example\", \"of\", \"text\", \"justification.\"], maxWidth = 16", "output": "[\"This    is    an\", \"example  of text\", \"justification.  \"]"},
            {"input": "words = [\"What\",\"must\",\"be\",\"acknowledgment\",\"shall\",\"be\"], maxWidth = 16", "output": "[\"What   must   be\", \"acknowledgment  \", \"shall be        \"]"},
        ],
        "approach": "排版规则是“贪心打包 + 空格分配”，字符串扫描信号：逐词装行，装不下就结算当前行。非末行把缺的空格均分到词间缝隙、余数落在左侧缝隙；末行与单单词行左对齐补空格。变化点在于装行判断要带上当前词数（即缝隙数），以及 divmod 后余数分配给左侧缝隙。",
        "code": """class Solution:
    def fullJustify(self, words, maxWidth):
        result, line, width = [], [], 0
        for w in words:
            if width + len(w) + len(line) > maxWidth:   # 变化点: 预判装不下再结算当前行
                result.append(self._justify(line, width, maxWidth))
                line, width = [], 0
            line.append(w)
            width += len(w)
        last = ' '.join(line).ljust(maxWidth)           # 变化点: 末行左对齐、行尾补空格
        return result + [last]

    def _justify(self, line, width, maxWidth):
        gaps = len(line) - 1
        if gaps == 0:
            return ''.join(line).ljust(maxWidth)
        base, extra = divmod(maxWidth - width, gaps)    # 变化点: 余数空格落到左侧缝隙
        parts = []
        for i, w in enumerate(line):
            parts.append(w)
            if i < gaps:
                parts.append(' ' * (base + (1 if i < extra else 0)))
        return ''.join(parts)""",
        "time": "O(N)（N 为全部字符总数）",
        "space": "O(N)",
        "pitfalls": [
            "装行判断是 width + len(w) + len(line) > maxWidth，len(line) 是当前词数也是缝隙数，漏加会塞太满",
            "末行与单单词行都要 ljust 补齐，不能走均匀分配分支",
            "divmod 的余数必须分配给左侧缝隙，分给右侧会与标准输出不符",
        ],
    },
    25: {
        "statement": "如果在将所有大写字符转换为小写字符、并移除所有非字母数字字符之后，短语正着读与反着读一模一样，则可以认为该短语是一个回文串。字母和数字都属于字母数字字符。给定一个字符串 s，如果它是回文串，返回 true；否则返回 false。",
        "examples": [
            {"input": "s = \"A man, a plan, a canal: Panama\"", "output": "true"},
            {"input": "s = \"race a car\"", "output": "false"},
        ],
        "approach": "回文判断天然是两端向中间收缩，对撞双指针信号：left、right 各自跳过非字母数字字符，统一转小写后比较，不相等即失败。变化点在于指针除夹逼外还要“跳过”无效字符，内层跳过循环必须带 left < right 防越界。",
        "code": """class Solution:
    def isPalindrome(self, s):
        left, right = 0, len(s) - 1
        while left < right:
            while left < right and not s[left].isalnum():   # 变化点: 跳过非字母数字字符
                left += 1
            while left < right and not s[right].isalnum():
                right -= 1
            if s[left].lower() != s[right].lower():         # 变化点: 统一小写后比较
                return False
            left += 1
            right -= 1
        return True""",
        "time": "O(n)",
        "space": "O(1)",
        "pitfalls": [
            "跳过无效字符的内层循环必须带 left < right，否则会越过另一端",
            "比较前要 lower()，'A' 与 'a' 应视为相同字符",
            "空串或全为标点的串按回文处理，返回 True",
        ],
    },
    26: {
        "statement": "给定字符串 s 和 t，判断 s 是否为 t 的子序列。字符串的一个子序列是原始字符串删除一些（也可以不删除）字符而不改变剩余字符相对位置形成的新字符串，例如 \"ace\" 是 \"abcde\" 的子序列，而 \"aec\" 不是。",
        "examples": [
            {"input": "s = \"abc\", t = \"ahbgdc\"", "output": "true"},
            {"input": "s = \"axc\", t = \"ahbgdc\"", "output": "false"},
        ],
        "approach": "s 要按顺序在 t 中找齐，同向双指针信号：i 指向 s、t 直接遍历，命中 s[i] 时 i 才前进。扫完 t 后 i 走到 len(s) 即说明 s 全部按序匹配。变化点在于只有 t 是主动指针，s 的指针命中才动。",
        "code": """class Solution:
    def isSubsequence(self, s, t):
        i = 0
        for ch in t:                            # 变化点: 只有 t 在动，s 命中才前进
            if i < len(s) and s[i] == ch:
                i += 1
        return i == len(s)""",
        "time": "O(n)",
        "space": "O(1)",
        "pitfalls": [
            "i < len(s) 的判断必须在取 s[i] 之前，防止 s 匹配完后越界",
            "s 为空串时 i == 0 == len(s)，直接返回 True，天然正确",
            "进阶场景（海量 s 查询同一个 t）才需要预处理 t 的字符下标表，单次查询直接扫",
        ],
    },
    27: {
        "statement": "给你一个下标从 1 开始的整数数组 numbers，该数组已按非递减顺序排列。请找出满足相加之和等于 target 的两个数，并返回它们的数组下标（下标从 1 开始）。你可以假设每个输入只对应唯一的答案，且你不可以两次使用同一个元素。要求使用常数级的额外空间。",
        "examples": [
            {"input": "numbers = [2,7,11,15], target = 9", "output": "[1,2]"},
            {"input": "numbers = [2,3,4], target = 6", "output": "[1,3]"},
        ],
        "approach": "数组有序且要找两数之和，对撞双指针信号：left、right 从两端起步，和太小移左端增大和，和太大移右端减小和。变化点在于返回下标要 +1 转成 1-based，且题目保证唯一解、命中即可返回。",
        "code": """class Solution:
    def twoSum(self, numbers, target):
        left, right = 0, len(numbers) - 1
        while left < right:
            s = numbers[left] + numbers[right]
            if s == target:
                return [left + 1, right + 1]    # 变化点: 题目下标从 1 开始，返回前加一
            if s < target:
                left += 1                       # 变化点: 和偏小移左端，和偏大移右端
            else:
                right -= 1
        return []""",
        "time": "O(n)",
        "space": "O(1)",
        "pitfalls": [
            "返回值要 +1 转成 1-based，直接返回 left、right 是最高频错误",
            "移动规则不能写反：和太小只能靠 left 右移增大，和太大靠 right 左移减小",
            "题目保证唯一解，命中即返回，无需继续扫描或去重",
        ],
    },
    28: {
        "statement": "给定一个长度为 n 的整数数组 height，有 n 条垂线，第 i 条线的两个端点是 (i, 0) 和 (i, height[i])。找出其中的两条线，使得它们与 x 轴共同构成的容器可以容纳最多的水，返回容器可以储存的最大水量。你不能倾斜容器。",
        "examples": [
            {"input": "height = [1,8,6,2,5,4,8,3,7]", "output": "49"},
            {"input": "height = [1,1]", "output": "1"},
        ],
        "approach": "水量由较短边与宽度决定，对撞双指针信号：每次内移较矮的一侧——只有换掉短边面积才可能变大，被排除的一侧不可能产生更优解。变化点在于面积公式 min(两边高度) × 宽度，以及“先结算当前面积再内移”的顺序。",
        "code": """class Solution:
    def maxArea(self, height):
        left, right = 0, len(height) - 1
        best = 0
        while left < right:
            area = min(height[left], height[right]) * (right - left)    # 变化点: 短边 × 宽度
            best = max(best, area)
            if height[left] < height[right]:    # 变化点: 矮的一侧内移才可能更优
                left += 1
            else:
                right -= 1
        return best""",
        "time": "O(n)",
        "space": "O(1)",
        "pitfalls": [
            "面积用 min(两边高度)，误用 max 会高估水量",
            "内移的是矮的一侧，内移高的一侧会漏掉最优解",
            "先结算当前面积再移动指针，顺序颠倒会漏掉初始状态",
        ],
    },
    29: {
        "statement": "给你一个整数数组 nums，判断是否存在三元组 [nums[i], nums[j], nums[k]] 满足 i != j、i != k 且 j != k，并同时满足 nums[i] + nums[j] + nums[k] == 0。请你返回所有和为 0 且不重复的三元组，答案中不可以包含重复的三元组。",
        "examples": [
            {"input": "nums = [-1,0,1,2,-1,-4]", "output": "[[-1,-1,2],[-1,0,1]]"},
            {"input": "nums = [0,1,1]", "output": "[]"},
        ],
        "approach": "三数之和可固定一个数后转化为有序区间上的两数之和，对撞双指针信号：先排序，再对每个 i 在右侧区间左右夹逼。变化点在于固定值剪枝（nums[i] > 0 直接停）、固定值与命中后左右指针的三层去重。",
        "code": """class Solution:
    def threeSum(self, nums):
        nums.sort()
        result = []
        for i in range(len(nums) - 2):
            if nums[i] > 0:                     # 变化点: 最小值已为正，后面不可能凑出 0
                break
            if i > 0 and nums[i] == nums[i - 1]:    # 变化点: 固定值去重
                continue
            left, right = i + 1, len(nums) - 1
            while left < right:
                s = nums[i] + nums[left] + nums[right]
                if s < 0:
                    left += 1
                elif s > 0:
                    right -= 1
                else:
                    result.append([nums[i], nums[left], nums[right]])
                    left += 1
                    right -= 1
                    while left < right and nums[left] == nums[left - 1]:    # 变化点: 命中后左右指针去重
                        left += 1
                    while left < right and nums[right] == nums[right + 1]:
                        right -= 1
        return result""",
        "time": "O(n²)",
        "space": "O(log n)（排序递归栈）",
        "pitfalls": [
            "忘记排序是最大错误：对撞移动方向与三层去重都依赖有序",
            "命中后指针必须先移动再去重，否则相邻相等值会卡住死循环",
            "固定值去重用 nums[i] == nums[i-1]，i == 0 时不判，否则会跳过首个合法组合",
        ],
    },
    30: {
        "statement": "给定一个含有 n 个正整数的数组 nums 和一个正整数 target。找出该数组中满足其总和大于等于 target 的长度最小的连续子数组，并返回其长度；如果不存在符合条件的子数组，返回 0。",
        "examples": [
            {"input": "target = 7, nums = [2,3,1,2,4,3]", "output": "2"},
            {"input": "target = 4, nums = [1,4,4]", "output": "1"},
        ],
        "approach": "连续子数组求最短且元素全为正，滑动窗口信号：right 扩张累加 total，total 达标后 left 尽量收缩，窗口每缩小一次都可能更短。变化点在于结算发生在收缩循环内部（达标即结算），以及正确性依赖元素全为正、窗口和的单调性。",
        "code": """class Solution:
    def minSubArrayLen(self, target, nums):
        left = 0
        total = 0
        best = float('inf')
        for right, x in enumerate(nums):
            total += x                          # 变化点: 入窗累加
            while total >= target:              # 变化点: 达标即收缩，每缩一步都可能更短
                best = min(best, right - left + 1)
                total -= nums[left]
                left += 1
        return 0 if best == float('inf') else best""",
        "time": "O(n)",
        "space": "O(1)",
        "pitfalls": [
            "结算必须在收缩循环内部，只在外层循环结算会错过最短窗口",
            "滑动窗口依赖元素全为正（窗口和随收缩单调减），数组含负数时本写法失效",
            "找不到达标窗口返回 0，不是 -1",
        ],
    },
    31: {
        "statement": "给定一个字符串 s，请你找出其中不含有重复字符的最长子串的长度。子串要求连续。",
        "examples": [
            {"input": "s = \"abcabcbb\"", "output": "3"},
            {"input": "s = \"bbbbb\"", "output": "1"},
        ],
        "approach": "最长且无重复约束的连续子串，滑动窗口信号：right 逐字符入窗并维护计数，刚入窗的字符计数超过 1 时收缩 left 直到恢复合法。变化点在于收缩条件只针对当前字符，结算在收缩完成后进行，此时窗口必然无重复。",
        "code": """class Solution:
    def lengthOfLongestSubstring(self, s):
        left = 0
        window = {}
        best = 0
        for right, ch in enumerate(s):
            window[ch] = window.get(ch, 0) + 1  # 变化点: 入窗维护字符计数
            while window[ch] > 1:               # 变化点: 只有当前字符重复才收缩
                window[s[left]] -= 1
                left += 1
            best = max(best, right - left + 1)
        return best""",
        "time": "O(n)",
        "space": "O(min(n, 字符集大小))",
        "pitfalls": [
            "结算在收缩完成之后，此时窗口才是合法的，提前结算会把重复窗口计入",
            "收缩条件针对“刚入窗的字符”计数超过 1，不是窗口里任意字符",
            "空串时循环不进入，best 初值 0 保证返回 0",
        ],
    },
    32: {
        "statement": "给定一个字符串 s 和一个字符串数组 words，words 中所有字符串长度相同。串联子串是指一个包含 words 中所有字符串以任意顺序排列连接起来的子串，且每个字符串恰好出现一次（按 words 中的次数使用）。返回 s 中所有串联子串的起始索引，顺序不重要。",
        "examples": [
            {"input": "s = \"barfoothefoobarman\", words = [\"foo\",\"bar\"]", "output": "[0,9]"},
            {"input": "s = \"barfoofoobarthefoobarman\", words = [\"bar\",\"foo\",\"the\"]", "output": "[6,9,12]"},
        ],
        "approach": "窗口单位是等长单词而非字符，滑动窗口信号：以单词长度 wl 为步长、按 wl 个余数分通道滑动，哈希计数维护窗口内单词。超量的单词从左侧按单词粒度弹出。变化点在于按余数分 wl 条通道，命中条件是窗口跨度恰等于 wl × 单词数。",
        "code": """class Solution:
    def findSubstring(self, s, words):
        need = {}
        for w in words:
            need[w] = need.get(w, 0) + 1
        wl, count = len(words[0]), len(words)
        total = wl * count
        result = []
        for offset in range(wl):                # 变化点: 按余数分 wl 条滑动通道
            left, have = offset, {}
            for right in range(offset, len(s) - wl + 1, wl):
                word = s[right:right + wl]
                have[word] = have.get(word, 0) + 1
                while have[word] > need.get(word, 0):   # 变化点: 超额单词从左侧按词粒度弹出
                    left_word = s[left:left + wl]
                    have[left_word] -= 1
                    left += wl
                if right + wl - left == total:  # 变化点: 窗口跨度恰等于单词总长即命中
                    result.append(left)
        return result""",
        "time": "O(n·wl)（n 为 s 长度，wl 为单词长度）",
        "space": "O(m·wl)（m 为 words 单词数）",
        "pitfalls": [
            "必须按 wl 个余数分别起窗，只从下标 0 开始会漏掉对齐在其他余数上的解",
            "words 里可能有重复单词，need 要累加计数而不是简单去重",
            "右端上限是 len(s) - wl + 1，切片 s[right:right+wl] 才不会截到残缺词",
        ],
    },
    33: {
        "statement": "给你一个字符串 s 和一个字符串 t，返回 s 中涵盖 t 所有字符（包括重复字符）的最小子串。如果 s 中不存在涵盖 t 所有字符的子串，则返回空字符串 \"\"。测试数据保证答案唯一。",
        "examples": [
            {"input": "s = \"ADOBECODEBANC\", t = \"ABC\"", "output": "\"BANC\""},
            {"input": "s = \"a\", t = \"a\"", "output": "\"a\""},
        ],
        "approach": "最小覆盖子串，滑动窗口信号：need 记录 t 的字符需求，right 扩张入窗，窗口覆盖 need 后 left 尽量收缩求最短。变化点在于覆盖判定用 window 与 need 的计数比较，且结算必须在收缩循环内进行、每收缩一步都可能刷新最短。",
        "code": """class Solution:
    def minWindow(self, s, t):
        need = {}
        for ch in t:
            need[ch] = need.get(ch, 0) + 1
        window = {}
        left = 0
        best_start, best_len = 0, float('inf')
        for right, ch in enumerate(s):
            window[ch] = window.get(ch, 0) + 1          # 变化点: 全字符入窗，收缩时统一递减
            while all(window.get(c, 0) >= v for c, v in need.items()):  # 变化点: 覆盖成立才收缩
                if right - left + 1 < best_len:     # 变化点: 先结算再收缩，每步都可能更短
                    best_start, best_len = left, right - left + 1
                window[s[left]] -= 1
                left += 1
        return "" if best_len == float('inf') else s[best_start:best_start + best_len]""",
        "time": "O(n)（n 为 s 长度，覆盖判定随字符集常数）",
        "space": "O(|t| + 字符集)",
        "pitfalls": [
            "t 含重复字符时 need 必须累加计数，只记录“出现过”会误判覆盖",
            "结算要在收缩循环内部，收缩后窗口变短但仍需保持覆盖才继续，时机错开就不是最小覆盖",
            "不存在覆盖时返回空串 \"\"，不是 None 或 -1",
        ],
    },
}
