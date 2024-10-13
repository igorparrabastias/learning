const { insertionSort } = require('./insertionSort')

describe('Testing insertionSort...', () => {
  it('', () => {
    const arr = [4, 8, 7, 2, 11, 1, 3]
    const r = insertionSort(arr)
    const expected = [1, 2, 3, 4, 7, 8, 11]
    expect(r).toEqual(expected)
  })
})
