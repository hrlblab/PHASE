import nibabel as nib
import numpy as np
import pyvista as pv
from skimage import measure

file_path = 'Duke_34y_V5_2mm/Duke_head_with_shoulder.nii.gz'
nii_img = nib.load(file_path)
nii_data = nii_img.get_fdata()
nii_data = np.ceil(nii_data)
nii_data = nii_data.astype(np.uint8)
print(nii_data.shape)
print(np.max(nii_data))
print(np.min(nii_data))

grid_extent = nii_data.shape
voxel_size = nii_img.header.get_zooms()
voxel_size_m = tuple([v/1000 for v in voxel_size])
print(voxel_size_m)

nx, ny, nz = grid_extent
print(nx, ny, nz)
raw_data = np.zeros(nx * ny * nz, dtype=np.uint8)
for i in range(nx):
    for j in range(ny):
        for k in range(nz):
            p = k * nx * ny + j * nx + i
            raw_data[p] = nii_data[i, j, k]
            # print(raw_data[p])

print(raw_data.dtype)
output_path = 'Duke_34y_V5_2mm/Duke_head_with_shoulder.raw'
with open(output_path, 'wb') as raw_file:
    raw_file.write(raw_data.tobytes())

print(f'Raw file saved to: {output_path}')