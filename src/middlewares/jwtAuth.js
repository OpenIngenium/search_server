var { expressjwt } = require("express-jwt");
const config = require('../config/app-config');

const jwtAuth = expressjwt({
  secret: config.public_pem,
  algorithms: ['RS256'],
  requestProperty: 'auth',
}).unless({ path: [/^\/api-docs\/?.*/, '/api/v1/health'] });

module.exports = jwtAuth;


