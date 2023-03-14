// DFS of Graph
// You are given a connected undirected graph. Perform a
// Depth First Traversal of the graph.
// Note: Use a recursive approach to find the DFS
// traversal of the graph starting from the 0th vertex
// from left to right according to the graph.
// Expected Time Complexity: O(V + E)
// Expected Auxiliary Space: O(V)
// refs:
// https://www.geeksforgeeks.org/depth-first-search-or-dfs-for-a-graph/

/**
 * @param {number} V
 * @param {number[][]} adj
 * @returns {number[]}
*/
class Solution {
  DFSUtil (i, adj, V, vis, res) {
    // marking vertex as visited and adding it to output list.
    if (vis[i]) return
    vis[i] = true
    res.push(i)

    // iterating over connected components of the vertex and if any
    // of them is not visited then calling the function recursively.
    for (let j = 0; j < adj[i].length; j++) {
      if (!vis[adj[i][j]]) {
        this.DFSUtil(adj[i][j], adj, V, vis, res)
      }
    }
  }

  // Function to return a list containing the DFS traversal of the graph.
  dfsOfGraph (V, adj) {
    // using a boolean list to mark all the vertices as not visited.
    let vis = new Array(V)
    vis.fill(false)
    let res = new Array()
    for (let i = 0; i < V; i++) {
      // if any vertex isn't visited then calling the function.
      if (vis[i] == 0) {
        this.DFSUtil(i, adj, V, vis, res)
      }
    }
    // returning the output list.
    return res
  }
}

module.exports = { Solution }
