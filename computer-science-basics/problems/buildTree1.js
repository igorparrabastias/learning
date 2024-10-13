// Construct a tree from given inorder and preorder
// traversals and return the postorder traversal
// ref: https://www.geeksforgeeks.org/construct-tree-from-given-inorder-and-preorder-traversal/
// https://www.youtube.com/watch?v=PoBGyrIWisE

class Node {
  constructor (x) {
    this.key = x
    this.left = null
    this.right = null
  }
}
class Solution {
  postOrder (node, acc = []) {
    if (node) {
      this.postOrder(node.left, acc)
      this.postOrder(node.right, acc)
      acc.push(node.key)
    }
    return acc
  }

  buildTreeWorker (inorder, preorder, inOrderStart, inOrderEnd) {
    if (inOrderStart > inOrderEnd) { return null }

    const tNode = new Node(preorder[this.preIndex++])

    // Base case
    if (inOrderStart === inOrderEnd) { return tNode }

    // Walk over inorder
    let inIndex = this.mapa.get(tNode.key)

    tNode.left = this.buildTreeWorker(inorder, preorder, inOrderStart, inIndex - 1)
    tNode.right = this.buildTreeWorker(inorder, preorder, inIndex + 1, inOrderEnd)

    return tNode
  }

  buildTree (inorder, preorder, n) {
    this.preIndex = 0
    this.mapa = new Map()
    for (let i = 0; i < inorder.length; i++) {
      this.mapa.set(inorder[i], i)
    }
    const node = this.buildTreeWorker(inorder, preorder, 0, n - 1)
    return this.postOrder(node)
  }
}

module.exports = { Solution }
