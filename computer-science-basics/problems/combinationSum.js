// Given an array of positive integers arr[] and
// a sum x, find all unique combinations in arr[]
// where the sum is equal to x. The same repeated
// number may be chosen from arr[] unlimited number of times.
// refs:
// https://www.geeksforgeeks.org/combinational-sum/
// https://stackoverflow.com/questions/4632322/finding-all-possible-combinations-of-numbers-to-reach-a-given-sum

class Solution {
  combinationSum (arr, sum) {
    let ans = new Array()
    let temp = new Array()

    // first do hashing since hashset does not always sort
    // removing the duplicates using HashSet and
    // Sorting the arrayList
    let set = new Set([...arr])
    arr = [...set]
    arr.sort()

    this.findNumbers(ans, arr, sum, 0, temp)
    return ans
  }

  findNumbers (ans, arr, sum, index, temp) {
    if (sum == 0) {
      // pushing deep copy of list to ans

      ans.push([...temp])
      return
    }

    for (let i = index; i < arr.length; i++) {
      // checking that sum does not become negative

      if ((sum - arr[i]) >= 0) {
        // pushing element which can contribute to
        // sum

        temp.push(arr[i])

        this.findNumbers(ans, arr, sum - arr[i], i, temp)

        // removing element from list (backtracking)
        temp.splice(temp.indexOf(arr[i]), 1)
      }
    }
  }
}

module.exports = { Solution }
