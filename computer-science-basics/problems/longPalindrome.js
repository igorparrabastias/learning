// Longest Palindromic Substring
// ref: https://www.geeksforgeeks.org/longest-palindromic-substring-set-2/

class Solution {
  // A O(n^2) time and O(1) space program to
  // find the longest palindromic substring
  longPalindrome (str) {
    let n = str.length
    if (n < 2) { return n }
    let temp = ''

    let maxLength = 1; let start = 0
    let low, high
    for (let i = 0; i < n; i++) {
      low = i - 1
      high = i + 1
      // increment 'high'
      while (high < n && str[high] === str[i]) {
        high++
        console.log({ high, str: str[i] })
      }

      // decrement 'low'
      while (low >= 0 && str[low] === str[i]) {
        low--
        console.log({ low, str: str[i] })
      }

      console.log({ low, high })
      while (low >= 0 && high < n && str[low] === str[high]) {
        low--
        high++
        console.log({ 'LOGGING str:::': str[low] })
      }

      let length = high - low - 1
      if (maxLength < length) {
        maxLength = length
        start = low + 1
      }
      temp = str.substring(start, maxLength + start)
      console.log({ 'LOGGING temp': temp })
    }

    return str.substring(start, maxLength + start)
  }
}

module.exports = { Solution }
