// Longest Palindromic Substring
// ref: https://www.geeksforgeeks.org/longest-palindromic-substring-set-2/
// https://www.youtube.com/watch?v=XYQecbcd6_c&ab_channel=NeetCode

class Solution {
  // A O(n^2) time and O(1) space program to
  // find the longest palindromic substring

  checkPalindrome (str, low, high) {
    while (low >= 0 && high < this.n && str[low] === str[high]) {
      low--
      high++
    }

    let length = high - low - 1
    if (this.maxLength < length) {
      this.maxLength = length
      this.start = low + 1
    }
  }

  longPalindrome (str) {
    this.n = str.length
    if (this.n < 2) { return str }

    this.maxLength = 1
    this.start = 0
    for (let i = 0; i < this.n; i++) {
      // for even lenght
      this.checkPalindrome(str, i, i)
      // for odd lenght
      this.checkPalindrome(str, i, i + 1)
    }

    return str.substring(this.start, this.maxLength + this.start)
  }
}

module.exports = { Solution }
