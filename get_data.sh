#!/bin/bash
# TODO: Refine the script for repeating procedures.
DATA_FOLDER=./data/src/
mkdir -p $DATA_FOLDER
wget -nc -t 5 -O $DATA_FOLDER/20080713.zip https://www.dropbox.com/sh/f2l0dhlnok7ggkh/AADXpXQO0EWZHO9_ttk-zmqya/ST2008071306%20Gg/CUT_ST2008071306_06_Gg_HY_OLIC?dl=1
wget -nc -t 5 -O $DATA_FOLDER/20110607.zip https://www.dropbox.com/sh/f2l0dhlnok7ggkh/AADYdNoizZoyf14gjl6G_6W_a/03_ST20110607_02_Gg%20%E4%BE%86\(PT\)/ST20110607_02_Gg_cut?dl=1
wget -nc -t 5 -O $DATA_FOLDER/20110704.zip https://www.dropbox.com/sh/f2l0dhlnok7ggkh/AABnF4TWVklsZ19VfO4-LfJfa/ST20110704_01_Gg_BH_%E4%BE%86%20\(PT\)/ST20110704_01_Gg_cut?dl=1
wget -nc -t 5 -O $DATA_FOLDER/20130801.zip https://www.dropbox.com/sh/f2l0dhlnok7ggkh/AACbjnUHqbbROTep55ECjDFNa/ST20130801_01%E8%8A%B1%E7%B4%8B\(%E6%97%A9\)%20JE/CUT%20ST20130801_01%E8%8A%B1%E7%B4%8B\(%E6%97%A9\)%20JE_Olic?dl=1
wget -nc -t 5 -O $DATA_FOLDER/20140811.zip https://www.dropbox.com/sh/f2l0dhlnok7ggkh/AABCfqQTNd7C1ixOCuBCjX2Ga/07_TT_20140811/CUT_TT20140811_pm_IFs?dl=1
wget -nc -t 5 -O $DATA_FOLDER/20140813.zip https://www.dropbox.com/sh/f2l0dhlnok7ggkh/AAAjlEQRWYcGjIUAkIT1tBT5a/08_TT20140813/CUT_TT20140813_pm_IFs?dl=1
unzip -d $DATA_FOLDER/20080713 -n $DATA_FOLDER/20080713.zip
unzip -d $DATA_FOLDER/20110607 -n $DATA_FOLDER/20110607.zip
unzip -d $DATA_FOLDER/20110704 -n $DATA_FOLDER/20110704.zip
unzip -d $DATA_FOLDER/20130801 -n $DATA_FOLDER/20130801.zip
unzip -d $DATA_FOLDER/20140811 -n $DATA_FOLDER/20140811.zip
unzip -d $DATA_FOLDER/20140813 -n $DATA_FOLDER/20140813.zip
rm -fr $DATA_FOLDER/*.zip
