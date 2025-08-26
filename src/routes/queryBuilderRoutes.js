const express = require('express');
const router = express.Router();
const { getAllQueryBuilder, getQueryBuilder, postQueryBuilder, deleteQueryBuilder } = require('../controllers/queryBuilderController');

router.get('/querybuilders', getAllQueryBuilder);

router.get('/querybuilders/:id', getQueryBuilder);

router.post('/querybuilders', postQueryBuilder);

router.delete('/querybuilders/:id', deleteQueryBuilder);


module.exports = router;