#!/usr/bin/env python3

import os
import json
from typing import List

g_nodes: List[List[str],] = None  # host, user, password


def get_nodes(config_file: str) -> list:
    global g_nodes
    if not g_nodes:
        with open(config_file, 'r') as f:
            g_nodes = json.load(f)
    return g_nodes


if __name__ == '__main__':
    cur_dir = os.path.dirname(__file__)
    for host, user, passwd in get_nodes(os.path.join(cur_dir, 'nodes.json')):
        print(host, user, passwd)
