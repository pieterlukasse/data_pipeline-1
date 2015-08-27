from collections import defaultdict

__author__ = 'andreap'
import os
import ConfigParser

iniparser = ConfigParser.ConfigParser()
iniparser.read('db.ini')

class Config():

    ENV=os.environ.get('CTTV_EL_LOADER') or 'dev'
    ELASTICSEARCH_URL = 'http://'+iniparser.get(ENV, 'elurl')+':'+iniparser.get(ENV, 'elport')+'/'
    # ELASTICSEARCH_URL = [{"host": iniparser.get(ENV, 'elurl'), "port": iniparser.get(ENV, 'elport')}]
    ELASTICSEARCH_DATA_INDEX_NAME = 'evidence-data'
    ELASTICSEARCH_DATA_DOC_NAME = 'evidencestring'
    ELASTICSEARCH_EFO_LABEL_INDEX_NAME = 'efo-data'
    ELASTICSEARCH_EFO_LABEL_DOC_NAME = 'efo'
    ELASTICSEARCH_ECO_INDEX_NAME = 'eco-data'
    ELASTICSEARCH_ECO_DOC_NAME = 'eco'
    ELASTICSEARCH_GENE_NAME_INDEX_NAME = 'gene-data'
    ELASTICSEARCH_GENE_NAME_DOC_NAME = 'genedata'
    ELASTICSEARCH_EXPRESSION_INDEX_NAME = 'expression-data'
    ELASTICSEARCH_EXPRESSION_DOC_NAME = 'expression'
    ELASTICSEARCH_REACTOME_INDEX_NAME = 'reactome-data'
    ELASTICSEARCH_REACTOME_REACTION_DOC_NAME = 'reactome-reaction'
    ELASTICSEARCH_DATA_SCORE_INDEX_NAME = 'evidence-score'
    ELASTICSEARCH_DATA_SCORE_DOC_NAME = 'evidencescore'
    DEBUG = True
    PROFILE = False
    PUBLIC_API_BASE_PATH = '/api/public/v'
    PRIVATE_API_BASE_PATH = '/api/private/v'
    API_VERSION = '0.2'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    ERROR_IDS_FILE = 'errors.txt'
    POSTGRES_DATABASE = {'drivername': 'postgres',
            'host': iniparser.get(ENV, 'host'),
            'port': iniparser.get(ENV, 'port'),
            'username': iniparser.get(ENV, 'username'),
            'password': iniparser.get(ENV, 'password'),
            'database': iniparser.get(ENV, 'database')}
    HPA_NORMAL_TISSUE_URL = 'http://www.proteinatlas.org/download/normal_tissue.csv.zip'
    HPA_CANCER_URL = 'http://www.proteinatlas.org/download/cancer.csv.zip'
    HPA_SUBCELLULAR_LOCATION_URL = 'http://www.proteinatlas.org/download/subcellular_location.csv.zip'
    HPA_RNA_URL = 'http://www.proteinatlas.org/download/rna.csv.zip'
    REACTOME_ENSEMBL_MAPPINGS = 'http://www.reactome.org/download/current/Ensembl2Reactome.txt'
    # REACTOME_ENSEMBL_MAPPINGS = 'http://www.reactome.org/download/current/Ensembl2Reactome_All_Levels.txt'
    REACTOME_PATHWAY_DATA = 'http://www.reactome.org/download/current/ReactomePathways.txt'
    REACTOME_PATHWAY_RELATION = 'http://www.reactome.org/download/current/ReactomePathwaysRelation.txt'
    REACTOME_SBML_REST_URI = 'http://www.reactome.org/ReactomeRESTfulAPI/RESTfulWS/sbmlExporter/{0}'
    EVIDENCEVALIDATION_FTP_SUBMISSION_PATH = '/home/gk680303/windows/data/ftp' #'/opt/share/data/ftp'
    EVIDENCEVALIDATION_MAX_NB_ERRORS_REPORTED = 1000
    EVIDENCEVALIDATION_NB_TOP_DISEASES = 20
    EVIDENCEVALIDATION_NB_TOP_TARGETS = 20
    EVIDENCEVALIDATION_PERCENT_SCALE = 20
    EVIDENCEVALIDATION_ENSEMBL_ASSEMBLY = 'GRCh38'
    DATASOURCE_ASSOCIATION_SCORE_WEIGHT=dict(gwas_catalog=2.5)
    DATASOURCE_ASSOCIATION_SCORE_AUTO_EXTEND_RANGE=dict(
                                                        #phenodigm=dict(min=0.4, max= 1),
                                                        )
    DATASOURCE_INTERNAL_NAME_TRANSLATION = dict(reactome = 'CTTV006_Networks_Reactome',
                                                intact = 'CTTV006_Networks_IntAct',
                                                chembl = 'CTTV008_ChEMBL',
                                                gwas_catalog = 'CTTV009_GWAS_Catalog',
                                                uniprot = 'CTTV011_UniProt',
                                                eva = 'CTTV012_Variation',
                                                gwas_ibd = 'CTTV018_IBD_GWAS',
                                                phenodigm = 'CTTV_External_MouseModels',
                                                cancer_gene_census = 'CTTV_External_Cancer_Gene_Census',
                                                europmc = 'CTTV025_Literature',
                                                disgenet = 'CTTV_External_DisGeNet',
                                                rare2common = 'CTTV005_Rare2Common',
                                                tissue_specificity = 'CTTV010_Tissue_Specificity'
                                                )
    DATASOURCE_TO_DATATYPE_MAPPING = defaultdict(lambda: "other")
    DATASOURCE_TO_DATATYPE_MAPPING['expression_atlas'] = 'rna_expression'
    DATASOURCE_TO_DATATYPE_MAPPING['uniprot'] = 'genetic_association'
    DATASOURCE_TO_DATATYPE_MAPPING['reactome'] = 'affected_pathway'
    DATASOURCE_TO_DATATYPE_MAPPING['eva'] = 'genetic_association'
    DATASOURCE_TO_DATATYPE_MAPPING['phenodigm'] = 'animal_model'
    DATASOURCE_TO_DATATYPE_MAPPING['gwas_catalog'] = 'genetic_association'
    DATASOURCE_TO_DATATYPE_MAPPING['cancer_gene_census'] = 'somatic_mutation'
    DATASOURCE_TO_DATATYPE_MAPPING['eva_somatic'] = 'somatic_mutation'
    DATASOURCE_TO_DATATYPE_MAPPING['chembl'] = 'known_drug'
    DATASOURCE_TO_DATATYPE_MAPPING['europmc'] = 'literature'
    DATASOURCE_TO_DATATYPE_MAPPING['disgenet'] = 'literature'

def _get_evidence_string_generic_mapping():
    return {
            "_all" : {"enabled" : True},
            "_routing":{ "required":True,
                         "path":"disease.id"},
            "properties" : {
                "target" : {
                    "type" : "object",
                     "properties" : {
                         "id" : {
                              "type" : "string",
                              "index" : "not_analyzed"
                         },
                         "target_type" : {
                              "type" : "string",
                              "index" : "not_analyzed"
                         },
                         "activity" : {
                              "type" : "string",
                              "index" : "not_analyzed"
                         },

                     }
                },
                "disease" : {
                    "type" : "object",
                     "properties" : {
                         "id" : {
                              "type" : "string",
                              "index" : "not_analyzed"
                         }
                     }
                },
                "_private" : {
                    "type" : "object",
                     "properties" : {
                         "efo_codes" : {
                              "type" : "string",
                              "index" : "not_analyzed"
                         },
                         "facets" : {
                            "type" : "object",
                            "properties" : {
                                "uniprot_keywords": {
                                    "type" : "string",
                                    "index" : "not_analyzed"
                                }
                            }
                         }
                     }
                },
                "disease.efo_info" : {
                    "type" : "object",
                     "properties" : {
                         "path" : {
                              "type" : "string",
                              "index" : "not_analyzed"
                         }
                     }
                },
                "evidence" : {
                    "type" : "object",
                    # "index": "no",
                     "properties" : {
                         "evidence_codes" : {
                              "type" : "string",
                              "index" : "not_analyzed"
                         },
                #      #
                #      #     "association_score":{
                #      #         "type" : "object",
                #      #         "properties" : {
                #      #             "probability" : {
                #      #                 "type" : "object",
                #      #                 "properties" : {
                #      #                     "value" : {
                #      #                        "type" : "double",
                #      #                     },
                #      #                     "method" : {
                #      #                        "type" : "string",
                #      #                     }
                #      #                 }
                #      #             }
                #      #         }
                #      #     },
                     }
                }
            },
        "dynamic_templates" : [
            {
                "scores" : {
                    "path_match" : "scores.*",
                    "mapping" : {
                         "type" : "double",
                    }
                }
            },


            {
                "do_not_index_evidence" : {
                    "path_match" : "evidence.*",
                    "path_unmatch" : "evidence.evidence_codes*",
                    "mapping" : {
                        "index" : "no"
                    }
                }
            },

            {
                "do_not_index_drug" : {
                    "path_match" : "drug.*",
                    "mapping" : {
                        "index" : "no"
                    }
                }
            },
            {
                "do_not_index_unique_ass" : {
                    "path_match" : "unique_association_fields.*",
                    "mapping" : {
                        "index" : "no"
                    }
                }
            },

        ]
       }



class ElasticSearchConfiguration():


    available_databases = Config().DATASOURCE_TO_DATATYPE_MAPPING.keys()
    available_databases.append('other')

    if os.environ.get('CTTV_EL_LOADER')== 'prod' or \
            os.environ.get('CTTV_EL_LOADER')== 'stag':
        generic_shard_number = 3
        generic_replicas_number = 1
        evidence_shard_number = 3
        evidence_replicas_number = 1

        bulk_load_chunk =1000
    else:
        generic_shard_number = 2
        generic_replicas_number = 0
        evidence_shard_number = 3
        evidence_replicas_number = 0
        bulk_load_chunk =100

    eco_data_mapping = {"mappings": {
                           Config.ELASTICSEARCH_ECO_DOC_NAME : {
                                "properties" : {
                                    "code" : {
                                        "type" : "string",
                                        "index" : "not_analyzed"
                                        },
                                    "path_codes" : {
                                        "type" : "string",
                                        "index" : "not_analyzed"
                                        },
                                    "path" : {
                                        "properties" : {
                                            "url" : {
                                                "type" : "string",
                                                "index" : "not_analyzed"
                                                },
                                            },
                                        },
                                    }
                                }
                           },
                        "settings":  {"number_of_shards" : generic_shard_number,
                                      "number_of_replicas" : generic_replicas_number,
                                      },
                        }

    efo_data_mapping = {
        "mappings": {
            Config.ELASTICSEARCH_EFO_LABEL_DOC_NAME : {
                "properties" : {
                    "code" : {
                        "type" : "string",
                        "index" : "not_analyzed"
                        },
                    "path_codes" : {
                        "type" : "string",
                        "index" : "not_analyzed"
                        },
                    "path" : {
                        "properties" : {
                            "url" : {
                                "type" : "string",
                                "index" : "not_analyzed"
                                },
                            },
                        },
                    "_private" : {
                        "type" : "object",
                        "properties" : {
                            "suggestions" : {
                                "type" : "completion",
                                "index_analyzer" : "whitespace_analyzer",
                                "search_analyzer" : "edgeNGram_analyzer",
                                "payloads" : True
                                },
                            },
                        },
                    }
                }
            },
        "settings":  {
            "number_of_shards" : generic_shard_number,
            "number_of_replicas" : generic_replicas_number,
            "analysis": {
                 "filter": {
                    "edgeNGram_filter": {
                       "type": "edgeNGram",
                       "min_gram": 2,
                       "max_gram": 20,
                       "token_chars": [
                          "letter",
                          "digit"
                       ]
                    },
                    "simple_filter": {
                       "type": "standard",
                       "token_chars": [
                          "letter",
                          "digit"
                       ]
                    }
                 },
                 "analyzer": {
                    "edgeNGram_analyzer": {
                       "type": "custom",
                       "tokenizer": "whitespace",
                       "filter": [
                          "lowercase",
                          "asciifolding",
                          "edgeNGram_filter"
                       ]
                    },
                    "whitespace_analyzer": {
                       "type": "custom",
                       "tokenizer": "whitespace",
                       "filter": [
                          "lowercase",
                          "asciifolding",
                          "simple_filter",
                       ]
                    }
                 }
               }
            },
        }

    gene_data_mapping = {
         "settings": {
                "number_of_shards" : generic_shard_number,
                "number_of_replicas" : generic_replicas_number,
                "analysis": {
                    "filter": {
                         "edgeNGram_filter": {
                            "type": "edgeNGram",
                            "min_gram": 2,
                            "max_gram": 20,
                            "token_chars": [
                               "letter",
                               "digit"
                            ]
                         },
                         "simple_filter": {
                            "type": "standard",
                            "token_chars": [
                               "letter",
                               "digit"
                            ]
                         }
                    },
                    "analyzer": {
                         "edgeNGram_analyzer": {
                            "type": "custom",
                            "tokenizer": "whitespace",
                            "filter": [
                               "lowercase",
                               "asciifolding",
                               "edgeNGram_filter"
                            ]
                         },
                        "whitespace_analyzer": {
                            "type": "custom",
                            "tokenizer": "whitespace",
                            "filter": [
                               "lowercase",
                               "asciifolding",
                               "simple_filter",
                            ]
                        }
                    }
                }
            },
        "mappings": {
            Config.ELASTICSEARCH_GENE_NAME_DOC_NAME : {
                "properties" : {
        #             "symbol_synonyms" : {
        #                 "type" : "string",
        #                 "index" : "not_analyzed"
        #                 },
        #             "approved_symbol" : {
        #                 "type" : "string",
        #                 "index" : "not_analyzed"
        #                 },
        #             "ensembl_external_name" : {
        #                 "properties" : {
        #                     "type" : "string",
        #                     "index" : "not_analyzed"
        #                     },
        #                 },
                    "_private" : {
                        "type" : "object",
                        "properties" : {
                            "suggestions" : {
                                "type" : "completion",
                                "index_analyzer" : "whitespace_analyzer",
                                "search_analyzer" : "whitespace_analyzer",
                                "payloads" : True
                                },
                            "facets":{
                                "type" : "object",
                                "properties" : {
                                    "reactome" : {
                                        "type" : "object",
                                        "properties" : {
                                            "pathway_type_code" : {
                                                "type" : "string",
                                                "index" : "not_analyzed"
                                            },
                                            "pathway_code" : {
                                                "type" : "string",
                                                "index" : "not_analyzed"
                                            }
                                        }
                                    },
                                    "uniprot_keywords" : {
                                        "type" : "string",
                                        "index" : "not_analyzed"
                                    }

                                }
                            },
                        },
                    },
                },
                "dynamic_templates" : [

                    {
                        "do_not_index_drugbank" : {
                            "path_match" : "drugbank.*",
                            "mapping" : {
                                "index" : "no"
                            }
                        }
                    },

                    {
                        "do_not_index_go" : {
                            "path_match" : "go.*",
                            "mapping" : {
                                "index" : "no"
                            }
                        }
                    },
                    {
                        "do_not_index_interpro" : {
                            "path_match" : "interpro.*",
                            "mapping" : {
                                "index" : "no"
                            }
                        }
                    },
                    {
                        "do_not_index_pdb" : {
                            "path_match" : "pdb.*",
                            "mapping" : {
                                "index" : "no"
                            }
                        }
                    },
                    {
                        "do_not_index_reactome" : {
                            "path_match" : "reactome.*",
                            "mapping" : {
                                "index" : "no"
                            }
                        }
                    },
                ]
            },
        }
    }

    expression_data_mapping = {
        "settings": {
                "number_of_shards" : generic_shard_number,
                "number_of_replicas" : generic_replicas_number,
                }

    }

    evidence_mappings = {}
    for db in available_databases:
        evidence_mappings[Config.ELASTICSEARCH_DATA_DOC_NAME+'-'+db]= _get_evidence_string_generic_mapping()

    evidence_data_mapping = { "settings": {"number_of_shards" : evidence_shard_number,
                                           "number_of_replicas" : evidence_replicas_number,
                                           # "index.store.type": "memory"
                                           },
                              "mappings": evidence_mappings,
                            }
    score_data_mapping = { "settings": {"number_of_shards" : evidence_shard_number,
                                       "number_of_replicas" : evidence_replicas_number,
                                       "index.store.type": "memory"
                                       },
                              "mappings": evidence_mappings,
                            }
