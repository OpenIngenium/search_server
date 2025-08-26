module.exports = {
  "mappings": {
    "properties": {
      "execution_user_input": {
        "properties": {
          "reference_procedure_version": {
            "type": "long"
          },
          "duration": {
            "type": "long"
          },
          "timeout": {
            "type": "long"
          },
          "lookback": {
            "type": "long"
          },
        }
      },
      "authoring_user_input": {
        "properties": {
          "reference_procedure_version": {
            "type": "long"
          },
          "timeout": {
            "type": "long"
          },
          "lookback": {
            "type": "long"
          },
        }
      },
      "execution": {
        "properties": {
          "meta_data": {
            "properties": {
              "time_started": {
                "type": "date",
                "format": "strict_date_optional_time"
              },
              "time_updated": {
                "type": "date",
                "format": "strict_date_optional_time"
              },
              "time_completed": {
                "type": "date",
                "format": "strict_date_optional_time"
              }
            }
          }
        }
      },
      "procedureDetails": {
        "properties": {
          "time_created": {
            "type": "date",
            "format": "strict_date_optional_time"
          },
          "time_saved": {
            "type": "date",
            "format": "strict_date_optional_time"
          },
        }
      },
      "procedureVersionDetails": {
        "properties": {
          "version": {
            "type": "long"
          },
          "time_saved": {
            "type": "date",
            "format": "strict_date_optional_time"
          },
          "time_versioned": {
            "type": "date",
            "format": "strict_date_optional_time"
          },
        }
      },
      "executionDetails": {
        "properties": {
          "time_completed": {
            "type": "date",
            "format": "strict_date_optional_time"
          },
          "time_started": {
            "type": "date",
            "format": "strict_date_optional_time"
          },
          "transitions": {
            "properties": {
              "time_updated": {
                "type": "date",
                "format": "strict_date_optional_time"
              },
            }
          }
        }
      },
      "venueDetails": {
        "properties": {
          "venue_status": {
            "properties": {
              "started_on": {
                "type": "date",
                "format": "strict_date_optional_time"
              },
            }
          }
        }
      },
    },
    "dynamic_templates": [
      {
        "string_as_wildcard": {
          "match_mapping_type": "string",
          "mapping": {
            "type": "wildcard"
          }
        },
      }
    ]
  }
}
