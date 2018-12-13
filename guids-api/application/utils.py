import os
import json
from uuid import uuid4
from factories.log import create_logger


log = create_logger('guids-api')


def generate_data(filename):
    if not os.path.isfile(filename):
        result = {}
        n = 100000
        log.info('Generating data...')
        for i in range(n):
            result[str(uuid4())] = str(uuid4())
            if i % (n / 10) == 0:
                log.info(f'Generating {i * 10} done')
        with open(filename, 'w') as f:
            json.dump(result, f)


