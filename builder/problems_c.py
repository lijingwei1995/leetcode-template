# -*- coding: utf-8 -*-
"""题解数据 68-88：二叉树 / 层次遍历 / 二叉搜索树。"""

DATA = {
    68: {
        "statement": "给定一棵二叉树的根节点 root，返回它的最大深度。二叉树的最大深度是指从根节点到最远叶子节点的最长路径上的节点数。叶子节点是指没有子节点的节点。",
        "examples": [
            {"input": "root = [3,9,20,null,null,15,7]", "output": "3"},
            {"input": "root = [1,null,2]", "output": "2"},
        ],
        "approach": "整棵树的深度可由左右子树的深度直接推出，信号是“子问题结构 + 无状态合并”，直接套二叉树递归模板：空树深度为 0，非空取左右子树深度的最大值加 1。变化点在于递归返回值本身就是答案，不需要额外数组或全局变量。",
        "code": """class Solution:
    def maxDepth(self, root):
        if not root:
            return 0
        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))   # 变化点: 深度 = 左右子树最大深度 + 1""",
        "time": "O(n)",
        "space": "O(h)（递归栈，最坏退化为链状时 O(n)）",
        "pitfalls": [
            "空树返回 0，递归基必须先写",
            "深度按节点数计，不是边数，叶子自身贡献 1",
            "递归深度为树高，最坏退化为链状时栈深 O(n)",
        ],
    },
    69: {
        "statement": "给定两棵二叉树的根节点 p 和 q，编写函数检验这两棵树是否相同。如果两棵树在结构上相同，并且节点具有相同的值，则认为它们是相同的。",
        "examples": [
            {"input": "p = [1,2,3], q = [1,2,3]", "output": "true"},
            {"input": "p = [1,2], q = [1,null,2]", "output": "false"},
        ],
        "approach": "“两棵树同步递归”是本题信号，仍是二叉树递归模板，只是把单棵树的双向递归改成 p、q 成对下传。任一棵为空而另一棵非空、或当前值不等即判假；两边同时为空为真。变化点在于递归参数是两个节点，必须沿相同方向同步下走。",
        "code": """class Solution:
    def isSameTree(self, p, q):
        if not p and not q:
            return True
        if not p or not q or p.val != q.val:      # 变化点: 结构不同或值不同都判假
            return False
        return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)""",
        "time": "O(n)",
        "space": "O(h)（最坏 O(n)）",
        "pitfalls": [
            "先判双空、再判单空，两个递归基的顺序不能颠倒",
            "结构不同（一棵有左孩子另一棵没有）也要返回 False，不能只比值",
            "值相等时继续比较左右子树，两边递归方向必须一致",
        ],
    },
    70: {
        "statement": "给定一棵二叉树的根节点 root，翻转这棵二叉树，并返回其根节点。翻转即将每个节点的左子树和右子树整体交换。",
        "examples": [
            {"input": "root = [4,2,7,1,3,6,9]", "output": "[4,7,2,9,6,3,1]"},
        ],
        "approach": "翻转整棵树等于翻转左右子树再交换，是二叉树递归模板最典型的“后序处理”。先递归得到已翻转的左右子树，再交换两个孩子的引用，空树返回 None。变化点是交换动作发生在递归之后，且必须返回子树新根供上层拼接。",
        "code": """class Solution:
    def invertTree(self, root):
        if not root:
            return None
        root.left, root.right = self.invertTree(root.right), self.invertTree(root.left)   # 变化点: 翻转后的左右子树直接互换
        return root""",
        "time": "O(n)",
        "space": "O(h)（最坏 O(n)）",
        "pitfalls": [
            "用元组赋值一次性交换，先递归后交换，避免引用覆盖导致漏翻",
            "空树返回 None，不要抛异常",
            "原 root 仍是新树的根，函数必须返回它",
        ],
    },
    71: {
        "statement": "给定一棵二叉树的根节点 root，检查它是否轴对称，即检查它是否与自身的镜像相同：每个节点的左子树与右子树互为镜像。",
        "examples": [
            {"input": "root = [1,2,2,3,4,4,3]", "output": "true"},
            {"input": "root = [1,2,2,null,3,null,3]", "output": "false"},
        ],
        "approach": "对称判断需要“两个指针镜像下行”，仍是二叉树递归模板的变体：递归函数接收一对节点，同空为对称、单空或值不等为不对称。变化点在于递归调用是交叉镜像方向：a 的左配 b 的右、a 的右配 b 的左，而不是普通同向比较。入口把 root 传两次。",
        "code": """class Solution:
    def isSymmetric(self, root):
        def mirror(a, b):
            if not a and not b:
                return True
            if not a or not b or a.val != b.val:
                return False
            return mirror(a.left, b.right) and mirror(a.right, b.left)   # 变化点: 交叉比较镜像位置
        return mirror(root, root)                 # 变化点: 同一根传两次，与自身镜像比较""",
        "time": "O(n)",
        "space": "O(h)（最坏 O(n)）",
        "pitfalls": [
            "递归入口要传 (root, root)，不要先拆成左右子树再分别处理",
            "比较方向必须交叉：a.left 配 b.right，写反就退化成相同的树判断",
            "值不等时立即返回 False，防止继续深入浪费比较",
        ],
    },
    72: {
        "statement": "给定两个整数数组 preorder 和 inorder，其中 preorder 是二叉树的前序遍历，inorder 是同一棵树的中序遍历，构造二叉树并返回其根节点。假设树中没有重复的值。",
        "examples": [
            {"input": "preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]", "output": "[3,9,20,null,null,15,7]"},
            {"input": "preorder = [-1], inorder = [-1]", "output": "[-1]"},
        ],
        "approach": "前序首元素是根、中序中根的左边是左子树右边是右子树，信号是“分治构造”，套树递归模板：先建根，再按中序切出区间递归。变化点一：用哈希表把中序值映射到下标，避免每层线性扫描；变化点二：用一个自增指针顺序消耗前序数组，天然保证根的取用顺序与建树次序一致。",
        "code": """class Solution:
    def buildTree(self, preorder, inorder):
        idx = {v: i for i, v in enumerate(inorder)}   # 变化点: 值→中序下标哈希，免线性扫描
        self.pos = 0

        def build(left, right):
            if left > right:
                return None
            root = TreeNode(preorder[self.pos])
            self.pos += 1                             # 变化点: 前序指针顺序消耗根
            mid = idx[root.val]
            root.left = build(left, mid - 1)
            root.right = build(mid + 1, right)
            return root

        return build(0, len(inorder) - 1)""",
        "time": "O(n)",
        "space": "O(n)（哈希表 + 递归栈）",
        "pitfalls": [
            "先取前序元素建根、再查中序下标，self.pos 自增要放在建子树之前",
            "递归边界是闭区间 [left, right]，left > right 返回 None",
            "题目保证无重复值，哈希映射才成立；有重复时此法失效",
        ],
    },
    73: {
        "statement": "给定两个整数数组 inorder 和 postorder，其中 inorder 是二叉树的中序遍历，postorder 是同一棵树的后序遍历，构造二叉树并返回其根节点。假设树中没有重复的值。",
        "examples": [
            {"input": "inorder = [9,3,15,20,7], postorder = [9,15,7,20,3]", "output": "[3,9,20,null,null,15,7]"},
            {"input": "inorder = [-1], postorder = [-1]", "output": "[-1]"},
        ],
        "approach": "后序末元素是根，与 105 题同属分治构造，仍是树递归模板，只是根来自数组尾部、指针递减。中序哈希定位切分点后递归构造左右子树。变化点：必须先递归建右子树再建左子树，因为指针从后往前消耗时，右子树的后序段恰好排在左子树之后。",
        "code": """class Solution:
    def buildTree(self, inorder, postorder):
        idx = {v: i for i, v in enumerate(inorder)}
        self.pos = len(postorder) - 1

        def build(left, right):
            if left > right:
                return None
            root = TreeNode(postorder[self.pos])
            self.pos -= 1                             # 变化点: 后序从尾部倒序取根
            mid = idx[root.val]
            root.right = build(mid + 1, right)        # 变化点: 必须先建右子树再建左子树
            root.left = build(left, mid - 1)
            return root

        return build(0, len(inorder) - 1)""",
        "time": "O(n)",
        "space": "O(n)（哈希表 + 递归栈）",
        "pitfalls": [
            "指针从 len(postorder)-1 起递减，根取的是 postorder 末尾元素",
            "先建右子树、后建左子树，顺序写反会把右子树的根错配给左子树",
            "空数组时 build(0, -1) 直接返回 None，无需单独特判",
        ],
    },
    74: {
        "statement": "给定二叉树的根节点 root，填充它的每个 next 指针，让该指针指向其下一个右侧节点。如果找不到下一个右侧节点，则将 next 指针置为 null。初始状态下所有 next 指针都是 null，且树不一定是完美二叉树。",
        "examples": [
            {"input": "root = [1,2,3,4,5,null,7]", "output": "[1,#,2,3,#,4,5,7,#]"},
        ],
        "approach": "“逐层连接”直接指向层序模板：队列快照就是同一层，处理第 i 个节点时让同层前一个的 next 指向它即可，整层串成一条链。孩子判空后收进新队列进入下一层。变化点：利用枚举下标在同层内串链，无需 dummy 节点或指针跳跃技巧。",
        "code": """class Solution:
    def connect(self, root):
        if not root:
            return None
        queue = [root]
        while queue:
            nxt = []
            for i, node in enumerate(queue):
                if i:                                 # 变化点: 同层前一个节点的 next 指向当前节点
                    queue[i - 1].next = node
                if node.left:
                    nxt.append(node.left)
                if node.right:
                    nxt.append(node.right)
            queue = nxt
        return root""",
        "time": "O(n)",
        "space": "O(n)（队列）",
        "pitfalls": [
            "树不是满二叉树，孩子入队前必须判空",
            "i == 0 的节点没有前驱，要跳过串链，否则会接到上一层末尾",
            "每层处理完用新列表替换队列，跨层节点不能混在同一个快照里",
        ],
    },
    75: {
        "statement": "给定二叉树的根节点 root，将其展开为一个单链表：展开后的链表仍使用 TreeNode，right 指针指向下一个节点，left 指针始终为 null，且顺序与二叉树的先序遍历相同。函数无返回值，需原地修改。",
        "examples": [
            {"input": "root = [1,2,5,3,4,null,6]", "output": "[1,null,2,null,3,null,4,null,5,null,6]"},
            {"input": "root = []", "output": "[]"},
        ],
        "approach": "按先序展开可以从尾部往前接：按“右→左→根”的逆先序递归访问，用全局 prev 记录上一个访问的节点。模板仍是树递归，变化点是把 node.right 指向 prev、left 置 None，后序位置就地改指针。由于先递归孩子、后改本节点，孩子的引用不会被提前覆盖。",
        "code": """class Solution:
    def flatten(self, root):
        self.prev = None

        def flat(node):
            if not node:
                return
            flat(node.right)                          # 变化点: 逆先序访问，右子树最先展开
            flat(node.left)
            node.right = self.prev                    # 变化点: 右指针接上已展开的后续部分
            node.left = None                          # 变化点: 左指针必须清空形成单链
            self.prev = node

        flat(root)""",
        "time": "O(n)",
        "space": "O(h)（递归栈，最坏 O(n)）",
        "pitfalls": [
            "递归顺序必须是右→左→根，与先序相反，才能从链尾往前接",
            "node.left 必须置 None，只改右指针会留下残余子树",
            "函数无返回值，空树时直接结束即可",
        ],
    },
    76: {
        "statement": "给定二叉树的根节点 root 和表示目标和的整数 targetSum，判断是否存在从根节点到叶子节点的路径，使路径上所有节点值相加等于 targetSum。叶子节点是指没有子节点的节点。",
        "examples": [
            {"input": "root = [5,4,8,11,null,13,4,7,2,null,null,null,1], targetSum = 22", "output": "true"},
            {"input": "root = [1,2,3], targetSum = 5", "output": "false"},
        ],
        "approach": "“根到叶路径 + 数值目标”是二叉树递归信号：把剩余目标和逐层下传做减法，到达叶子时判断剩余值是否恰为叶子值。变化点：只在叶子处判定，中间节点即使剩余减到 0 也必须继续，因为目标和必须以叶子结尾。",
        "code": """class Solution:
    def hasPathSum(self, root, targetSum):
        if not root:
            return False
        if not root.left and not root.right:      # 变化点: 只在叶子处判定剩余目标
            return targetSum == root.val
        return self.hasPathSum(root.left, targetSum - root.val) or \\
               self.hasPathSum(root.right, targetSum - root.val)""",
        "time": "O(n)",
        "space": "O(h)（最坏 O(n)）",
        "pitfalls": [
            "空树返回 False，即使 targetSum 为 0",
            "必须走到叶子才能判定，中途剩余为 0 不算满足条件",
            "递归下传用 targetSum - node.val 做减法，而不是累加后再比较",
        ],
    },
    77: {
        "statement": "给定二叉树的根节点 root，树中每个节点存放一个 0 到 9 的数字。每条从根到叶的路径代表一个数字，例如路径 1→2→3 代表数字 123。计算所有根到叶路径生成的数字之和。",
        "examples": [
            {"input": "root = [1,2,3]", "output": "25"},
            {"input": "root = [4,9,0,5,1]", "output": "1026"},
        ],
        "approach": "“根到叶拼数字再求和”仍是二叉树递归：把当前累计值下传，每层乘 10 加当前节点值；叶子处把拼好的数字作为该路径贡献返回，非叶子返回左右子树贡献之和。变化点：拼接发生在判空之后、叶子判定之前，每个节点只拼一次。",
        "code": """class Solution:
    def sumNumbers(self, root):
        def dfs(node, cur):
            if not node:
                return 0
            cur = cur * 10 + node.val             # 变化点: 每层乘 10 拼接当前数字
            if not node.left and not node.right:  # 变化点: 叶子处路径数字定格
                return cur
            return dfs(node.left, cur) + dfs(node.right, cur)

        return dfs(root, 0)""",
        "time": "O(n)",
        "space": "O(h)（最坏 O(n)）",
        "pitfalls": [
            "空子树贡献 0，必须返回数值而不是 None",
            "数字要在叶子处定格返回，非叶子节点只下传不结算",
            "拼接公式是 cur * 10 + val，写成 val * 10 + cur 就错了",
        ],
    },
    78: {
        "statement": "二叉树中的路径定义为节点序列中每对相邻节点之间都存在边，且每个节点至多出现一次；路径至少包含一个节点，不必经过根节点。路径和是路径中各节点值的总和。给定根节点 root，返回最大路径和。节点值可能为负。",
        "examples": [
            {"input": "root = [1,2,3]", "output": "6"},
            {"input": "root = [-10,9,20,null,null,15,7]", "output": "42"},
        ],
        "approach": "信号是“答案要在每个节点处汇总拐点路径”，套树递归模板：递归返回“从当前节点向下延伸的单向最大贡献”。左右贡献为负则弃用取 0；用当前值加左右两条贡献更新全局答案（可同时吃两条腿），但上抛时只能选一条。变化点：更新答案与返回贡献是两条线，返回值取 max(left, right)。",
        "code": """class Solution:
    def maxPathSum(self, root):
        self.ans = float("-inf")

        def gain(node):
            if not node:
                return 0
            left = max(gain(node.left), 0)        # 变化点: 子树贡献为负时弃用
            right = max(gain(node.right), 0)
            self.ans = max(self.ans, node.val + left + right)   # 变化点: 以当前节点为拐点更新答案
            return node.val + max(left, right)    # 变化点: 上抛只带一条腿，路径不能分叉

        gain(root)
        return self.ans""",
        "time": "O(n)",
        "space": "O(h)（最坏 O(n)）",
        "pitfalls": [
            "节点值可能为负，贡献要与 0 取 max 再参与计算",
            "全局答案初始化为 -inf，全负树的答案是最大负值而不是 0",
            "上抛贡献不能同时加左右，否则路径在当前节点分叉",
        ],
    },
    79: {
        "statement": "实现一个二叉搜索树迭代器类 BSTIterator，表示按中序遍历 BST 的迭代器：初始化传入根节点；next() 返回中序遍历的下一个最小数；hasNext() 判断是否还有下一个数。要求两者平均时间 O(1)，空间 O(h)，h 为树高。",
        "examples": [
            {"input": "inputs = [\"BSTIterator\",\"next\",\"next\",\"hasNext\",\"next\",\"hasNext\",\"next\",\"hasNext\",\"next\",\"hasNext\",\"next\",\"hasNext\"], root = [7,3,15,null,null,9,20]", "output": "[null,3,7,true,9,true,15,true,20,false]"},
        ],
        "approach": "“中序遍历惰性化”指向 BST 中序模板：用栈保存最左链，栈顶就是下一个最小节点。next() 弹出栈顶后把其右子树的最左链压栈，遍历状态一次只推进一小段。变化点：构造函数只压根的最左链而不全量遍历，next() 的摊还成本才是 O(1)。",
        "code": """class BSTIterator:
    def __init__(self, root):
        self.stack = []
        self._push_left(root)                     # 变化点: 初始化只压最左链，惰性遍历

    def _push_left(self, node):
        while node:
            self.stack.append(node)
            node = node.left

    def next(self):
        node = self.stack.pop()
        if node.right:                            # 变化点: 弹出后压入右子树的最左链
            self._push_left(node.right)
        return node.val

    def hasNext(self):
        return bool(self.stack)""",
        "time": "next 均摊 O(1)",
        "space": "O(h)",
        "pitfalls": [
            "构造函数不要把整棵树遍历成数组，会超出 O(h) 空间要求",
            "next() 弹栈后若右子树非空，必须把右子树最左链压入，否则中序断链",
            "hasNext() 判断栈是否非空，不要另设游标变量造成状态不一致",
        ],
    },
    80: {
        "statement": "给定一棵完全二叉树的根节点 root，返回树的节点个数。完全二叉树中除最底层外每层都填满，最底层节点集中在左侧。进阶要求：遍历树节点数少于 O(n) 的时间复杂度。",
        "examples": [
            {"input": "root = [1,2,3,4,5,6]", "output": "6"},
            {"input": "root = []", "output": "0"},
            {"input": "root = [1]", "output": "1"},
        ],
        "approach": "完全二叉树“子树高度可直接量出”是关键信号：沿最左链量高度只要 O(h)。若左右等高，左子树是满树（2^h 个节点含根），答案为 2^h 加上递归右子树；否则右子树是满树，答案为 2^rh 加上递归左子树。变化点：每次递归至少砍掉一整棵满子树，结合树递归与二分思想，复杂度降到 O(log² n)。",
        "code": """class Solution:
    def countNodes(self, root):
        if not root:
            return 0
        lh = self._depth(root.left)
        rh = self._depth(root.right)
        if lh == rh:                              # 变化点: 左右等高 ⇒ 左子树满，整块砍掉
            return (1 << lh) + self.countNodes(root.right)
        return (1 << rh) + self.countNodes(root.left)   # 变化点: 右子树满，砍右保左

    def _depth(self, node):
        h = 0
        while node:
            h += 1
            node = node.left                      # 变化点: 沿最左链 O(h) 量高度
        return h""",
        "time": "O(log² n)",
        "space": "O(log n)",
        "pitfalls": [
            "满子树的节点数是 2^h（h 为其高度），指数层级别数错",
            "等高时砍左子树递归右，不等高时砍右子树递归左，方向写反结果就错",
            "空树返回 0，先判空再量高度，否则空指针",
        ],
    },
    81: {
        "statement": "给定二叉树和其中两个节点 p、q，找到它们的最近公共祖先。最近公共祖先是同时为 p 和 q 的祖先且深度最大的节点（一个节点可以是它自己的祖先）。所有节点值唯一，且 p、q 都存在于树中。",
        "examples": [
            {"input": "root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1", "output": "3"},
            {"input": "root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 4", "output": "5"},
        ],
        "approach": "后序递归自底向上汇聚信息是本题信号，套树递归模板：递归返回“子树中是否命中 p 或 q”。命中目标或空节点直接上抛；左右子树各命中一个时，当前节点就是最近公共祖先；只有一侧命中就继续上抛那一侧。变化点：返回的是节点对象而非布尔值，命中判定用 is 比较节点身份。",
        "code": """class Solution:
    def lowestCommonAncestor(self, root, p, q):
        if not root or root is p or root is q:    # 变化点: 命中目标节点直接上抛
            return root
        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)
        if left and right:                        # 变化点: 两侧各命中一个，当前即 LCA
            return root
        return left or right""",
        "time": "O(n)",
        "space": "O(h)（最坏 O(n)）",
        "pitfalls": [
            "命中判定要用 root is p 节点身份比较，不要按值新建节点",
            "一个节点可以是另一个的祖先，递归基必须先判 root is p or root is q",
            "p、q 保证存在，无需处理找不到的情况，答案只可能是 p、q 或真正的分叉点",
        ],
    },
    82: {
        "statement": "给定二叉树的根节点 root，想象自己站在树的右侧，返回从顶部到底部能看到的节点值列表，即每一层最右边节点的值。",
        "examples": [
            {"input": "root = [1,2,3,null,5,null,4]", "output": "[1,3,4]"},
            {"input": "root = [1,null,3]", "output": "[1,3]"},
        ],
        "approach": "“每层只取一个特定节点”是层序模板信号：队列快照就是一层，最后一个元素即本层最右节点。逐层出队收集孩子进入下一层，每层只把末尾节点的值追加到答案。变化点：取 queue[-1].val 而不是 queue[0]，且一层只记一个值。",
        "code": """class Solution:
    def rightSideView(self, root):
        if not root:
            return []
        res = []
        queue = [root]
        while queue:
            res.append(queue[-1].val)             # 变化点: 每层最后一个节点即右视图
            queue = [c for node in queue for c in (node.left, node.right) if c]
        return res""",
        "time": "O(n)",
        "space": "O(n)（队列）",
        "pitfalls": [
            "取每层最后一个而非第一个，方向取反会得到左视图",
            "孩子收集必须判空过滤 None，否则访问 .val 报错",
            "空树返回空列表 []",
        ],
    },
    83: {
        "statement": "给定非空二叉树的根节点 root，以数组形式返回每一层节点值的平均值。与实际答案误差在 1e-5 以内的结果均可接受。",
        "examples": [
            {"input": "root = [3,9,20,null,null,15,7]", "output": "[3.00000,14.50000,11.00000]"},
            {"input": "root = [3,9,20,15,7]", "output": "[3.00000,14.50000,11.00000]"},
        ],
        "approach": "“逐层统计量”直接套层序模板：当前队列快照就是一层，先整层求和、除以层大小得到平均值，再把孩子收进新队列进入下一层。变化点：统计对象是整层节点值的和，遍历快照时只读值，不需要其他状态。",
        "code": """class Solution:
    def averageOfLevels(self, root):
        res = []
        queue = [root] if root else []
        while queue:
            res.append(sum(node.val for node in queue) / len(queue))   # 变化点: 整层求和除以层大小
            queue = [c for node in queue for c in (node.left, node.right) if c]
        return res""",
        "time": "O(n)",
        "space": "O(n)（队列）",
        "pitfalls": [
            "平均值用浮点除法 /，整除会丢精度",
            "孩子入队前判空过滤 None，防止 None.val 报错",
            "题目保证树非空，无需特判空树，但孩子判空不可省",
        ],
    },
    84: {
        "statement": "给定二叉树的根节点 root，返回其节点值的层序遍历结果：逐层、从左到右访问所有节点，结果按层分组为二维数组。",
        "examples": [
            {"input": "root = [3,9,20,null,null,15,7]", "output": "[[3],[9,20],[15,7]]"},
            {"input": "root = [1]", "output": "[[1]]"},
        ],
        "approach": "本题就是层序模板本体：队列快照即一层，把快照中每个节点的值收集为一组，再把所有孩子收进新队列，直到队空。变化点在于模板本身：记住“整层快照处理”的写法，其余层序题都是在它上面做局部修改。",
        "code": """class Solution:
    def levelOrder(self, root):
        if not root:
            return []
        res = []
        queue = [root]
        while queue:
            res.append([node.val for node in queue])   # 变化点: 队列快照即一整层
            queue = [c for node in queue for c in (node.left, node.right) if c]
        return res""",
        "time": "O(n)",
        "space": "O(n)（队列）",
        "pitfalls": [
            "先把当前层的值收集完、再统一收下一层孩子，避免层间混杂",
            "空树返回 []，不要返回 [[]]",
            "列表推导收集孩子时要记得过滤 None",
        ],
    },
    85: {
        "statement": "给定二叉树的根节点 root，返回其节点值的锯齿形层序遍历：第一层从左往右，第二层从右往左，如此逐层交替，结果按层分组为二维数组。",
        "examples": [
            {"input": "root = [3,9,20,null,null,15,7]", "output": "[[3],[20,9],[15,7]]"},
            {"input": "root = [1]", "output": "[[1]]"},
        ],
        "approach": "层序模板加层奇偶标记：仍然整层快照收集节点值，偶数层保持原序、奇数层反转后写入答案。变化点：只在输出阶段对 vals 做反转，队列内孩子仍按左→右顺序收集，下一层的遍历顺序不受影响。",
        "code": """class Solution:
    def zigzagLevelOrder(self, root):
        if not root:
            return []
        res = []
        queue = [root]
        level = 0
        while queue:
            vals = [node.val for node in queue]
            res.append(vals[::-1] if level % 2 else vals)   # 变化点: 奇数层反转输出
            queue = [c for node in queue for c in (node.left, node.right) if c]
            level += 1
        return res""",
        "time": "O(n)",
        "space": "O(n)（队列）",
        "pitfalls": [
            "反转只作用于输出列表，不要反转队列本身，否则下一层孩子顺序错乱",
            "层号从 0 开始，第 0 层（根层）是正序",
            "空树返回 []",
        ],
    },
    86: {
        "statement": "给定一棵二叉搜索树的根节点 root，树中节点值各不相同，返回树中任意两个不同节点值之间的最小差值。差值是一个正数，必须来自两个不同的节点。",
        "examples": [
            {"input": "root = [4,2,6,1,3]", "output": "1"},
            {"input": "root = [1,0,48,null,null,12,49]", "output": "1"},
        ],
        "approach": "BST 中序遍历得到升序序列，最小差值只能出现在相邻两个值之间，套 BST 中序模板：递归左子树、与上一个值比较、更新 prev。变化点：维护全局 prev 记录上一个中序值，比较只需 O(1)，无需把整棵树先展开成数组再扫一遍。",
        "code": """class Solution:
    def getMinimumDifference(self, root):
        self.prev = None
        self.ans = float("inf")

        def inorder(node):
            if not node:
                return
            inorder(node.left)
            if self.prev is not None:             # 变化点: 只比较相邻两个中序值
                self.ans = min(self.ans, node.val - self.prev)
            self.prev = node.val
            inorder(node.right)

        inorder(root)
        return self.ans""",
        "time": "O(n)",
        "space": "O(h)（递归栈）",
        "pitfalls": [
            "prev 用 is not None 判断，不能用真值判断，节点值可能为 0",
            "中序严格递增，差值 node.val - prev 天然非负，无需 abs",
            "最小差一定在相邻中序值之间，两两比较全部节点是多余功",
        ],
    },
    87: {
        "statement": "给定二叉搜索树的根节点 root 和整数 k，返回树中第 k 小的元素（k 从 1 开始计数）。进阶：如果树经常被插入、删除修改，能否进一步优化。",
        "examples": [
            {"input": "root = [3,1,4,null,2], k = 1", "output": "1"},
            {"input": "root = [5,3,6,2,4,null,null,1], k = 3", "output": "3"},
        ],
        "approach": "第 k 小对应中序遍历的第 k 次访问，套 BST 中序模板：左递归、访问时计数、右递归。用全局计数器递减，减到 0 时锁定当前节点值并提前终止后续递归。变化点：访问计数代替收集全部序列，只需走 O(h + k) 个节点。",
        "code": """class Solution:
    def kthSmallest(self, root, k):
        self.k = k
        self.ans = None

        def inorder(node):
            if not node or self.ans is not None:  # 变化点: 已找到答案立即剪枝
                return
            inorder(node.left)
            if self.ans is not None:
                return
            self.k -= 1                           # 变化点: 中序第 k 次访问即第 k 小
            if self.k == 0:
                self.ans = node.val
                return
            inorder(node.right)

        inorder(root)
        return self.ans""",
        "time": "O(h + k)",
        "space": "O(h)",
        "pitfalls": [
            "找到答案后要剪枝提前返回，不要把整棵树遍历完",
            "k 从 1 开始，计数器减到 0 时才取值",
            "剪枝条件用 ans is not None，不能用真值判断，0 也是合法答案",
        ],
    },
    88: {
        "statement": "给定二叉树的根节点 root，判断它是否是一棵有效的二叉搜索树。有效 BST 定义：左子树所有节点值均小于根，右子树所有节点值均大于根，且左右子树本身也必须是有效 BST。注意不能只与直接孩子比较。",
        "examples": [
            {"input": "root = [2,1,3]", "output": "true"},
            {"input": "root = [5,1,4,null,null,3,6]", "output": "false"},
        ],
        "approach": "BST 性质等价于“中序序列严格递增”，套 BST 中序模板做验证：递归左子树，失败则短路返回 False；用 prev 检查当前值是否大于上一个值；最后递归右子树。变化点：把中序访问改成逐个短路校验，任一步违规立即失败，无需真的收集整个序列。",
        "code": """class Solution:
    def isValidBST(self, root):
        self.prev = None

        def inorder(node):
            if not node:
                return True
            if not inorder(node.left):
                return False
            if self.prev is not None and node.val <= self.prev:   # 变化点: 中序必须严格递增
                return False
            self.prev = node.val
            return inorder(node.right)

        return inorder(root)""",
        "time": "O(n)",
        "space": "O(h)（最坏 O(n)）",
        "pitfalls": [
            "不能只比较父子两代，[5,4,6,null,null,3,7] 这类必须靠中序才能查出",
            "严格递增要求 node.val > prev，相等也判无效",
            "prev 用 is not None 判断，不能用真值判断，0 会误判",
        ],
    },
}
