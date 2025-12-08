export default {
  testEnvironment: 'jsdom',
  collectCoverageFrom: [
    'js/**/*.js',
    '!js/**/*.test.js'
  ],
  testMatch: [
    '**/tests/**/*.test.js'
  ],
  moduleFileExtensions: ['js'],
  verbose: true,
  transform: {}
};
