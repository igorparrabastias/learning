// Given a binary tree, the task is to find the maximum path sum. The path
// may start and end at any node in the tree.
// Time Complexity: O(n) where n is number of nodes in Binary Tree.
// https://www.geeksforgeeks.org/find-maximum-path-sum-in-a-binary-tree/

class Node {
  constructor (data) {
    this.data = data
    this.left = null
    this.right = null
  }
}

class Solution {
  constructor () {
    this.res = -999999999
  }

  // Function to calculate maximum path sum.
  findMaxUtil (root) {
    // base case for recursion.
    if (root === null) { return 0 }

    // l and r store maximum path sum going recursively through left and
    // right subtrees of root(current node) respectively
    let l = this.findMaxUtil(root.left)
    let r = this.findMaxUtil(root.right)

    // max path sum for parent call of root. This path must
    // include at-most one child of root.
    let max_single = Math.max(Math.max(l, r) + root.data, root.data)

    // max_top represents the sum when the node under consideration
    // is the root of the max sum path and no ancestors of root
    // are there in max sum path.
    let max_top = Math.max(max_single, l + r + root.data)

    // storing the maximum result.
    this.res = Math.max(this.res, max_top)

    return max_single
  }

  // Function to return maximum path sum from any node in a tree.
  findMaxPathSumBinaryTree (root) {
    this.findMaxUtil(root)
    // returning the result.
    return this.res
  }
}

module.exports = { Solution, Node }
