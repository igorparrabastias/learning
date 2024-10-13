const { bubbleSort } = require('./bubbleSort')

describe('Testing bubbleSort...', () => {
  it('', () => {
    const arr = [243, 45, 23, 356, 3, 5346, 35, 5]
    const r = bubbleSort(arr)
    const expected = [3, 5, 23, 35, 45, 243, 356, 5346]
    expect(r).toEqual(expected)
  })
})
