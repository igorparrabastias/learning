const { BinarySearchTree, Node, isBalanced } = require('./BinarySearchTree')

describe('Testing BinarySearchTree...', () => {
//   it('isBalanced', () => {
//     let root = new Node(1)
//     root.left = new Node(2)
//     root.right = new Node(3)
//     root.left.left = new Node(4)
//     root.left.right = new Node(5)
//     root.left.left.left = new Node(8)
//     if (isBalanced(root)) { console.log('Tree is balanced') } else { console.log('Tree is not balanced') }
//   })
  it('ops', () => {
    // create an object for the BinarySearchTree
    let BST = new BinarySearchTree()

    // Inserting nodes to the BinarySearchTree
    BST.insert(15)
    BST.insert(25)
    BST.insert(10)
    BST.insert(7)
    BST.insert(22)
    BST.insert(17)
    BST.insert(13)
    BST.insert(5)
    BST.insert(9)
    BST.insert(27)

    //     15
    //     / \
    //   10 25
    //   / \ / \
    //   7 13 22 27
    //   / \ /
    // 5 9 17

    const root = BST.getRootNode()

    // prints 5 7 9 10 13 15 17 22 25 27
    BST.inOrder(root)

    // Removing node with no children
    BST.remove(5)

    //     15
    //     / \
    //   10 25
    //   / \ / \
    //   7 13 22 27
    //   \ /
    //   9 17

    // prints 7 9 10 13 15 17 22 25 27
    BST.inOrder(root)

    // Removing node with one child
    BST.remove(7)

    //     15
    //     / \
    //   10 25
    //   / \ / \
    //   9 13 22 27
    //     /
    //     17

    // prints 9 10 13 15 17 22 25 27
    BST.inOrder(root)

    // Removing node with two children
    BST.remove(15)

    //     17
    //     / \
    //   10 25
    //   / \ / \
    //   9 13 22 27

    console.log('inOrder traversal')

    // prints 9 10 13 17 22 25 27
    BST.inOrder(root)

    console.log('postOrder traversal')
    BST.postOrder(root)
    console.log('preOrder traversal')
    BST.preOrder(root)
  })
})
