import nibabel as nib
import numpy as np
import os
import re

input_dir = 'MRI-CT_8label/'
CT_dir = 'MRI-CT paired data/MRI/'
SimNIBS_dir = 'MRI-CT_SimNIBS'
fat_dir = 'GRACE_fat/'
output_dir = 'MRI-CT_non_manual/'

file_num = 5780

def extract_number(filename):
    match = re.search(r'CT-MRI-(\d+)_seg_mapped\.nii\.gz', filename)
    if match:
        return int(match.group(1))
    return None

for filename in os.listdir(input_dir):
    if 'CT-MRI-' + str(file_num) in filename:
        # print(file_num)
        input_path = os.path.join(input_dir, filename)
        volume_nii = nib.load(input_path)
        volume_data = volume_nii.get_fdata()
        # print(volume_data.shape)

        bone_filename = 'CT-MRI-' + str(file_num) + '_seg.nii.gz'
        bone_path = os.path.join(CT_dir, bone_filename)
        bone_nii = nib.load(bone_path)
        bone_data = bone_nii.get_fdata()

        iSEG_filename = 'CT-MRI-' + str(file_num) + '_iSEG.nii.gz'
        iSEG_path = os.path.join(SimNIBS_dir, iSEG_filename)
        iSEG_nii = nib.load(iSEG_path)
        iSEG_data = iSEG_nii.get_fdata()[:, :, :, 0]

        # bone mask
        bone_mask0 = (bone_data == 2) | (iSEG_data == 7) | (iSEG_data == 8)
        bone_mask = (volume_data == 0) & bone_mask0
        volume_data[bone_mask] = 10

        # CSF mask
        csf_mask1 = (volume_data == 0) & (bone_data != 2) & (iSEG_data == 3)
        csf_mask2 = (volume_data == 0) & (bone_data == 1) & (iSEG_data == 2)
        csf_mask = csf_mask1 | csf_mask2
        volume_data[csf_mask] = 8

        # eyeball mask
        eye_mask = (volume_data == 0) & (bone_data == 0) & (iSEG_data == 6)
        volume_data[eye_mask] = 9

        # blood mask
        blood_mask = (volume_data == 0) & (iSEG_data == 9)
        volume_data[blood_mask] = 11

        # complete white matter in brain
        x, y, z = np.indices(volume_data.shape)
        # z_mask = z > 100
        more_WM_mask1 = (volume_data == 0) & (bone_data == 1)
        z_mask_n = z < 100
        more_WM_mask2 = (volume_data == 0) & (iSEG_data == 1) & z_mask_n
        more_WM_mask = more_WM_mask1 | more_WM_mask2
        volume_data[more_WM_mask] = 7

        # other mask (muscle, skin, ...)
        other_mask = (volume_data == 0) & (bone_data == 0) & (iSEG_data == 5)
        volume_data[other_mask] = 12

        # final make up leak CSF
        csf_mask_makeup = (volume_data == 0) & (bone_data == 1)
        volume_data[csf_mask_makeup] = 8
        break

fat_filename = 'seg_fat_' + str(file_num) + '.nii'
fat_path = os.path.join(fat_dir, fat_filename)
fat_nii = nib.load(fat_path)
fat_data = fat_nii.get_fdata()

region_filename = 'CT-MRI-' + str(file_num) + '_seg.nii.gz'
region_path = os.path.join('MRI-CT paired data/MRI/', region_filename)
region_nii = nib.load(region_path)
region_data = region_nii.get_fdata()

# skin mask
skin_mask0 = (volume_data == 0) | (volume_data == 12)
skin_mask = (fat_data == 9) & skin_mask0
volume_data[skin_mask] = 14

# Fat mask
fat_mask0 = (volume_data == 12) | (volume_data == 0)
fat_mask = (fat_data == 10) & fat_mask0
volume_data[fat_mask] = 15

# compensate the muscle
x, y, z = np.indices(volume_data.shape)
z_mask = (z < 50) & ((y > 180) | (y < 55))
muscle_mask1 = (fat_data == 11) & (volume_data == 0) & (region_data == 0)
# muscle_mask2 = ((fat_data == 7) | (fat_data == 8)) & (volume_data == 0) & (region_data == 0) & z_mask
muscle_mask2 = (fat_data != 0) & (volume_data == 0) & (region_data == 0) & z_mask
muscle_mask = muscle_mask1 | muscle_mask2
volume_data[muscle_mask] = 12


volume_data = volume_data.astype(np.uint8)
print(volume_data.shape)
new_nifti = nib.Nifti1Image(volume_data, affine=volume_nii.affine, header=volume_nii.header)

output_filename = 'seg_' + str(file_num) + '_non_manual.nii.gz'
output_path = os.path.join(output_dir, output_filename)
nib.save(new_nifti, output_path)

print(f"Fat combined volume saved to {output_path}")