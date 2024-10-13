// Time Complexity: O(n).
// Since one loop is needed from 0 to n to check all rotations and the sum of the present rotation is calculated from the previous rotations in O(1) time).
// Auxiliary Space: O(1).
// As no extra space is required to so the space complexity will be O(1)
// https://www.geeksforgeeks.org/maximum-sum-iarri-among-rotations-given-array/
// https://www.youtube.com/watch?v=reayIgOJO0Y&ab_channel=RamSimTechEdu

class Solution {
// An efficient JavaScript program to compute
// maximum sum of i*arr[i]

  maxSumRotationArray (arr, n) {
    // Compute sum of all array elements
    let cum_sum = 0
    for (let i = 0; i < n; i++) { cum_sum += arr[i] }

    // Compute sum of i*arr[i] for initial
    // configuration.
    let curr_val = 0
    for (let i = 0; i < n; i++) { curr_val += i * arr[i] }

    // Initialize result
    let res = curr_val

    // Compute values for other iterations
    for (let i = 1; i < n; i++) {
      // Compute next value using previous
      // value in O(1) time
      let next_val = curr_val - (cum_sum - arr[i - 1]) + arr[i - 1] * (n - 1)

      // Update current value
      curr_val = next_val

      // Update result if required
      res = Math.max(res, next_val)
    }

    return res
  }
}

module.exports = { Solution }
