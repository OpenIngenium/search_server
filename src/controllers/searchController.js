const { client } = require('../config/elasticsearch-config');
const logger = require('../utils/logger');

function buildElasticsearchQuery(pattern) {
  if (!pattern) {
    return null;
  }

  const conditions = pattern.condition === 'AND' ? 'must' : 'should';
  const rules = pattern.rules.map((rule) => {
    if (rule.condition && rule.rules) {
      return buildElasticsearchQuery(rule);
    } else {
      const operator = getOperator(rule.operator);
      const fields = rule.field.split(',').map((field) => field.trim());
      const value = rule.value;

      if (operator === 'range') {
        const comparisonOperator = getComparisonOperator(rule.operator);
        return {
          range: {
            [fields[0]]: {
              [comparisonOperator]: value,
            },
          },
        };
      } else if (operator === 'not_match_wildcard') {
        const mustNotConditions = fields.map((field) => ({
          wildcard: {
            [field]: {
              value: `*${value}*`,
              boost: 1.0,
              rewrite: "constant_score",
              case_insensitive: true
            },
          },
        }));

        return {
          bool: {
            must_not: mustNotConditions,
          },
        };
      } else if (operator === 'match') {
        const shouldConditions = fields.map((field) => ({
          match: {
            [field]: {
              query: value,
            },
          },
        }));

        return {
          bool: {
            should: shouldConditions,
            minimum_should_match: 1,
          },
        };
      } else if (operator === 'not_match') {
        const mustNotConditions = fields.map((field) => ({
          match: {
            [field]: {
              query: value,
            },
          },
        }));

        return {
          bool: {
            must_not: mustNotConditions,
          },
        };
      } else {
        const shouldConditions = fields.map((field) => ({
          wildcard: {
            [field]: {
              value: `*${value}*`,
              boost: 1.0,
              rewrite: "constant_score",
              case_insensitive: true
            },
          },
        }));

        return {
          bool: {
            should: shouldConditions,
            minimum_should_match: 1,
          },
        };
      }
    }
  });

  return {
    bool: {
      [conditions]: rules,
    },
  };
}

function getOperator(operator) {
  switch (operator) {
    case '=':
      return 'match_wildcard';
    case '==':
        return 'match';
    case '>':
    case '>=':
    case '<':
    case '<=':
      return 'range';
    case '!=':
      return 'not_match_wildcard';
    case '!==':
      return 'not_match';
    default:
      return 'match';
  }
}

function getComparisonOperator(operator) {
  switch (operator) {
    case '>':
      return 'gt';
    case '>=':
      return 'gte';
    case '<':
      return 'lt';
    case '<=':
      return 'lte';
    default:
      return '';
  }
}



async function searchQuery(req, res) {

  const { queryBuilderParams, limit, offset, index } = req.body;
  try {
    const pageSize = limit; 
    const indexes = index == 'all' ? ['procedure_element', 'element'] : index;
    logger.info(`queryBuilderParams: ${JSON.stringify(queryBuilderParams, 0, 2)}`);
    const query = buildElasticsearchQuery(queryBuilderParams);
    logger.info(`query: ${JSON.stringify(query, 0, 2)}`);
    const body = await client.search({
        index: indexes,
        body: {
            query: query,
        },
        from: offset,
        size: pageSize,
    });

    const total = body.hits.total.value;
    const results = body.hits.hits.map((hit) => {
        return {
            id: hit._id,
            ...hit._source,
        };
    });
    logger.info('Data received from search');
    res.status(200).json({results,total});
  } catch (error) {
    logger.error(`Error searching data in search: ${error}`);
    res.status(500).json({ message: `Error searching data in search: ${error}` });
  }
};

module.exports = {
  searchQuery
}