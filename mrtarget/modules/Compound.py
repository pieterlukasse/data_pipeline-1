import json
import logging
import requests
from tqdm import tqdm
from mrtarget.Settings import Config
from mrtarget.common import Actions
from requests.exceptions import Timeout, HTTPError, ConnectionError

import mrtarget.common as c

__copyright__  = "Copyright 2014-2018, Open Targets"
__credits__    = ["ChuangKee Ong"]
__license__    = "Apache 2.0"
__version__    = "1.2.8"
__maintainer__ = "ChuangKee Ong"
__email__      = ["data@targetvalidation.org"]
__status__     = "Production"


class CompoundActions(Actions):
    PROCESS = 'process'

class CompoundProcess():

    def __init__(self, loader):
        self._logger = logging.getLogger(__name__)
        self.loader = loader

        self.cpd_ids = []
        self.cpd_data = {}

    def process(self):

        self.get_cpd_ids()
        self.parse_cpd_data()
        self.store_to_elasticsearch()

    def get_cpd_ids(self):

        ct = 0
        data = self.query_rest_api(Config.CHEMBL_MOLECULE)

        for i in tqdm(data,
                  desc='Extract compound IDs from ChEMBL API',
                  unit=' compound(s)'):

            if ct == 1000:
                break

            cpd_id = i['molecule_chembl_id']

            if cpd_id not in self.cpd_ids:
                self.cpd_ids.append(cpd_id)
                ct += 1

    def parse_cpd_data(self):

        for cpd_id in tqdm(self.cpd_ids,
                  desc='Extract compound attributes, indications & mechanisms from ChEMBL API',
                  unit=' compound(s)'):

            cpd_attributes = self.download_from_uri(cpd_id, Config.CHEMBL_MOLECULE)
            cpd_indication = self.download_from_uri(cpd_id, Config.CHEMBL_INDICATION)
            cpd_mechanism = self.download_from_uri(cpd_id, Config.CHEMBL_MECHANISM)

            if cpd_id not in self.cpd_data:
                self.cpd_data[cpd_id] = \
                    {
                        'attributes': cpd_attributes['molecules'],
                        'indications': [],
                        'mechanisms': []
                    }

            if cpd_indication:
                for row in cpd_indication['drug_indications']:

                    line = \
                        {
                            'disease_id': row['efo_id'],
                            'disease_label': row['efo_term'],
                            'disease_max_phase': row['max_phase_for_ind'],
                            'reference': row['indication_refs'],
                            'mesh_heading': row['mesh_heading'],
                            'mesh_id': row['mesh_id']
                        }

                    try:
                        self.cpd_data[cpd_id]['indications'].append(line)
                    except KeyError:
                        self.cpd_data[cpd_id]['indications'] = list()
                        self.cpd_data[cpd_id]['indications'].append(line)

            if cpd_mechanism:
                for row in cpd_mechanism['mechanisms']:

                    try:
                        self.cpd_data[cpd_id]['mechanisms'].append(row)
                    except KeyError:
                        self.cpd_data[cpd_id]['mechanisms'] = list()
                        self.cpd_data[cpd_id]['mechanisms'].append(row)

    def query_rest_api(self, uri):
        '''return to json from uri'''
        next_get = True
        limit = 1000000
        offset = 0

        def _fmt(**kwargs):
            '''generate uri string params from kwargs dict'''
            l = ['='.join([k, str(v)]) for k, v in kwargs.iteritems()]
            return '?' + '&'.join(l)

        while next_get:
            chunk = None
            with c.URLZSource(uri + _fmt(limit=limit, offset=offset)).open() as f:
                chunk = json.loads(f.read())

            page_meta = chunk['page_meta']
            data_key = list(set(chunk.keys()) - set(['page_meta']))[0]

            if 'next' in page_meta and page_meta['next'] is not None:
                limit = page_meta['limit']
                offset += limit
            else:
                next_get = False

            for el in chunk[data_key]:
                yield el

    def download_from_uri(self, compound_id, uri):
            url = uri + '?molecule_chembl_id=' + compound_id

            try:
                r = requests.get(url, timeout=300)
                if r.status_code == 200:
                    return r.json()
                else:
                    raise IOError('failed to get data from ChEMBL API')

            except (ConnectionError, Timeout, HTTPError) as e:
                raise IOError(e)

    def store_to_elasticsearch(self):

        self._logger.debug('Store compound data into ElasticSearch')

        for key, data in self.cpd_data.items():
            self.loader.put(Config.ELASTICSEARCH_COMPOUND_INDEX_NAME,
                            Config.ELASTICSEARCH_COMPOUND_DOC_NAME,
                            key,
                            json.dumps(data),
                            True)

