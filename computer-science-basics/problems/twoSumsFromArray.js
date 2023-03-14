// "Given an array of integers nums and an integer target, return
// indices of the two numbers such that they add up to target.
// You may assume that each input would have exactly one solution,
// and you may not use the same element twice."
// refs: https://leetcode.com/problems/two-sum/solution/

class Solution {
  // Using One-pass Hash Table
  // Time O(n)
  // Space O(n)
  twoSumsFromArray (nums, target) {
    const cont = new Map()
    for (let i = 0; i < nums.length; i++) {
      const comp = target - nums[i]
      if (cont.has(comp)) {
        return [cont.get(comp), i]
      }
      cont.set(nums[i], i)
    }
    return []
  }
}

module.exports = { Solution }
