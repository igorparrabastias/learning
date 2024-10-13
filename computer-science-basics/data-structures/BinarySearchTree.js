class Node {
  constructor (data) {
    this.data = data
    this.left = null
    this.right = null
  }
}

class BinarySearchTree {
  constructor () {
    this.root = null
  }

  // https://www.educative.io/courses/mastering-data-structures-and-sorting-algorithms-in-javascript/7nOvNPYpA4j
  insert (data) {
    const newNode = new Node(data)
    if (!this.root) {
      this.root = newNode
    } else {
      this.insertNode(this.root, newNode)
    }
  }

  insertNode (node, newNode) {
    if (newNode.data < node.data) {
      if (!node.left) {
        node.left = newNode
      } else {
        this.insertNode(node.left, newNode)
      }
    } else {
      if (!node.right) {
        node.right = newNode
      } else {
        this.insertNode(node.right, newNode)
      }
    }
  }

  // https://www.educative.io/courses/mastering-data-structures-and-sorting-algorithms-in-javascript/B889jjv22NX
  remove (data) {
    this.root = this.removeNode(this.root, data)
  }

  removeNode (node, data) {
    if (!node) {
      return null
    }
    if (data < node.data) {
      node.left = this.removeNode(node.left, data)
      return node
    } else if (data > node.data) {
      node.right = this.removeNode(node.right, data)
      return node
    } else {
      // case w/o childs, deleting a leaf
      if (!node.left && !node.right) {
        node = null
        return node
      }
      if (!node.left) {
        node = node.right
        return node
      }
      if (!node.right) {
        node = node.left
        return node
      }

      // find the node whose value must be moved up
      let min = this.findMinNode(node.right)
      node.data = min.data
      node.right = this.removeNode(node.right, min.data)
      return node
    }
  }

  // Finds the minimum node in tree searching starts from given node
  findMinNode (node) {
    // Base case
    // if left of a node is null
    // then it must be minimum node
    if (node.left === null) {
      return node
    }
    return this.findMinNode(node.left)
  }

  // The inorder way is important if you want to flatten the tree back into its original sequence.
  inOrder (node) {
    if (node) {
      this.inOrder(node.left)
      console.log(node.data)
      this.inOrder(node.right)
    }
  }

  // The preorder way is important if you need to inspect roots before inspecting the leaves.
  preOrder (node) {
    if (node) {
      console.log(node.data)
      this.preOrder(node.left)
      this.preOrder(node.right)
    }
  }

  // The postorder way is important if you want to delete an entire tree, or simply want to inspect the leaves before inspecting the nodes. If you deleted the root node, you wouldn’t be able to delete the nodes in the right subtree!
  postOrder (node) {
    if (node) {
      this.postOrder(node.left)
      this.postOrder(node.right)
      console.log(node.data)
    }
  }

  traverseBFS () {
    if (!this.root) return
    this.queue = []
    this.queue.push(this.root)
    this.output = []

    while (this.queue.length) {
      const node = this.queue.shift()
      if (node.left) {
        this.queue.push(node.left)
      }
      if (node.right) {
        this.queue.push(node.right)
      }
      this.output.push(node.data)
    }
    return this.output
  }

  getMin () {
    let node = this.root
    while (node.left) {
      node = node.left
    }
    return node.data
  }

  getMax () {
    let node = this.root
    while (node.right) {
      node = node.right
    }
    return node.data
  }

  // returns root of the tree
  getRootNode () {
    return this.root
  }
}

/**
 * Function to check if tree is height-balanced or not
 * ref: https://www.geeksforgeeks.org/how-to-determine-if-a-binary-tree-is-balanced/
 */
function isBalanced (root) {
  // Base condition
  if (root == null) { return true }

  // for left and right subtree height
  let lh = height(root.left)
  let rh = height(root.right)

  // allowed values for (lh - rh) are 1, -1, 0
  if (Math.abs(lh - rh) <= 1 && isBalanced(
    root.left) == true && isBalanced(root.right) == true) { return true }

  // if we reach here means tree is not
  // height-balanced tree
  return false
}

/**
 * Function to find height of binary tree
 */
function height (root) {
  // base condition when binary tree is empty
  if (root == null) { return 0 }

  return Math.max(height(root.left), height(root.right)) + 1
}

module.exports = { BinarySearchTree, Node, isBalanced }
