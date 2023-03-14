const { Solution } = require('./maxSumRotationArray')

describe.only('Testing maxSumRotationArray...', () => {
  it('test', () => {
    const expected = 29
    const obj = new Solution()
    const r = obj.maxSumRotationArray(
      [8, 3, 1, 2], 4
    )
    expect(r).toEqual(expected)
  })
  it('test', () => {
    const expected = 7
    const obj = new Solution()
    const r = obj.maxSumRotationArray(
      [3, 2, 1], 3
    )
    expect(r).toEqual(expected)
  })
})
