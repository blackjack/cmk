#!/usr/bin/env python

import argparse
import os
import yaml


parser = argparse.ArgumentParser(description='Run autogen')
parser.add_argument('--input-dir', help='File with input files')
parser.add_argument('--output-dir', help='Output directory')
parser.add_argument('--dry-run',
                    help='Do dont regenerate source files', action='store_true')
parser.add_argument('--cmake', help='CMake file list')

args = parser.parse_args()

args.input_dir = os.path.abspath(args.input_dir)
args.output_dir = os.path.abspath(args.output_dir)
args.cmake = os.path.abspath(args.cmake)


input_files = []

for _, _, files in os.walk(args.input_dir):
    input_files = input_files + files

input_files = [os.path.join(args.input_dir, f) for f in input_files]


header_template = """
#pragma once
namespace %s {
    void print();
}
"""
source_template = """
#include "%s.h"
#include <iostream>

void %s::print() {
    std::cout << __FILE__ << std::endl;
}
"""

cmake_template = """
set(GENERATED_SRCS "%s" CACHE INTERNAL "")
message("SOURCES: ${GENERATED_SRCS}")
"""

output_files = []


def processFile(yaml):
    for f in yaml['files']:
        header = os.path.join(args.output_dir, f + '.h')
        source = os.path.join(args.output_dir, f + '.cpp')

        output_files.append(source)
        if args.dry_run:
            continue

        if not os.path.isdir(args.output_dir):
            os.mkdir(args.output_dir)

        with open(header, 'w') as h:
            h.write(header_template % f)

        with open(source, 'w') as s:
            s.write(source_template % (f, f))


for input_filename in input_files:
    with open(input_filename, 'r') as f:
        processFile(yaml.load(f))

with open(args.cmake, 'w') as f:
    f.write(cmake_template % ';'.join(output_files))
