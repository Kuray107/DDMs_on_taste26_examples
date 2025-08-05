import argparse
import glob
import numpy as np
import os
import librosa
import matplotlib.pyplot as plt



def code_for_tags(e_name, tags):
    e_code = []
    for tag in tags:
        e_code.append(f"""
        <div class="col-4 col-6-medium col-12-small">
            <article class="box style2">
                <a class="image featured"><img src="examples/{e_name}_{tag.lower()}.png" alt="" /></a>
                <p>{tag}</p>
                <audio controls="controls" preload="preload"><source src='examples/{e_name}_{tag.lower()}.wav'></source></audio>
            </article>
        </div>
        """)
    return e_code

def main(examples_dir: str, output_dir: str = None, task_name: str = None):

    # output directory
    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(__file__))

    output_dir = os.path.join(output_dir, 'code')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print('output_dir:', output_dir)


    # Select examples based on clean data
    audio_files = glob.glob(f'{examples_dir}/{task_name}*_70percent.wav')

    example_names = [os.path.basename(f).replace('_70percent.wav', '') for f in audio_files]

    code = []

    for e_name in example_names:

        e_code = []

        print('e_name:', e_name)

        e_name_base = e_name.replace(f'{task_name}_', '')

        # clean, noisy
        e_code.append(f'<p><h3>{e_name_base}</h3></p>\n')
        e_code.append('<div class="row">\n')
        e_code += code_for_tags(e_name=e_name, tags=['70percent', '100percent', '130percent'])
        e_code.append('</div>\n')

        e_code.append('<br>\n')


        # SB
        # e_code.append('<div class="row">\n')
        # e_code += code_for_tags(e_name=e_name, tags=['Proposed_spk1', 'Proposed_spk2'])
        # e_code.append('</div>\n')

        code += e_code

    with open(os.path.join(output_dir, f'code_{task_name}.html'), 'w') as f:
        f.writelines(code)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--examples-dir', required=True, type=str, help='Data directory')
    parser.add_argument('--output-dir', required=False, type=str, help='Output directory')
    parser.add_argument('--task-name', default="n_different_length_comparison", type=str, help='Name of the task (dataset)')
    args = parser.parse_args()

    main(examples_dir=args.examples_dir, output_dir=args.output_dir, task_name=args.task_name)