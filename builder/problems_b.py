# -*- coding: utf-8 -*-
"""题解数据 34-67：矩阵 / 哈希表 / 区间 / 栈 / 链表。"""

DATA = {
    34: {
        "statement": "请判断一个 9 x 9 的数独是否有效。只需要根据以下规则验证已填入的数字：数字 1-9 在每一行只能出现一次；在每一列只能出现一次；在每一个以粗实线分隔的 3x3 宫内只能出现一次。棋盘中空白格用 '.' 表示，数独不必可解，只要已填入的数字不违反上述规则即有效。",
        "examples": [
            {"input": "board = [[\"5\",\"3\",\".\",\".\",\"7\",\".\",\".\",\".\",\".\"],[\"6\",\".\",\".\",\"1\",\"9\",\"5\",\".\",\".\",\".\"],[\".\",\"9\",\"8\",\".\",\".\",\".\",\".\",\"6\",\".\"],[\"8\",\".\",\".\",\".\",\"6\",\".\",\".\",\".\",\"3\"],[\"4\",\".\",\".\",\"8\",\".\",\"3\",\".\",\".\",\"1\"],[\"7\",\".\",\".\",\".\",\"2\",\".\",\".\",\".\",\"6\"],[\".\",\"6\",\".\",\".\",\".\",\".\",\"2\",\"8\",\".\"],[\".\",\".\",\".\",\"4\",\"1\",\"9\",\".\",\".\",\"5\"],[\".\",\".\",\".\",\".\",\"8\",\".\",\".\",\"7\",\"9\"]]", "output": "true"},
            {"input": "同上，但 board[0][0] 由 \"5\" 改为 \"8\"（第 0 列与左上 3×3 宫内出现两个 8）", "output": "false"},
        ],
        "approach": "行、列、宫三个维度都要查重，是哈希映射的信号：为每行、每列、每宫各配一个集合，扫描棋盘时对已填数字同时检查三张表。变化点在下标折算——宫编号 b = (i//3)*3 + j//3，以及 '.' 空格直接跳过。",
        "code": """class Solution:
    def isValidSudoku(self, board):
        rows = [set() for _ in range(9)]
        cols = [set() for _ in range(9)]
        boxes = [set() for _ in range(9)]
        for i in range(9):
            for j in range(9):
                ch = board[i][j]
                if ch == ".":
                    continue
                b = (i // 3) * 3 + j // 3           # 变化点: 行列下标折算出宫编号
                if ch in rows[i] or ch in cols[j] or ch in boxes[b]:
                    return False                    # 变化点: 行、列、宫三张表同时查重
                rows[i].add(ch)
                cols[j].add(ch)
                boxes[b].add(ch)
        return True""",
        "time": "O(1)（棋盘固定 9×9）",
        "space": "O(1)",
        "pitfalls": [
            "宫编号公式 (i//3)*3 + j//3 别写错，写成 i//3*2 之类会漏检",
            "'.' 必须跳过，把空格当数字加入集合会误判",
            "本题只查已填数字的重复，不需要验证数独可解；行、列、宫要用三张独立的表",
        ],
    },
    35: {
        "statement": "给你一个 m 行 n 列的矩阵 matrix，请按照顺时针螺旋顺序（从左上角开始，沿右、下、左、上方向层层向内）返回矩阵中的所有元素。",
        "examples": [
            {"input": "matrix = [[1,2,3],[4,5,6],[7,8,9]]", "output": "[1,2,3,6,9,8,7,4,5]"},
            {"input": "matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]", "output": "[1,2,3,4,8,12,11,10,9,5,6,7]"},
        ],
        "approach": "按螺旋顺序输出全部元素，是矩阵模拟的边界收缩信号：维护 top/bottom/left/right 四条边界，每圈按 右→下→左→上 四段循环输出，结束后边界同步向内收缩。变化点在单行、单列时必须跳过底行和左列，否则同一元素会被输出两次。",
        "code": """class Solution:
    def spiralOrder(self, matrix):
        top, bottom = 0, len(matrix) - 1
        left, right = 0, len(matrix[0]) - 1
        res = []
        while top <= bottom and left <= right:
            for j in range(left, right + 1):
                res.append(matrix[top][j])
            for i in range(top + 1, bottom + 1):
                res.append(matrix[i][right])
            if top < bottom:                        # 变化点: 单行时跳过底行，防止重复输出
                for j in range(right - 1, left - 1, -1):
                    res.append(matrix[bottom][j])
            if top < bottom and left < right:       # 变化点: 单列时跳过左列，防止重复输出
                for i in range(bottom - 1, top, -1):
                    res.append(matrix[i][left])
            top += 1                                # 变化点: 四条边界每圈同步向内收缩
            bottom -= 1
            left += 1
            right -= 1
        return res""",
        "time": "O(mn)",
        "space": "O(1)（输出数组不计入）",
        "pitfalls": [
            "单行单列的矩阵必须跳过后两段遍历，否则会把同一行或列输出两次",
            "四段遍历都是左闭右闭区间，第一段从 left 到 right，第二段从 top+1 开始避免重读角元素",
            "循环条件是 top <= bottom 且 left <= right，收缩写在循环末尾统一做",
        ],
    },
    36: {
        "statement": "给定一个 n × n 的二维矩阵 matrix 表示一幅图像，请你将图像顺时针旋转 90 度。必须在原地旋转图像，即直接修改输入的二维矩阵，不要使用另一个矩阵来旋转图像。",
        "examples": [
            {"input": "matrix = [[1,2,3],[4,5,6],[7,8,9]]", "output": "返回 null，matrix 变为 [[7,4,1],[8,5,2],[9,6,3]]"},
            {"input": "matrix = [[5,1,9,11],[2,4,8,10],[13,3,6,7],[15,14,12,16]]", "output": "返回 null，matrix 变为 [[15,13,2,5],[14,3,4,1],[12,6,8,9],[16,7,10,11]]"},
        ],
        "approach": "原地旋转 90° 是矩阵模拟的坐标变换信号：顺时针旋转 90° 等价于先沿主对角线转置、再把每一行左右翻转，两步都能原地完成。变化点在转置只遍历上三角（j 从 i+1 开始），全矩阵交换会互相抵消。",
        "code": """class Solution:
    def rotate(self, matrix):
        n = len(matrix)
        for i in range(n):
            for j in range(i + 1, n):
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]     # 变化点: 沿主对角线转置，只走上三角
        for row in matrix:
            row.reverse()                           # 变化点: 再逐行左右翻转，得到顺时针 90°""",
        "time": "O(n²)",
        "space": "O(1)",
        "pitfalls": [
            "转置只能遍历上三角，j 从 0 开始会让每个元素被交换两次、矩阵回到原样",
            "顺序必须是先转置后左右翻转；先翻转再转置得到的是逆时针旋转",
            "题目要求原地操作，不能用新建矩阵接住结果再赋值回去",
        ],
    },
    37: {
        "statement": "给定一个 m x n 的矩阵 matrix，如果一个元素为 0，则将其所在行和列的所有元素都设为 0。请使用原地算法，尽量减少额外空间的使用。",
        "examples": [
            {"input": "matrix = [[1,1,1],[1,0,1],[1,1,1]]", "output": "返回 null，matrix 变为 [[1,0,1],[0,0,0],[1,0,1]]"},
            {"input": "matrix = [[0,1,2,0],[3,4,5,2],[1,3,1,5]]", "output": "返回 null，matrix 变为 [[0,0,0,0],[0,4,5,0],[0,3,1,0]]"},
        ],
        "approach": "置零且空间要求 O(1)，是矩阵模拟的原地标记信号：借用首行、首列充当标记数组，内部出现 0 就把对应行首与列首写成 0。变化点在三处——先记录首行首列自身是否本来就含 0，内部打标记，最后单独清理首行与首列。",
        "code": """class Solution:
    def setZeroes(self, matrix):
        m, n = len(matrix), len(matrix[0])
        first_row = any(matrix[0][j] == 0 for j in range(n))
        first_col = any(matrix[i][0] == 0 for i in range(m))    # 变化点: 先记录首行首列自身是否含 0
        for i in range(1, m):
            for j in range(1, n):
                if matrix[i][j] == 0:
                    matrix[i][0] = matrix[0][j] = 0             # 变化点: 内部 0 写入行首列首作标记
        for i in range(1, m):
            for j in range(1, n):
                if matrix[i][0] == 0 or matrix[0][j] == 0:
                    matrix[i][j] = 0
        if first_row:
            for j in range(n):
                matrix[0][j] = 0
        if first_col:                                           # 变化点: 最后单独清理首行首列
            for i in range(m):
                matrix[i][0] = 0""",
        "time": "O(mn)",
        "space": "O(1)",
        "pitfalls": [
            "首行首列是否本身含 0 必须在打标记之前用两个布尔记录，否则标记会把它们污染",
            "打标记和按标记置零都只处理内部区域（1..m-1, 1..n-1），首行首列单独收尾",
            "直接边扫边置零会让后续读到的 0 是污染值，必须先标记后统一置零",
        ],
    },
    38: {
        "statement": "给定一个 m x n 的棋盘 board，每个格子的状态由 0（死细胞）或 1（活细胞）表示。按康威生命游戏规则同时更新所有细胞：活细胞周围活邻居少于 2 个或超过 3 个则死亡；恰有 2 或 3 个活邻居则存活；死细胞恰有 3 个活邻居则复活。要求使用原地算法，不使用额外矩阵。",
        "examples": [
            {"input": "board = [[0,1,0],[0,0,1],[1,1,1],[0,0,0]]", "output": "返回 null，board 变为 [[0,0,0],[1,0,1],[0,1,1],[0,1,0]]"},
            {"input": "board = [[1,1],[1,0]]", "output": "返回 null，board 变为 [[1,1],[1,1]]"},
        ],
        "approach": "所有格子要按旧状态同时更新，是矩阵模拟的状态编码信号：用 -1 表示“旧活新死”、2 表示“旧死新活”，遍历时用 abs(值) == 1 判断旧状态是否为活。变化点在先打标记再第二遍统一恢复，数邻居时排除自身并处理越界。",
        "code": """class Solution:
    def gameOfLife(self, board):
        m, n = len(board), len(board[0])
        for i in range(m):
            for j in range(n):
                live = 0
                for di in (-1, 0, 1):
                    for dj in (-1, 0, 1):
                        if di == 0 and dj == 0:
                            continue
                        ni, nj = i + di, j + dj
                        if 0 <= ni < m and 0 <= nj < n and abs(board[ni][nj]) == 1:
                            live += 1               # 变化点: abs==1 读的是旧状态
                if board[i][j] == 1 and (live < 2 or live > 3):
                    board[i][j] = -1                # 变化点: -1 表示“旧活新死”
                elif board[i][j] == 0 and live == 3:
                    board[i][j] = 2                 # 变化点: 2 表示“旧死新活”
        for i in range(m):
            for j in range(n):
                board[i][j] = 1 if board[i][j] > 0 else 0""",
        "time": "O(mn)",
        "space": "O(1)",
        "pitfalls": [
            "不能边遍历边改：新值会污染邻居的统计，必须用 -1/2 编码旧状态做两遍",
            "数邻居要排除自身 (di==0 and dj==0)，并做越界检查",
            "恢复时按旧状态映射：>0（1 或 2）为活，否则为死",
        ],
    },
    39: {
        "statement": "给你两个字符串 ransomNote 和 magazine，判断 ransomNote 能不能由 magazine 里面的字符构成。如果可以，返回 true；否则返回 false。magazine 中的每个字符只能在 ransomNote 中使用一次。",
        "examples": [
            {"input": "ransomNote = \"a\", magazine = \"b\"", "output": "false"},
            {"input": "ransomNote = \"aa\", magazine = \"aab\"", "output": "true"},
        ],
        "approach": "判断字符串能否由另一串的字符拼出，是计数统计的信号：magazine 先建 26 位计数数组，ransomNote 再逐字扣减。变化点在扣减后一旦出现负数即库存不足，立即返回 False，不必统计完再整体比较。",
        "code": """class Solution:
    def canConstruct(self, ransomNote, magazine):
        cnt = [0] * 26                          # 变化点: 小写字母集用 26 位数组计数
        for ch in magazine:
            cnt[ord(ch) - ord('a')] += 1
        for ch in ransomNote:
            idx = ord(ch) - ord('a')
            cnt[idx] -= 1
            if cnt[idx] < 0:                    # 变化点: 扣成负数说明库存不足
                return False
        return True""",
        "time": "O(n+m)",
        "space": "O(1)（26 位计数数组）",
        "pitfalls": [
            "必须先统计 magazine 再扣减 ransomNote，方向反了扣减时计数还是 0",
            "扣减后小于 0 就该返回 False，别等循环结束再逐位比较",
            "下标换算是 ord(ch) - ord('a')，两个字符串都要换算",
        ],
    },
    40: {
        "statement": "给定两个字符串 s 和 t，判断它们是否同构。如果 s 中的字符可以被替换得到 t，那么这两个字符串是同构的：所有出现的字符都必须被替换，同时保留字符的顺序；两个字符不能映射到同一个字符上，但字符可以映射到自己。",
        "examples": [
            {"input": "s = \"egg\", t = \"add\"", "output": "true"},
            {"input": "s = \"foo\", t = \"bar\"", "output": "false"},
        ],
        "approach": "字符要一一对应且不冲突，是哈希映射双向映射的信号：同时维护 s→t 与 t→s 两张表，逐对字符校验既有映射值是否一致。变化点在双向同时检查——单向映射会把 badc/baba 这类“两个字符映射到同一字符”误判为同构。",
        "code": """class Solution:
    def isIsomorphic(self, s, t):
        s2t = {}
        t2s = {}
        for a, b in zip(s, t):
            if s2t.get(a, b) != b or t2s.get(b, a) != a:    # 变化点: 双向映射同时校验，防多对一
                return False
            s2t[a] = b
            t2s[b] = a
        return True""",
        "time": "O(n)",
        "space": "O(n)（字符集大小）",
        "pitfalls": [
            "必须双向映射：只建 s→t 会漏掉 t 中两个字符映射到同一字符的情况",
            "用 get(键, 本轮值) 的默认值技巧，映射缺失时视为可建立新映射",
            "题目保证 len(s) == len(t)，zip 直接配对即可；通用写法可先比长度",
        ],
    },
    41: {
        "statement": "给定一种规律 pattern 和一个字符串 s，判断 s 是否遵循相同的规律。这里的遵循指完全匹配：pattern 中每个字母与 s 中每个非空单词之间存在双向连接的对应规律。s 由小写字母和空格组成，单词之间用单个空格分隔。",
        "examples": [
            {"input": "pattern = \"abba\", s = \"dog cat cat dog\"", "output": "true"},
            {"input": "pattern = \"abba\", s = \"dog cat cat fish\"", "output": "false"},
        ],
        "approach": "pattern 的字母与 s 的单词要构成双向对应，仍是哈希映射的双向映射信号：先 split 出单词并与 pattern 对齐数量，再逐对复用双向校验。变化点在映射对象从字符换成单词，以及扫描前先检查数量是否一致。",
        "code": """class Solution:
    def wordPattern(self, pattern, s):
        words = s.split()
        if len(words) != len(pattern):          # 变化点: 先对齐单词数与字母数
            return False
        c2w = {}
        w2c = {}
        for ch, w in zip(pattern, words):
            if c2w.get(ch, w) != w or w2c.get(w, ch) != ch:     # 变化点: 字母↔单词双向校验
                return False
            c2w[ch] = w
            w2c[w] = ch
        return True""",
        "time": "O(n)",
        "space": "O(n)",
        "pitfalls": [
            "数量不等必须先返回：单词多或字母多都无法一一对应",
            "双向映射缺一不可，\"abba\"/\"dog dog dog dog\" 就是靠 w2c 拦下的",
            "用 split() 不带参数可以容忍连续空格；split(' ') 会切出空串导致错位",
        ],
    },
    42: {
        "statement": "给定两个字符串 s 和 t，编写一个函数来判断 t 是否是 s 的字母异位词，即两个字符串包含的字母及各字母数量完全相同（仅顺序可能不同）。进阶：如果输入字符串包含 Unicode 字符该怎么办？",
        "examples": [
            {"input": "s = \"anagram\", t = \"nagaram\"", "output": "true"},
            {"input": "s = \"rat\", t = \"car\"", "output": "false"},
        ],
        "approach": "判断是否互为异位词，是计数统计的信号：26 位计数数组对 s 累加、对 t 扣减，全部扣减后不出现负数即为异位词。变化点在长度不等可提前返回，以及扣减中一旦出现负数立即判负。",
        "code": """class Solution:
    def isAnagram(self, s, t):
        if len(s) != len(t):                    # 变化点: 长度不等直接剪枝
            return False
        cnt = [0] * 26
        for ch in s:
            cnt[ord(ch) - ord('a')] += 1
        for ch in t:
            idx = ord(ch) - ord('a')
            cnt[idx] -= 1
            if cnt[idx] < 0:                    # 变化点: 任何字母透支即不是异位词
                return False
        return True""",
        "time": "O(n)",
        "space": "O(1)（26 位计数数组）",
        "pitfalls": [
            "长度不等的字符串不可能是异位词，先比长度可省一次遍历",
            "26 位数组只适用小写字母；含 Unicode 时改用字典计数（Counter）",
            "只比较计数集合（各字母是否出现）不够，数量也要一致",
        ],
    },
    43: {
        "statement": "给你一个字符串数组 strs，请你将字母异位词组合在一起。字母异位词是由重新排列源单词的所有字母得到的新单词，返回结果列表可以按任意顺序排列。",
        "examples": [
            {"input": "strs = [\"eat\", \"tea\", \"tan\", \"ate\", \"nat\", \"bat\"]", "output": "[[\"bat\"],[\"nat\",\"tan\"],[\"ate\",\"eat\",\"tea\"]]"},
            {"input": "strs = [\"\"]", "output": "[[\"\"]]]"},
        ],
        "approach": "把互为异位词的单词收进同一组，是哈希映射分组的信号：为每个单词求一个规范形作 key，value 是该组的单词列表。变化点在 key 的选取——排序后的字符串（也可用 26 位计数的元组），setdefault 一次完成收集。",
        "code": """class Solution:
    def groupAnagrams(self, strs):
        groups = {}
        for s in strs:
            key = "".join(sorted(s))            # 变化点: 排序后的字符串作分组键
            groups.setdefault(key, []).append(s)    # 变化点: 键不存在则建组，存在则追加
        return list(groups.values())""",
        "time": "O(n·k log k)（k 为单词平均长度）",
        "space": "O(n·k)",
        "pitfalls": [
            "不能用原字符串当 key，否则同组异位词会被拆开",
            "除排序字符串外，也可把 26 位计数转成元组当 key，避免排序开销",
            "返回值只需同组元素聚在一起，组与组的顺序、组内顺序都不限",
        ],
    },
    44: {
        "statement": "给定一个整数数组 nums 和一个整数目标值 target，请在该数组中找出和为目标值 target 的那两个整数，并返回它们的数组下标。你可以假设每种输入只会对应一个答案，同一个元素不能被重复使用，可以按任意顺序返回答案。",
        "examples": [
            {"input": "nums = [2,7,11,15], target = 9", "output": "[0,1]"},
            {"input": "nums = [3,2,4], target = 6", "output": "[1,2]"},
        ],
        "approach": "在无序数组里为当前值找配对，是哈希映射“先查再存”的信号：遍历时先查补数 target - x 是否出现过，命中即返回两个下标。变化点在 key/value 的语义——值到下标的映射，以及先查后存的顺序避免自己配自己。",
        "code": """class Solution:
    def twoSum(self, nums, target):
        seen = {}
        for i, x in enumerate(nums):
            if target - x in seen:              # 变化点: 先查“补数”是否出现过
                return [seen[target - x], i]
            seen[x] = i                         # 变化点: 值 -> 下标的映射语义
        return []""",
        "time": "O(n)",
        "space": "O(n)",
        "pitfalls": [
            "先查补数再存当前值，顺序颠倒会出现同一元素配自己",
            "返回 [seen[补数], i]，先出现的下标在前",
            "题目保证有唯一解，兜底返回空列表仅为语法完整",
        ],
    },
    45: {
        "statement": "编写一个算法来判断一个正整数 n 是不是快乐数。快乐数定义为：反复将这个数替换为它每个位置上的数字的平方和，最终能变为 1；如果无限循环（始终变不到 1），则不是快乐数。如果 n 是快乐数就返回 true，否则返回 false。",
        "examples": [
            {"input": "n = 19", "output": "true（19 → 82 → 68 → 100 → 1）"},
            {"input": "n = 2", "output": "false（4 → 16 → 37 → … 无限循环）"},
        ],
        "approach": "不断替换为下一个数并判断是否无限循环，是快慢指针的信号：把“数位平方和”看成链表的 next，slow 每走一步、fast 每走两步，相遇即成环。变化点在判定条件——fast 在路上先到 1 就是快乐数，相遇且值不是 1 则不是。",
        "code": """class Solution:
    def _next(self, n):
        total = 0
        while n:
            d = n % 10
            total += d * d
            n //= 10
        return total

    def isHappy(self, n):
        slow, fast = n, self._next(n)           # 变化点: fast 先走一步与 slow 错开
        while fast != 1 and slow != fast:
            slow = self._next(slow)
            fast = self._next(self._next(fast))     # 变化点: fast 每次走两步
        return fast == 1                            # 变化点: 在路上先到 1 即快乐数""",
        "time": "O(log n)（数位平方和迅速收敛）",
        "space": "O(1)",
        "pitfalls": [
            "不是快乐数时序列进入循环而不是发散到无穷，判环与判 1 等价",
            "fast 初值取 _next(n) 而不是 n，否则 n=1 时两指针起点相同会误判",
            "循环条件要在 fast == 1 或 slow == fast 时退出，别写成 while True 内部判",
        ],
    },
    46: {
        "statement": "给你一个整数数组 nums 和一个整数 k，判断数组中是否存在两个不同的下标 i 和 j，满足 nums[i] == nums[j] 且 abs(i - j) <= k。如果存在，返回 true；否则返回 false。",
        "examples": [
            {"input": "nums = [1,2,3,1], k = 3", "output": "true"},
            {"input": "nums = [1,2,3,1,2,3], k = 2", "output": "false"},
        ],
        "approach": "判断重复元素的下标距离是否不超过 k，可以用哈希映射维护每个值最近一次出现的下标——等价于一个长度为 k 的窗口内查重。逐个比较 i - last[x]，命中即返回。变化点在只存最近位置、先判断后更新。",
        "code": """class Solution:
    def containsNearbyDuplicate(self, nums, k):
        last = {}
        for i, x in enumerate(nums):
            if x in last and i - last[x] <= k:  # 变化点: 与最近一次出现的下标比距离
                return True
            last[x] = i                         # 变化点: 只保留最近位置，先判断后更新
        return False""",
        "time": "O(n)",
        "space": "O(n)",
        "pitfalls": [
            "哈希表只存每个值最近一次出现的下标，更早的位置不需要保留",
            "必须先判断再更新 last[x]，先更新会把 i - last[x] 算成 0",
            "距离判定用当前下标减旧下标，两个下标天然不同，无需排除相等",
        ],
    },
    47: {
        "statement": "给定一个未排序的整数数组 nums，找出数字连续的最长序列（序列元素在原数组中不需要连续排列）的长度。请你设计并实现时间复杂度为 O(n) 的算法解决此问题。",
        "examples": [
            {"input": "nums = [100,4,200,1,3,2]", "output": "4（最长连续序列是 [1,2,3,4]）"},
            {"input": "nums = [0,3,7,2,5,8,4,6,0,1]", "output": "9"},
        ],
        "approach": "求最长连续序列且要求 O(n)，是哈希映射（集合）的信号：数字放进集合去重，只对“没有左邻居 x-1”的连续段起点向右扩展计数。变化点在起点判断——其余元素一律跳过，保证每段只被扫一次、总时间线性。",
        "code": """class Solution:
    def longestConsecutive(self, nums):
        num_set = set(nums)
        best = 0
        for x in num_set:
            if x - 1 in num_set:                # 变化点: 有左邻居就不是段起点，跳过
                continue
            cur, length = x, 1
            while cur + 1 in num_set:           # 变化点: 只从段起点向右扩展
                cur += 1
                length += 1
            best = max(best, length)
        return best""",
        "time": "O(n)",
        "space": "O(n)",
        "pitfalls": [
            "先 set() 去重，否则重复元素会重复触发起点判断",
            "没有“x-1 不在集合”的判断会退化成 O(n²)，这是本题 O(n) 的关键",
            "空数组返回 0，best 初值为 0 而不是 1",
        ],
    },
    48: {
        "statement": "给定一个按非递减顺序排列的整数数组 nums（无重复元素），返回恰好覆盖数组中所有数字的最小有序区间范围列表。也就是说，nums 的每个元素都恰好被某个区间范围所覆盖，且不存在属于某个范围但不属于 nums 的数字。每个区间 [a,b] 应输出为 \"a->b\"，单个数字 [a] 输出为 \"a\"。",
        "examples": [
            {"input": "nums = [0,1,2,4,5,7]", "output": "[\"0->2\",\"4->5\",\"7\"]"},
            {"input": "nums = [0,2,3,4,6,8,9]", "output": "[\"0\",\"2->4\",\"6\",\"8->9\"]"},
        ],
        "approach": "把升序数组切成连续段，是区间贪心的信号：线性扫描，相邻差 1 就延伸当前区间，否则结算上一段并开启新区间。变化点在连续判定 nums[i+1] == nums[i] + 1，以及单点、跨段两种输出格式的拼接。",
        "code": """class Solution:
    def summaryRanges(self, nums):
        res = []
        i, n = 0, len(nums)
        while i < n:
            start = i
            while i + 1 < n and nums[i + 1] == nums[i] + 1:     # 变化点: 相邻差 1 则延伸区间
                i += 1
            if start == i:
                res.append(str(nums[start]))    # 变化点: 单点与跨段两种格式
            else:
                res.append("%d->%d" % (nums[start], nums[i]))
            i += 1
        return res""",
        "time": "O(n)",
        "space": "O(1)（不计输出）",
        "pitfalls": [
            "内层先判 i + 1 < n 再取 nums[i+1]，防止越界",
            "单点区间输出 \"a\" 而不是 \"a->a\"，用 start == i 区分",
            "拼接要用 str / 格式化，直接 append 数字会类型错误",
        ],
    },
    49: {
        "statement": "以数组 intervals 表示若干个区间的集合，其中单个区间为 intervals[i] = [start_i, end_i]。请你合并所有重叠的区间，并返回一个不重叠的区间数组，该数组需恰好覆盖输入中的所有区间。",
        "examples": [
            {"input": "intervals = [[1,3],[2,6],[8,10],[15,18]]", "output": "[[1,6],[8,10],[15,18]]"},
            {"input": "intervals = [[1,4],[4,5]]", "output": "[[1,5]]"},
        ],
        "approach": "合并重叠区间是区间贪心的信号：先按左端点排序，再线性扫描，当前起点不超过上一结果的右端就合并。变化点在合并时右端取 max——被合并区间的右端可能比当前结果更长，不能直接覆盖。",
        "code": """class Solution:
    def merge(self, intervals):
        intervals.sort(key=lambda x: x[0])      # 变化点: 按左端点排序
        res = []
        for start, end in intervals:
            if res and start <= res[-1][1]:
                res[-1][1] = max(res[-1][1], end)   # 变化点: 重叠则扩张右端，取 max
            else:
                res.append([start, end])
        return res""",
        "time": "O(n log n)",
        "space": "O(n)",
        "pitfalls": [
            "排序后只需比较当前起点与上一区间的右端，无需两两比较",
            "相接也算重叠：[1,4] 与 [4,5] 的 4 相等要合并，判定用 <= 而非 <",
            "合并右端必须取 max，直接赋 end 会丢掉更长的右边界",
        ],
    },
    50: {
        "statement": "给你一个无重叠的、按照区间起始端点排序的区间列表 intervals，其中 intervals[i] = [start_i, end_i]。再给你一个新区间 newInterval，你需要将 newInterval 插入列表中，使得列表中的所有区间仍然按起始端点排序且互不重叠。必要时可以合并相邻甚至重叠的区间，直接返回插入后的区间列表即可。",
        "examples": [
            {"input": "intervals = [[1,3],[6,9]], newInterval = [2,5]", "output": "[[1,5],[6,9]]"},
            {"input": "intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]], newInterval = [4,8]", "output": "[[1,2],[3,10],[12,16]]"},
        ],
        "approach": "往有序无重叠区间中插入新区间，是区间贪心的三段式信号：先把起点之前完全不重叠的区间放入结果，再逐个合并与新区间重叠的部分，最后接回剩余区间。变化点在合并循环的条件 intervals[i][0] <= newInterval[1]（相接也算重叠），以及 newInterval 的就地扩张。",
        "code": """class Solution:
    def insert(self, intervals, newInterval):
        res = []
        i, n = 0, len(intervals)
        while i < n and intervals[i][1] < newInterval[0]:   # 变化点: 左侧完全不重叠的直接放入
            res.append(intervals[i])
            i += 1
        while i < n and intervals[i][0] <= newInterval[1]:  # 变化点: 与新区间重叠的逐个合并
            newInterval[0] = min(newInterval[0], intervals[i][0])
            newInterval[1] = max(newInterval[1], intervals[i][1])
            i += 1
        res.append(newInterval)
        while i < n:                                        # 变化点: 右侧剩余接回
            res.append(intervals[i])
            i += 1
        return res""",
        "time": "O(n)",
        "space": "O(n)",
        "pitfalls": [
            "三段缺一不可：只合并不接尾部会把右侧区间弄丢",
            "左侧过滤用 intervals[i][1] < 新区间起点，合并判定用 intervals[i][0] <= 新区间终点",
            "合并过程中 newInterval 就地扩张即可，不需要复制每个旧区间",
        ],
    },
    51: {
        "statement": "气球用水平方向上的区间表示：points[i] = [start_i, end_i]。一支箭沿 x 轴垂直射出，如果一支箭的坐标为 x，凡满足 start_i ≤ x ≤ end_i 的气球都会被引爆（端点相切也算命中）。射爆所有气球所需弓箭的最小数量是多少？",
        "examples": [
            {"input": "points = [[10,16],[2,8],[1,6],[7,12]]", "output": "2（x=6 引爆前三个，x=12 引爆最后一个）"},
            {"input": "points = [[1,2],[3,4],[5,6],[7,8]]", "output": "4"},
        ],
        "approach": "最少箭数等价于最多不重叠区间数，是区间贪心的信号：按右端点排序，箭尽量射在当前最靠前的右端点上，能顺带引爆所有覆盖该点的气球。变化点在排序键是右端 x[1] 而非左端，且端点相切算命中、只有 start > prev_end 才补箭。",
        "code": """class Solution:
    def findMinArrowShots(self, points):
        points.sort(key=lambda x: x[1])         # 变化点: 按右端点排序，箭尽量射在最早结束处
        arrows = 0
        prev_end = None
        for start, end in points:
            if prev_end is None or start > prev_end:    # 变化点: 相切算命中，start > prev_end 才补箭
                arrows += 1
                prev_end = end
        return arrows""",
        "time": "O(n log n)",
        "space": "O(1)（不计排序栈空间）",
        "pitfalls": [
            "排序键是右端点：让箭尽量射在最早结束的位置，才能覆盖最多后续气球",
            "端点相切（start == prev_end）也算命中，判定新箭用 > 而不是 >=",
            "坐标可能为负，prev_end 初值不能用 0，要用 None 或负无穷",
        ],
    },
    52: {
        "statement": "给定一个只包括 '('、')'、'{'、'}'、'['、']' 的字符串 s，判断字符串是否有效。有效字符串需满足：左括号必须用相同类型的右括号闭合；左括号必须以正确的顺序闭合；每个右括号都有一个对应的相同类型的左括号。",
        "examples": [
            {"input": "s = \"()[]{}\"", "output": "true"},
            {"input": "s = \"([)]\"", "output": "false"},
        ],
        "approach": "括号匹配是栈与表达式的信号：遇左括号压栈，遇右括号弹出栈顶比对类型，嵌套顺序天然由栈保证。变化点在用字典建立右括号到左括号的对应，且栈空弹栈、扫描结束栈非空两种失败情形都要覆盖。",
        "code": """class Solution:
    def isValid(self, s):
        pairs = {')': '(', ']': '[', '}': '{'}  # 变化点: 右括号到左括号的类型映射
        stack = []
        for ch in s:
            if ch in '([{':
                stack.append(ch)
            elif not stack or stack.pop() != pairs[ch]:     # 变化点: 栈空或类型不匹配都无效
                return False
        return not stack""",
        "time": "O(n)",
        "space": "O(n)",
        "pitfalls": [
            "遇右括号时栈空要直接无效，先判空再弹栈",
            "扫描结束后栈非空也是无效（左括号多余），不能只 return True",
            "只统计左右括号个数相等不够，\"([)]\" 顺序错误会漏判",
        ],
    },
    53: {
        "statement": "给你一个 Unix 风格的绝对路径 path，请你将其简化为规范路径。规范路径需满足：以单个 '/' 开头；任意两个目录名之间只有一个 '/'，目录名后不跟 '/'（根目录除外）；'.' 表示当前目录本身，'..' 表示将目录切换到上一级（根目录的上一级仍是根目录）；多个连续 '/' 视为单个 '/'。",
        "examples": [
            {"input": "path = \"/home//foo/\"", "output": "\"/home/foo\""},
            {"input": "path = \"/a/./b/../../c/\"", "output": "\"/c\""},
        ],
        "approach": "路径化简是栈 + 字符串扫描的信号：按 '/' 切分段落逐段处理，空段与 '.' 跳过，'..' 弹栈回退上一级，其余入栈。变化点在 '..' 弹栈前要判空（根目录再回退仍是根），最后用 '/' 拼接并补上开头的 '/'。",
        "code": """class Solution:
    def simplifyPath(self, path):
        stack = []
        for part in path.split('/'):            # 变化点: 按 / 切分逐段扫描
            if part == '' or part == '.':
                continue
            if part == '..':
                if stack:
                    stack.pop()                 # 变化点: .. 回退上一级，弹栈前判空
            else:
                stack.append(part)
        return '/' + '/'.join(stack)            # 变化点: 拼接时补开头斜杠""",
        "time": "O(n)",
        "space": "O(n)",
        "pitfalls": [
            "空段与 '.' 都要跳过：切分产生的空串对应连续斜杠",
            "'..' 在栈空时直接忽略，根目录再回退仍是根目录",
            "\"...\" 是合法目录名，不要当成回退处理",
        ],
    },
    54: {
        "statement": "设计一个支持 push、pop、top 操作，并能在常数时间内检索到最小元素的栈。实现 MinStack 类：push(val) 将元素压入栈；pop() 删除栈顶元素；top() 获取栈顶元素；getMin() 获取栈中最小元素。每个函数的时间复杂度都必须是 O(1)。",
        "examples": [
            {"input": "操作序列：[\"MinStack\",\"push\",\"push\",\"push\",\"getMin\",\"pop\",\"top\",\"getMin\"]，参数 [[],[-2],[0],[-3],[],[],[],[]]", "output": "[null,null,null,null,-3,null,0,-2]"},
            {"input": "操作序列：push(1)、push(1)、getMin()、pop()、getMin()", "output": "1、1、1"},
        ],
        "approach": "要在 O(1) 内取最小值，是数据结构设计的信号：主栈正常进出，另设辅助栈同步保存“当前最小值”，辅助栈顶始终是全栈最小。变化点在 push 时 val <= 辅助栈顶才压入（相等也要压，否则重复最小值弹出后失配），pop 时弹出值等于辅助栈顶才同步弹出。",
        "code": """class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []                     # 变化点: 辅助栈同步保存当前最小值

    def push(self, val):
        self.stack.append(val)
        if not self.min_stack or val <= self.min_stack[-1]:     # 变化点: 相等也要压入
            self.min_stack.append(val)

    def pop(self):
        val = self.stack.pop()
        if val == self.min_stack[-1]:           # 变化点: 弹出的是当前最小则同步弹出
            self.min_stack.pop()

    def top(self):
        return self.stack[-1]

    def getMin(self):
        return self.min_stack[-1]""",
        "time": "各操作 O(1)",
        "space": "O(n)",
        "pitfalls": [
            "push 的判定必须是 <=：最小值重复出现时若不重复压入，pop 后辅助栈会空",
            "pop 只在弹出值等于辅助栈顶时同步弹出，其余情况辅助栈不动",
            "getMin 永远看辅助栈顶，不要遍历主栈找最小",
        ],
    },
    55: {
        "statement": "给你一个字符串数组 tokens，表示一个根据逆波兰表示法（后缀表达式）表示的算术表达式。请你计算该表达式，返回一个整数。有效运算符为 '+'、'-'、'*'、'/'；除法运算向零截断；表达式中不含除零运算；结果及中间计算结果均为 32 位整数。",
        "examples": [
            {"input": "tokens = [\"2\",\"1\",\"+\",\"3\",\"*\"]", "output": "9（(2 + 1) * 3）"},
            {"input": "tokens = [\"4\",\"13\",\"5\",\"/\",\"+\"]", "output": "6（4 + (13 / 5)）"},
        ],
        "approach": "后缀表达式求值是栈与表达式的信号：数字直接入栈，遇运算符弹出两个操作数、结算后把结果压回，扫描结束栈中唯一元素即答案。变化点在弹出顺序——先弹的是右操作数 b、后弹的是左操作数 a，且除法要用 int(a/b) 向零截断而非 //。",
        "code": """class Solution:
    def evalRPN(self, tokens):
        stack = []
        for t in tokens:
            if t in '+-*/':
                b = stack.pop()                 # 变化点: 先弹的是右操作数，注意运算顺序
                a = stack.pop()
                if t == '+':
                    stack.append(a + b)
                elif t == '-':
                    stack.append(a - b)
                elif t == '*':
                    stack.append(a * b)
                else:
                    stack.append(int(a / b))    # 变化点: 除法向零截断，不能用 //
            else:
                stack.append(int(t))
        return stack[0]""",
        "time": "O(n)",
        "space": "O(n)",
        "pitfalls": [
            "操作数顺序：a - b、a / b 中 a 是先入栈的那个，弹反了结果就错",
            "除法截断方向：int(a/b) 向零取整，-7 / 2 得 -3；用 // 会得到 -4",
            "负数字符串如 \"-11\" 不是运算符，用 int(t) 转换即可；判断运算符别用 len(t) == 1",
        ],
    },
    56: {
        "statement": "给你一个字符串表达式 s，请你实现一个基本计算器来计算并返回它的值。表达式由整数（非负）、'+'、'-'、'('、')' 和空格组成，s 表示一个有效的表达式；'-' 也可以用作一元运算符（如 \"-1\" 和 \"-(2 + 3)\"）；不能将两个相邻的整数用空格分隔（如 \"13 + 2\" 合法，\"1 3\" 非法）。",
        "examples": [
            {"input": "s = \"(1+(4+5+2)-3)+(6+8)\"", "output": "23"},
            {"input": "s = \" 2-1 + 2 \"", "output": "3"},
        ],
        "approach": "含括号的加减表达式是栈与表达式的信号：逐字符扫描，遇 '(' 把括号外的累计结果 total 与当前符号 sign 压栈隔离，遇 ')' 结算括号内后乘回符号、加回结果。变化点在运算符与括号出现时都要先把滞留的 num 结算进 total，一元负号靠 sign=-1 配 num=0 自然处理。",
        "code": """class Solution:
    def calculate(self, s):
        total = 0
        sign = 1
        num = 0
        stack = []
        for ch in s:
            if ch.isdigit():
                num = num * 10 + int(ch)
            elif ch == '+':
                total += sign * num
                num, sign = 0, 1
            elif ch == '-':
                total += sign * num             # 变化点: 一元负号时 num=0，自然生效
                num, sign = 0, -1
            elif ch == '(':
                stack.append(total)             # 变化点: 括号外的结果与符号压栈隔离
                stack.append(sign)
                total, sign = 0, 1
            elif ch == ')':
                total += sign * num
                num = 0
                total *= stack.pop()            # 变化点: 乘回括号前符号、加回括号前结果
                total += stack.pop()
        return total + sign * num""",
        "time": "O(n)",
        "space": "O(n)",
        "pitfalls": [
            "遇到运算符、括号和 ')' 时都要先把滞留的 num 结算进 total，否则多位数会漏加",
            "压栈顺序：先压 total 再压 sign，弹出时先弹 sign 乘、再弹 total 加，顺序不能反",
            "扫描结束还有最后一个数字没结算，返回前要补 total + sign * num",
        ],
    },
    57: {
        "statement": "给你一个链表的头节点 head，判断链表中是否有环。如果链表中存在环，则通过连续跟踪 next 指针可以再次到达某个节点；pos 表示尾节点连接到链表中的位置（从 0 开始计数），pos = -1 表示没有环。如果链表中存在环，返回 true；否则返回 false。",
        "examples": [
            {"input": "head = [3,2,0,-4], pos = 1", "output": "true（尾节点连接到下标 1 的节点）"},
            {"input": "head = [1], pos = -1", "output": "false"},
        ],
        "approach": "判环是快慢指针的信号：slow 每走一步、fast 每走两步，有环则两者必然相遇，无环则 fast 先到空。变化点在循环条件先判 fast 与 fast.next 非空，并用 is 判断是否同一节点。",
        "code": """class Solution:
    def hasCycle(self, head):
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next               # 变化点: fast 每次两步制造速度差
            if slow is fast:                    # 变化点: is 判断是否同一节点
                return True
        return False""",
        "time": "O(n)",
        "space": "O(1)",
        "pitfalls": [
            "循环条件先判 fast 再判 fast.next，两步走的指针才不会越界",
            "判断相遇用 is（同一节点对象），而不是比较值",
            "空链表或单节点无环时循环不进入，直接返回 False",
        ],
    },
    58: {
        "statement": "给你两个非空的链表，表示两个非负的整数。它们每位数字都是按照逆序的方式存储的，并且每个节点只能存储一位数字。请你将两个数相加，并以相同形式返回一个表示和的链表。你可以假设除了数字 0 之外，这两个数都不会以 0 开头。",
        "examples": [
            {"input": "l1 = [2,4,3], l2 = [5,6,4]", "output": "[7,0,8]（342 + 465 = 807）"},
            {"input": "l1 = [0], l2 = [0]", "output": "[0]"},
        ],
        "approach": "逆序存储的两数相加是链表哨兵的信号：dummy 建结果链，逐位取出两链值相加并传递进位，缺位补 0。变化点在循环条件带上 carry——两位都走完后进位非零还要补一个节点，以及取值时先判空再取 val。",
        "code": """class Solution:
    def addTwoNumbers(self, l1, l2):
        dummy = ListNode(0)
        cur = dummy
        carry = 0
        while l1 or l2 or carry:                # 变化点: carry 非零也要补一个节点
            total = (l1.val if l1 else 0) + (l2.val if l2 else 0) + carry   # 变化点: 缺位补 0
            carry = total // 10
            cur.next = ListNode(total % 10)
            cur = cur.next
            l1 = l1.next if l1 else None
            l2 = l2.next if l2 else None
        return dummy.next""",
        "time": "O(max(m,n))",
        "space": "O(1)（输出链表不计入）",
        "pitfalls": [
            "循环条件必须带 carry，否则 [9,9]+[1] 的最高位进位会丢失",
            "两链长度不等时缺位要按 0 处理，先判空再取 val",
            "每位存 total % 10、进位 carry = total // 10，别把两位数直接塞进节点",
        ],
    },
    59: {
        "statement": "将两个升序链表合并为一个新的升序链表并返回。新链表是通过拼接给定的两个链表的所有节点组成的，不能新建节点。",
        "examples": [
            {"input": "list1 = [1,2,4], list2 = [1,3,4]", "output": "[1,1,2,3,4,4]"},
            {"input": "list1 = [], list2 = []", "output": "[]"},
        ],
        "approach": "合并两个有序链表是链表哨兵的信号：dummy 起头，比较两链当前节点、把较小者接在结果尾部并前移。变化点在一方走完后把剩余整段直接接回——剩余链表本身有序，无需逐个比较。",
        "code": """class Solution:
    def mergeTwoLists(self, list1, list2):
        dummy = ListNode(0)
        cur = dummy
        while list1 and list2:
            if list1.val <= list2.val:          # 变化点: 比较后接走较小节点
                cur.next = list1
                list1 = list1.next
            else:
                cur.next = list2
                list2 = list2.next
            cur = cur.next
        cur.next = list1 if list1 else list2    # 变化点: 剩余一整段直接接回
        return dummy.next""",
        "time": "O(m+n)",
        "space": "O(1)",
        "pitfalls": [
            "剩余段要整段接回，接的是链表对象而不是重新逐节点比较",
            "比较相等时选哪条都行，用 <= 保证稳定性",
            "两链都空时 dummy.next 是 None，恰好是正确答案",
        ],
    },
    60: {
        "statement": "给你一个长度为 n 的链表，每个节点包含一个额外增加的随机指针 random，该指针可以指向链表中的任何节点或空节点。构造这个链表的深拷贝，返回复制链表的头节点；复制链表中的节点不应引用原链表中的任何节点（用 next 和 random 指向的节点在原链表和复制链表中应一一对应）。",
        "examples": [
            {"input": "head = [[7,null],[13,0],[11,4],[10,2],[1,0]]", "output": "[[7,null],[13,0],[11,4],[10,2],[1,0]]"},
            {"input": "head = []", "output": "[]"},
        ],
        "approach": "带 random 指针的深拷贝是哈希映射的信号：用旧节点到新节点的字典查表复制，next 与 random 都从表里取。变化点在两遍扫描——先建全部新节点再逐个接指针，random 为 None 时 get 恰好返回 None。",
        "code": """class Solution:
    def copyRandomList(self, head):
        if not head:
            return None
        old_new = {}                            # 变化点: 旧节点 -> 新节点的映射
        cur = head
        while cur:
            old_new[cur] = Node(cur.val)
            cur = cur.next
        cur = head
        while cur:
            old_new[cur].next = old_new.get(cur.next)
            old_new[cur].random = old_new.get(cur.random)   # 变化点: random 也查表复制
            cur = cur.next
        return old_new[head]""",
        "time": "O(n)",
        "space": "O(n)",
        "pitfalls": [
            "必须两遍：先建完全部新节点，否则 random 指向的目标可能还没建出来",
            "next 与 random 都用 dict.get 取，源为 None 时 get 返回 None 恰好正确",
            "字典的 key 是旧节点对象本身，不是节点值（值可能重复）",
        ],
    },
    61: {
        "statement": "给你单链表的头指针 head 和两个整数 left 和 right，其中 left <= right。请你反转从位置 left 到位置 right 的链表节点，返回反转后的链表。1 <= left <= right <= 链表长度。",
        "examples": [
            {"input": "head = [1,2,3,4,5], left = 2, right = 4", "output": "[1,4,3,2,5]"},
            {"input": "head = [5], left = 1, right = 1", "output": "[5]"},
        ],
        "approach": "区间反转是链表反转的信号：先走到 left 的前一个节点 prev，再用头插法把 [left, right] 内的节点逐个插到 prev 之后，tail 始终是反转段尾。变化点在 prev 起步于 dummy 走 left-1 步——left=1 时头节点也能被统一处理。",
        "code": """class Solution:
    def reverseBetween(self, head, left, right):
        dummy = ListNode(0, head)
        prev = dummy
        for _ in range(left - 1):               # 变化点: prev 停在 left 前一个节点（含 dummy）
            prev = prev.next
        tail = prev.next                        # 反转段原头，反转后成段尾
        cur = tail.next
        for _ in range(right - left):
            nxt = cur.next
            cur.next = prev.next                # 变化点: 头插法，把 cur 插到 prev 之后
            prev.next = cur
            tail.next = nxt
            cur = nxt
        return dummy.next""",
        "time": "O(n)",
        "space": "O(1)",
        "pitfalls": [
            "prev 要从 dummy 起步走 left-1 步，直接从 head 走会在 left=1 时找不到前驱",
            "头插时 tail.next 每轮都要更新，漏掉会把后续节点接错位置",
            "left == right 时反转零次，代码路径要能自然通过",
        ],
    },
    62: {
        "statement": "给你链表的头节点 head，每 k 个节点一组进行翻转，请你返回修改后的链表。节点总数不是 k 的整数倍时，请将最后剩余的节点保持原有顺序。你不能只是单纯的改变节点内部的值，而需要实际进行节点交换。",
        "examples": [
            {"input": "head = [1,2,3,4,5], k = 2", "output": "[2,1,4,3,5]"},
            {"input": "head = [1,2,3,4,5], k = 3", "output": "[3,2,1,4,5]"},
        ],
        "approach": "K 个一组翻转是链表反转的信号：先探明本组是否凑够 k 个节点，够则把这一段反转并接回前后组，不够保持原样退出。变化点在反转的边界是下一组头 nxt_group 而不是 None，以及上一组尾要前移为下一组的哨兵。",
        "code": """class Solution:
    def reverseKGroup(self, head, k):
        dummy = ListNode(0, head)
        prev_group = dummy
        while True:
            node = prev_group
            for _ in range(k):                  # 变化点: 先探明本组是否够 k 个
                node = node.next
                if not node:
                    return dummy.next
            group_end = prev_group.next         # 本组头，反转后成组尾
            nxt_group = node.next
            prev, cur = nxt_group, group_end    # 变化点: 反转以 nxt_group 为界而非 None
            for _ in range(k):
                nxt = cur.next
                cur.next = prev
                prev = cur
                cur = nxt
            prev_group.next = prev              # 前一组接新组头
            group_end.next = nxt_group
            prev_group = group_end              # 变化点: 本组尾成为下一组的哨兵""",
        "time": "O(n)",
        "space": "O(1)",
        "pitfalls": [
            "先探明整组节点是否够 k 个再动手，反转到一半发现不足无法回退",
            "反转段的终点是下一组头 nxt_group，写成 None 会把后面已反转的组接错",
            "处理完一组后 prev_group 要前移到本组尾（原组头），否则下一组挂错位置",
        ],
    },
    63: {
        "statement": "给你一个链表，删除链表的倒数第 n 个结点，并且返回链表的头结点。进阶：尝试使用一趟扫描实现。",
        "examples": [
            {"input": "head = [1,2,3,4,5], n = 2", "output": "[1,2,3,5]"},
            {"input": "head = [1], n = 1", "output": "[]"},
        ],
        "approach": "删除倒数第 n 个节点是链表哨兵 + 快慢指针的信号：fast 先走 n 步拉开固定差距，再与 slow 同速前进，fast 到尾时 slow 恰停在目标前驱。变化点在 fast 起步于 dummy 走 n 步、删除用一行 slow.next = slow.next.next 完成。",
        "code": """class Solution:
    def removeNthFromEnd(self, head, n):
        dummy = ListNode(0, head)
        fast = slow = dummy
        for _ in range(n):                      # 变化点: fast 先走 n 步拉开距离
            fast = fast.next
        while fast.next:
            fast = fast.next
            slow = slow.next
        slow.next = slow.next.next              # 变化点: slow 停在倒数第 n+1 个节点，跳过目标
        return dummy.next""",
        "time": "O(n)",
        "space": "O(1)",
        "pitfalls": [
            "两个指针都要从 dummy 出发，否则删除头节点时没有前驱",
            "fast 先走 n 步后循环条件是 fast.next 非空，保证 slow 停在目标前驱而不是目标",
            "一趟扫描的关键是固定的 n 步差距，别先数总长度再走第二遍",
        ],
    },
    64: {
        "statement": "给定一个已排序的链表的头 head，删除原始链表中所有重复数字的节点，只留下不同的数字。返回已排序的链表。注意：出现次数超过一次的数字要全部删除，一个都不保留。",
        "examples": [
            {"input": "head = [1,2,3,3,4,4,5]", "output": "[1,2,5]"},
            {"input": "head = [1,1,1,2,3]", "output": "[2,3]"},
        ],
        "approach": "把重复值整段删光（一个不留）是链表哨兵的信号：prev 停在“确定保留”的段尾，发现相邻两值相等就记下该值，把后续所有等值节点全部摘除。变化点在内层 while 按值跳过、且删除期间 prev 不动。",
        "code": """class Solution:
    def deleteDuplicates(self, head):
        dummy = ListNode(0, head)
        prev = dummy
        while prev.next and prev.next.next:
            if prev.next.val == prev.next.next.val:     # 变化点: 发现重复值
                dup = prev.next.val
                while prev.next and prev.next.val == dup:   # 变化点: 内层循环摘除该值全部节点
                    prev.next = prev.next.next
            else:
                prev = prev.next
        return dummy.next""",
        "time": "O(n)",
        "space": "O(1)",
        "pitfalls": [
            "发现重复要先把 dup 值记下来，再整体跳过所有等值节点，不能用逐个比较",
            "删除期间 prev 不动：下一个节点可能还是新值，等确认唯一再前移",
            "头节点就重复时靠 dummy 兜底，返回 dummy.next",
        ],
    },
    65: {
        "statement": "给你一个链表的头节点 head，将链表每个节点向右移动 k 个位置后返回新的头节点。0 <= k <= 10^9，k 可能远大于链表长度。",
        "examples": [
            {"input": "head = [1,2,3,4,5], k = 2", "output": "[4,5,1,2,3]"},
            {"input": "head = [0,1,2], k = 4", "output": "[2,0,1]"},
        ],
        "approach": "整链右移 k 位是链表哨兵的信号：先数出长度并把尾节点连到头成环，再从新尾断开。变化点在 k 对长度取模、新尾是倒数第 k+1 个节点（从头走 length-k-1 步），以及 k % length == 0 时先复原再返回。",
        "code": """class Solution:
    def rotateRight(self, head, k):
        if not head or not head.next or k == 0:
            return head
        old = head
        length = 1
        while old.next:
            old = old.next
            length += 1
        old.next = head                         # 尾连头成环
        k %= length                             # 变化点: k 对长度取模
        if k == 0:
            old.next = None                     # 变化点: 无需旋转，先复原再返回
            return head
        cur = head
        for _ in range(length - k - 1):         # 新尾是倒数第 k+1 个节点
            cur = cur.next
        new_head = cur.next
        cur.next = None                         # 变化点: 从新尾断开环
        return new_head""",
        "time": "O(n)",
        "space": "O(1)",
        "pitfalls": [
            "k 可能远大于长度，必须先 k %= length，否则循环越界或空转",
            "成环后一定要断开：包括 k % length == 0 的提前返回分支也要恢复",
            "新尾是倒数第 k+1 个节点，走 length - k - 1 步，别数错成 length - k",
        ],
    },
    66: {
        "statement": "给你一个链表的头节点 head 和一个特定值 x，请你对链表进行分隔，使得所有小于 x 的节点都出现在大于或等于 x 的节点之前。你应当保留每个分区中各节点的初始相对位置。",
        "examples": [
            {"input": "head = [1,4,3,2,5,2], x = 3", "output": "[1,2,2,4,3,5]"},
            {"input": "head = [2,1], x = 2", "output": "[1,2]"},
        ],
        "approach": "按值分隔且保持相对顺序，是链表哨兵的信号：维护 small、large 两条独立链分别收集两类节点，最后把大链接在小链尾部。变化点在大链尾必须显式置 None 防止成环，拼接用 large_dummy.next。",
        "code": """class Solution:
    def partition(self, head, x):
        small_dummy = ListNode(0)
        large_dummy = ListNode(0)               # 变化点: 两条哨兵链分别收集
        small, large = small_dummy, large_dummy
        cur = head
        while cur:
            if cur.val < x:
                small.next = cur
                small = small.next
            else:
                large.next = cur
                large = large.next
            cur = cur.next
        large.next = None                       # 变化点: 大链断尾，防止成环
        small.next = large_dummy.next           # 变化点: 小链尾接大链头
        return small_dummy.next""",
        "time": "O(n)",
        "space": "O(1)",
        "pitfalls": [
            "large.next 必须置 None：原链尾可能还指着某个已摘走的节点，拼接后成环",
            "保持相对顺序用尾插法，千万不要头插或交换值",
            "x 本身不算“小于”，等于 x 的节点进大链",
        ],
    },
    67: {
        "statement": "请你设计并实现一个满足 LRU（最近最少使用）缓存约束的数据结构。实现 LRUCache 类：LRUCache(capacity) 以正整数容量初始化；get(key) 如果密钥存在于缓存中则返回其值，否则返回 -1；put(key, value) 如果 key 已存在则变更其值，如果不存在则插入该组键值对，插入前若容量已满则逐出最久未使用的键。get 和 put 的每个函数时间复杂度必须为 O(1)。",
        "examples": [
            {"input": "操作序列：[\"LRUCache\",\"put\",\"put\",\"get\",\"put\",\"get\",\"put\",\"get\",\"get\",\"get\"]，参数 [[2],[1,1],[2,2],[1],[3,3],[2],[4,4],[1],[3],[4]]", "output": "[null,null,null,1,null,-1,null,-1,3,4]"},
            {"input": "操作序列：LRUCache(1)、put(1,1)、get(1)、put(2,2)、get(2)", "output": "null、null、1、null、-1"},
        ],
        "approach": "O(1) 的 get/put 且按访问时间淘汰，是数据结构设计的信号：哈希表负责 key 到节点的 O(1) 定位，双向链表维护使用新旧次序。变化点有三处——访问（get、put 旧键）后把节点摘下移到链表头部；容量满时淘汰尾部最久未用节点并同步删哈希表；哑头哑尾简化边界。",
        "code": """class Node:
    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.map = {}                           # 变化点: 哈希表 key -> 链表节点，O(1) 定位
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head              # 哑头尾间挂双向链表，头端最新、尾端最旧

    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_front(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        if key not in self.map:
            return -1
        node = self.map[key]
        self._remove(node)
        self._add_front(node)                   # 变化点: 访问后移到头部，表示最近使用
        return node.value

    def put(self, key, value):
        if key in self.map:
            node = self.map[key]
            node.value = value
            self._remove(node)
            self._add_front(node)
            return
        if len(self.map) >= self.cap:           # 变化点: 容量满时淘汰尾部最久未用节点
            last = self.tail.prev
            self._remove(last)
            del self.map[last.key]
        node = Node(key, value)
        self.map[key] = node
        self._add_front(node)""",
        "time": "get / put 均 O(1)",
        "space": "O(capacity)",
        "pitfalls": [
            "put 已存在的键是“更新 + 移到头部”，不能当作新插入触发淘汰逻辑",
            "淘汰的是哑尾前一个节点，摘链的同时必须 del 哈希表映射，否则泄漏",
            "节点要存 key（淘汰时删映射用），只存 value 的话淘汰环节拿不到键",
        ],
    },
}
