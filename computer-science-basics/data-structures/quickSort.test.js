const { quickSort } = require('./quickSort')

describe('Testing quickSort...', () => {
  it('', () => {
    const arr = [7, -2, 4, 1, 6, 5, 0, -4, 2]
    quickSort(arr, 0, arr.length - 1)
    const expected = [-4, -2, 0, 1, 2, 4, 5, 6, 7]
    expect(arr).toEqual(expected)
  })
})
