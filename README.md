# PHASE: Personalized Head-based Automatic Simulation for Electromagnetic Properties in 7T MRI
The official implementation of PHASE.

<img src="Figs/Problem_figure.png" alt="First Figure" width="800"/>

# Abstract
Accurate and individualized human head models are becoming increasingly important for electromagnetic (EM) simulations. These simulations depend on precise anatomical representations to realistically model electric and magnetic field distributions, particularly when evaluating Specific Absorption Rate (SAR) within safety guidelines. We introduce Personalized Head-based Automatic Simulation for EM properties (PHASE), an automated open-source toolbox that generates high-resolution, patient-specific head models for EM simulations using paired T1-weighted (T1w) magnetic resonance imaging (MRI) and computed tomography (CT) scans with 13 tissue labels. To evaluate the performance of PHASE models, we conduct semi-automated segmentation and EM simulations on 15 real human patients, serving as the gold standard reference. The PHASE model achieved comparable global SAR and localized SAR averaged over 10 grams of tissue (SAR-10g), demonstrating its potential as a promising tool for generating large-scale human model datasets in the future.

# Hightlights
- We propose PHASE, an automatic toolbox which can automatically generate personalized human head models for EM simulation usage from pairs of real MRI and CT scans.
- We perform a comparative analysis against the outputs of manually refined reference models and existing models, evaluating the SAR accuracy through EM simulations. 
- We explore tissue groupings to evaluate how varying levels of anatomical details affect the EM simulation results of ultrahigh field RF transmit coil.
- We release PHASE as an open resource toolbox to support research in medical physics, including applications in RF coil design and EM safety evaluation.


# Quick start
## Brain segmentation and mapping
SLANT brain segmentation [1] is applied to segment detailed brain region.
Refer to [SLANT](https://github.com/MASILab/SLANTbrainSeg?tab=readme-ov-file) to run the trained model on your T1w MRI volume and get the segmented `.nii.gz` final results.

A brain mapping from 133 anatomical labels to 8 tissue groups with distinct electrical properties is applied to the segmented brain. Run:
```bash
python SLANT_label_mapping.py --input_dir your/input/dict --output_dir your/output/dict --mapping_file braincolor_hierarchy_STAPLE.txt
```

## Other tissues
[SimNIBS](https://simnibs.github.io/simnibs/build/html/index.html) [2] and [GRACE](https://github.com/lab-smile/GRACE) [3] are used to segment and fill in the other parts of the human head.

## Automatic correction
With segmented brain from SLANT, other tissues from SimNIBS and GRACE, bones from registered CT, run to combine and perform correction:
```bash
python combination.py
```
## Model construction: from `.nii` to `.raw`
A script is provided to transform `.nii` file to `.raw` file which is importable for most simulation software.
```bash
python nii_to_raw.py
```
An example of a header `.txt` file needed for `.raw` when importing is provided. The grid extent and spatial steps need to be refined to your models.

# Reference
[1] Huo, Yuankai, et al. "3D whole brain segmentation using spatially localized atlas network tiles." NeuroImage 194 (2019): 105-119.  
[2] Puonti, Oula, et al. "Accurate and robust whole-head segmentation from magnetic resonance images for individualized head modeling." Neuroimage 219 (2020): 117044.  
[3] Stolte, Skylar E., et al. "Precise and rapid whole-head segmentation from magnetic resonance images of older adults using deep learning." Imaging Neuroscience 2 (2024): 1-21.

# Contact
For any questions or discussion, [email us](mailto:zhengyi.lu@vanderbilt.edu).