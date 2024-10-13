const { Solution } = require('./closestPair')

describe.only('Testing closestPair...', () => {
  it('test', () => {
    const expected = [7, 30]
    const obj = new Solution()
    const r = obj.closestPair(
      [1, 4, 5, 7],
      [10, 20, 30, 40],
      4,
      4,
      38
    )
    expect(r).toEqual(expected)
  })
  it('test', () => {
    const expected = [7, 40]
    const obj = new Solution()
    const r = obj.closestPair(
      [1, 4, 5, 7],
      [10, 20, 30, 40],
      4,
      4,
      50
    )
    expect(r).toEqual(expected)
  })
})
