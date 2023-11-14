
DOWNLOAD DATA FROM SCIEBO 
---------------------------

cwd = fileparts(matlab.desktop.editor.getActiveFilename);
url= "https://uni-bonn.sciebo.de/s/9FxelLhARmHpw85";
mkdir(strcat(cwd,'/data'));
cd cwd % IMPORTANT TO CHANGE DIRECTORY
websave(strcat(cwd,'/data/testfile.csv'), strcat(url, '/download') );

--------------------------
## Day  1 

### S1 : intro and orientation

installation, matlab orientation, livescripts, matlab basics, experiment intro

### S2 : basic stats and barplots

loading csvs, basic stats on continuous data, stats on categorical data( grouped data), barplots on categorical data

## Day  2

### S1 : subject response
 barplot, pointplot with errorbars, exporting a figure 


### S2 : wheel turning speed

data sub-selection (eg. active trials only), line plots, heatmap, finding turning direction and validating against steinmetz

## Day  3 

### S1 : LFP analysis

boxplots, masking, plot of lfp vs time for different response types, subplots according to brain area, heatmap according to brain area

### S2 : Pupil position

scatterplots, regression and correlation, histograms and t-test

## Day  4 :

### S1 :  Frequency analysis

### S2 : spike counts

## Day  5 

### S1 : spike timings
