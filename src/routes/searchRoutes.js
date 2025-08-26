const express = require('express');
const { searchQuery } = require('../controllers/searchController');

const router = express.Router();

router.post('/search', searchQuery);


module.exports = router;
