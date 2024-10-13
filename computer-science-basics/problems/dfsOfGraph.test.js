const { Solution } = require('./dfsOfGraph')

describe.only('Testing dfsOfGraph...', () => {
  it('test', () => {
    const expected = [0, 2, 4, 3, 1]
    const obj = new Solution()
    const r = obj.dfsOfGraph(5, [
      [2, 3, 1],
      [0],
      [0, 4],
      [0],
      [2]
    ])
    expect(r).toEqual(expected)
  })
  it('test', () => {
    const expected = [0, 1, 2, 3]
    const obj = new Solution()
    const r = obj.dfsOfGraph(4, [
      [1, 3],
      [0, 2],
      [0],
      [0]
    ])
    expect(r).toEqual(expected)
  })
})
