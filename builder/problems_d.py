# -*- coding: utf-8 -*-
"""题解数据 89-113：图、图的广度优先搜索、字典树、回溯、分治、Kadane。"""

DATA = {
    89: {
        "statement": "给你一个由 '1'（陆地）和 '0'（水）组成的二维网格 grid，请你计算网格中岛屿的数量。岛屿总是被水包围，并且每座岛屿只能由水平方向和/或竖直方向上相邻的陆地连接形成。可以假设网格的四条边均被水包围。",
        "examples": [
            {"input": "grid = [['1','1','1','1','0'],['1','1','0','1','0'],['1','1','0','0','0'],['0','0','0','0','0']]", "output": "1"},
            {"input": "grid = [['1','1','0','0','0'],['1','1','0','0','0'],['0','0','1','0','0'],['0','0','0','1','1']]", "output": "3"},
        ],
        "approach": "连片的 '1' 构成一座岛，信号是网格连通块计数，直接套网格 DFS 模板：外层扫描每个格子，遇到未访问的陆地就启动一次 DFS，把整块陆地“沉岛”标记成 '0' 并计数加一。变化点在于标记方式——直接改写网格省掉 visited 数组，每个格子至多被访问一次，计数即答案。",
        "code": """class Solution:
    def numIslands(self, grid):
        m, n = len(grid), len(grid[0])

        def dfs(i, j):
            if not (0 <= i < m and 0 <= j < n) or grid[i][j] != '1':
                return
            grid[i][j] = '0'                       # 变化点: 访问后沉岛标记，防重复计数
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                dfs(i + di, j + dj)

        count = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] == '1':              # 变化点: 每块新陆地启动一次 DFS 并计数
                    count += 1
                    dfs(i, j)
        return count""",
        "time": "O(mn)，每个格子至多访问一次",
        "space": "O(mn)（递归栈，最坏全为陆地时）",
        "pitfalls": [
            "网格元素是字符 '1'/'0'，拿数字 1/0 比较永远不相等",
            "进入格子后立即标记再向四邻扩展，后标记会重复访问甚至死循环",
            "外层双层循环不可省，任何一块陆地都可能藏在网格的任意位置",
        ],
    },
    90: {
        "statement": "给你一个 m×n 的矩阵 board，由若干字符 'X' 和 'O' 组成，请捕获所有被围绕的区域：把被围绕区间里的所有 'O' 用 'X' 填充。任何不在边界上、或不与边界上的 'O' 相连的 'O' 最终都会被填充为 'X'；与边界连通的 'O' 保持不变。要求原地修改，无需返回值。",
        "examples": [
            {"input": "board = [['X','X','X','X'],['X','O','O','X'],['X','X','O','X'],['X','O','X','X']]", "output": "[['X','X','X','X'],['X','X','X','X'],['X','X','X','X'],['X','O','X','X']]"},
            {"input": "board = [['X']]", "output": "[['X']]"},
        ],
        "approach": "正向判断“是否被围”无从下手，反过来想：被 'X' 包住的 'O' 一定不与边界相连。信号仍是网格 DFS，但方向反转——只从四条边界上的 'O' 出发反向 DFS，把边界连通的 'O' 临时标记成 '#'；最后扫全表，把残余 'O' 置 'X'、把 '#' 还原成 'O'。变化点就在于“从边界反向标记”这一思维转换。",
        "code": """class Solution:
    def solve(self, board):
        m, n = len(board), len(board[0])

        def dfs(i, j):
            if not (0 <= i < m and 0 <= j < n) or board[i][j] != 'O':
                return
            board[i][j] = '#'                      # 变化点: 边界可达的 O 临时标记为 #
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                dfs(i + di, j + dj)

        for i in range(m):                         # 变化点: 只从四条边界的 O 反向出发
            dfs(i, 0)
            dfs(i, n - 1)
        for j in range(n):
            dfs(0, j)
            dfs(m - 1, j)

        for i in range(m):                         # 变化点: 一次遍历用 if/elif 同时翻转与还原
            for j in range(n):
                if board[i][j] == 'O':
                    board[i][j] = 'X'
                elif board[i][j] == '#':
                    board[i][j] = 'O'""",
        "time": "O(mn)",
        "space": "O(mn)（递归栈，最坏情况）",
        "pitfalls": [
            "占位符必须用 '#' 这类第三方字符，直接改成 'X' 会破坏边界连通性判断",
            "收尾的翻转与还原在同一次遍历里用 if/elif 完成，改过的格子不能再被二次判断",
            "DFS 起点只有边界的 O，若把内部 O 也当起点，被围区域会被误标成 '#'",
        ],
    },
    91: {
        "statement": "给你无向连通图中一个节点的引用 node，请返回该图的深拷贝（克隆）。图中每个节点都包含它的值 val 和邻居列表 neighbors，邻居是与它直接相连的其它节点。返回的克隆图必须与原图结构和值完全一致，并且不能对原图做任何修改。",
        "examples": [
            {"input": "adjList = [[2,4],[1,3],[2,4],[1,3]]", "output": "[[2,4],[1,3],[2,4],[1,3]]（结构与原图相同的克隆图）"},
            {"input": "adjList = [[]]", "output": "[[]]"},
        ],
        "approach": "克隆的难点在环状引用会无限复制，信号是“遍历 + 旧新映射”，套图 BFS 模板并用哈希表 old_new 兼做 visited：首次遇到邻居时先复制节点再入队，出队时把新邻居挂到新节点的 neighbors 上。变化点在于建映射与连边同步进行，哈希表一举两得——既防重复克隆又提供新旧对照。",
        "code": """from collections import deque

class Solution:
    def cloneGraph(self, node):
        if not node:
            return None
        old_new = {node: Node(node.val)}           # 变化点: 哈希表存旧节点→新节点，兼做 visited
        q = deque([node])
        while q:
            cur = q.popleft()
            for nb in cur.neighbors:
                if nb not in old_new:              # 变化点: 首次见到邻居先复制再入队
                    old_new[nb] = Node(nb.val)
                    q.append(nb)
                old_new[cur].neighbors.append(old_new[nb])   # 变化点: 在新节点之间连边
        return old_new[node]""",
        "time": "O(V+E)",
        "space": "O(V)",
        "pitfalls": [
            "复制节点要在入队前登记进 old_new，等出队再登记会让同一节点被克隆多次",
            "连边必须连新节点：old_new[cur].neighbors.append(old_new[nb])，混入旧节点会破坏克隆",
            "输入节点为 None 时直接返回 None，空图也要处理",
        ],
    },
    92: {
        "statement": "给你一个变量对数组 equations 和实数数组 values，其中 equations[i] = [Ai, Bi] 与 values[i] 共同表示等式 Ai / Bi = values[i]。再给出若干查询 queries[j] = [Cj, Dj]，请对每个查询求出 Cj / Dj 的结果；变量未出现或无法确定时返回 -1.0。所有变量用小写字母串表示，题目保证等式之间无矛盾。",
        "examples": [
            {"input": "equations = [['a','b'],['b','c']], values = [2.0,3.0], queries = [['a','c'],['b','a'],['a','e'],['a','a'],['x','x']]", "output": "[6.00000,0.50000,-1.00000,1.00000,-1.00000]"},
            {"input": "equations = [['a','b'],['b','c'],['c','d']], values = [2.0,3.0,4.0], queries = [['a','d'],['d','a']]", "output": "[24.00000,0.04167]"},
        ],
        "approach": "等式就是带权边：a/b = v，同时 b/a = 1/v，信号是“带权图上求两点路径权值积”，套图 BFS 模板并把距离换成乘积。每个查询从起点出发沿边累乘权值，首次到达终点即为答案；任一变量不在图中直接返回 -1.0。变化点在于建图时正反两条边都要加，反向边权取倒数。",
        "code": """from collections import deque

class Solution:
    def calcEquation(self, equations, values, queries):
        graph = {}
        for (a, b), v in zip(equations, values):
            graph.setdefault(a, {})[b] = v         # 变化点: 带权图，a/b = v
            graph.setdefault(b, {})[a] = 1 / v     # 变化点: 反向边权取倒数

        def query(a, b):
            if a not in graph or b not in graph:
                return -1.0
            q = deque([(a, 1.0)])
            visited = {a}
            while q:
                cur, prod = q.popleft()
                if cur == b:
                    return prod                    # 变化点: 队列里带路径权值积
                for nxt, w in graph[cur].items():
                    if nxt not in visited:
                        visited.add(nxt)
                        q.append((nxt, prod * w))
            return -1.0

        return [query(a, b) for a, b in queries]""",
        "time": "O(Q·(V+E))，Q 为查询数",
        "space": "O(V+E)",
        "pitfalls": [
            "必须同时建 b→a 这条权值 1/v 的反向边，否则方向反转的查询会查不到",
            "查询变量可能压根没出现过（如 'x'），先判在不在图中再进 BFS",
            "访问标记在入队时登记，防止环上边权被重复累乘",
        ],
    },
    93: {
        "statement": "这个学期你必须选修 numCourses 门课程，编号为 0 到 numCourses-1。有些课程有先修要求，prerequisites[i] = [ai, bi] 表示想修课程 ai 必须先修完课程 bi。请你判断能否修完全部课程：可以返回 true，存在循环依赖无法完成返回 false。",
        "examples": [
            {"input": "numCourses = 2, prerequisites = [[1,0]]", "output": "true"},
            {"input": "numCourses = 2, prerequisites = [[1,0],[0,1]]", "output": "false"},
        ],
        "approach": "课程依赖构成有向图，“能修完”等价于“图中无环”，信号是拓扑排序模板：建图统计入度，入度 0 的课程入队，出队时删出边、把入度归零的后继入队。变化点在于本题只需比较出队总数与课程数——有环时环上的课程入度永远无法归零。",
        "code": """from collections import deque

class Solution:
    def canFinish(self, numCourses, prerequisites):
        graph = [[] for _ in range(numCourses)]
        indeg = [0] * numCourses
        for a, b in prerequisites:
            graph[b].append(a)                     # 变化点: 先修 b 才能修 a，边方向 b→a
            indeg[a] += 1
        q = deque(i for i in range(numCourses) if indeg[i] == 0)
        done = 0
        while q:
            u = q.popleft()
            done += 1
            for v in graph[u]:
                indeg[v] -= 1                      # 变化点: 入度归零即解锁，入队
                if indeg[v] == 0:
                    q.append(v)
        return done == numCourses                  # 变化点: 出队数不足说明有环""",
        "time": "O(V+E)",
        "space": "O(V+E)",
        "pitfalls": [
            "边方向别建反：prerequisites 给的是 [ai, bi]，先修 bi，边应从 bi 指向 ai",
            "判断依据是出队数 == n，不能只看队列最终是否为空",
            "无先修约束的课程入度为 0，初始队列要一次收集齐所有此类课程",
        ],
    },
    94: {
        "statement": "与“课程表”相同的前提：numCourses 门课程与 prerequisites 依赖关系，必修完 bi 才能修 ai。现在要求返回任意一种能修完所有课程的修课顺序；如果不可能完成，返回空数组。答案顺序可能不唯一，返回任意一种合法顺序即可。",
        "examples": [
            {"input": "numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]", "output": "[0,1,2,3]（或 [0,2,1,3] 等任意合法顺序）"},
            {"input": "numCourses = 1, prerequisites = []", "output": "[0]"},
        ],
        "approach": "在“能否修完”的基础上多输出一份顺序，仍是拓扑排序模板：出队顺序天然满足所有先修约束。变化点在于用 order 数组按出队序记录课程号，最后若长度不足 n 说明有环，返回空数组。",
        "code": """from collections import deque

class Solution:
    def findOrder(self, numCourses, prerequisites):
        graph = [[] for _ in range(numCourses)]
        indeg = [0] * numCourses
        for a, b in prerequisites:
            graph[b].append(a)
            indeg[a] += 1
        q = deque(i for i in range(numCourses) if indeg[i] == 0)
        order = []
        while q:
            u = q.popleft()
            order.append(u)                        # 变化点: 记录出队顺序即为一种修课顺序
            for v in graph[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)
        return order if len(order) == numCourses else []   # 变化点: 有环返回空数组""",
        "time": "O(V+E)",
        "space": "O(V+E)",
        "pitfalls": [
            "必须先比较 order 长度与 n 再决定返回，有环时直接返回 []",
            "边方向同样是 bi→ai，建反后输出的顺序不满足先修约束",
            "无依赖课程也要出现在结果里，初始队列收集所有入度 0 的课程",
        ],
    },
    95: {
        "statement": "给你一个 n×n 的棋盘 board，格号从下到上、每行蛇形排列，board 中的正数 r 表示踩到该格会被强制传送到格号 r（蛇或梯子），-1 表示无传送。你从格 1 出发，每次掷骰子前进 1~6 步，求到达格 n² 所需的最少掷骰次数；无法到达返回 -1。传送是强制的且只传送一次，传送到的格子不再二次触发传送。",
        "examples": [
            {"input": "board = [[-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1],[-1,35,-1,-1,13,-1],[-1,-1,-1,-1,-1,-1],[-1,15,-1,-1,-1,-1]]", "output": "4"},
            {"input": "board = [[-1,-1,-1],[-1,-1,-1],[-1,-1,7]]", "output": "2"},
        ],
        "approach": "格号 1..n² 是节点，掷骰子的 6 个落点是邻居，最少次数即无权图最短路，套图 BFS 模板。变化点一：一维格号要换算到蛇形棋盘坐标才能读传送目标；变化点二：踩到蛇/梯必须强制传送，把传送后的格号当作真正邻居入队。",
        "code": """from collections import deque

class Solution:
    def snakesAndLadders(self, board):
        n = len(board)
        target = n * n

        def to_rc(s):
            quot, rem = divmod(s - 1, n)
            r = n - 1 - quot                       # 变化点: 一维格号换算蛇形坐标
            c = rem if quot % 2 == 0 else n - 1 - rem
            return r, c

        q = deque([(1, 0)])
        visited = {1}
        while q:
            s, step = q.popleft()
            for nxt in range(s + 1, min(s + 6, target) + 1):   # 变化点: 邻居=掷骰子 1~6 步
                r, c = to_rc(nxt)
                if board[r][c] != -1:              # 变化点: 蛇/梯强制传送
                    nxt = board[r][c]
                if nxt == target:
                    return step + 1
                if nxt not in visited:
                    visited.add(nxt)
                    q.append((nxt, step + 1))
        return -1""",
        "time": "O(n²)",
        "space": "O(n²)",
        "pitfalls": [
            "坐标换算按蛇形：自底向上偶数行（0 起）从左到右，奇数行从右到左",
            "掷骰子可能越过终点，枚举上界是 min(s+6, n²)，越界落点直接跳过",
            "visited 标记传送后的格号而不是落点格号，否则同一格会被多次入队",
        ],
    },
    96: {
        "statement": "基因序列由 8 个字符组成，每个字符只能是 'A'、'C'、'G'、'T' 之一。每次变化可以修改序列中的一个字符，且变化后的序列必须仍属于基因库 bank。给定起始基因串 start、目标基因串 end 与基因库 bank，求从 start 变到 end 的最少变化次数；无法完成返回 -1。起始串本身不计入变化次数。",
        "examples": [
            {"input": "start = \"AACCGGTT\", end = \"AACCGGTA\", bank = [\"AACCGGTA\"]", "output": "1"},
            {"input": "start = \"AACCGGTT\", end = \"AAACGGTA\", bank = [\"AACCGGTA\",\"AACCGCTA\",\"AAACGGTA\"]", "output": "2"},
        ],
        "approach": "每个合法基因串是一个状态，“单字符替换且结果在库中”定义邻居，最少次数正是图 BFS 模板的层级。变化点在于邻居生成：8 个位置 × 4 种碱基逐一枚举替换，生成的串必须在 bank 中且未访问才入队；起点等于终点时出队即返回 0。",
        "code": """from collections import deque

class Solution:
    def minMutation(self, startGene, endGene, bank):
        bank = set(bank)
        q = deque([(startGene, 0)])
        seen = {startGene}
        while q:
            gene, step = q.popleft()
            if gene == endGene:
                return step
            for i in range(8):                     # 变化点: 邻居=单位置替换碱基
                for ch in "ACGT":
                    if ch == gene[i]:
                        continue
                    nxt = gene[:i] + ch + gene[i + 1:]
                    if nxt in bank and nxt not in seen:   # 变化点: 只有库内串可走
                        seen.add(nxt)
                        q.append((nxt, step + 1))
        return -1""",
        "time": "O(B·L²)，B 为基因库大小、L=8",
        "space": "O(B)",
        "pitfalls": [
            "中间产物必须在 bank 中才合法，生成邻居后先查库再入队",
            "end 不在 bank 时 BFS 永远到不了，自然返回 -1；start==end 时应返回 0",
            "入队时立即加入 seen，同一基因串可能被多条路径替换得到",
        ],
    },
    97: {
        "statement": "在字典 wordList 中找出从 beginWord 到 endWord 的最短转换序列的长度：每次转换只能改变一个字母，且中间单词都必须在字典中；beginWord 本身不计入序列长度。若不存在这样的转换序列，返回 0。序列的第一个单词是 beginWord，最后一个单词是 endWord。",
        "examples": [
            {"input": "beginWord = \"hit\", endWord = \"cog\", wordList = [\"hot\",\"dot\",\"dog\",\"lot\",\"log\",\"cog\"]", "output": "5"},
            {"input": "beginWord = \"hit\", endWord = \"cog\", wordList = [\"hot\",\"dot\",\"dog\",\"lot\",\"log\"]", "output": "0"},
        ],
        "approach": "单词是节点，相差一个字母的单词之间连边，最短转换序列长度就是 BFS 的层数（按节点数计）。变化点在于邻居生成：对每个位置尝试替换 26 个字母，拼出新串查字典集合，命中且未访问才入队；endWord 不在字典时直接返回 0。",
        "code": """from collections import deque

class Solution:
    def ladderLength(self, beginWord, endWord, wordList):
        words = set(wordList)
        if endWord not in words:                   # 变化点: 终点不在字典直接无解
            return 0
        q = deque([(beginWord, 1)])                # 变化点: 步数按节点数计，起点为 1
        seen = {beginWord}
        while q:
            word, step = q.popleft()
            if word == endWord:
                return step
            for i in range(len(word)):
                for ch in "abcdefghijklmnopqrstuvwxyz":
                    if ch == word[i]:
                        continue
                    nxt = word[:i] + ch + word[i + 1:]
                    if nxt in words and nxt not in seen:
                        seen.add(nxt)
                        q.append((nxt, step + 1))
        return 0""",
        "time": "O(N·26·L²)，N 为字典单词数、L 为单词长度",
        "space": "O(N·L)",
        "pitfalls": [
            "endWord 不在 wordList 时直接返回 0，否则 BFS 会空跑",
            "答案按节点数计（hit→hot→dot→dog→cog 为 5），起点占 1，别按边数返回 4",
            "替换字母要拼成新串去查集合，在原串上原地改会污染当前状态",
        ],
    },
    98: {
        "statement": "请实现 Trie（前缀树）类，包含三个方法：Trie() 初始化前缀树对象；insert(word) 向树中插入字符串 word；search(word) 判断 word 是否在树中（必须是完整插入过的单词）；startsWith(prefix) 判断之前插入的字符串中是否存在以 prefix 为前缀的字符串。所有输入仅由小写英文字母组成。",
        "examples": [
            {"input": "操作 [\"Trie\",\"insert\",\"search\",\"search\",\"startsWith\",\"insert\",\"search\"]，参数 [[],[\"apple\"],[\"apple\"],[\"app\"],[\"app\"],[\"app\"],[\"app\"]]", "output": "[null,null,true,false,true,null,true]"},
            {"input": "操作 [\"Trie\",\"insert\",\"search\",\"startsWith\"]，参数 [[],[\"app\"],[\"ap\"],[\"ap\"]]", "output": "[null,null,false,true]"},
        ],
        "approach": "“公共前缀共享一条路径”是字典树的信号，套字典树模板：节点持有 children 映射与 end 标记，insert 沿字符逐层建节点、末尾打标记。变化点在于查询语义分两档——search 走完路径还要求 end 为真，startsWith 只要路径走得通即可；两者复用同一个按字符下行的查找。",
        "code": """class Trie:
    def __init__(self):
        self.children = {}
        self.end = False                           # 变化点: end 标记区分“前缀存在”与“单词完整”

    def insert(self, word):
        node = self
        for ch in word:
            if ch not in node.children:
                node.children[ch] = Trie()         # 变化点: 沿字符逐层建节点
            node = node.children[ch]
        node.end = True

    def search(self, word):
        node = self._walk(word)
        return node is not None and node.end       # 变化点: 完整单词要求 end 为真

    def startsWith(self, prefix):
        return self._walk(prefix) is not None

    def _walk(self, s):
        node = self
        for ch in s:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node""",
        "time": "insert / search / startsWith 每次 O(L)，L 为字符串长度",
        "space": "O(总插入字符数)",
        "pitfalls": [
            "search 与 startsWith 的唯一区别是 end 标记，存在前缀但没打标记时 search 必须返回 False",
            "insert 只在子节点缺失时新建，已有路径直接走下去，覆盖节点会丢掉其它单词",
            "三个方法都从根（self）出发按字符下行，查不到边就返回 None/False",
        ],
    },
    99: {
        "statement": "请设计一个支持添加单词与搜索单词的数据结构 WordDictionary：addWord(word) 把 word 加入结构；search(word) 判断 word 是否在结构中，word 可以包含 '.'，每个 '.' 能匹配任意一个字母。所有输入由小写字母与 '.' 组成。",
        "examples": [
            {"input": "操作 [\"WordDictionary\",\"addWord\",\"addWord\",\"addWord\",\"search\",\"search\",\"search\",\"search\"]，参数 [[],[\"bad\"],[\"dad\"],[\"mad\"],[\"pad\"],[\"bad\"],[\".ad\"],[\"b..\"]]", "output": "[null,null,null,null,false,true,true,true]"},
            {"input": "操作 [\"WordDictionary\",\"addWord\",\"search\",\"search\"]，参数 [[],[\"a\"],[\".\"],[\"ab\"]]", "output": "[null,null,true,false]"},
        ],
        "approach": "结构与字典树相同，addWord 沿字符建路径并打 end 标记，套字典树模板。变化点在于 search 遇到 '.' 时没有唯一边可走，需要 DFS 枚举当前节点的所有子分支，任一分支递归成功即返回 True；普通字符仍按固定边下行。",
        "code": """class WordDictionary:
    def __init__(self):
        self.children = {}
        self.end = False

    def addWord(self, word):
        node = self
        for ch in word:
            if ch not in node.children:
                node.children[ch] = WordDictionary()
            node = node.children[ch]
        node.end = True

    def search(self, word):
        def dfs(i, node):
            if i == len(word):
                return node.end                    # 变化点: 走到词尾看 end 标记
            ch = word[i]
            if ch == '.':
                return any(dfs(i + 1, nxt) for nxt in node.children.values())   # 变化点: '.' 枚举全部分支
            if ch in node.children:
                return dfs(i + 1, node.children[ch])
            return False

        return dfs(0, self)""",
        "time": "addWord O(L)；search 最坏 O(26^L·L)（全为 '.' 时）",
        "space": "O(总插入字符数)",
        "pitfalls": [
            "'.' 分支枚举后任一成功即真，any 短路可避免无效递归",
            "递归终止在下标等于词长，此时返回 node.end，而不是 True",
            "普通字符没有对应边直接返回 False，别把 '.' 当普通字符查表",
        ],
    },
    100: {
        "statement": "给定 m×n 的网格 board 和单词列表 words，找出所有同时在网格和字典中出现的单词。单词必须由网格中相邻（上下左右）的字母按顺序构成，同一个单元格的字母在同一个单词中不允许重复使用。可以按任意顺序返回答案。",
        "examples": [
            {"input": "board = [['o','a','a','n'],['e','t','a','e'],['i','h','k','r'],['i','f','l','v']], words = ['oath','pea','eat','rain']", "output": "['oath','eat']"},
            {"input": "board = [['a','b'],['c','d']], words = ['abcb']", "output": "[]"},
        ],
        "approach": "逐词对网格做 DFS 会大量重复走相同前缀，信号是“多词共享前缀”，先用字典树把所有单词建好，再从每个格子出发回溯：DFS 每步同步在 Trie 上前进，叶子里直接存完整单词，命中即收集并从树中删除防重。变化点在于 Trie 剪枝——子树走空后整枝删除，搜索空间随命中单调收缩。",
        "code": """class Solution:
    def findWords(self, board, words):
        trie = {}
        for w in words:
            node = trie
            for ch in w:
                node = node.setdefault(ch, {})
            node['#'] = w                          # 变化点: 叶子直接存完整单词

        m, n = len(board), len(board[0])
        res = []

        def dfs(i, j, parent):
            ch = board[i][j]
            node = parent.get(ch)
            if node is None:
                return
            word = node.pop('#', None)             # 变化点: 命中即收集并删除，防重复收集
            if word:
                res.append(word)
            board[i][j] = '#'                      # 占位防回头
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                ni, nj = i + di, j + dj
                if 0 <= ni < m and 0 <= nj < n and board[ni][nj] != '#':
                    dfs(ni, nj, node)
            board[i][j] = ch                       # 恢复原字符
            if not node:                           # 变化点: 子树走空整枝剪掉
                del parent[ch]

        for i in range(m):
            for j in range(n):
                dfs(i, j, trie)
        return res""",
        "time": "O(mn·3^L)（回溯）+ O(总字符数)（建树），L 为最长单词长度",
        "space": "O(总字符数)（Trie）+ O(L)（递归栈）",
        "pitfalls": [
            "叶子里存完整单词而不是 end 布尔，命中时才能直接收集",
            "命中后立刻 pop 掉 '#'，否则同一路径或另一条路径会重复收集同一个词",
            "占位符用 '#' 且恢复放在四方向递归之后；'#' 不是合法字母，天然挡住回头路",
        ],
    },
    101: {
        "statement": "给定一个仅包含数字 2-9 的字符串 digits，返回所有它能表示的字母组合。数字到字母的映射与电话键盘相同（如 '2' 对应 \"abc\"）。答案按任意顺序返回；digits 为空时返回空列表。",
        "examples": [
            {"input": "digits = \"23\"", "output": "[\"ad\",\"ae\",\"af\",\"bd\",\"be\",\"bf\",\"cd\",\"ce\",\"cf\"]"},
            {"input": "digits = \"\"", "output": "[]"},
        ],
        "approach": "每个数字位从映射字母串中选一个字符，选满所有位即得到一个组合，是回溯框架最标准的“按位做选择”：path 收集已选字符，下标 i 表示当前处理第几位。变化点在于选择列表来自映射表 phone[digits[i]]，终止条件是 i 走到 digits 末尾，收集时 join 成字符串快照。",
        "code": """class Solution:
    def letterCombinations(self, digits):
        if not digits:
            return []
        phone = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl",
                 "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}
        res, path = [], []

        def backtrack(i):
            if i == len(digits):                   # 变化点: 每个数字位都选完才收集
                res.append(''.join(path))
                return
            for ch in phone[digits[i]]:            # 变化点: 选择列表由数字映射给出
                path.append(ch)
                backtrack(i + 1)
                path.pop()

        backtrack(0)
        return res""",
        "time": "O(4^n·n)（7、9 对应 4 个字母）",
        "space": "O(n)（递归栈，不含输出）",
        "pitfalls": [
            "digits 为空要特判返回 []，否则会返回 [''] 一个空串组合",
            "收集时用 ''.join(path) 生成新串，直接 append(path) 会被后续 pop 改坏",
            "映射表别漏写 7 的 'pqrs' 与 9 的 'wxyz'（4 个字母）",
        ],
    },
    102: {
        "statement": "给定两个整数 n 和 k，返回范围 [1, n] 中所有可能的 k 个数的组合。可以按任意顺序返回答案。",
        "examples": [
            {"input": "n = 4, k = 2", "output": "[[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]"},
            {"input": "n = 1, k = 1", "output": "[[1]]"},
        ],
        "approach": "组合与顺序无关，信号是回溯框架 + start 参数：每层从 start 开始枚举，下一层传 i+1，天然保证不重不漏且内部有序。变化点在于剪枝——path 已有 len 个，剩余 [x, n] 共 n-x+1 个数字，凑不满 k 就整层剪掉，把搜索树压到实际组合数规模。",
        "code": """class Solution:
    def combine(self, n, k):
        res, path = [], []

        def backtrack(start):
            if len(path) == k:                     # 变化点: 凑满 k 个即收集
                res.append(path[:])
                return
            for x in range(start, n + 1):
                if len(path) + (n - x + 1) < k:    # 变化点: 剩余数字不够凑满，整层剪掉
                    return
                path.append(x)
                backtrack(x + 1)                   # 变化点: 组合传 i+1，顺序无关不重复
                path.pop()

        backtrack(1)
        return res""",
        "time": "O(C(n,k)·k)",
        "space": "O(k)（递归栈，不含输出）",
        "pitfalls": [
            "下一层传 x+1；传 x 会允许重复选取，不传推进会漏解",
            "剪枝用 return 不是 continue：候选从 x 到 n 都不够，后面的只会更少",
            "收集用 path[:] 拷贝快照，回溯复用同一个 path 列表",
        ],
    },
    103: {
        "statement": "给定一个不含重复数字的数组 nums，返回其所有可能的全排列。可以按任意顺序返回答案。",
        "examples": [
            {"input": "nums = [1,2,3]", "output": "[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]"},
            {"input": "nums = [0,1]", "output": "[[0,1],[1,0]]"},
        ],
        "approach": "排列与顺序有关、每个元素恰好用一次，信号是回溯框架 + used 标记：每层扫描所有未被使用的元素做选择，递归返回后撤销。变化点在于用 used 数组代替组合的 start 区间，path 长度等于数组长度时收集一个排列。",
        "code": """class Solution:
    def permute(self, nums):
        res, path = [], []
        used = [False] * len(nums)                 # 变化点: 排列用 used 标记已选元素

        def backtrack():
            if len(path) == len(nums):
                res.append(path[:])                # 变化点: 拷贝快照再收集
                return
            for i, x in enumerate(nums):
                if used[i]:
                    continue
                used[i] = True                     # 做选择
                path.append(x)
                backtrack()
                path.pop()                         # 撤销选择
                used[i] = False

        backtrack()
        return res""",
        "time": "O(n·n!)",
        "space": "O(n)（递归栈与 used，不含输出）",
        "pitfalls": [
            "used 与 path.pop() 必须成对还原，漏一边会少解或死循环",
            "收集时 path[:] 拷贝，否则最终答案全是空列表或同一引用",
            "本题元素互异可直接用下标标记；若含重复数字需先排序再加去重条件",
        ],
    },
    104: {
        "statement": "给你一个无重复元素的整数数组 candidates 和一个目标整数 target，找出 candidates 中所有可以使数字之和等于 target 的不同组合。同一个数字可以被无限制重复选取，组合至少包含一个候选数字；按任意顺序返回答案。",
        "examples": [
            {"input": "candidates = [2,3,6,7], target = 7", "output": "[[2,2,3],[7]]"},
            {"input": "candidates = [2,3,5], target = 8", "output": "[[2,2,2,2],[2,3,3],[3,5]]"},
        ],
        "approach": "“凑出 target 且可重复选取”是回溯框架的变体：递归参数带剩余额度 rest，每选一个 x 就 rest 减 x，rest 归零收集。变化点有两处——下一层仍从 i 开始（允许重复选当前数）；先把候选排序，遇到 x > rest 直接 break 剪枝，后面的候选只会更大。",
        "code": """class Solution:
    def combinationSum(self, candidates, target):
        candidates.sort()                          # 变化点: 排序后才能用 break 剪枝
        res, path = [], []

        def backtrack(start, rest):
            if rest == 0:
                res.append(path[:])
                return
            for i in range(start, len(candidates)):
                x = candidates[i]
                if x > rest:
                    break                          # 变化点: 候选有序，后面只会更大
                path.append(x)
                backtrack(i, rest - x)             # 变化点: 可重复选取，下一层仍从 i 开始
                path.pop()

        backtrack(0, target)
        return res""",
        "time": "指数级（剪枝后为实际搜索树大小）",
        "space": "O(target / 最小候选值)（递归栈）",
        "pitfalls": [
            "下一层传 i 而不是 i + 1，否则重复选取失效直接漏解",
            "剪枝用 break 不是 continue：排序后 x > rest，后续候选必然更大",
            "rest == 0 收集、rest < 0 由剪枝兜底，不要在循环里再写冗余的 rest < 0 判断",
        ],
    },
    105: {
        "statement": "n 皇后问题研究如何将 n 个皇后放置在 n×n 的棋盘上，且任意两个皇后不能互相攻击——即不能处于同一行、同一列或同一条对角线（两个方向都算）。本题只需求出不同的解决方案的数量，不需要返回具体的棋盘布局。",
        "examples": [
            {"input": "n = 4", "output": "2"},
            {"input": "n = 1", "output": "1"},
        ],
        "approach": "逐行放置天然消去行冲突，信号是回溯框架：列冲突用 cols 集合判重，两条斜线方向分别用行减列 r-c、行加列 r+c 两个不变量作键。变化点在于本题只要方案数——递归走到第 n 行时计数加一，无需维护 path 或棋盘，撤销时三个集合成对删除。",
        "code": """class Solution:
    def totalNQueens(self, n):
        cols, diag1, diag2 = set(), set(), set()
        count = 0

        def backtrack(r):
            nonlocal count
            if r == n:                             # 变化点: 只数方案数，不保存棋盘
                count += 1
                return
            for c in range(n):
                if c in cols or (r - c) in diag1 or (r + c) in diag2:   # 变化点: 列与两条对角线判重
                    continue
                cols.add(c)
                diag1.add(r - c)
                diag2.add(r + c)
                backtrack(r + 1)
                cols.remove(c)                     # 撤销选择
                diag1.remove(r - c)
                diag2.remove(r + c)

        backtrack(0)
        return count""",
        "time": "O(n!)",
        "space": "O(n)（递归栈与三个集合）",
        "pitfalls": [
            "对角线判重的键是 r-c 与 r+c，只判列会漏掉斜线攻击",
            "撤销时三个集合成对 remove，漏任何一个都会污染后续分支",
            "本题返回方案数，误建棋盘列表既费内存又容易偏离题意",
        ],
    },
    106: {
        "statement": "给出数字 n，生成所有由 n 对括号组成、且每一个左括号都有对应右括号闭合的合法括号序列。可以按任意顺序返回答案。",
        "examples": [
            {"input": "n = 3", "output": "[\"((()))\",\"(()())\",\"(())()\",\"()(())\",\"()()()\"]"},
            {"input": "n = 1", "output": "[\"()\"]"},
        ],
        "approach": "长度固定 2n、每步在 '(' 与 ')' 中二选一，信号是回溯框架，但选择受两条合法性约束：已用左括号数 < n 才能加 '('；已用右括号数 < 已用左括号数才能加 ')'。变化点在于用 left/right 计数代替扫描检查，长度凑满 2n 时 join 收集。",
        "code": """class Solution:
    def generateParenthesis(self, n):
        res, path = [], []

        def backtrack(left, right):
            if len(path) == 2 * n:
                res.append(''.join(path))
                return
            if left < n:                           # 变化点: 左括号没用完就能加 '('
                path.append('(')
                backtrack(left + 1, right)
                path.pop()
            if right < left:                       # 变化点: 已用右括号少于左括号才合法
                path.append(')')
                backtrack(left, right + 1)
                path.pop()

        backtrack(0, 0)
        return res""",
        "time": "O(4^n / √n)（卡特兰数个合法序列）",
        "space": "O(n)（递归栈，不含输出）",
        "pitfalls": [
            "两条约束缺一不可，只判数量会生成 ')(' 这类非法前缀",
            "加 ')' 的条件是 right < left（已用右括号少于已用左括号），写成 right < n 会提前产出非法串",
            "长度凑满 2n 才收集，别用 left==n 就提前 join，此时右括号还没用完",
        ],
    },
    107: {
        "statement": "给定 m×n 的网格 board 和一个字符串单词 word，如果 word 存在于网格中返回 true，否则返回 false。单词必须由网格中相邻（上下左右）的字母按顺序构成，同一个单元格的字母不允许在单词中重复使用。",
        "examples": [
            {"input": "board = [['A','B','C','E'],['S','F','C','S'],['A','D','E','E']], word = \"ABCCED\"", "output": "true"},
            {"input": "board = [['A','B','C','E'],['S','F','C','S'],['A','D','E','E']], word = \"ABCB\"", "output": "false"},
        ],
        "approach": "从每个格子尝试匹配 word 的第 k 个字符，匹配则向四邻推进第 k+1 个，这是网格 DFS 与回溯的合体：占位标记防回头，递归结束后恢复原字符。变化点在于 DFS 参数带匹配进度 k，k 走到词尾即宣告成功；外层必须枚举所有格子作为起点。",
        "code": """class Solution:
    def exist(self, board, word):
        m, n = len(board), len(board[0])

        def dfs(i, j, k):
            if board[i][j] != word[k]:             # 变化点: 当前格必须匹配第 k 个字符
                return False
            if k == len(word) - 1:
                return True
            saved, board[i][j] = board[i][j], '#'  # 占位防回头
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                ni, nj = i + di, j + dj
                if 0 <= ni < m and 0 <= nj < n and dfs(ni, nj, k + 1):
                    board[i][j] = saved            # 变化点: 成功路径也要恢复原字符
                    return True
            board[i][j] = saved                    # 变化点: 失败时撤销占位
            return False

        for i in range(m):
            for j in range(n):
                if dfs(i, j, 0):
                    return True
        return False""",
        "time": "O(mn·3^L)，L 为单词长度",
        "space": "O(L)（递归栈）",
        "pitfalls": [
            "占位符 '#' 要在四方向递归之后恢复，否则会挡住兄弟分支与后续起点",
            "匹配成功同样要恢复原字符再返回，外层还在继续枚举起点",
            "起点必须枚举所有格子，只从 (0,0) 开始会漏解",
        ],
    },
    108: {
        "statement": "给定一个按严格升序排列的整数数组 nums，请将其转换为一棵高度平衡的二叉搜索树。高度平衡二叉树要求每个节点的左右两个子树的高度差的绝对值不超过 1。答案不唯一，返回任何符合题意的树均可。",
        "examples": [
            {"input": "nums = [-10,-3,0,5,9]", "output": "[0,-3,9,-10,null,5]（任意平衡 BST 均可）"},
            {"input": "nums = [1,3]", "output": "[1,null,3] 或 [3,1]"},
        ],
        "approach": "有序数组的中点必是平衡 BST 的根，信号是分治模板：取中点建根，左半区间递归建左子树、右半区间递归建右子树，子树规模减半、两侧天然平衡。变化点在于拆分方式取 mid = (lo+hi)//2，基准情形是区间为空返回 None。",
        "code": """class Solution:
    def sortedArrayToBST(self, nums):
        def build(lo, hi):
            if lo > hi:                            # 变化点: 区间为空返回 None
                return None
            mid = (lo + hi) // 2                   # 变化点: 中点作根，两侧天然平衡
            node = TreeNode(nums[mid])
            node.left = build(lo, mid - 1)
            node.right = build(mid + 1, hi)
            return node

        return build(0, len(nums) - 1)""",
        "time": "O(n)",
        "space": "O(log n)（递归栈，不计输出树）",
        "pitfalls": [
            "mid 取左中点或右中点都合法，但左右区间边界要与之一致、不得重叠",
            "基准情形 lo > hi 返回 None，漏写会无限递归",
            "答案不唯一，与官方示例树形状不同不代表错误，平衡且是 BST 即可",
        ],
    },
    109: {
        "statement": "给定链表的头结点 head，请将其按节点值升序排列并返回排序后的链表头。要求时间复杂度为 O(n log n)；链表节点数在 [0, 5×10⁴] 范围内。",
        "examples": [
            {"input": "head = [4,2,1,3]", "output": "[1,2,3,4]"},
            {"input": "head = [-1,5,3,4,0]", "output": "[-1,0,3,4,5]"},
        ],
        "approach": "链表不便随机访问、快排不占优，归并排序是 O(n log n) 的自然选择，信号是分治：快慢指针找中点断成两半，分别递归排序，再按“合并两个有序链表”方式拼接。变化点在于快指针先走一步让中点落在前半段、断链后再递归，合并阶段复用 dummy 头技巧。",
        "code": """class Solution:
    def sortList(self, head):
        if not head or not head.next:
            return head

        slow, fast = head, head.next               # 变化点: fast 先走一步，中点必落前半段
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        mid = slow.next
        slow.next = None                           # 变化点: 断链后才能分别递归

        left = self.sortList(head)
        right = self.sortList(mid)

        dummy = cur = ListNode(0)                  # 变化点: 合并=拼接两个有序链表
        while left and right:
            if left.val <= right.val:
                cur.next, left = left, left.next
            else:
                cur.next, right = right, right.next
            cur = cur.next
        cur.next = left if left else right
        return dummy.next""",
        "time": "O(n log n)",
        "space": "O(log n)（递归栈）",
        "pitfalls": [
            "找中点时 fast 从 head.next 出发，两节点链表才切得开，否则死循环",
            "slow.next = None 必须在两次递归之前执行，否则递归处理的仍是整条链",
            "合并结束后把剩余部分 cur.next 接上，漏接会丢尾部节点",
        ],
    },
    110: {
        "statement": "给你一个 n×n 的矩阵 grid（n 是 2 的幂），请为它建立四叉树：若当前区域的值全部相同，建一个 isLeaf 为 True、val 为该值的叶子节点；否则建 isLeaf 为 False 的内部节点，把区域四等分（左上、右上、左下、右下），依次递归为四个子节点。",
        "examples": [
            {"input": "grid = [[0,1],[1,0]]", "output": "内部节点，四个叶子依次为 [0],[1],[1],[0]"},
            {"input": "grid = [[1,1],[1,1]]", "output": "单个叶子节点 [1]"},
        ],
        "approach": "四叉树是二维分治：大区域可拆成四个同构小区域，信号正是分治模板的“拆分方式与合并”。变化点在于同值判定先行——先检查整块区域是否同值，同值建叶子返回，否则四等分递归；内部节点的 val 无意义，填任意值即可。",
        "code": """class Solution:
    def construct(self, grid):
        n = len(grid)

        def same(r, c, size):
            val = grid[r][c]
            for i in range(r, r + size):
                for j in range(c, c + size):
                    if grid[i][j] != val:
                        return False
            return True

        def build(r, c, size):
            if same(r, c, size):                   # 变化点: 区域同值合并为叶子
                return Node(grid[r][c] == 1, True, None, None, None, None)
            half = size // 2
            return Node(True, False,               # 变化点: 四象限递归，内部 val 任意
                        build(r, c, half),
                        build(r, c + half, half),
                        build(r + half, c, half),
                        build(r + half, c + half, half))

        return build(0, 0, n)""",
        "time": "O(n² log n)",
        "space": "O(log n)（递归栈，不计输出树）",
        "pitfalls": [
            "先判同值再划分，顺序颠倒会把本可合并的区域错误细分",
            "四个象限的起点别写混：(r,c)、(r,c+half)、(r+half,c)、(r+half,c+half)",
            "内部节点 isLeaf 必须为 False，val 按惯例填 True 等任意值",
        ],
    },
    111: {
        "statement": "给你一个链表数组 lists，其中每个链表都已按节点值升序排列。请你将所有链表合并成一个升序链表，并返回合并后的头结点。lists 可能为空或包含空链表，节点总数可达 10⁴。",
        "examples": [
            {"input": "lists = [[1,4,5],[1,3,4],[2,6]]", "output": "[1,1,2,3,4,4,5,6]"},
            {"input": "lists = []", "output": "[]"},
        ],
        "approach": "k 条有序序列归并是堆的典型场景：把每条链的当前头节点放进小顶堆，弹出最小者接到结果链尾部，再把它的后继补进堆，直到堆空。变化点在于堆元素必须带链表序号 i 做平局裁决——ListNode 之间不可比较，(val, i, node) 三元组才能入堆。",
        "code": """import heapq

class Solution:
    def mergeKLists(self, lists):
        dummy = cur = ListNode(0)
        h = []
        for i, node in enumerate(lists):
            if node:
                heapq.heappush(h, (node.val, i, node))   # 变化点: 三元组入堆，序号避免比较节点

        while h:
            _, i, node = heapq.heappop(h)
            cur.next = node
            cur = cur.next
            if node.next:
                heapq.heappush(h, (node.next.val, i, node.next))   # 变化点: 弹出后补该链的下一个节点
        return dummy.next""",
        "time": "O(N log k)，N 为总节点数、k 为链表条数",
        "space": "O(k)",
        "pitfalls": [
            "堆元素必须带序号 i，值相同时 heapq 会尝试比较 ListNode 而抛 TypeError",
            "空链表头（None）不要入堆；弹出节点的 next 为空时也不再补堆",
            "补堆的对象是 node.next，别把原始 lists 里的头节点重复入堆",
        ],
    },
    112: {
        "statement": "给你一个整数数组 nums，请找出和最大的连续子数组（子数组最少包含一个元素），返回其最大和。数组长度至少为 1，元素可能为负数。",
        "examples": [
            {"input": "nums = [-2,1,-3,4,-1,2,1,-5,4]", "output": "6"},
            {"input": "nums = [5,4,-1,7,8]", "output": "23"},
        ],
        "approach": "cur 定义为“以当前元素结尾的最大子数组和”：要么接上以 i-1 结尾的那段，要么从 x 重新开始，信号是只依赖前一个状态，套 Kadane 模板滚动推进。变化点在于转移方程 max(x, cur + x)，另用 best 记录全程最大值作为答案。",
        "code": """class Solution:
    def maxSubArray(self, nums):
        cur = best = nums[0]                       # 变化点: 从首元素起步，全负也不出错
        for x in nums[1:]:
            cur = max(x, cur + x)                  # 变化点: 接上前一段或从 x 重新开始
            best = max(best, cur)
        return best""",
        "time": "O(n)",
        "space": "O(1)",
        "pitfalls": [
            "cur 从 nums[0] 起步而不是 0，全负数组要返回最大的单个元素",
            "best 必须随 cur 同步更新，只在循环外取 cur 会漏掉中段最优值",
            "cur 的语义是“以当前元素结尾”，它是过程量，答案永远是 best",
        ],
    },
    113: {
        "statement": "给定一个长度为 n 的环形整数数组 nums（首尾相接成环），返回其非空子数组的最大可能和。环形子数组允许跨过首尾边界，但不能使用同一位置两次，即子数组长度不超过 n。",
        "examples": [
            {"input": "nums = [1,-2,3,-2]", "output": "3"},
            {"input": "nums = [5,-3,5]", "output": "10"},
        ],
        "approach": "环形答案只有两种来源：不跨界的普通最大子数组和，或跨界的“总和减去中间那段最小子数组和”。信号是 Kadane 模板跑两遍，最大、最小两套滚动变量在同一循环里同步推进。变化点在于全负数组的特判——此时最小子数组吞掉整个数组，total - best_min 会得到非法的 0（空段），必须直接返回 best_max。",
        "code": """class Solution:
    def maxSubarraySumCircular(self, nums):
        cur_max = best_max = float('-inf')
        cur_min = best_min = float('inf')
        total = 0
        for x in nums:
            total += x
            cur_max = max(x, cur_max + x)
            best_max = max(best_max, cur_max)
            cur_min = min(x, cur_min + x)          # 变化点: 同步维护最小子数组和
            best_min = min(best_min, cur_min)
        if best_max < 0:                           # 变化点: 全负时直接返回最大元素
            return best_max
        return max(best_max, total - best_min)     # 变化点: 环形=max(不跨环, 总和-最小子数组)""",
        "time": "O(n)",
        "space": "O(1)",
        "pitfalls": [
            "全负数组必须返回 best_max，total - best_min 会算出 0 这个空段的假答案",
            "跨界情形的本质是挖掉一段最小和，用等价转化而不是真的枚举起点",
            "最大、最小两套滚动变量在同一循环里各自独立更新，别互相串值",
        ],
    },
}
