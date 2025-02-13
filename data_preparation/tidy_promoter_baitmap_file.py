#!/usr/bin/env python 

import pandas as pd
import argparse
import time
import os
import sys


def tidy_promoter_file(baits,out_file,p_id):
    cols = ['chr', 'start', 'end', 'frag_id', 'genes']
    bait_df = pd.read_csv(baits, sep="\t", names = cols).drop_duplicates()
    bait_df['genes'] = bait_df['genes'].str.replace(', ', ',')
    bait_df['genes'] = bait_df['genes'].str.split(',')
    bait_df_new = bait_df.explode('genes')
    bait_df_new = bait_df_new.dropna()
    bait_df_new = bait_df_new.drop_duplicates()
    bait_df_new['project'] = p_id
    bait_df_new.sort_values(by = 'genes', inplace=True, ascending=True)
    bait_df_new.to_csv(out_file, sep='\t', header=False, index=False)

def parse_args():
    parser = argparse.ArgumentParser(
            description="Tidy up promoter file for CoDeS3D pipeline")

    parser.add_argument(
            '-f', '--bait-file', required = True,
            help = '''Pass a promoter information file with an extension .baitmap 
            which was used to do CHiCAGO analysis''')
    
    parser.add_argument(
            '-o', '--out-fp', required = True,
            help = '''Provide path to an output file''')

    parser.add_argument(
            '-p', '--project-id', type=str, required = True,
            help = '''Project ID will be appended into the output file
            which will be used while running the CoDeS3D pipeline.
            Example: 'InkyungJung2019'. ''')
    return parser.parse_args()


if __name__ == '__main__':
    
    args =  parse_args()
    if not (args.bait_file or args.out_fp or args.project_id):
        message = '''One or more of the required parameters are missing.
        Use tidy_promoter_baitmap_file.py -h for more details.'''
        print(message)
        sys.exit()

    tidy_promoter_file(args.bait_file, 
                       args.out_fp, 
                       args.project_id)


