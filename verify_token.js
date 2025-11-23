const jwt = require('jsonwebtoken');

const token = 'eyJhbGciOiJIUzI1NiJ9.eyJ2aWRlbyI6eyJyb29tIjoicHJvY2Vzc2VkLW91dHB1dCIsInJvb21Kb2luIjp0cnVlLCJjYW5QdWJsaXNoIjp0cnVlLCJjYW5TdWJzY3JpYmUiOmZhbHNlfSwiaXNzIjoiQVBJVHcyWXAyVHYzeWZnIiwiZXhwIjoxNzYzODgxNTYzLCJuYmYiOjAsInN1YiI6Im9icy1wcm9jZXNzZWQtb3V0cHV0In0.YWxIGPwqD-quYdmioKnjzbVI7f_b-o6Pf_WDU9jJuT0';
const secret = 'eVYY0UB69XDGLiGzclYuGUhXuVpc8ry3YcazimFryDW';

try {
  const verified = jwt.verify(token, secret);
  console.log('Token is VALID');
  console.log('Decoded:', JSON.stringify(verified, null, 2));
  console.log('\nExpiration:', new Date(verified.exp * 1000).toLocaleString());
  console.log('Current time:', new Date().toLocaleString());
  console.log('Token expired?', verified.exp * 1000 < Date.now());
} catch (err) {
  console.log('Token verification FAILED:', err.message);
}
