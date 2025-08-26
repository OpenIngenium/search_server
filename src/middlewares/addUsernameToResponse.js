const jwt = require('jsonwebtoken');
const config = require('../config/app-config');
const logger = require('../utils/logger');

function addUsernameToResponse(req, res, next) {
  const authHeader = req.header('Authorization');

  if (authHeader) {
    const token = authHeader.split(' ')[1]; 

    try {
      const decoded = jwt.verify(token, config.public_pem);
      res.locals.username = decoded.username;
    } catch (err) {
      logger.error(`Error decoding JWT token:' ${err.message}`);
    }
  }

  next();
}

module.exports = addUsernameToResponse;
