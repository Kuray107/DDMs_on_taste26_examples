import argparse
import glob
import numpy as np
import os
import librosa
import matplotlib.pyplot as plt


# plt.style.use('dark_background')


def main(data_dir: str, output_dir: str = None):

    # output directory
    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(__file__))

    output_dir = os.path.join(output_dir, 'examples')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print('output_dir:', output_dir)


    # Select examples based on clean data
    audio_files = glob.glob(f'{data_dir}/*.wav')

    for a_file in audio_files:

        print('a_file:', a_file)
        
        y, sr = librosa.load(a_file, sr=None)

        # fig, ax = plt.subplots(nrows=2, ncols=1, sharex=True, gridspec_kw={'height_ratios': [1, 4]})
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 4))
        ax_spec = ax

        # # time domain
        # librosa.display.waveshow(y, sr=sr, ax=ax[0])
        # ax[0].set_xlabel('')

        # spectrogram
        hop_length = 128
        n_fft = 512
        spec = np.abs(librosa.stft(y=y, hop_length=hop_length, n_fft=n_fft))
        spec_db = librosa.amplitude_to_db(spec, ref=np.max, top_db=80)
        img = librosa.display.specshow(spec_db, y_axis='hz', x_axis='time', hop_length=hop_length, n_fft=n_fft, sr=sr, ax=ax_spec)
        
        # labels for frequencies
        ax_spec.set_yticks([2000, 4000, 6000, 8000])
        ax_spec.set_yticklabels(['2kHz', '4kHz', '6kHz', '8kHz'])
        ax_spec.set_ylabel('')

        # db colorbar
        cbar = fig.colorbar(img, ax=ax, format='%+2.f dB', aspect=50)
        cbar.ax.tick_params(labelsize=8)

        # output file
        spec_file = os.path.join(output_dir, os.path.basename(a_file)[:-4] + '.png')

        plt.tight_layout()
        plt.savefig(spec_file, bbox_inches='tight')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data-dir', required=True, type=str, help='Data directory')
    parser.add_argument('--output-dir', required=False, type=str, help='Output directory')
    args = parser.parse_args()

    main(data_dir=args.data_dir, output_dir=args.output_dir)