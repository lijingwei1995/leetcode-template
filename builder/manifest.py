# -*- coding: utf-8 -*-
"""题库清单：顺序、分类、难度、LeetCode slug 与模板映射。
数据来源：《面试经典 150 题》学习计划。
"""

MANIFEST = [
    # 数组 / 字符串
    (1, "数组 / 字符串", "合并两个有序数组", "简单", "merge-sorted-array", ["two-pointer-opposite"]),
    (2, "数组 / 字符串", "移除元素", "简单", "remove-element", ["two-pointer-same"]),
    (3, "数组 / 字符串", "删除有序数组中的重复项", "简单", "remove-duplicates-from-sorted-array", ["two-pointer-same"]),
    (4, "数组 / 字符串", "删除有序数组中的重复项 II", "中等", "remove-duplicates-from-sorted-array-ii", ["two-pointer-same"]),
    (5, "数组 / 字符串", "多数元素", "简单", "majority-element", ["frequency-count"]),
    (6, "数组 / 字符串", "轮转数组", "中等", "rotate-array", ["two-pointer-opposite"]),
    (7, "数组 / 字符串", "买卖股票的最佳时机", "简单", "best-time-to-buy-and-sell-stock", ["prefix-decomposition", "greedy-linear"]),
    (8, "数组 / 字符串", "买卖股票的最佳时机 II", "中等", "best-time-to-buy-and-sell-stock-ii", ["greedy-linear"]),
    (9, "数组 / 字符串", "跳跃游戏", "中等", "jump-game", ["greedy-linear"]),
    (10, "数组 / 字符串", "跳跃游戏 II", "中等", "jump-game-ii", ["greedy-linear"]),
    (11, "数组 / 字符串", "H 指数", "中等", "h-index", ["frequency-count"]),
    (12, "数组 / 字符串", "O(1) 时间插入、删除和获取随机元素", "中等", "insert-delete-getrandom-o1", ["design-structure", "hash-map"]),
    (13, "数组 / 字符串", "除了自身以外数组的乘积", "中等", "product-of-array-except-self", ["prefix-decomposition"]),
    (14, "数组 / 字符串", "加油站", "中等", "gas-station", ["greedy-linear"]),
    (15, "数组 / 字符串", "分发糖果", "困难", "candy", ["greedy-linear"]),
    (16, "数组 / 字符串", "接雨水", "困难", "trapping-rain-water", ["two-pointer-opposite", "prefix-decomposition"]),
    (17, "数组 / 字符串", "罗马数字转整数", "简单", "roman-to-integer", ["hash-map"]),
    (18, "数组 / 字符串", "整数转罗马数字", "中等", "integer-to-roman", ["math-simulation"]),
    (19, "数组 / 字符串", "最后一个单词的长度", "简单", "length-of-last-word", ["string-scan"]),
    (20, "数组 / 字符串", "最长公共前缀", "简单", "longest-common-prefix", ["string-scan"]),
    (21, "数组 / 字符串", "反转字符串中的单词", "中等", "reverse-words-in-a-string", ["string-scan"]),
    (22, "数组 / 字符串", "Z 字形变换", "中等", "zigzag-conversion", ["string-scan"]),
    (23, "数组 / 字符串", "找出字符串中第一个匹配项的下标", "简单", "find-the-index-of-the-first-occurrence-in-a-string", ["string-scan"]),
    (24, "数组 / 字符串", "文本左右对齐", "困难", "text-justification", ["string-scan"]),
    # 双指针
    (25, "双指针", "验证回文串", "简单", "valid-palindrome", ["two-pointer-opposite"]),
    (26, "双指针", "判断子序列", "简单", "is-subsequence", ["two-pointer-same"]),
    (27, "双指针", "两数之和 II - 输入有序数组", "中等", "two-sum-ii-input-array-is-sorted", ["two-pointer-opposite"]),
    (28, "双指针", "盛最多水的容器", "中等", "container-with-most-water", ["two-pointer-opposite"]),
    (29, "双指针", "三数之和", "中等", "3sum", ["two-pointer-opposite"]),
    # 滑动窗口
    (30, "滑动窗口", "长度最小的子数组", "中等", "minimum-size-subarray-sum", ["sliding-window"]),
    (31, "滑动窗口", "无重复字符的最长子串", "中等", "longest-substring-without-repeating-characters", ["sliding-window"]),
    (32, "滑动窗口", "串联所有单词的子串", "困难", "substring-with-concatenation-of-all-words", ["sliding-window"]),
    (33, "滑动窗口", "最小覆盖子串", "困难", "minimum-window-substring", ["sliding-window"]),
    # 矩阵
    (34, "矩阵", "有效的数独", "中等", "valid-sudoku", ["hash-map", "matrix-simulation"]),
    (35, "矩阵", "螺旋矩阵", "中等", "spiral-matrix", ["matrix-simulation"]),
    (36, "矩阵", "旋转图像", "中等", "rotate-image", ["matrix-simulation"]),
    (37, "矩阵", "矩阵置零", "中等", "set-matrix-zeroes", ["matrix-simulation"]),
    (38, "矩阵", "生命游戏", "中等", "game-of-life", ["matrix-simulation"]),
    # 哈希表
    (39, "哈希表", "赎金信", "简单", "ransom-note", ["frequency-count"]),
    (40, "哈希表", "同构字符串", "简单", "isomorphic-strings", ["hash-map"]),
    (41, "哈希表", "单词规律", "简单", "word-pattern", ["hash-map"]),
    (42, "哈希表", "有效的字母异位词", "简单", "valid-anagram", ["frequency-count"]),
    (43, "哈希表", "字母异位词分组", "中等", "group-anagrams", ["hash-map"]),
    (44, "哈希表", "两数之和", "简单", "two-sum", ["hash-map"]),
    (45, "哈希表", "快乐数", "简单", "happy-number", ["fast-slow", "hash-map"]),
    (46, "哈希表", "存在重复元素 II", "简单", "contains-duplicate-ii", ["sliding-window", "hash-map"]),
    (47, "哈希表", "最长连续序列", "中等", "longest-consecutive-sequence", ["hash-map"]),
    # 区间
    (48, "区间", "汇总区间", "简单", "summary-ranges", ["interval-greedy"]),
    (49, "区间", "合并区间", "中等", "merge-intervals", ["interval-greedy"]),
    (50, "区间", "插入区间", "中等", "insert-interval", ["interval-greedy"]),
    (51, "区间", "用最少数量的箭引爆气球", "中等", "minimum-number-of-arrows-to-burst-balloons", ["interval-greedy"]),
    # 栈
    (52, "栈", "有效的括号", "简单", "valid-parentheses", ["stack-expression"]),
    (53, "栈", "简化路径", "中等", "simplify-path", ["stack-expression", "string-scan"]),
    (54, "栈", "最小栈", "中等", "min-stack", ["design-structure"]),
    (55, "栈", "逆波兰表达式求值", "中等", "evaluate-reverse-polish-notation", ["stack-expression"]),
    (56, "栈", "基本计算器", "困难", "basic-calculator", ["stack-expression"]),
    # 链表
    (57, "链表", "环形链表", "简单", "linked-list-cycle", ["fast-slow"]),
    (58, "链表", "两数相加", "中等", "add-two-numbers", ["linked-list-dummy", "math-simulation"]),
    (59, "链表", "合并两个有序链表", "简单", "merge-two-sorted-lists", ["linked-list-dummy"]),
    (60, "链表", "随机链表的复制", "中等", "copy-list-with-random-pointer", ["hash-map", "linked-list-dummy"]),
    (61, "链表", "反转链表 II", "中等", "reverse-linked-list-ii", ["linked-list-reverse", "linked-list-dummy"]),
    (62, "链表", "K 个一组翻转链表", "困难", "reverse-nodes-in-k-group", ["linked-list-reverse", "linked-list-dummy"]),
    (63, "链表", "删除链表的倒数第 N 个结点", "中等", "remove-nth-node-from-end-of-list", ["linked-list-dummy", "fast-slow"]),
    (64, "链表", "删除排序链表中的重复元素 II", "中等", "remove-duplicates-from-sorted-list-ii", ["linked-list-dummy"]),
    (65, "链表", "旋转链表", "中等", "rotate-list", ["linked-list-dummy", "fast-slow"]),
    (66, "链表", "分隔链表", "中等", "partition-list", ["linked-list-dummy"]),
    (67, "链表", "LRU 缓存", "中等", "lru-cache", ["design-structure", "hash-map"]),
    # 二叉树
    (68, "二叉树", "二叉树的最大深度", "简单", "maximum-depth-of-binary-tree", ["tree-recursion", "bfs-level"]),
    (69, "二叉树", "相同的树", "简单", "same-tree", ["tree-recursion"]),
    (70, "二叉树", "翻转二叉树", "简单", "invert-binary-tree", ["tree-recursion"]),
    (71, "二叉树", "对称二叉树", "简单", "symmetric-tree", ["tree-recursion"]),
    (72, "二叉树", "从前序与中序遍历序列构造二叉树", "中等", "construct-binary-tree-from-preorder-and-inorder-traversal", ["tree-recursion", "divide-conquer"]),
    (73, "二叉树", "从中序与后序遍历序列构造二叉树", "中等", "construct-binary-tree-from-inorder-and-postorder-traversal", ["tree-recursion", "divide-conquer"]),
    (74, "二叉树", "填充每个节点的下一个右侧节点指针 II", "中等", "populating-next-right-pointers-in-each-node-ii", ["bfs-level"]),
    (75, "二叉树", "二叉树展开为链表", "中等", "flatten-binary-tree-to-linked-list", ["tree-recursion"]),
    (76, "二叉树", "路径总和", "简单", "path-sum", ["tree-recursion"]),
    (77, "二叉树", "求根节点到叶节点数字之和", "中等", "sum-root-to-leaf-numbers", ["tree-recursion"]),
    (78, "二叉树", "二叉树中的最大路径和", "困难", "binary-tree-maximum-path-sum", ["tree-recursion"]),
    (79, "二叉树", "二叉搜索树迭代器", "中等", "binary-search-tree-iterator", ["tree-bst-inorder", "design-structure"]),
    (80, "二叉树", "完全二叉树的节点个数", "中等", "count-complete-tree-nodes", ["tree-recursion", "binary-search"]),
    (81, "二叉树", "二叉树的最近公共祖先", "中等", "lowest-common-ancestor-of-a-binary-tree", ["tree-recursion"]),
    # 二叉树层次遍历
    (82, "二叉树层次遍历", "二叉树的右视图", "中等", "binary-tree-right-side-view", ["bfs-level"]),
    (83, "二叉树层次遍历", "二叉树的层平均值", "简单", "average-of-levels-in-binary-tree", ["bfs-level"]),
    (84, "二叉树层次遍历", "二叉树的层序遍历", "中等", "binary-tree-level-order-traversal", ["bfs-level"]),
    (85, "二叉树层次遍历", "二叉树的锯齿形层序遍历", "中等", "binary-tree-zigzag-level-order-traversal", ["bfs-level"]),
    # 二叉搜索树
    (86, "二叉搜索树", "二叉搜索树的最小绝对差", "简单", "minimum-absolute-difference-in-bst", ["tree-bst-inorder"]),
    (87, "二叉搜索树", "二叉搜索树中第 K 小的元素", "中等", "kth-smallest-element-in-a-bst", ["tree-bst-inorder"]),
    (88, "二叉搜索树", "验证二叉搜索树", "中等", "validate-binary-search-tree", ["tree-bst-inorder"]),
    # 图
    (89, "图", "岛屿数量", "中等", "number-of-islands", ["grid-dfs", "graph-bfs"]),
    (90, "图", "被围绕的区域", "中等", "surrounded-regions", ["grid-dfs"]),
    (91, "图", "克隆图", "中等", "clone-graph", ["graph-bfs", "hash-map"]),
    (92, "图", "除法求值", "中等", "evaluate-division", ["graph-bfs", "hash-map"]),
    (93, "图", "课程表", "中等", "course-schedule", ["topo-sort"]),
    (94, "图", "课程表 II", "中等", "course-schedule-ii", ["topo-sort"]),
    # 图的广度优先搜索
    (95, "图的广度优先搜索", "蛇梯棋", "中等", "snakes-and-ladders", ["graph-bfs"]),
    (96, "图的广度优先搜索", "最小基因变化", "中等", "minimum-genetic-mutation", ["graph-bfs"]),
    (97, "图的广度优先搜索", "单词接龙", "困难", "word-ladder", ["graph-bfs"]),
    # 字典树
    (98, "字典树", "实现 Trie (前缀树)", "中等", "implement-trie-prefix-tree", ["trie", "design-structure"]),
    (99, "字典树", "添加与搜索单词 - 数据结构设计", "中等", "design-add-and-search-words-data-structure", ["trie", "backtracking"]),
    (100, "字典树", "单词搜索 II", "困难", "word-search-ii", ["trie", "backtracking"]),
    # 回溯
    (101, "回溯", "电话号码的字母组合", "中等", "letter-combinations-of-a-phone-number", ["backtracking"]),
    (102, "回溯", "组合", "中等", "combinations", ["backtracking"]),
    (103, "回溯", "全排列", "中等", "permutations", ["backtracking"]),
    (104, "回溯", "组合总和", "中等", "combination-sum", ["backtracking"]),
    (105, "回溯", "N 皇后 II", "困难", "n-queens-ii", ["backtracking"]),
    (106, "回溯", "括号生成", "中等", "generate-parentheses", ["backtracking"]),
    (107, "回溯", "单词搜索", "中等", "word-search", ["backtracking", "grid-dfs"]),
    # 分治
    (108, "分治", "将有序数组转换为二叉搜索树", "简单", "convert-sorted-array-to-binary-search-tree", ["divide-conquer", "tree-recursion"]),
    (109, "分治", "排序链表", "中等", "sort-list", ["divide-conquer", "linked-list-dummy"]),
    (110, "分治", "建立四叉树", "中等", "construct-quad-tree", ["divide-conquer"]),
    (111, "分治", "合并 K 个升序链表", "困难", "merge-k-sorted-lists", ["heap-topk", "divide-conquer"]),
    # Kadane
    (112, "Kadane 算法", "最大子数组和", "中等", "maximum-subarray", ["kadane"]),
    (113, "Kadane 算法", "环形子数组的最大和", "中等", "maximum-sum-circular-subarray", ["kadane"]),
    # 二分查找
    (114, "二分查找", "搜索插入位置", "简单", "search-insert-position", ["binary-search"]),
    (115, "二分查找", "搜索二维矩阵", "中等", "search-a-2d-matrix", ["binary-search"]),
    (116, "二分查找", "寻找峰值", "中等", "find-peak-element", ["binary-search", "binary-search-bound"]),
    (117, "二分查找", "搜索旋转排序数组", "中等", "search-in-rotated-sorted-array", ["binary-search-bound"]),
    (118, "二分查找", "在排序数组中查找元素的第一个和最后一个位置", "中等", "find-first-and-last-position-of-element-in-sorted-array", ["binary-search-bound"]),
    (119, "二分查找", "寻找旋转排序数组中的最小值", "中等", "find-minimum-in-rotated-sorted-array", ["binary-search-bound"]),
    (120, "二分查找", "寻找两个正序数组的中位数", "困难", "median-of-two-sorted-arrays", ["binary-search-bound", "divide-conquer"]),
    # 堆
    (121, "堆", "数组中的第K个最大元素", "中等", "kth-largest-element-in-an-array", ["heap-topk"]),
    (122, "堆", "IPO", "困难", "ipo", ["heap-topk", "greedy-linear"]),
    (123, "堆", "查找和最小的 K 对数字", "中等", "find-k-pairs-with-smallest-sums", ["heap-topk"]),
    (124, "堆", "数据流的中位数", "困难", "find-median-from-data-stream", ["heap-topk", "design-structure"]),
    # 位运算
    (125, "位运算", "二进制求和", "简单", "add-binary", ["bit-manipulation", "string-scan"]),
    (126, "位运算", "颠倒二进制位", "简单", "reverse-bits", ["bit-manipulation"]),
    (127, "位运算", "位1的个数", "简单", "number-of-1-bits", ["bit-manipulation"]),
    (128, "位运算", "只出现一次的数字", "简单", "single-number", ["bit-manipulation"]),
    (129, "位运算", "只出现一次的数字 II", "中等", "single-number-ii", ["bit-manipulation"]),
    (130, "位运算", "数字范围按位与", "中等", "bitwise-and-of-numbers-range", ["bit-manipulation"]),
    # 数学
    (131, "数学", "回文数", "简单", "palindrome-number", ["math-simulation"]),
    (132, "数学", "加一", "简单", "plus-one", ["math-simulation"]),
    (133, "数学", "阶乘后的零", "中等", "factorial-trailing-zeroes", ["math-simulation"]),
    (134, "数学", "x 的平方根", "简单", "sqrtx", ["binary-search"]),
    (135, "数学", "Pow(x, n)", "中等", "powx-n", ["divide-conquer"]),
    (136, "数学", "直线上最多的点数", "困难", "max-points-on-a-line", ["hash-map", "math-simulation"]),
    # 一维动态规划
    (137, "一维动态规划", "爬楼梯", "简单", "climbing-stairs", ["dp-linear"]),
    (138, "一维动态规划", "打家劫舍", "中等", "house-robber", ["dp-linear"]),
    (139, "一维动态规划", "单词拆分", "中等", "word-break", ["dp-knapsack"]),
    (140, "一维动态规划", "零钱兑换", "中等", "coin-change", ["dp-knapsack"]),
    (141, "一维动态规划", "最长递增子序列", "中等", "longest-increasing-subsequence", ["dp-linear", "binary-search"]),
    # 多维动态规划
    (142, "多维动态规划", "三角形最小路径和", "中等", "triangle", ["dp-grid"]),
    (143, "多维动态规划", "最小路径和", "中等", "minimum-path-sum", ["dp-grid"]),
    (144, "多维动态规划", "不同路径 II", "中等", "unique-paths-ii", ["dp-grid"]),
    (145, "多维动态规划", "最长回文子串", "中等", "longest-palindromic-substring", ["dp-string"]),
    (146, "多维动态规划", "交错字符串", "中等", "interleaving-string", ["dp-string"]),
    (147, "多维动态规划", "编辑距离", "中等", "edit-distance", ["dp-string"]),
    (148, "多维动态规划", "买卖股票的最佳时机 III", "困难", "best-time-to-buy-and-sell-stock-iii", ["dp-stock"]),
    (149, "多维动态规划", "买卖股票的最佳时机 IV", "困难", "best-time-to-buy-and-sell-stock-iv", ["dp-stock"]),
    (150, "多维动态规划", "最大正方形", "中等", "maximal-square", ["dp-grid"]),
]

CATEGORIES = []
for _row in MANIFEST:
    if _row[1] not in CATEGORIES:
        CATEGORIES.append(_row[1])

assert len(MANIFEST) == 150, len(MANIFEST)
assert len(set(r[0] for r in MANIFEST)) == 150
assert len(set(r[4] for r in MANIFEST)) == 150
