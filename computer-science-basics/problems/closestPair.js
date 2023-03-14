// Given two sorted arrays and a number x, find
// the pair whose sum is closest to x and the pair
// has an element from each array.
// refs:
// https://www.geeksforgeeks.org/given-two-sorted-arrays-number-x-find-pair-whose-sum-closest-x/
// Time Complexity : O(n)
// Auxiliary Space : O(1)

class Solution {
  // Javascript program to find
  // the pair from two sorted arrays such
  // that the sum of pair is closest
  // to a given number x

  // ar1[0..m-1] and ar2[0..n-1] are
  // two given sorted arrays
  // and x is given number.
  // This function prints the pair
  // from both arrays such that the
  // sum of the pair is closest to x.

  closestPair (ar1, ar2, m, n, x) {
    // Initialize the diff
    // between pair sum and x.
    let diff = Number.MAX_VALUE

    // res_l and res_r are result
    // indexes from ar1[] and ar2[]
    // respectively
    let res_l, res_r

    // Start from left side of ar1[] and
    // right side of ar2[]
    let l = 0; let r = n - 1
    while (l < m && r >= 0) {
      // If this pair is closer to
      // x than the previously
      // found closest, then update
      // res_l, res_r and diff
      if (Math.abs(ar1[l] + ar2[r] - x) < diff) {
        res_l = l
        res_r = r
        diff = Math.abs(ar1[l] + ar2[r] - x)
      }

      // If sum of this pair is more than x,
      // move to smaller side
      if (ar1[l] + ar2[r] > x) { r-- }
      // move to the greater side
      else { l++ }
    }

    return [ar1[res_l], ar2[res_r]]
  }
}

module.exports = { Solution }
