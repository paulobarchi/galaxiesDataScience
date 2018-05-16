#!/bin/bash
# save images for each class
## k10
### 3 classes
echo "k10 -- 3 classes"
# mkdir k10/imgs/3classes/E/
# mkdir k10/imgs/3classes/S_/
# mkdir k10/imgs/3classes/SB_/
# python saveImagesFromFits.py k10/fits/3classes/E/ k10/imgs/3classes/E/
python saveImagesFromFits.py k10/fits/3classes/S_/ k10/imgs/3classes/S_/
python saveImagesFromFits.py k10/fits/3classes/SB_/ k10/imgs/3classes/SB_/
### 11 classes
echo "k10 -- 11 classes"
mkdir k10/imgs/11classes/Ec/
mkdir k10/imgs/11classes/Ei/
mkdir k10/imgs/11classes/Er/
mkdir k10/imgs/11classes/Sa/
mkdir k10/imgs/11classes/Sb/
mkdir k10/imgs/11classes/Sc/
mkdir k10/imgs/11classes/Sd/
mkdir k10/imgs/11classes/SBa/
mkdir k10/imgs/11classes/SBb/
mkdir k10/imgs/11classes/SBc/
mkdir k10/imgs/11classes/SBd/
#
python saveImagesFromFits.py k10/fits/11classes/Ec/ k10/imgs/11classes/Ec/
python saveImagesFromFits.py k10/fits/11classes/Ei/ k10/imgs/11classes/Ei/
python saveImagesFromFits.py k10/fits/11classes/Er/ k10/imgs/11classes/Er/
python saveImagesFromFits.py k10/fits/11classes/Sa/ k10/imgs/11classes/Sa/
python saveImagesFromFits.py k10/fits/11classes/Sb/ k10/imgs/11classes/Sb/
python saveImagesFromFits.py k10/fits/11classes/Sc/ k10/imgs/11classes/Sc/
python saveImagesFromFits.py k10/fits/11classes/Sd/ k10/imgs/11classes/Sd/
python saveImagesFromFits.py k10/fits/11classes/SBa/ k10/imgs/11classes/SBa/
python saveImagesFromFits.py k10/fits/11classes/SBb/ k10/imgs/11classes/SBb/
python saveImagesFromFits.py k10/fits/11classes/SBc/ k10/imgs/11classes/SBc/
python saveImagesFromFits.py k10/fits/11classes/SBd/ k10/imgs/11classes/SBd/

## k20
### 3 classes
echo "k20 -- 3 classes"
mkdir k20/imgs/3classes/E/
mkdir k20/imgs/3classes/S_/
mkdir k20/imgs/3classes/SB_/
python saveImagesFromFits.py k20/fits/3classes/E/ k20/imgs/3classes/E/
python saveImagesFromFits.py k20/fits/3classes/S_/ k20/imgs/3classes/S_/
python saveImagesFromFits.py k20/fits/3classes/SB_/ k20/imgs/3classes/SB_/
### 11 classes
echo "k20 -- 11 classes"
mkdir k20/imgs/11classes/Ec/
mkdir k20/imgs/11classes/Ei/
mkdir k20/imgs/11classes/Er/
mkdir k20/imgs/11classes/Sa/
mkdir k20/imgs/11classes/Sb/
mkdir k20/imgs/11classes/Sc/
mkdir k20/imgs/11classes/Sd/
mkdir k20/imgs/11classes/SBa/
mkdir k20/imgs/11classes/SBb/
mkdir k20/imgs/11classes/SBc/
mkdir k20/imgs/11classes/SBd/
#
python saveImagesFromFits.py k20/fits/11classes/Ec/ k20/imgs/11classes/Ec/
python saveImagesFromFits.py k20/fits/11classes/Ei/ k20/imgs/11classes/Ei/
python saveImagesFromFits.py k20/fits/11classes/Er/ k20/imgs/11classes/Er/
python saveImagesFromFits.py k20/fits/11classes/Sa/ k20/imgs/11classes/Sa/
python saveImagesFromFits.py k20/fits/11classes/Sb/ k20/imgs/11classes/Sb/
python saveImagesFromFits.py k20/fits/11classes/Sc/ k20/imgs/11classes/Sc/
python saveImagesFromFits.py k20/fits/11classes/Sd/ k20/imgs/11classes/Sd/
python saveImagesFromFits.py k20/fits/11classes/SBa/ k20/imgs/11classes/SBa/
python saveImagesFromFits.py k20/fits/11classes/SBb/ k20/imgs/11classes/SBb/
python saveImagesFromFits.py k20/fits/11classes/SBc/ k20/imgs/11classes/SBc/
python saveImagesFromFits.py k20/fits/11classes/SBd/ k20/imgs/11classes/SBd/