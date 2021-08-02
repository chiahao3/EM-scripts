# EM-scripts
Personal repo for EM related codes

## 1. DIGIMAT_defect_finding.ipynb

Demo script of finding point defects in ADF-STEM images with deep learning (fully convolutional network)

## 2. GetVeloxDCFIShifts.py

Extract and visualize the shift vectors applied by Velox (DCFI). This helps validating the frame averaging process because the stage movement should be 'smooth' or 'continuous' if the frame time is short enough.

## 3. SerpentineAcquisition_0801.ipynb

Automated acquisition powered by pywinauto and temscript. The script combines move stage (temscript), aberration correction (Sherpa), and acquisition (Velox). Presented in M&M 2021 [DOI: 10.1017/S1431927621003482](https://www.cambridge.org/core/journals/microscopy-and-microanalysis/article/deep-learning-enabled-atombyatom-analysis-of-2d-materials-on-the-millionatom-scale/3D988B4DA74CB2C7B090ED534420A23F)
