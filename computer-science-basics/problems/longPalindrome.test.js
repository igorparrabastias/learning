const { Solution } = require('./longPalindrome2')

describe.only('Testing longPalindrome...', () => {
  it('test', () => {
    const expected = 'geeksskeeg'
    const obj = new Solution()
    const r = obj.longPalindrome('forgeeksskeegfor')
    expect(r).toEqual(expected)
  })
  it('test', () => {
    const expected = 'radar'
    const obj = new Solution()
    const r = obj.longPalindrome('radares')
    expect(r).toEqual(expected)
  })
  it('test', () => {
    const expected = 'aabbaa'
    const obj = new Solution()
    const r = obj.longPalindrome('aaaabbaa')
    expect(r).toEqual(expected)
  })
})
