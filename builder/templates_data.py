# -*- coding: utf-8 -*-
"""模板定义：35 个可复用的套路。"""

TEMPLATES = [
    # ---------------- 指针与窗口 ----------------
    {
        "id": "two-pointer-same",
        "name": "同向双指针（读写指针）",
        "group": "指针与窗口",
        "tagline": "一个指针读，一个指针写，原地压缩数组。",
        "idea": "read 指针负责扫描全部元素，write 指针指向下一个可写位置。满足保留条件时把 read 写到 write，并让 write 前移；扫描结束时 write 就是新长度。",
        "signals": ["要求原地修改，额外空间 O(1)", "删除 / 保留满足条件的元素", "有序数组去重，或双序列按序匹配"],
        "skeleton": """write = 0
for read in range(len(nums)):
    if nums[read] != val:        # 变化点：保留条件
        nums[write] = nums[read]
        write += 1
return write""",
        "variations": [
            "保留条件不同：不等于 val、与前一个元素不同、最多保留两次",
            "双序列匹配时，两个指针分别在各自字符串上前进",
            "返回值可能是新长度，也可能是压缩后的数组",
        ],
        "complexity": "O(n) 时间，O(1) 空间",
        "ref": "labuladong · 双指针技巧",
    },
    {
        "id": "two-pointer-opposite",
        "name": "对撞双指针",
        "group": "指针与窗口",
        "tagline": "左右夹逼，每一步排除一个不可能的候选。",
        "idea": "left 与 right 从两端向中间收缩。每次根据当前状态决定移动哪一侧，并证明被排除的一侧不可能产生更优解。",
        "signals": ["有序数组求两数之和 / 三数之和", "两端向中间的最优值问题（面积、雨水）", "回文判断或从后往前合并"],
        "skeleton": """left, right = 0, len(nums) - 1
while left < right:
    if 满足条件:                 # 变化点：移动哪一侧
        left += 1
    else:
        right -= 1""",
        "variations": [
            "移动规则不同：和太小移 left，容器高度矮的一侧内移",
            "从后往前合并两个有序数组，避免覆盖未处理元素",
            "固定一个数后，在剩余区间做对撞双指针（三数之和）",
        ],
        "complexity": "O(n) 时间，O(1) 空间",
        "ref": "labuladong · 双指针技巧",
    },
    {
        "id": "fast-slow",
        "name": "快慢指针",
        "group": "指针与窗口",
        "tagline": "用速度差制造距离，用相遇判断环。",
        "idea": "slow 每次走一步，fast 每次走两步。相遇说明有环；相遇后让一个指针回到起点、同速前进，再次相遇处就是环入口。",
        "signals": ["链表判环 / 找环入口", "找链表中点、倒数第 k 个节点", "把“下一个状态”看成链表（快乐数）"],
        "skeleton": """slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
    if slow is fast:             # 变化点：相遇后的处理
        ...""",
        "variations": [
            "找环入口：相遇后一个指针回到 head，同速再走",
            "找中点：fast 到尾时 slow 在中点；倒数第 k 让 fast 先走 k 步",
            "快乐数：把数位平方和当作 next，检测是否进入 1 或环",
        ],
        "complexity": "O(n) 时间，O(1) 空间",
        "ref": "labuladong · 双指针技巧",
    },
    {
        "id": "sliding-window",
        "name": "滑动窗口",
        "group": "指针与窗口",
        "tagline": "右指针扩张，左指针收缩，窗口内始终可判定。",
        "idea": "right 逐位扩张窗口并维护窗口状态；当窗口不满足约束时，left 右移收缩，直到重新合法。每一步用窗口长度或窗口状态更新答案。",
        "signals": ["连续子数组 / 子串", "求最长、最短、是否覆盖", "窗口约束可用计数或哈希维护"],
        "skeleton": """left = 0
window = {}
for right, x in enumerate(s):
    window[x] = window.get(x, 0) + 1     # 变化点：入窗维护
    while 窗口不合法:                      # 变化点：收缩条件
        window[s[left]] -= 1
        left += 1
    ans = max(ans, right - left + 1)     # 变化点：更新答案""",
        "variations": [
            "固定长度窗口：入窗后当长度超过 k 再出窗",
            "覆盖型窗口：need / valid 计数，达到要求时缩左边界",
            "按单词长度分组起点，处理“串联所有单词”",
        ],
        "complexity": "O(n) 时间，O(字符集) 空间",
        "ref": "labuladong · 滑动窗口技巧进阶",
    },
    {
        "id": "prefix-decomposition",
        "name": "前缀 / 后缀分解",
        "group": "指针与窗口",
        "tagline": "把“除了自己”拆成左侧前缀与右侧后缀。",
        "idea": "一次从左到右累计前缀信息，一次从右到左累计后缀信息，两次扫描合并出每个位置的答案；也可用前缀和把区间查询降为 O(1)。",
        "signals": ["每个位置依赖左侧 / 右侧整体信息", "除自身以外的乘积、接雨水、股票最低价", "子数组和 / 区间和查询"],
        "skeleton": """prefix = 1
for i in range(n):
    ans[i] = prefix              # 变化点：使用左侧前缀
    prefix *= nums[i]

suffix = 1
for i in range(n - 1, -1, -1):
    ans[i] *= suffix             # 变化点：与右侧后缀合并
    suffix *= nums[i]""",
        "variations": [
            "前缀积 / 前缀最大值 / 前缀最小值",
            "接雨水：min(左最大, 右最大) - 当前高度",
            "前缀和 + 哈希表统计子数组和",
        ],
        "complexity": "O(n) 时间，O(1) 或 O(n) 空间",
        "ref": "labuladong · 前缀和技巧",
    },

    # ---------------- 查找·排序·贪心 ----------------
    {
        "id": "binary-search",
        "name": "二分查找",
        "group": "查找·排序·贪心",
        "tagline": "维护答案区间，每轮砍掉一半。",
        "idea": "先固定区间定义（推荐左闭右开），再写收缩规则。循环结束时 left 是第一个满足条件的位置；也可以对答案空间二分。",
        "signals": ["有序数组查找 / 插入位置", "求第一个满足条件的位置", "答案具有单调性，可判定（二分答案）"],
        "skeleton": """left, right = 0, len(nums)      # 左闭右开
while left < right:
    mid = (left + right) // 2
    if nums[mid] < target:         # 变化点：判定条件
        left = mid + 1
    else:
        right = mid
return left                         # 第一个 >= target""",
        "variations": [
            "查找目标值：相等时直接返回",
            "lower_bound / upper_bound：第一个 >= 或 > 的位置",
            "二分答案：x 的平方根，判定 mid² 与 x 的关系",
        ],
        "complexity": "O(log n) 时间，O(1) 空间",
        "ref": "labuladong · 二分查找详解",
    },
    {
        "id": "binary-search-bound",
        "name": "二分边界与旋转数组",
        "group": "查找·排序·贪心",
        "tagline": "整体不有序，但每一轮都能判断哪一半可丢。",
        "idea": "利用局部单调性构造判定：旋转数组先判断哪一侧有序；找最小值与右端点比较；找边界则做两次 lower_bound；两个有序数组中位数对短数组二分划分。",
        "signals": ["旋转排序数组搜索 / 找最小值", "第一个和最后一个位置", "峰值问题、两个有序数组的中位数"],
        "skeleton": """left, right = 0, len(nums) - 1
while left <= right:
    mid = (left + right) // 2
    if nums[mid] == target:
        return mid
    if nums[left] <= nums[mid]:      # 变化点：判断有序侧
        ...                           # 在有序侧继续二分
    else:
        ...                           # 在另一侧继续二分""",
        "variations": [
            "旋转数组：先判 left..mid 是否有序，再决定保留哪半",
            "找最小值 / 峰值：与右端点或相邻元素比较",
            "第一个和最后一个位置：两次 lower_bound",
            "两个数组中位数：对较短数组二分划分，使左右数量平衡",
        ],
        "complexity": "O(log n) 时间，O(1) 空间",
        "ref": "labuladong · 二分查找详解",
    },
    {
        "id": "interval-greedy",
        "name": "区间贪心",
        "group": "查找·排序·贪心",
        "tagline": "先排序，再线性扫描合并或选择。",
        "idea": "合并区间按左端点排序，维护当前区间右端；求最多不重叠区间按右端点排序，每次选择结束最早的区间。",
        "signals": ["合并 / 插入区间", "最多不重叠区间、最少箭矢", "连续区间汇总"],
        "skeleton": """intervals.sort(key=lambda x: x[0])      # 变化点：排序键
res = []
for start, end in intervals:
    if not res or start > res[-1][1]:
        res.append([start, end])
    else:
        res[-1][1] = max(res[-1][1], end)  # 变化点：合并规则""",
        "variations": [
            "合并重叠区间：按左端点排序，右端取 max",
            "插入区间：先把左侧不重叠的放入，再合并，最后接右侧",
            "射气球：按右端点排序，箭尽量射在当前区间右端",
        ],
        "complexity": "O(n log n) 时间，O(n) 空间",
        "ref": "labuladong · 贪心算法之区间调度问题",
    },
    {
        "id": "greedy-linear",
        "name": "线性贪心",
        "group": "查找·排序·贪心",
        "tagline": "只保留对后续有用的一两个状态，边走边更新。",
        "idea": "每一步做当前看起来最优的选择，并维护一个（或少数）能代表历史最优的状态。难点不在代码，而在于说明为什么局部最优能推出全局最优。",
        "signals": ["跳跃游戏、股票买卖", "加油站、分发糖果", "每次选择当前最优且不影响后续可行性"],
        "skeleton": """cur = 0
for x in nums:
    cur = max(cur, x)        # 变化点：维护的贪心状态
    ...""",
        "variations": [
            "股票：维护历史最低价，或累加所有正收益",
            "跳跃：维护当前可达最远位置，或按层扩张步数",
            "加油站：总油量非负 + 起点重置",
            "分发糖果：左右各扫描一次取 max",
        ],
        "complexity": "O(n) 时间，O(1) 空间",
        "ref": "labuladong · 贪心算法之区间调度问题",
    },
    {
        "id": "heap-topk",
        "name": "堆与 TopK",
        "group": "查找·排序·贪心",
        "tagline": "只要前 k 个，就维护一个大小为 k 的堆。",
        "idea": "求第 k 大用小顶堆，堆顶就是答案；多路有序数据用堆归并；数据流中位数用大顶堆放左半、小顶堆放右半并保持平衡。",
        "signals": ["第 k 大 / 前 k 小", "多路有序序列合并", "动态数据流中位数、带约束的最优选择"],
        "skeleton": """h = []
for x in nums:
    heapq.heappush(h, x)       # 变化点：入堆元素
    if len(h) > k:
        heapq.heappop(h)
return h[0]""",
        "variations": [
            "第 k 大：小顶堆容量 k；第 k 小：大顶堆容量 k",
            "K 对数字：堆中存 (和, i, j)，弹出后推进 j",
            "IPO：按资本排序后用大顶堆取当前可做项目",
            "中位数：两个堆大小差不超过 1",
        ],
        "complexity": "O(n log k) 时间，O(k) 空间",
        "ref": "labuladong · 二叉堆详解实现优先级队列",
    },
    {
        "id": "divide-conquer",
        "name": "分治",
        "group": "查找·排序·贪心",
        "tagline": "拆成同类子问题，分别求解再合并。",
        "idea": "找到中点或分割方式，把问题拆成规模更小的同类问题；递归求解后合并。关键是设计可合并的中间结果。",
        "signals": ["有序数组建 BST、链表归并排序", "四叉树 / 二维区域划分", "合并 K 个有序链表、快速幂"],
        "skeleton": """def solve(lo, hi):
    if lo >= hi:
        return base
    mid = (lo + hi) // 2
    left = solve(lo, mid)         # 变化点：拆分方式
    right = solve(mid + 1, hi)
    return merge(left, right)     # 变化点：合并方式""",
        "variations": [
            "有序数组建 BST：中点作根，左右递归",
            "链表归并排序：快慢指针找中点再合并",
            "建立四叉树：四象限同值则合并为叶子",
            "快速幂：按指数奇偶拆分，递归后平方",
        ],
        "complexity": "O(n log n) 时间，O(log n) 递归栈",
        "ref": "labuladong · 分治与快速幂",
    },
    {
        "id": "kadane",
        "name": "Kadane 算法",
        "group": "查找·排序·贪心",
        "tagline": "以 i 结尾的最优解，只取决于前一个状态。",
        "idea": "cur 表示以当前元素结尾的最大子数组和：要么接上前一段，要么从当前元素重新开始。环形数组再补一个“总和减去最小子数组”的情况。",
        "signals": ["最大子数组和", "环形数组最大和", "连续区间的最优值"],
        "skeleton": """cur = best = nums[0]
for x in nums[1:]:
    cur = max(x, cur + x)        # 变化点：是否延续前一段
    best = max(best, cur)
return best""",
        "variations": [
            "普通最大子数组和",
            "环形最大和：max(普通最大, 总和 - 最小子数组)，全负单独处理",
            "乘积最大子数组：同时维护最大值与最小值",
        ],
        "complexity": "O(n) 时间，O(1) 空间",
        "ref": "labuladong · 动态规划详解进阶",
    },

    # ---------------- 哈希·字符串·矩阵 ----------------
    {
        "id": "hash-map",
        "name": "哈希映射",
        "group": "哈希·字符串·矩阵",
        "tagline": "用空间换时间，把“找配对”变成 O(1)。",
        "idea": "遍历时把已经见过的信息存入哈希表，查询当前元素需要的配对。先想清楚 key 与 value 的语义：值→下标、字符→字符、规范形→分组。",
        "signals": ["两数之和、重复元素", "字符双射（同构、单词规律）", "异位词分组、连续序列"],
        "skeleton": """seen = {}
for i, x in enumerate(nums):
    if x in seen:              # 变化点：查询的键
        return ...
    seen[x] = i                # 变化点：存储的键值语义""",
        "variations": [
            "值 → 下标：两数之和",
            "字符双向映射：同构字符串、单词规律",
            "排序后的字符串作 key：字母异位词分组",
            "集合 + 只从连续段起点扩展：最长连续序列",
        ],
        "complexity": "O(n) 时间，O(n) 空间",
        "ref": "labuladong · 哈希表相关题目",
    },
    {
        "id": "frequency-count",
        "name": "计数统计",
        "group": "哈希·字符串·矩阵",
        "tagline": "先数清楚，再按阈值或极值下结论。",
        "idea": "用字典或长度固定的数组统计频次，再按题意找超过一半、达到 h、字符库存是否足够等条件。小写字母题优先用 26 位数组。",
        "signals": ["多数元素、H 指数", "异位词、赎金信", "字符集固定且需要比较库存"],
        "skeleton": """count = {}
for x in nums:
    count[x] = count.get(x, 0) + 1
for x, c in count.items():
    if c > n // 2:             # 变化点：判定条件
        return x""",
        "variations": [
            "多数元素：Boyer-Moore 投票可降为 O(1) 空间",
            "H 指数：计数桶按引用数分桶，从后往前累计",
            "异位词：26 位计数数组逐位比较",
            "赎金信：先统计 magazine，再逐字扣减",
        ],
        "complexity": "O(n) 时间，O(字符集) 空间",
        "ref": "labuladong · 高频面试系列",
    },
    {
        "id": "string-scan",
        "name": "字符串扫描与模拟",
        "group": "哈希·字符串·矩阵",
        "tagline": "按题意切分、扫描、重建，边界决定成败。",
        "idea": "把字符串拆成单词、字符或固定宽度的分组，逐段处理后拼接。常见变化点是扫描方向（从后往前）、周期/行号映射、补齐空格和 KMP 匹配。",
        "signals": ["单词级处理（最后一个单词、反转单词）", "按行 / 周期重排字符", "子串匹配、文本对齐"],
        "skeleton": """res = []
for part in s.split(...):      # 变化点：切分 / 扫描方式
    ...
return "".join(res)""",
        "variations": [
            "从后往前跳过空格，找最后一个单词",
            "纵向扫描：每一列比较所有字符串",
            "Z 字形：用周期和行号映射下标",
            "KMP：预处理 next 数组做线性匹配",
            "文本对齐：逐行确定单词数与空格分配",
        ],
        "complexity": "O(n) 时间，O(n) 空间",
        "ref": "labuladong · 字符串乘法",
    },
    {
        "id": "matrix-simulation",
        "name": "矩阵模拟",
        "group": "哈希·字符串·矩阵",
        "tagline": "用边界框住未处理区域，或做原地坐标变换。",
        "idea": "螺旋类问题维护上下左右四条边界，按方向推进并收缩；旋转用“转置 + 翻转”；置零用首行首列做标记；生命游戏用额外状态位保存旧值。",
        "signals": ["螺旋遍历 / 生成矩阵", "原地旋转、原地置零", "需要同时保留旧状态的矩阵修改"],
        "skeleton": """top, bottom = 0, len(matrix) - 1
left, right = 0, len(matrix[0]) - 1
while top <= bottom and left <= right:
    ...                        # 变化点：遍历方向与边界收缩
    top += 1""",
        "variations": [
            "螺旋矩阵：右→下→左→上，注意单行/单列",
            "旋转图像：先转置，再左右翻转",
            "矩阵置零：首行首列标记，最后单独处理",
            "生命游戏：用 2/3 表示“旧活新死 / 旧死新活”",
        ],
        "complexity": "O(mn) 时间，O(1) 额外空间",
        "ref": "labuladong · 花式遍历",
    },

    # ---------------- 栈·链表·设计 ----------------
    {
        "id": "stack-expression",
        "name": "栈与表达式",
        "group": "栈·链表·设计",
        "tagline": "把尚未匹配或尚未结算的部分压入栈。",
        "idea": "括号类问题遇左括号压栈、遇右括号弹栈校验；表达式类问题把数字、符号、括号分层压栈，遇到运算符就弹出操作数结算。",
        "signals": ["括号匹配、路径化简", "逆波兰表达式、基本计算器", "需要回退到最近未处理状态"],
        "skeleton": """stack = []
for ch in s:
    if ch == '(':
        stack.append(ch)
    elif ch == ')':
        if not stack:
            return False
        stack.pop()
return not stack""",
        "variations": [
            "括号匹配：右括号与栈顶类型对应",
            "简化路径：按 / 分段，.. 弹栈，. 跳过",
            "逆波兰：遇运算符弹两个数，注意运算顺序",
            "计算器：符号入栈，括号用递归或栈隔离",
        ],
        "complexity": "O(n) 时间，O(n) 空间",
        "ref": "labuladong · 实现计算器",
    },
    {
        "id": "design-structure",
        "name": "数据结构设计",
        "group": "栈·链表·设计",
        "tagline": "先看每个操作的时间要求，再组合基础结构。",
        "idea": "设计题先列出各操作复杂度，再选组合：哈希 + 数组支持 O(1) 随机，哈希 + 双向链表支持 LRU，辅助栈支持最小栈，双堆支持中位数。",
        "signals": ["要求 O(1) 的插入 / 删除 / 随机", "缓存淘汰、最小栈", "数据流中位数、BST 迭代器"],
        "skeleton": """class Foo:
    def __init__(self):
        self.data = {}         # 变化点：组合哪些结构
        self.cap = 0
    def op(self, x):
        ...""",
        "variations": [
            "O(1) 随机集合：数组存值，哈希存值→下标，删除时与末尾交换",
            "最小栈：辅助栈同步保存当前最小值",
            "LRU：哈希表 + 双向链表，访问后移到头部",
            "中位数：大顶堆 + 小顶堆，保持大小平衡",
        ],
        "complexity": "视操作而定，通常 O(1)",
        "ref": "labuladong · LRU算法",
    },
    {
        "id": "linked-list-dummy",
        "name": "链表哨兵与遍历",
        "group": "栈·链表·设计",
        "tagline": "加一个 dummy，消除头节点的特判。",
        "idea": "dummy 指向 head，prev 指向已处理部分的尾部。按题意移动 prev / cur，修改 next 指针；返回 dummy.next 避免头节点被删除时的分支。",
        "signals": ["可能删除头节点的链表题", "合并、分隔、旋转链表", "删除倒数第 N 个节点"],
        "skeleton": """dummy = ListNode(0, head)
prev = dummy
while prev.next and prev.next.next:
    if prev.next.val == prev.next.next.val:   # 变化点：处理条件
        ...
    else:
        prev = prev.next
return dummy.next""",
        "variations": [
            "合并两个有序链表：比较后接较小节点",
            "删除重复段：内层 while 跳过所有相同值",
            "分隔链表：维护两条链，最后拼接",
            "两数相加：处理进位与长度差",
        ],
        "complexity": "O(n) 时间，O(1) 空间",
        "ref": "labuladong · 递归反转链表的一部分",
    },
    {
        "id": "linked-list-reverse",
        "name": "链表反转",
        "group": "栈·链表·设计",
        "tagline": "三个指针原地掉头，区间反转再接回。",
        "idea": "prev / cur / nxt 三指针逐个反转 next。区间反转先走到 left 前一个节点，记住连接点，反转指定数量后把三段接回。",
        "signals": ["反转整个 / 部分链表", "K 个一组翻转", "需要改变 next 指向的链表操作"],
        "skeleton": """prev, cur = None, head
while cur:
    nxt = cur.next
    cur.next = prev            # 变化点：反转区间边界
    prev, cur = cur, nxt
return prev""",
        "variations": [
            "反转 [left, right]：记录 left 前驱与反转段头尾",
            "K 个一组：先数够 k 个，再反转这一段并接回",
            "递归写法：先反转后面的部分，再处理当前节点",
        ],
        "complexity": "O(n) 时间，O(1) 空间",
        "ref": "labuladong · 递归反转链表的一部分",
    },

    # ---------------- 树·图·搜索 ----------------
    {
        "id": "tree-recursion",
        "name": "二叉树递归",
        "group": "树·图·搜索",
        "tagline": "先定义 dfs 返回值的语义，再决定前序还是后序处理。",
        "idea": "二叉树问题几乎都能落到“递归左右子树”上。明确 dfs 返回什么（高度、和、是否存在、路径），需要跨子树信息时用全局变量或返回多个值。",
        "signals": ["求深度、节点数、路径", "判断相同 / 对称 / 平衡", "构造树、最近公共祖先、最大路径和"],
        "skeleton": """def dfs(node):
    if not node:
        return 0                # 变化点：空节点返回值
    left = dfs(node.left)
    right = dfs(node.right)
    return 1 + max(left, right) # 变化点：后序汇合逻辑""",
        "variations": [
            "求深度 / 节点数：返回单值累加",
            "路径和：向下传递剩余 target 或当前数字",
            "构造树：用下标哈希定位根，递归区间",
            "最大路径和：返回单边最大值，全局记录左右拐点",
            "LCA：左右都找到则当前节点为答案",
            "原地展开：先保存 right，再改指针",
        ],
        "complexity": "O(n) 时间，O(h) 递归栈",
        "ref": "labuladong · 二叉树系列1 / 二叉树总结",
    },
    {
        "id": "tree-bst-inorder",
        "name": "BST 中序遍历",
        "group": "树·图·搜索",
        "tagline": "中序遍历天然升序，把 BST 问题变成序列问题。",
        "idea": "中序访问顺序递增：第 k 小用计数器，最小绝对差比较相邻节点，验证 BST 检查是否严格递增；迭代器用显式栈模拟中序。",
        "signals": ["第 k 小 / 最小差值", "验证二叉搜索树", "BST 迭代器"],
        "skeleton": """def dfs(node):
    if not node:
        return
    dfs(node.left)             # 中序：升序
    visit(node.val)            # 变化点：访问时的比较 / 计数
    dfs(node.right)""",
        "variations": [
            "第 k 小：中序计数到 k 停止",
            "最小绝对差：维护 prev 节点",
            "验证 BST：中序严格递增，或递归传上下界",
            "迭代器：栈中存左链，next 时弹出并转向右子树",
        ],
        "complexity": "O(n) 时间，O(h) 空间",
        "ref": "labuladong · BST1 / BST2",
    },
    {
        "id": "bfs-level",
        "name": "层序遍历（BFS）",
        "group": "树·图·搜索",
        "tagline": "一层一批，用队列推进。",
        "idea": "队列保存当前层节点，for len(q) 锁定这一层；层内可以取最后一个（右视图）、求平均、按奇偶反转，或把 next 指针串起来。",
        "signals": ["按层输出 / 右视图 / 层平均", "锯齿形遍历", "填充 next 指针"],
        "skeleton": """q = deque([root])
while q:
    for _ in range(len(q)):    # 一层一批
        node = q.popleft()
        ...
        if node.left: q.append(node.left)     # 变化点：入队与层内处理
        if node.right: q.append(node.right)""",
        "variations": [
            "右视图：记录每层最后一个节点",
            "层平均：层内求和后除以当前层大小",
            "锯齿：按层号决定是否反转",
            "next 指针：层内记录 prev，prev.next = node",
        ],
        "complexity": "O(n) 时间，O(n) 空间",
        "ref": "labuladong · BFS框架",
    },
    {
        "id": "grid-dfs",
        "name": "网格 DFS / FloodFill",
        "group": "树·图·搜索",
        "tagline": "把网格当图，访问后立即标记。",
        "idea": "每个格子向四邻接扩展；进入时检查边界与条件，随后标记已访问，避免重复和死循环。需要枚举路径时改成回溯并撤销标记。",
        "signals": ["岛屿数量、被围绕区域", "连通块染色", "网格路径枚举（配合回溯）"],
        "skeleton": """def dfs(i, j):
    if not (0 <= i < m and 0 <= j < n) or grid[i][j] != '1':
        return
    grid[i][j] = '0'           # 变化点：标记方式 / 扩展条件
    for di, dj in dirs:
        dfs(i + di, j + dj)""",
        "variations": [
            "岛屿数量：每个未访问陆地启动一次 DFS 并计数",
            "被围绕区域：从四条边界的 O 反向标记，剩下的是被围的",
            "单词搜索：回溯 + 临时标记，递归后恢复",
        ],
        "complexity": "O(mn) 时间，O(mn) 递归栈",
        "ref": "labuladong · 岛屿题目",
    },
    {
        "id": "graph-bfs",
        "name": "图 BFS / 最短步数",
        "group": "树·图·搜索",
        "tagline": "无权图求最少步数，按层扩展。",
        "idea": "队列保存待扩展节点，dist 记录首次到达的步数。邻居必须在入队时标记访问，否则会重复入队。关键是定义“状态”和“邻居生成函数”。",
        "signals": ["最少变换次数、最短路径", "单词接龙、基因变化、蛇梯棋", "克隆图的遍历"],
        "skeleton": """q = deque([start])
dist = {start: 0}
while q:
    node = q.popleft()
    for nxt in neighbors(node):
        if nxt not in dist:
            dist[nxt] = dist[node] + 1   # 变化点：邻居生成方式
            q.append(nxt)""",
        "variations": [
            "单词接龙：逐位替换或通配符建图",
            "最小基因变化：字符集 ACGT 替换",
            "蛇梯棋：一维编号映射到棋盘坐标",
            "克隆图：哈希表存旧节点→新节点",
        ],
        "complexity": "O(V+E) 时间，O(V) 空间",
        "ref": "labuladong · BFS框架",
    },
    {
        "id": "topo-sort",
        "name": "拓扑排序",
        "group": "树·图·搜索",
        "tagline": "入度为 0 的先出队，能输出全部节点则无环。",
        "idea": "根据依赖关系建有向图并统计入度，把入度为 0 的节点入队；逐个出队、删除其出边并更新入度。若最终输出数量等于节点数，则无环。",
        "signals": ["课程安排 / 依赖顺序", "判断有向图是否有环", "输出一种可行顺序"],
        "skeleton": """indeg = [0] * n
graph = [[] for _ in range(n)]
for a, b in prerequisites:
    graph[b].append(a)
    indeg[a] += 1
q = deque([i for i in range(n) if indeg[i] == 0])
order = []
while q:
    u = q.popleft()
    order.append(u)
    for v in graph[u]:
        indeg[v] -= 1          # 变化点：入度归零时入队
        if indeg[v] == 0:
            q.append(v)
return len(order) == n""",
        "variations": [
            "只判断能否完成：比较出队数量与 n",
            "输出拓扑序：记录出队顺序",
            "要求字典序最小：把队列换成最小堆",
        ],
        "complexity": "O(V+E) 时间，O(V+E) 空间",
        "ref": "labuladong · 拓扑排序",
    },
    {
        "id": "trie",
        "name": "字典树",
        "group": "树·图·搜索",
        "tagline": "公共前缀共享一条路径。",
        "idea": "每个节点代表一个字符，根到节点构成前缀；插入沿字符逐层建节点，末尾打标记。查询前缀只需沿路径走，通配符则 DFS 枚举分支。",
        "signals": ["前缀查询、单词插入", "通配符匹配", "单词搜索 II 的剪枝"],
        "skeleton": """class Trie:
    def __init__(self):
        self.root = {}
        self.end = '#'
    def insert(self, word):
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})   # 变化点：节点结构
        node[self.end] = True""",
        "variations": [
            "前缀查询：走完路径即存在前缀",
            "通配符 .：DFS 枚举所有子节点",
            "单词搜索 II：Trie + 网格回溯，节点保存完整单词",
            "也可用 26 叉数组实现，查询更快但更占空间",
        ],
        "complexity": "O(L) 每次操作，O(总字符数) 空间",
        "ref": "labuladong · 字典树",
    },
    {
        "id": "backtracking",
        "name": "回溯框架",
        "group": "树·图·搜索",
        "tagline": "做选择 → 递归 → 撤销选择。",
        "idea": "在递归树上做 DFS：维护 path、当前选择列表与终止条件。每层做选择后进入下一层，返回时撤销。用 start 控制组合顺序，用 used 控制排列，用剪枝减少无效分支。",
        "signals": ["组合 / 排列 / 子集", "括号生成、N 皇后", "网格路径枚举"],
        "skeleton": """def backtrack(path, choices):
    if 终止条件:
        res.append(path[:])      # 变化点：收集方式
        return
    for x in choices:
        if 剪枝(x):
            continue
        path.append(x)           # 做选择
        backtrack(path, next_choices(x))
        path.pop()               # 撤销选择""",
        "variations": [
            "组合：用 start 保证不重复且顺序无关",
            "排列：用 used 数组标记已选元素",
            "组合总和：可重复选取则下一层仍从 i 开始",
            "括号生成：记录左右剩余数量",
            "N 皇后：列 + 两条对角线集合判重",
            "单词搜索：网格四方向 + 临时标记与恢复",
        ],
        "complexity": "指数级，取决于搜索树大小",
        "ref": "labuladong · 回溯算法详解修订版",
    },

    # ---------------- 动态规划 ----------------
    {
        "id": "dp-linear",
        "name": "线性 DP",
        "group": "动态规划",
        "tagline": "dp[i] 表示前缀或“以 i 结尾”的最优值。",
        "idea": "定义 dp[i] 的语义，写出从更小下标转移的方程，确定初始化与遍历顺序。若只依赖前一两项，可用滚动变量压缩空间。",
        "signals": ["爬楼梯、打家劫舍", "最长递增子序列", "状态只沿一个维度推进"],
        "skeleton": """dp = [0] * (n + 1)
dp[0] = base
for i in range(1, n + 1):
    dp[i] = ... dp[i-1] ... dp[i-2]   # 变化点：转移方程
return dp[n]""",
        "variations": [
            "爬楼梯：dp[i] = dp[i-1] + dp[i-2]",
            "打家劫舍：dp[i] = max(dp[i-1], dp[i-2] + nums[i])",
            "LIS：dp[i] 以 i 结尾，内层枚举 j；可加二分优化到 O(n log n)",
        ],
        "complexity": "O(n) 或 O(n²)，可优化空间",
        "ref": "labuladong · 动态规划设计：最长递增子序列",
    },
    {
        "id": "dp-knapsack",
        "name": "背包 DP",
        "group": "动态规划",
        "tagline": "从物品集合中选，凑出目标。",
        "idea": "把问题转成背包：dp[j] 表示凑出容量/金额 j 的最优值或可达性。0-1 背包容量倒序，完全背包正序；求最少个数初始化为 inf，求方案数初始化为 1。",
        "signals": ["零钱兑换、单词拆分", "组合数 / 方案数", "每个物品可选一次或无限次"],
        "skeleton": """dp = [inf] * (amount + 1)     # 或 [False] * (n + 1)
dp[0] = 0
for coin in coins:            # 完全背包：物品在外
    for j in range(coin, amount + 1):
        dp[j] = min(dp[j], dp[j - coin] + 1)   # 变化点：转移
return dp[amount]""",
        "variations": [
            "零钱兑换：完全背包求最少硬币数",
            "单词拆分：布尔可达性，按单词长度切分",
            "组合数：累加方案数，注意遍历顺序避免重复计数",
            "0-1 背包：容量必须倒序遍历",
        ],
        "complexity": "O(物品数 × 目标容量)",
        "ref": "labuladong · 背包问题",
    },
    {
        "id": "dp-grid",
        "name": "网格 DP",
        "group": "动态规划",
        "tagline": "状态落在格子上，从上方或左方转移。",
        "idea": "dp[i][j] 表示到达 (i,j) 的最优值或方案数，转移来自上方与左方（三角形来自上一层相邻两个）。先初始化第一行第一列，再处理障碍与边界。",
        "signals": ["最小路径和、不同路径", "三角形最小路径和", "最大正方形"],
        "skeleton": """dp = [[0] * n for _ in range(m)]
dp[0][0] = base
for i in range(m):
    for j in range(n):
        dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + grid[i][j]   # 变化点：转移 / 边界
return dp[m-1][n-1]""",
        "variations": [
            "最小路径和：取 min 后加当前格",
            "不同路径 II：障碍格方案数置 0",
            "三角形：自底向上，dp[j] = min(dp[j], dp[j+1]) + 当前",
            "最大正方形：dp 表示以 (i,j) 为右下角的最大边长",
        ],
        "complexity": "O(mn) 时间，O(mn) 或 O(n) 空间",
        "ref": "labuladong · 动态规划详解进阶",
    },
    {
        "id": "dp-string",
        "name": "字符串 DP",
        "group": "动态规划",
        "tagline": "两个前缀之间的最优解，比较末尾字符。",
        "idea": "dp[i][j] 表示 s 的前 i 个字符与 t 的前 j 个字符的关系（编辑距离、是否交错、是否匹配）。比较 s[i-1] 与 t[j-1] 决定转移；回文类用区间 dp[i][j]。",
        "signals": ["编辑距离、最长公共子序列", "交错字符串", "最长回文子串"],
        "skeleton": """dp = [[0] * (n + 1) for _ in range(m + 1)]
for i in range(m + 1):
    dp[i][0] = i          # 变化点：边界初始化
for j in range(n + 1):
    dp[0][j] = j
for i in range(1, m + 1):
    for j in range(1, n + 1):
        if s[i-1] == t[j-1]:
            dp[i][j] = dp[i-1][j-1]
        else:
            dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1   # 变化点：编辑操作
return dp[m][n]""",
        "variations": [
            "编辑距离：增、删、替换三种操作取 min + 1",
            "交错字符串：dp 为 bool，按当前字符选择来源",
            "最长回文子串：区间 dp，或中心扩展",
            "LCS：匹配则左上 + 1，否则取 max",
        ],
        "complexity": "O(mn) 时间，O(mn) 或 O(n) 空间",
        "ref": "labuladong · 编辑距离 / 子序列问题模板",
    },
    {
        "id": "dp-stock",
        "name": "股票买卖 DP",
        "group": "动态规划",
        "tagline": "天数 × 交易次数 × 是否持股。",
        "idea": "定义 buy[j] / sell[j] 为最多 j 次交易时持有/不持有股票的最大收益。每天先更新买入（消耗一次交易），再更新卖出；用滚动数组压缩天数维。",
        "signals": ["限定交易次数的股票问题", "带冷冻期 / 手续费的状态机", "每天只有少量状态"],
        "skeleton": """buy = [-inf] * (k + 1)
sell = [0] * (k + 1)
for price in prices:
    for j in range(1, k + 1):
        buy[j] = max(buy[j], sell[j-1] - price)   # 变化点：买入 / 卖出顺序
        sell[j] = max(sell[j], buy[j] + price)
return sell[k]""",
        "variations": [
            "只允许一次交易：维护历史最低价",
            "无限次交易：累加所有正收益",
            "至多 k 次交易：本题骨架",
            "含冷冻期 / 手续费：增加状态或调整转移",
        ],
        "complexity": "O(nk) 时间，O(k) 空间",
        "ref": "labuladong · 团灭股票问题",
    },

    # ---------------- 位运算·数学 ----------------
    {
        "id": "bit-manipulation",
        "name": "位运算",
        "group": "位运算·数学",
        "tagline": "把整数看成 32 位向量，成批处理。",
        "idea": "异或消对、n & (n-1) 消掉最低位的 1、逐位统计取模，是三类核心操作。二进制求和则把进位当成状态逐位模拟。",
        "signals": ["只出现一次的数字", "二进制中 1 的个数", "位反转、范围按位与、二进制加法"],
        "skeleton": """ans = 0
for x in nums:
    ans ^= x                    # 变化点：位运算选择
return ans""",
        "variations": [
            "只出现一次：全部异或",
            "出现三次：逐位统计后对 3 取模",
            "1 的个数：n & (n-1) 循环消位",
            "颠倒二进制位：逐位取出并左移拼接",
            "范围按位与：找公共前缀，或移位消低位",
            "二进制求和：逐位相加并维护进位",
        ],
        "complexity": "O(n) 或 O(32n)",
        "ref": "labuladong · 常用的位操作",
    },
    {
        "id": "math-simulation",
        "name": "数学与按位模拟",
        "group": "位运算·数学",
        "tagline": "逐位拆数，按规则推进，照顾边界。",
        "idea": "按题意拆数位或按规则模拟。常见边界：负数、0、进位连锁、前导零、整数溢出；涉及除法时优先用乘法判断以避免溢出。",
        "signals": ["回文数、加一、阶乘尾零", "罗马数字转换", "直线上最多的点数"],
        "skeleton": """res = []
while n > 0:
    digit = n % 10
    n //= 10
    res.append(...)            # 变化点：按位 / 按规则处理
return ...""",
        "variations": [
            "回文数：只反转一半，负数直接 False",
            "加一：从末尾处理 9 的进位",
            "阶乘尾零：统计因子 5 的个数",
            "罗马数字：从大到小贪心匹配值表",
            "直线点数：斜率用 gcd 约分，单独处理重复点",
        ],
        "complexity": "O(log n) 或 O(n²)",
        "ref": "labuladong · 数学相关题目",
    },
]

TEMPLATE_BY_ID = {t["id"]: t for t in TEMPLATES}
GROUPS = []
for _t in TEMPLATES:
    if _t["group"] not in GROUPS:
        GROUPS.append(_t["group"])

assert len(TEMPLATE_BY_ID) == len(TEMPLATES)
