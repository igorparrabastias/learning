const { Solution } = require('./twoSumsFromArray')

describe('Testing twoSumsFromArray...', () => {
  it('test', () => {
    const expected = [0, 1]
    const obj = new Solution()
    const r = obj.twoSumsFromArray([2, 7, 11, 15], 9)
    expect(r).toEqual(expected)
  })
  it('test', () => {
    const expected = [1, 2]
    const obj = new Solution()
    const r = obj.twoSumsFromArray([3, 2, 4], 6)
    console.log({ 'LOGGING r': r })
    expect(r).toEqual(expected)
  })
  it('test', () => {
    const expected = [0, 1]
    const obj = new Solution()
    const r = obj.twoSumsFromArray([2, 7, 3, 15], 9)
    console.log({ 'LOGGING r': r })
    expect(r).toEqual(expected)
  })
  it('test', () => {
    const expected = [0, 1]
    const obj = new Solution()
    const r = obj.twoSumsFromArray([3, 3], 6)
    expect(r).toEqual(expected)
  })
})
