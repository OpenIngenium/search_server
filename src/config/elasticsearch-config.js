const { Client } = require('@elastic/elasticsearch');
const config = require('./app-config');
const logger = require('../utils/logger');
const mappingConfig = require('./mapping-config');

const client = new Client({
  node: config.ELASTIC_SEARCH_HOST,
});

async function initElasticsearch() {
  let maxTrials = 20;
  let numTrials = 0;
  while (numTrials <= maxTrials) {
    try {
      numTrials++
      console.log(`Trying to connect to Elastic Search. Trial: ${numTrials}`)
      const res = await client.info()
      console.log(JSON.stringify(res, 0, 2))
      break
    } catch (error) {
      console.log(error);
      if (numTrials === maxTrials) {
        console.log(`Elastic Search is not available. Exit Ingenium Search Service`)
        process.exit(1);      
      }
      await new Promise(r => setTimeout(r, 5000));
    }
  }

  for (const index of config.elastic_search_indices) {
    let indexInfo = null;
    try {
      indexInfo = await client.indices.get({index});
      logger.info(`Index exists: ${index}`);
      continue;
    } catch (error) {
      console.log(error);
      logger.info(`Index does not exist: ${index}`);
    }

    console.log(`Creating index: ${index}`);

    // create index
    try {
      await client.indices.create({ index });
      logger.info(`Index was created: ${index}`);
    } catch (error) {
      console.log(error);
      console.log(`Failed to create index in ElasticSearch. Exit Ingenium Search Service`)
      process.exit(1)
    }

    // set mapping
    try {
      // The same mapping is used for all indices including 'syncdata', 'querybuilder'.
      // Probably it does not hurt.
      await client.indices.putMapping({
        index: index,
        body: mappingConfig.mappings,
      });
      logger.info(`Mapping was set for: ${index}`);
    } catch (error) {
      console.log(error);
      console.log(`Failed to create index in ElasticSearch. Exit Ingenium Search Service`)
      process.exit(1)
    }
  }

  // Update index settings
  try {
    await client.indices.putSettings({
      index: '_all',
      body: {
        'index.mapping.total_fields.limit': config.index_mapping_total_fields_limit,
        'index.max_result_window': config.index_max_result_window,
      },
    });
  } catch (error) {
    console.log(error);
    console.log(`Failed to configure index in ElasticSearch. Exit Ingenium Search Service`)
    process.exit(1)
  }
}

module.exports = {
  client,
  initElasticsearch,
};

