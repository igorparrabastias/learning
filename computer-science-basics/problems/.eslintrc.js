module.exports = {
  env: {
    commonjs: true,
    es2021: true,
    node: true,
    jest: true
  },
  extends: 'standard',
  overrides: [
  ],
  parserOptions: {
    ecmaVersion: 'latest'
  },
  rules: {
    'prefer-const': 0,
    camelcase: 0,
    // Very important, as geeksforgeeks editors use ==
    eqeqeq: 0,
    'no-array-constructor': 0
  }
}
