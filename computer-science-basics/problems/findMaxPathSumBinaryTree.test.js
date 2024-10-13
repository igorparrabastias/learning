const { Solution, Node } = require('./findMaxPathSumBinaryTree')

describe.only('Testing findMaxPathSumBinaryTree...', () => {
  it('test', () => {
    const root = new Node(10)
    root.left = new Node(2)
    root.right = new Node(10)
    root.left.left = new Node(20)
    root.left.right = new Node(1)
    root.right.right = new Node(-25)
    root.right.right.left = new Node(3)
    root.right.right.right = new Node(4)

    const expected = 42
    const obj = new Solution()
    const r = obj.findMaxPathSumBinaryTree(root)
    expect(r).toEqual(expected)
  })
})
