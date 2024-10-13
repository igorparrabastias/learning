const { Solution } = require('./treeSumGivesZero')

describe.only('Testing treeSumGivesZero...', () => {
  it('test', () => {
    const expected = [[-1, -1, 2], [-1, 0, 1]]
    const obj = new Solution()
    const r = obj.treeSumGivesZero([-1, 0, 1, 2, -1, -4])
    console.log({ 'LOGGING r': r })
    expect(r).toEqual(expected)
  })
  //   it('test', () => {
  //     const expected = []
  //     const obj = new Solution()

//     const r = obj.treeSumGivesZero([0, 1, 1])
//     expect(r).toEqual(expected)
//   })
//   it('test', () => {
//     const expected = [[0, 0, 0]]
//     const obj = new Solution()
//     const r = obj.treeSumGivesZero([0, 0, 0])
//     expect(r).toEqual(expected)
//   })
})
