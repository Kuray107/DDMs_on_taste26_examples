import argparse
import glob
import os
import random
import shutil

SETUPS = {
    'AR_DD_Comparison': {
        'original': 'org_speech',
        'auto-regressive': 'ar',
        'discrete-diffusion': 'dd_50steps',
    },
    'different_num_steps_comparison': {
        'original': 'org_speech',
        '1steps': 'dd_1steps',
        '10steps': 'dd_10steps',
        '25steps': 'dd_25steps',
        '50steps': 'dd_50steps',
        '100steps': 'dd_100steps',
    },
    'different_length_comparison': {
        'original': 'org_speech',
        '70percent': 'dd_length0.7',
        '100percent': 'dd_50steps',
        '130percent': 'dd_length1.3',
    },
}


def main(data_dir: str, output_dir: str = None, num_examples: int = 5, random_seed: int = 1911):

    # seed
    random.seed(random_seed)

    # output directory
    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(__file__))

    output_dir = os.path.join(output_dir, 'examples')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print('output_dir:', output_dir)

    for setup, setup_paths in SETUPS.items():

        print('setup:', setup)

        # Select examples based on clean data
        all_clean_files = glob.glob(f'{data_dir}/{setup_paths["original"]}/*.wav')


        # Randomly select an item
        reference_examples = random.sample(all_clean_files, num_examples)
        reference_examples = [os.path.basename(x)[:-4] for x in reference_examples]

        print(reference_examples) 

        for name, proc_path in setup_paths.items():
            print('name:', name)
            print('proc_path:', proc_path)

            for re in reference_examples:
                # source file
                if name.startswith('proposed'):    
                    src_file = os.path.join(data_dir, proc_path, f'processed_{re}.wav')
                else:
                    src_file = os.path.join(data_dir, proc_path, f'{re}.wav')

                # dst file
                dst_file = os.path.join(output_dir, f'{setup}_{re}_{name}.wav')

                # copy example
                shutil.copy(src_file, dst_file)




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data-dir', required=True, type=str, help='Data directory')
    parser.add_argument('--output-dir', required=False, default=None, type=str, help='Output directory')
    parser.add_argument('--num-examples', default=5, type=int, help='Number of examples to select')
    args = parser.parse_args()

    main(data_dir=args.data_dir, output_dir=args.output_dir, num_examples=args.num_examples)