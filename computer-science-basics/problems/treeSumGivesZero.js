// Given an array nums of n integers, are there elements a, b, c
// in nums such that a + b + c = 0? Find all unique triplets in
// the array which gives the sum of zero."
// refs: https://leetcode.com/problems/3sum/
// https://www.geeksforgeeks.org/unique-triplets-sum-given-value/

class Solution {
//   // Naive solution: O(n3)
//   treeSumGivesZero (nums = []) {
//     const r = []
//     nums.sort((a, b) => a - b)
//     const triplets = new Set()
//     const len = nums.length
//     for (let i = 0; i < len; i++) {
//       for (let j = i + 1; j < len; j++) {
//         for (let k = j + 1; k < len; k++) {
//           if (
//             nums[i] + nums[j] + nums[k] === 0) {
//             // Avoid repeat same value
//             const test = `${nums[i]}:${nums[j]}:${nums[k]}`
//             if (!triplets.has(test)) {
//               r.push(
//                 [nums[i], nums[j], nums[k]]
//               )
//             }
//             triplets.add(test)
//           }
//         }
//       }
//     }
//     return r
//   }
  // Improved solution: O(n2)
  treeSumGivesZero (nums = []) {
    const result = []
    nums.sort((a, b) => a - b)
    const len = nums.length
    for (let i = 0; i < len; i++) {
      const x = nums[i]
      console.log({ 'LOGGING x-----------': x })
      let y = -x
      // Now find the opposite to x, such that x+y==0
      let l = x
      let r = len - 1
      //   let stoppit = 0
      while (l < r) {
        if (nums[l] + nums[r] === y) {
          console.log({ 'LOGGING y': y }, x)
          result.push(
            [nums[i], nums[l], nums[r]]
          )
          break
        }
        if (nums[l] + nums[r] < y) { l++ } else r--
        // console.log({ 'LOGGING r': r })

        // if (stoppit++ == 10) break
      }
    }
    return result
  }
}

module.exports = { Solution }
