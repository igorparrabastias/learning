const { Solution } = require('./combinationSum')

describe.only('Testing combinationSum...', () => {
  it('test', () => {
    const expected = [
      [2, 2, 2, 2],
      [2, 2, 4],
      [2, 6],
      [4, 4],
      [8]
    ]
    const obj = new Solution()
    const r = obj.combinationSum([2, 4, 6, 8], 8)
    expect(r).toEqual(expected)
  })
  it('test', () => {
    const expected = [
      [2, 2, 2, 2, 2, 2, 2, 2],
      [2, 2, 2, 2, 2, 6],
      [2, 2, 2, 5, 5],
      [2, 2, 5, 7],
      [2, 2, 6, 6],
      [2, 7, 7],
      [5, 5, 6]
    ]
    const obj = new Solution()
    const r = obj.combinationSum([7, 2, 6, 5], 16)
    expect(r).toEqual(expected)
  })
})
