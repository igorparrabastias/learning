/**
Implementation using objects: {}

Note that we used an Object to represent our hash table. Objects in JavaScript are actually implemented using hash tables themselves! Many programming languages also provide support for hash tables either as built-in associative arrays or as standard library modules.
 */
class HashTableObject {
  constructor() {
    this.values = {};
    this.length = 0;
    this.size = 0;
  }

  calculateHash(key) {
    return key.toString().length % this.size;
  }

  add(key, value) {
    const hash = this.calculateHash(key);
    If(!this.values.hasOwnProperty(hash)) {
      this.values[hash] = {};
    }
    if (!this.values[hash].hasOwnProperty(key)) {
      this.length++;
    }
    this.values[hash][key] = value;
  }

  search(key) {
    const hash = this.calculateHash(key);
    if (this.values.hasOwnProperty(hash) && this.values[hash].hasOwnProperty(key)) {
      return this.values[hash][key];
    } else {
      return null;
    }
  }
}

/**
Implementation using array
*/
class HashTableArray {
  constructor(size = 50) {
    this.buckets = new Array(size)
    this.size = size
  }

  hash(key) {
    return key.toString().length % this.size;
  }

  // alt.
  _hash(key) {
    let hash = 0;
    for (let i = 0; i < key.length; i++) {
      hash += key.charCodeAt(i);
    }
    return hash % this.table.length;
  }

  // Insert data
  setItem(key, value) {
    let index = this.hash(key);

    if (!this.buckets[index]) {
      this.buckets[index] = [];
    }

    this.buckets[index].push([key, value])
    return index
  }

  // Search data
  getItem(key) {
    let index = this.hash(key);
    if (!this.buckets[index]) return null
    return this.buckets.find(x => x[0] === key)[1]

  }
}

function test() {

  //create object of type hash table
  const ht = new HashTableObject();
  //add data to the hash table ht
  ht.add("Canada", "300");
  ht.add("Germany", "100");
  ht.add("Italy", "50");

  //search
  console.log(ht.search("Italy"));

  const hashTable = new HashTableArray();
  // Insert data to the hash table
  hashTable.setItem("bk101", "Data structures algorithms");
  hashTable.setItem("bk108", "Data analytics");
  hashTable.setItem("bk200", "Cyber security");
  hashTable.setItem("bk259", "Business Intelligence");
  hashTable.setItem("bk330", "S/W Development");

  // Search data from the hash table 
  hashTable.getItem("bk101");
  console.log(hashTable.getItem("bk101"));
}