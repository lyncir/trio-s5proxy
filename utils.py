# -*- coding: utf8 -*-
import os
import configparser

import trio


_base_dir = os.path.abspath(os.path.dirname(__file__))


async def load_config(filename):
    """
    加载配置文件
    """
    config = configparser.ConfigParser()

    async with await trio.open_file(filename) as f:
        text = await f.read()

    config.read_string(text)
    if 'default' not in config:
        raise IOError('Unable to load configuration file "{}"'.format(filename))

    # 必选字段
    for k in ['server', 'server_port', 'local', 'local_port']:
        if k not in config['default']:
            raise KeyError('Not found field: "{}"'.format(k))

    return config


config = trio.run(load_config, 'config.ini')
print(config)
