# -*- coding: utf-8 -*-
"""题解数据 114-137：二分查找、堆、位运算、数学、一维动态规划。"""

DATA = {
    114: {
        "statement": "给定一个按升序排列且无重复元素的整数数组 nums 和一个目标值 target，如果 target 在数组中就返回它的下标；否则返回它按顺序插入后数组仍保持有序的位置。要求算法时间复杂度为 O(log n)。",
        "examples": [
            {"input": "nums = [1,3,5,6], target = 5", "output": "2"},
            {"input": "nums = [1,3,5,6], target = 2", "output": "1"},
        ],
        "approach": "数组有序，且“插入位置”恰好等于“第一个 >= target 的下标”，这是标准二分的信号。沿用左闭右开区间：nums[mid] < target 时答案必在右侧，否则 mid 可能就是答案。变化点在于相等时不立即返回、继续收缩，循环结束时 left 就是插入位置。",
        "code": """class Solution:
    def searchInsert(self, nums, target):
        left, right = 0, len(nums)              # 变化点: 右开区间，插到末尾也能覆盖
        while left < right:
            mid = (left + right) // 2
            if nums[mid] < target:              # 变化点: 找第一个 >= target 的位置
                left = mid + 1
            else:
                right = mid
        return left""",
        "time": "O(log n)",
        "space": "O(1)",
        "pitfalls": [
            "right 必须取 len(nums)，取 len(nums)-1 时插入到末尾的场景会漏",
            "相等分支归入 right = mid，天然兼容 target 已存在的情况，不必单独处理",
            "mid 必须向下取整，上取整会让 mid 越过右开边界导致越界",
        ],
    },
    115: {
        "statement": "给你一个 m × n 的整数矩阵 matrix，其满足两个性质：每行整数从左到右升序排列，且每行的第一个整数大于上一行的最后一个整数。判断目标值 target 是否存在于矩阵中。",
        "examples": [
            {"input": "matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 3", "output": "true"},
            {"input": "matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 13", "output": "false"},
        ],
        "approach": "每行整体大于上一行，把矩阵按行展开就是一段完整的有序序列，可折叠坐标做一次整体二分。用 mid//n 与 mid%n 把一维下标还原成行列取值再与 target 比较。变化点在于折叠与还原都围绕列数 n 进行，以及二分结束后还要校验 left 处的值是否真的等于 target。",
        "code": """class Solution:
    def searchMatrix(self, matrix, target):
        m, n = len(matrix), len(matrix[0])
        left, right = 0, m * n                  # 变化点: 二维折叠成一段有序一维序列
        while left < right:
            mid = (left + right) // 2
            val = matrix[mid // n][mid % n]     # 变化点: 一维下标还原成行列
            if val < target:
                left = mid + 1
            else:
                right = mid
        return left < m * n and matrix[left // n][left % n] == target""",
        "time": "O(log mn)",
        "space": "O(1)",
        "pitfalls": [
            "下标折叠与还原都要用列数 n：mid//n 取行、mid%n 取列",
            "整体有序的前提是每行第一个元素大于上一行最后一个；只保证行内有序时须逐行二分",
            "二分只保证停在第一个 >= target 的位置，返回前必须校验值相等",
        ],
    },
    116: {
        "statement": "峰值元素是严格大于其左右相邻值的元素。给定数组 nums，其中 nums[i] != nums[i+1]，并约定边界外 nums[-1] = nums[n] = -∞。返回任意一个峰值元素的下标，要求时间复杂度为 O(log n)。",
        "examples": [
            {"input": "nums = [1,2,3,1]", "output": "2"},
            {"input": "nums = [1,2,1,3,5,6,4]", "output": "1 或 5"},
        ],
        "approach": "数组虽不整体有序，但比较 nums[mid] 与右邻即可判断上坡还是下坡——每轮都能安全丢掉一半，属于边界二分信号。nums[mid] < nums[mid+1] 说明右侧必定存在峰值。变化点在于比较对象换成右邻元素而不是 target，区间收敛到 left == right 即峰值下标。",
        "code": """class Solution:
    def findPeakElement(self, nums):
        left, right = 0, len(nums) - 1
        while left < right:
            mid = (left + right) // 2
            if nums[mid] < nums[mid + 1]:       # 变化点: 与右邻比较，上坡侧必有峰值
                left = mid + 1
            else:
                right = mid
        return left""",
        "time": "O(log n)",
        "space": "O(1)",
        "pitfalls": [
            "比较 nums[mid+1] 时 mid 最大只能取到 right-1，用 left < right 收敛保证不越界",
            "峰值是局部定义（大于相邻），不是全局最大值",
            "相邻元素互不相等是判断方向的隐含前提",
        ],
    },
    117: {
        "statement": "整数数组 nums 原本按升序排列且元素互不相同，在未知下标处发生了旋转（如 [0,1,2,4,5,6,7] 旋转后变为 [4,5,6,7,0,1,2]）。给定 target，若它在数组中返回其下标，否则返回 -1。要求时间复杂度为 O(log n)。",
        "examples": [
            {"input": "nums = [4,5,6,7,0,1,2], target = 0", "output": "4"},
            {"input": "nums = [4,5,6,7,0,1,2], target = 3", "output": "-1"},
        ],
        "approach": "旋转数组每轮至少有一半是有序的，这是边界二分的信号：先判断哪一半有序，再看 target 是否落在该有序区间内。nums[left] <= nums[mid] 说明左半有序；若 nums[left] <= target < nums[mid] 则留在左半，否则去右半。变化点在于“判有序侧 + 判区间”两层条件的嵌套。",
        "code": """class Solution:
    def search(self, nums, target):
        left, right = 0, len(nums) - 1
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] == target:
                return mid
            if nums[left] <= nums[mid]:         # 变化点: 判断左半是否有序
                if nums[left] <= target < nums[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            else:                               # 变化点: 右半有序，按区间决定方向
                if nums[mid] < target <= nums[right]:
                    left = mid + 1
                else:
                    right = mid - 1
        return -1""",
        "time": "O(log n)",
        "space": "O(1)",
        "pitfalls": [
            "判断左半有序要用 <=：区间剩两个元素时 left == mid，缺等号会走错分支",
            "target 落在有序半的判断必须带区间端点：nums[left] <= target < nums[mid]",
            "本题元素互异；若允许重复（81 题变体）需要额外的退化处理",
        ],
    },
    118: {
        "statement": "给你一个按非递减顺序排列的整数数组 nums 和目标值 target，找出 target 在数组中的开始位置和结束位置。如果 target 不存在，返回 [-1, -1]。要求时间复杂度为 O(log n)。",
        "examples": [
            {"input": "nums = [5,7,7,8,8,10], target = 8", "output": "[3,4]"},
            {"input": "nums = [5,7,7,8,8,10], target = 6", "output": "[-1,-1]"},
        ],
        "approach": "查两个边界等价于做两次 lower_bound：第一个 >= target 是左边界；第一个 >= target+1 再减一是右边界。复用同一个闭式二分函数，避免手写两套方向逻辑。变化点在于用 target+1 巧妙定位右边界，并先校验 start 处是否真的等于 target。",
        "code": """class Solution:
    def searchRange(self, nums, target):
        def lower_bound(t):                     # 第一个 >= t 的位置
            left, right = 0, len(nums)
            while left < right:
                mid = (left + right) // 2
                if nums[mid] < t:
                    left = mid + 1
                else:
                    right = mid
            return left
        start = lower_bound(target)
        if start == len(nums) or nums[start] != target:
            return [-1, -1]                     # 变化点: 先确认 target 存在
        end = lower_bound(target + 1) - 1       # 变化点: target+1 定右边界
        return [start, end]""",
        "time": "O(log n)",
        "space": "O(1)",
        "pitfalls": [
            "两次调用同一个 lower_bound，右边界用 target + 1 而不是手写向左收缩",
            "start 可能等于 len(nums)，先判越界再取值",
            "nums[start] != target 时直接返回 [-1,-1]，不能继续算 end",
        ],
    },
    119: {
        "statement": "已知一个长度为 n 的数组原本按升序排列，元素互不相同，并被旋转了 1 到 n 次。例如 [0,1,2,4,5,6,7] 可能变成 [4,5,6,7,0,1,2]。请找出并返回数组中的最小元素，要求时间复杂度为 O(log n)。",
        "examples": [
            {"input": "nums = [3,4,5,1,2]", "output": "1"},
            {"input": "nums = [11,13,15,17]", "output": "11"},
        ],
        "approach": "旋转后数组由两段升序组成，最小值是第二段的起点，这是边界二分的信号。nums[mid] > nums[right] 说明最小值在右半；否则最小值在含 mid 的左半。变化点在于锚定右端点而不是左端点来判断方向，且 mid 可能就是答案，收缩时保留 right = mid。",
        "code": """class Solution:
    def findMin(self, nums):
        left, right = 0, len(nums) - 1
        while left < right:
            mid = (left + right) // 2
            if nums[mid] > nums[right]:         # 变化点: 与右端点比较，最小值在右半
                left = mid + 1
            else:
                right = mid                     # 变化点: mid 可能就是最小值，保留它
        return nums[left]""",
        "time": "O(log n)",
        "space": "O(1)",
        "pitfalls": [
            "锚定右端点而非左端点：与左端点比较无法区分“整体有序”和“最小值在右半”",
            "mid 可能就是最小值，右收缩用 right = mid 而不是 mid - 1",
            "用 left < right 收敛，区间只剩两个元素时也能正确停住",
        ],
    },
    120: {
        "statement": "给定两个大小分别为 m 和 n 的正序（从小到大）数组 nums1 和 nums2，找出并返回这两个正序数组的中位数。要求算法的时间复杂度为 O(log(m+n))，不允许直接合并两个数组。",
        "examples": [
            {"input": "nums1 = [1,3], nums2 = [2]", "output": "2.0"},
            {"input": "nums1 = [1,2], nums2 = [3,4]", "output": "2.5"},
        ],
        "approach": "中位数把合并序列切成左右等长两半：对较短数组二分它贡献到左半的个数 i，长数组按 j = half - i 补齐，再用四条边界值判断划分是否交叉有序。L1 > R2 说明 i 偏大要左移，L2 > R1 说明 i 偏小要右移。变化点在于用 ±inf 哨兵免去边界特判，并按总数奇偶选择 max(L1,L2) 或两侧均值作答案。",
        "code": """class Solution:
    def findMedianSortedArrays(self, nums1, nums2):
        if len(nums1) > len(nums2):             # 变化点: 对较短数组二分，保证 j 合法
            nums1, nums2 = nums2, nums1
        m, n = len(nums1), len(nums2)
        total, half = m + n, (m + n + 1) // 2
        left, right = 0, m
        while True:                             # 合法划分一定存在，可安全循环
            i = (left + right) // 2             # nums1 贡献左半 i 个
            j = half - i                        # nums2 贡献左半 j 个
            L1 = nums1[i - 1] if i > 0 else float("-inf")
            R1 = nums1[i] if i < m else float("inf")
            L2 = nums2[j - 1] if j > 0 else float("-inf")
            R2 = nums2[j] if j < n else float("inf")
            if L1 > R2:
                right = i - 1                   # 变化点: 划分偏右，i 左移
            elif L2 > R1:
                left = i + 1                    # 变化点: 划分偏左，i 右移
            else:
                break
        if total % 2:
            return max(L1, L2)
        return (max(L1, L2) + min(R1, R2)) / 2""",
        "time": "O(log min(m,n))",
        "space": "O(1)",
        "pitfalls": [
            "必须对较短数组二分，否则 j = half - i 可能为负而越界",
            "i、j 取 0 或取满时用 ±inf 哨兵，免去四类边界特判",
            "奇数总长取 max(L1, L2)，偶数取两侧均值，两种取值不要写混",
        ],
    },
    121: {
        "statement": "给定整数数组 nums 和整数 k，请返回数组中第 k 个最大的元素。注意是排序后的第 k 个最大元素，而不是第 k 个不同的元素。",
        "examples": [
            {"input": "nums = [3,2,1,5,6,4], k = 2", "output": "5"},
            {"input": "nums = [3,2,3,1,2,4,5,5,6], k = 4", "output": "4"},
        ],
        "approach": "只求第 k 大不必整段排序：用容量为 k 的小顶堆保留“当前最大的 k 个”，堆顶即答案，这是堆 TopK 的信号。每个元素入堆，容量超过 k 就弹出堆顶最小值。变化点在于求最大反而用小顶堆，以及先压后弹保证堆始终非空。",
        "code": """import heapq

class Solution:
    def findKthLargest(self, nums, k):
        h = []
        for x in nums:
            heapq.heappush(h, x)                # 变化点: 小顶堆，堆顶是当前第 k 大
            if len(h) > k:
                heapq.heappop(h)                # 变化点: 超容量弹出最小，保留最大 k 个
        return h[0]""",
        "time": "O(n log k)",
        "space": "O(k)",
        "pitfalls": [
            "第 k 大用容量 k 的小顶堆，堆顶即答案；用大顶堆就得全部入堆再弹 k-1 次",
            "先压后弹，保证堆从空到满的过程不会出错",
            "重复元素也占名次，这是排序意义下的第 k 大",
        ],
    },
    122: {
        "statement": "假设你初始资本为 w，最多可以完成 k 个项目。第 i 个项目需要 capital[i] 的启动资本，完成后可获得 profits[i] 的纯利润（利润累加进资本）。每个项目只能选择一次，求最终可以获得的最大资本。",
        "examples": [
            {"input": "k = 2, w = 0, profits = [1,2,3], capital = [0,1,1]", "output": "4"},
            {"input": "k = 1, w = 0, profits = [1,2,3], capital = [0,1,2]", "output": "1"},
        ],
        "approach": "资本只增不减，可启动项目的集合单调扩大：先按资本排序，用指针把资本达标的利润全部压入大顶堆，每轮取堆顶利润最高的项目完成。变化点在于“按资本排序 + 指针只前进 + 大顶堆取当前最优”的组合，堆空说明剩余项目都启动不了，提前退出。",
        "code": """import heapq

class Solution:
    def findMaximizedCapital(self, k, w, profits, capital):
        projects = sorted(zip(capital, profits))
        heap = []                               # 当前可启动项目的利润大顶堆
        i, n = 0, len(projects)
        for _ in range(k):
            while i < n and projects[i][0] <= w:
                heapq.heappush(heap, -projects[i][1])   # 变化点: 资本达标的项目全部入堆
                i += 1
            if not heap:
                break                           # 变化点: 无项目可做，提前结束
            w += -heapq.heappop(heap)           # 变化点: 每轮选利润最大的项目
        return w""",
        "time": "O(n log n)（排序）+ O(k log n)",
        "space": "O(n)",
        "pitfalls": [
            "每轮要把当前资本能启动的所有项目全部入堆，而不是只挑一个",
            "资本只增不减，已入堆项目不会失效，指针单调前进避免重复扫描",
            "堆空说明剩下的项目资本都不够，提前 break 防止空转 k 次",
        ],
    },
    123: {
        "statement": "给定两个以升序排列的整数数组 nums1 和 nums2，以及一个整数 k，返回和最小的 k 个数对 (u, v)，其中 u 来自 nums1，v 来自 nums2。数对顺序按和从小到大排列。",
        "examples": [
            {"input": "nums1 = [1,7,11], nums2 = [2,4,6], k = 3", "output": "[[1,2],[1,4],[1,6]]"},
            {"input": "nums1 = [1,1,2], nums2 = [1,2,3], k = 2", "output": "[[1,1],[1,1]]"},
        ],
        "approach": "数对 (i, j) 的最小后继是 (i, j+1)：把每行（固定 i）的首数对放入小顶堆，弹出谁就推进谁的同行下一列，类似多路归并。变化点在于堆元素存 (和, i, j) 三元组，且 i 只需初始化前 k 行，更靠后的数对不可能进入前 k 小。",
        "code": """import heapq

class Solution:
    def kSmallestPairs(self, nums1, nums2, k):
        heap = []
        for i in range(min(k, len(nums1))):     # 变化点: 只取前 k 行的首数对建堆
            heapq.heappush(heap, (nums1[i] + nums2[0], i, 0))
        res = []
        while heap and len(res) < k:
            s, i, j = heapq.heappop(heap)
            res.append([nums1[i], nums2[j]])
            if j + 1 < len(nums2):              # 变化点: 弹出后推进同行的 j
                heapq.heappush(heap, (nums1[i] + nums2[j + 1], i, j + 1))
        return res""",
        "time": "O(k log k)",
        "space": "O(k)",
        "pitfalls": [
            "堆中存 (和, i, j)，弹出后只推进 j + 1，i 方向的覆盖靠初始建堆",
            "i 只初始化到 min(k, len(nums1))，后面行的首数对不可能进前 k 小",
            "数对按位置计数，相同值不同下标的数对（如 [1,1] 与 [1,1]）都要保留",
        ],
    },
    124: {
        "statement": "中位数是有序整数列表中的中间值；如果列表长度为偶数，中位数是两个中间值的平均。实现 MedianFinder 类：addNum(num) 从数据流中添加一个整数，findMedian() 返回目前所有元素的中位数。",
        "examples": [
            {"input": "[\"MedianFinder\",\"addNum\",\"addNum\",\"findMedian\",\"addNum\",\"findMedian\"]\\n[[],[1],[2],[],[3],[]]", "output": "[null,null,null,1.5,null,2.0]"},
        ],
        "approach": "中位数要动态维护“较小一半”与“较大一半”的平衡：左半放大顶堆、右半放小顶堆，两堆大小差不超过 1，这是堆 TopK 的对顶堆变体。新数按与左堆顶的比较入堆，再把较大一侧的堆顶搬给另一侧保持平衡。变化点在于左堆用负数模拟大顶堆，以及奇数个元素时中位数就是左堆顶。",
        "code": """import heapq

class MedianFinder:
    def __init__(self):
        self.left = []                          # 大顶堆（存负数），放较小一半
        self.right = []                         # 小顶堆，放较大一半

    def addNum(self, num):
        if not self.left or num <= -self.left[0]:
            heapq.heappush(self.left, -num)     # 变化点: 取负模拟大顶堆
        else:
            heapq.heappush(self.right, num)
        if len(self.left) > len(self.right) + 1:    # 变化点: 平衡两堆大小
            heapq.heappush(self.right, -heapq.heappop(self.left))
        elif len(self.left) < len(self.right):
            heapq.heappush(self.left, -heapq.heappop(self.right))

    def findMedian(self):
        if len(self.left) > len(self.right):
            return -self.left[0]
        return (-self.left[0] + self.right[0]) / 2""",
        "time": "addNum O(log n)，findMedian O(1)",
        "space": "O(n)",
        "pitfalls": [
            "左堆存负数模拟大顶堆，取出堆顶要再取负还原",
            "平衡目标是 len(left) == len(right) 或多 1，奇数个时中位数取左堆顶",
            "两堆都为空时 findMedian 无定义，题目保证调用前至少有一次 addNum",
        ],
    },
    125: {
        "statement": "给你两个二进制字符串 a 和 b，以二进制字符串的形式返回它们的和。输入串只含字符 0 和 1，且除 \"0\" 本身外不含前导零。",
        "examples": [
            {"input": "a = \"11\", b = \"1\"", "output": "\"100\""},
            {"input": "a = \"1010\", b = \"1011\"", "output": "\"10101\""},
        ],
        "approach": "两个二进制串长度可能不同，从末尾对齐逐位相加，进位作为状态带入下一位，兼有字符串扫描与按位模拟的特征。任一串没扫完或还有进位都要继续。变化点在于循环条件携带 carry，结果按低位到高位生成后要翻转拼接。",
        "code": """class Solution:
    def addBinary(self, a, b):
        i, j = len(a) - 1, len(b) - 1
        carry = 0
        res = []
        while i >= 0 or j >= 0 or carry:        # 变化点: carry 未清零也要继续
            total = carry
            if i >= 0:
                total += int(a[i])              # 变化点: 字符转数字逐位相加
                i -= 1
            if j >= 0:
                total += int(b[j])
                j -= 1
            res.append(str(total % 2))
            carry = total // 2
        return "".join(reversed(res))""",
        "time": "O(max(len(a), len(b)))",
        "space": "O(1)（不计结果串）",
        "pitfalls": [
            "两串长度不同，用各自下标扫描对齐，不能用 zip 截断",
            "循环条件必须包含 carry，否则最高位进位丢失",
            "res 从低位到高位生成，返回前要 reverse 再 join",
        ],
    },
    126: {
        "statement": "颠倒给定的 32 位无符号整数的二进制位。例如输入的二进制串 00000010100101000001111010011100，颠倒后为 00111001011110000010100101000000，对应整数 964176192。",
        "examples": [
            {"input": "n = 00000010100101000001111010011100（即 43261596）", "output": "964176192"},
            {"input": "n = 11111111111111111111111111111101（即 4294967293）", "output": "3221225471"},
        ],
        "approach": "把 32 位当成固定长度的位向量逐位搬运：每轮取 n 的最低位拼进结果，再把 n 右移一位，结果左移腾出低位。变化点在于 ans = (ans << 1) | (n & 1) 的拼接顺序，以及必须固定循环 32 次，让第一个被取出的位最终落到最高位。",
        "code": """class Solution:
    def reverseBits(self, n):
        ans = 0
        for _ in range(32):
            ans = (ans << 1) | (n & 1)          # 变化点: 取最低位拼到结果低位
            n >>= 1                             # 变化点: 固定 32 轮，高位 0 也要搬运
        return ans""",
        "time": "O(32) = O(1)",
        "space": "O(1)",
        "pitfalls": [
            "必须固定循环 32 次，提前以 n == 0 退出会把已吸收的位留在错误位置",
            "ans = (ans << 1) | (n & 1)：取位与移位的顺序写反会得到错误镜像",
            "Java/C++ 需用无符号类型接收，Python 天然大整数无此顾虑",
        ],
    },
    127: {
        "statement": "给定一个 32 位无符号整数 n，返回其二进制表示中 1 的个数（汉明重量）。",
        "examples": [
            {"input": "n = 00000000000000000000000000001011（即 11）", "output": "3"},
            {"input": "n = 11111111111111111111111111111101（即 4294967293）", "output": "31"},
        ],
        "approach": "n & (n-1) 会把最低位的 1 变成 0，每执行一次恰好消掉一个 1，循环次数就是 1 的个数。变化点在于用消位代替逐位检查与移位，循环次数恰好等于答案本身。",
        "code": """class Solution:
    def hammingWeight(self, n):
        cnt = 0
        while n:
            n &= n - 1                          # 变化点: 每轮消去最低位的 1
            cnt += 1
        return cnt""",
        "time": "O(k)，k 为 1 的个数，最坏 O(32)",
        "space": "O(1)",
        "pitfalls": [
            "while n 天然处理 n 为 0 的情况，直接返回 0",
            "消位法循环次数等于 1 的个数，比固定 32 次逐位检查更快",
            "输入是无符号 32 位整数，Python 中不会出现负数，无需补码处理",
        ],
    },
    128: {
        "statement": "给定一个非空整数数组 nums，除某个元素只出现一次外，其余每个元素均出现两次。找出那个只出现了一次的元素。要求线性时间复杂度且不使用额外空间。",
        "examples": [
            {"input": "nums = [2,2,1]", "output": "1"},
            {"input": "nums = [4,1,2,1,2]", "output": "4"},
        ],
        "approach": "成对出现的数异或后互相抵消为 0，全部异或一遍剩下的就是唯一数——异或消对的信号。变化点在于没有配对逻辑，一个循环全部异或即可，天然满足 O(n) 时间与 O(1) 空间。",
        "code": """class Solution:
    def singleNumber(self, nums):
        ans = 0
        for x in nums:
            ans ^= x                            # 变化点: 异或消对，成对元素抵消
        return ans""",
        "time": "O(n)",
        "space": "O(1)",
        "pitfalls": [
            "异或满足交换律与结合律，元素顺序不影响结果",
            "数组只有一个元素时循环一次返回它本身",
            "异或消对只适用于出现两次；出现三次要换逐位计数（见下一题）",
        ],
    },
    129: {
        "statement": "给定一个非空整数数组 nums，除某个元素只出现一次外，其余每个元素均出现三次。找出那个只出现了一次的元素。要求线性时间复杂度且不使用额外空间。",
        "examples": [
            {"input": "nums = [2,2,3,2]", "output": "3"},
            {"input": "nums = [0,1,0,1,0,1,99]", "output": "99"},
        ],
        "approach": "三个相同的数在每个二进制位上贡献的 1 都是 3 的倍数，唯一数会在每位留下余数，这是位计数信号。逐位统计所有数该位是 1 的次数并对 3 取模，余 1 则该位属于答案。变化点在于按 32 位逐位计数取模，最后还要把最高位为 1 的结果转回有符号负数。",
        "code": """class Solution:
    def singleNumber(self, nums):
        ans = 0
        for b in range(32):
            cnt = sum((x >> b) & 1 for x in nums)   # 变化点: 逐位统计 1 的个数
            if cnt % 3:                         # 变化点: 对 3 取模留下唯一数的该位
                ans |= 1 << b
        if ans >= 2 ** 31:                      # 变化点: 32 位无符号转回有符号
            ans -= 2 ** 32
        return ans""",
        "time": "O(32n)",
        "space": "O(1)",
        "pitfalls": [
            "负数也要参与统计：Python 的算术右移让 (x >> b) & 1 取到补码位",
            "统计结束后最高位为 1 时要减 2^32 转回有符号数，否则结果偏大",
            "两两异或的做法只适用于出现两次，出现三次必须按位计数取模",
        ],
    },
    130: {
        "statement": "给定整数区间 [left, right]，返回区间内所有数字按位与的结果（含 left 与 right 两个端点）。",
        "examples": [
            {"input": "left = 5, right = 7", "output": "4"},
            {"input": "left = 1, right = 2147483647", "output": "0"},
        ],
        "approach": "区间内不同的低位一定会被夹在中间的数抹成 0，按位与的结果只剩二进制公共前缀。不断把 left 与 right 同时右移直到相等，再按移位次数左移还原。变化点在于用 shift 记录被消去的低位个数，还原时左移同样的位数。",
        "code": """class Solution:
    def rangeBitwiseAnd(self, left, right):
        shift = 0
        while left < right:                     # 变化点: 消去低位直到留下公共前缀
            left >>= 1
            right >>= 1
            shift += 1
        return left << shift""",
        "time": "O(log C)，C 为区间长度",
        "space": "O(1)",
        "pitfalls": [
            "left == right 时不进循环，直接返回该值，注意初值不要被改坏",
            "区间最长可达 2^31，逐个按位与必然超时，只能走公共前缀",
            "shift 要在右移时同步累加，还原时左移同样的位数",
        ],
    },
    131: {
        "statement": "给你一个整数 x，如果 x 是回文整数，返回 true；否则返回 false。回文整数是正着读和反着读都一样的整数，例如 121 是回文，而 123 不是。负数一律不是回文。",
        "examples": [
            {"input": "x = 121", "output": "true"},
            {"input": "x = -121", "output": "false"},
        ],
        "approach": "负数与“非零的尾零数”必不是回文，先排除；再只反转一半数字与剩余前半比较，既不用字符串也不怕溢出，是按位模拟的变体。变化点在于循环条件 x > rev 控制只反转一半，比较时区分偶数位与奇数位（rev//10 丢弃中间位）。",
        "code": """class Solution:
    def isPalindrome(self, x):
        if x < 0 or (x % 10 == 0 and x != 0):   # 变化点: 负数与尾零数直接排除
            return False
        rev = 0
        while x > rev:                          # 变化点: 只反转一半
            rev = rev * 10 + x % 10
            x //= 10
        return x == rev or x == rev // 10       # 变化点: 奇数位丢弃中间位""",
        "time": "O(log₁₀ x)",
        "space": "O(1)",
        "pitfalls": [
            "10、100 这类尾零数不是回文，要先排除；0 本身是回文",
            "比较要兼顾偶数位与奇数位：x == rev 或 x == rev // 10",
            "不要反转整个数再比较，其他语言有溢出风险，也无谓多做一半功",
        ],
    },
    132: {
        "statement": "给定一个由整数组成的非空数组 digits，表示一个非负整数，最高位数字在数组开头。对该整数加一，并返回表示结果的数组。",
        "examples": [
            {"input": "digits = [1,2,3]", "output": "[1,2,4]"},
            {"input": "digits = [9]", "output": "[1,0]"},
        ],
        "approach": "整数按位存于数组，加一只需从末位向前处理进位：小于 9 的位加一即结束，等于 9 的位置 0 继续进位，是数学模拟的典型形。变化点在于用“提前返回”代替显式进位变量，全部为 9 时在头部补 1 扩一位。",
        "code": """class Solution:
    def plusOne(self, digits):
        for i in range(len(digits) - 1, -1, -1):    # 变化点: 从末位向前处理进位
            if digits[i] < 9:
                digits[i] += 1
                return digits                   # 变化点: 无进位即结束
            digits[i] = 0
        return [1] + digits                     # 变化点: 全 9 需扩一位""",
        "time": "O(n)",
        "space": "O(1)（全 9 时 O(n) 新数组）",
        "pitfalls": [
            "最高位在下标 0，必须从末位开始向前扫描",
            "遇小于 9 的位加一后立即返回，不要继续循环",
            "全 9 时要新建数组并在头部补 1，不能原地扩容",
        ],
    },
    133: {
        "statement": "给定一个整数 n，返回 n! 结果中尾随零的个数。例如 n = 5 时 5! = 120，尾随零个数为 1。要求不使用对数函数。",
        "examples": [
            {"input": "n = 3", "output": "0"},
            {"input": "n = 5", "output": "1"},
        ],
        "approach": "尾随零来自因子 10 = 2×5，而因子 2 的数量远多于 5，只需统计 5 的个数，是数学模拟的因子分析。每把 n 除以 5 一次，就把当前层提供的 5 全部计入，累加即为答案。变化点在于 n //= 5 的逐层累加，替代逐个数 O(n) 的扫描。",
        "code": """class Solution:
    def trailingZeroes(self, n):
        cnt = 0
        while n:
            n //= 5                             # 变化点: 逐层累加因子 5 的贡献
            cnt += n
        return cnt""",
        "time": "O(log₅ n)",
        "space": "O(1)",
        "pitfalls": [
            "只统计因子 5 的个数，2 的数量永远足够",
            "25、125 提供多个 5，必须逐层累加而不是单次 n//5",
            "n 为 0 时直接返回 0，循环体不执行",
        ],
    },
    134: {
        "statement": "给你一个非负整数 x，计算并返回 x 的算术平方根的整数部分（只保留整数部分，舍去小数部分）。不允许使用任何内置指数函数和幂运算符，如 pow(x, 0.5) 或 x ** 0.5。",
        "examples": [
            {"input": "x = 4", "output": "2"},
            {"input": "x = 8", "output": "2"},
        ],
        "approach": "平方根整数部分对 mid 具有单调性：mid² ≤ x 则可行，否则偏大，可对答案空间做左闭右开二分。找第一个 mid² > x 的位置再减一，即为整数平方根。变化点在于二分对象是“答案 + 1”，判定条件换成平方与 x 的比较。",
        "code": """class Solution:
    def mySqrt(self, x):
        left, right = 1, x + 1                  # 变化点: 对答案空间二分
        while left < right:
            mid = (left + right) // 2
            if mid * mid <= x:                  # 变化点: 平方判定代替值比较
                left = mid + 1
            else:
                right = mid
        return left - 1                         # 变化点: 第一个 mid²>x 的位置减一""",
        "time": "O(log x)",
        "space": "O(1)",
        "pitfalls": [
            "返回的是第一个 mid² > x 的位置减一，别忘 -1",
            "x = 0 时区间为空直接返回 0",
            "用整数平方比较，不要用浮点开方（大数精度丢失）",
        ],
    },
    135: {
        "statement": "实现 pow(x, n)，即计算 x 的 n 次幂函数（x 为浮点数，n 为整数，可能为负）。不允许使用库函数 pow，且时间复杂度需低于 O(n)。",
        "examples": [
            {"input": "x = 2.0, n = 10", "output": "1024.0"},
            {"input": "x = 2.0, n = -2", "output": "0.25"},
        ],
        "approach": "x^n = (x^(n/2))²，n 为奇数再补乘一个 x，是分治快速幂的信号；负指数先转成 1/x 的正指数幂。变化点在于递归按 exp//2 折半、返回前平方，再按指数奇偶补乘底数，指数每轮砍半只需 O(log n) 层。",
        "code": """class Solution:
    def myPow(self, x, n):
        if n < 0:
            x, n = 1 / x, -n                    # 变化点: 负指数转倒数
        def qpow(base, exp):
            if exp == 0:
                return 1.0
            half = qpow(base, exp // 2)         # 变化点: 指数折半递归
            return half * half * (base if exp % 2 else 1)   # 变化点: 平方后按奇偶补乘
        return qpow(x, n)""",
        "time": "O(log n)",
        "space": "O(log n) 递归栈",
        "pitfalls": [
            "负指数先转 1/x；Python 中 -2^31 取负不会溢出，其他语言要防",
            "递归按 exp//2 折半，奇数轮补乘一次底数，别写成乘两次",
            "x 为 0 且 n 为负的场景题目保证不出现，无需特判",
        ],
    },
    136: {
        "statement": "给你一个点集 points，其中 points[i] = [xi, yi] 表示 X-Y 平面上的一个点。求同一条直线上最多有多少个点。本题保证所有给定的点互不相同。",
        "examples": [
            {"input": "points = [[1,1],[2,2],[3,3]]", "output": "3"},
            {"input": "points = [[1,1],[3,2],[5,3],[4,1],[2,3],[1,4]]", "output": "4"},
        ],
        "approach": "同一直线上的点相对同一锚点的方向向量成比例，浮点斜率有除零与精度双重风险，改用 gcd 约分后的最简整数对作哈希键。以每个点为锚点统计各方向的点数，取最大值加上锚点自身。变化点在于用最简整数方向对替代除法斜率，这正是数学模拟里的约分技巧。",
        "code": """from collections import defaultdict
from math import gcd

class Solution:
    def maxPoints(self, points):
        n = len(points)
        if n <= 2:
            return n
        best = 0
        for i in range(n):                      # 变化点: 以每个点为锚点统计方向
            x1, y1 = points[i]
            slopes = defaultdict(int)
            for j in range(n):
                if j == i:
                    continue
                dx, dy = points[j][0] - x1, points[j][1] - y1
                g = gcd(dx, dy)                 # 变化点: gcd 约分成最简整数对作键
                slopes[(dx // g, dy // g)] += 1
            best = max(best, max(slopes.values()) + 1)  # 变化点: 补上锚点自身
        return best""",
        "time": "O(n² log C)",
        "space": "O(n)",
        "pitfalls": [
            "浮点斜率有除零（竖线）与精度双重风险，必须用整数方向对作键",
            "gcd 约分要求两点不重合，本题保证点互异；若允许重合需单独计数",
            "答案是某锚点下最大方向计数 + 1，最后别忘了补锚点自身",
        ],
    },
    137: {
        "statement": "假设你正在爬楼梯，需要 n 阶才能到达楼顶。每次可以爬 1 或 2 个台阶，问有多少种不同的方法可以爬到楼顶。",
        "examples": [
            {"input": "n = 2", "output": "2"},
            {"input": "n = 3", "output": "3"},
        ],
        "approach": "到达第 i 阶只能从第 i-1 阶跨一步或第 i-2 阶跨两步，dp[i] = dp[i-1] + dp[i-2]，是线性 DP 的最简形态。dp[0] = dp[1] = 1，后项只依赖前两项。变化点在于用两个滚动变量代替数组，空间压到 O(1)。",
        "code": """class Solution:
    def climbStairs(self, n):
        prev, cur = 1, 1                        # dp[0] = dp[1] = 1
        for _ in range(2, n + 1):
            prev, cur = cur, prev + cur         # 变化点: dp[i] = dp[i-1] + dp[i-2]
        return cur""",
        "time": "O(n)",
        "space": "O(1)",
        "pitfalls": [
            "dp[0] = dp[1] = 1：到达第 0、1 阶都只有一种方式",
            "滚动变量更新必须一行完成 prev, cur = cur, prev + cur",
            "n = 1 时循环不执行，直接返回初值 cur",
        ],
    },
}
