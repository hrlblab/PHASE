import nibabel as nib
import numpy as np
import os
import argparse

def map_labels(input_dir, output_dir, mapping_file):
    data = np.loadtxt(mapping_file, delimiter=',')
    first_column = data[:, 0]
    fourth_column = data[:, 3]
    mapping = dict(zip(first_column, fourth_column))

    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if 'CT-MRI' in filename and filename.endswith('.nii.gz'):
            input_path = os.path.join(input_dir, filename)
            volume_nii = nib.load(input_path)
            volume_data = volume_nii.get_fdata()

            mapped_volume = np.vectorize(mapping.get)(volume_data)
            new_nifti = nib.Nifti1Image(mapped_volume, affine=volume_nii.affine, header=volume_nii.header)

            output_filename = f"{filename[:-7]}_mapped.nii.gz"
            output_path = os.path.join(output_dir, output_filename)
            nib.save(new_nifti, output_path)
            print(f"Mapped volume saved to {output_filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Map MRI/CT volume labels using a text-based mapping.")
    parser.add_argument('--input_dir', required=True, help="Directory containing input .nii.gz files")
    parser.add_argument('--output_dir', required=True, help="Directory to save mapped .nii.gz files")
    parser.add_argument('--mapping_file', required=True, help="Path to the label mapping .txt file")

    args = parser.parse_args()
    map_labels(args.input_dir, args.output_dir, args.mapping_file)
