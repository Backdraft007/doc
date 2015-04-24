#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import generate_tables

binding_infos = generate_tables.binding_infos
lang = 'en'

binding_name = {
'en':
""":ref:`{0} <api_bindings_{1}>`""",
'de':
""":ref:`{0} <api_bindings_{1}>`"""
}

binding_names = {
'en':
"""
.. |bindings| replace:: {0}
""",
'de':
"""
.. |bindings| replace:: {0}
"""
}

def make_substitutions():
    substitutions = ''

    formated_binding_names = []
    for binding_info in binding_infos:
        if binding_info.is_programming_language and binding_info.is_released:
            formated_binding_names.append(binding_name[lang].format(binding_info.display_name, binding_info.url_part))

    substitutions += binding_names[lang].format(', '.join(formated_binding_names)) + '\n'

    return substitutions

def write_if_changed(path, content):
    if os.path.exists(path):
        f = open(path, 'rb')
        existing = f.read()
        f.close()
        if existing == content:
            return

    f = open(path, 'wb')
    f.write(content)
    f.close()

def generate(path):
    global lang

    if path.endswith('/en'):
        lang = 'en'
    elif path.endswith('/de'):
        lang = 'de'
    else:
        print 'Wrong working directory'
        sys.exit(1)

    generate_tables.lang = lang

    print 'Generating ServerRoomMonitoring.substitutions'
    write_if_changed(os.path.join(path, 'source', 'Kits', 'ServerRoomMonitoring', 'ServerRoomMonitoring.substitutions'), make_substitutions())

if __name__ == "__main__":
    generate(os.getcwd())
