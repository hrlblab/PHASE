# PHASE: Personalized Head-based Automatic Simulation for Electromagnetic Properties in 7T MRI
The official implementation of PHASE.

<img src="Figs/Problem_figure.png" alt="First Figure" width="800"/>

# Abstract
Accurate and individualized human head models are becoming increasingly important for electromagnetic (EM) simulations. These simulations depend on precise anatomical representations to realistically model electric and magnetic field distributions, particularly when evaluating Specific Absorption Rate (SAR) within safety guidelines. We introduce Personalized Head-based Automatic Simulation for EM properties (PHASE), an automated open-source toolbox that generates high-resolution, patient-specific head models for EM simulations using paired T1-weighted (T1w) magnetic resonance imaging (MRI) and computed tomography (CT) scans with 13 tissue labels. To evaluate the performance of PHASE models, we conduct semi-automated segmentation and EM simulations on 15 real human patients, serving as the gold standard reference. The PHASE model achieved comparable global SAR and localized SAR averaged over 10 grams of tissue (SAR-10g), demonstrating its potential as a promising tool for generating large-scale human model datasets in the future.

# Quick start
## Brain mapping
SLANT brain segmentation[(Huo et al., 2019)](https://doi.org/10.1016/j.neuroimage.2019.03.041) is applied to segment detailed brain region.
Refer to [SLANT](https://github.com/MASILab/SLANTbrainSeg?tab=readme-ov-file) to run the trained model on your T1w MRI volume.

A brain mapping from 133 anatomical labels to 8 tissue groups with distinct electrical properties is applied to the segmented brain. Run:
<pre> python SLANT_label_mapping.py --input_dir your/input/dict --output_dir your/output/dict --mapping_file braincolor_hierarchy_STAPLE.txt
 </pre>