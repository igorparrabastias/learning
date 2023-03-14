const { Solution } = require('./buildTree1')

describe.only('Testing buildTree...', () => {
  it('test', () => {
    //       A
    //      /  \
    //     /    \
    //    B       C
    //   / \     /
    //  /   \   /
    // D    E  F
    const n = 6
    const inorder = ['D', 'B', 'E', 'A', 'F', 'C']
    const preorder = ['A', 'B', 'D', 'E', 'C', 'F']
    const expected = ['D', 'E', 'B', 'F', 'C', 'A']
    const obj = new Solution()
    const r = obj.buildTree(inorder, preorder, n)
    expect(r).toEqual(expected)
  })
  it('test', () => {
    const n = 4
    const inorder = [1, 6, 8, 7]
    const preorder = [1, 6, 7, 8]
    const expected = [8, 7, 6, 1]
    const obj = new Solution()
    const r = obj.buildTree(inorder, preorder, n)
    expect(r).toEqual(expected)
  })
  it('test', () => {
    const n = 6
    const inorder = [3, 1, 4, 0, 5, 2]
    const preorder = [0, 1, 3, 4, 2, 5]
    const expected = [3, 4, 1, 5, 2, 0]
    const obj = new Solution()
    const r = obj.buildTree(inorder, preorder, n)
    expect(r).toEqual(expected)
  })
})
