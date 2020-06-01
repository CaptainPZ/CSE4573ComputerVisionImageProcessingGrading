 the Integrity site that describes briefly what you requested of students and what you did to process?Student submissions, concatenating previous materials, archive of key web materials (homography.py, ...)





# General Recommended Requirement for Submission

- Package should be submitted in **zip** format

  > There do have students who wrapped their packages in rar format and caused unzip command fail since rar is not supported. 

- Whether script can be split into multiple files

  > Ask them to submit all python files in one file will make it easier to perform moss check since it will be easier to quantify how many lines of code in total in this submission have potential academic integrity issue. But it is still possible to post process and concatenate their files into one if split. 

- Submission package structure, which shall at lease includes instruction on following:

  - Main script name and location

    > Generally the main script shall resides in `src` folder under root directory, however, many students have showed issues in using relative directory to refer files outside `src` folder, it is recommended to ask them to just put main script in the root submission folder.

  - Results file, if required, also needs to specify the location & file name

  - notes, always ask them to create a note in their submission root directory in case they have special requirement to run their script. 

  - Report (if required)

  - All dependencies 

- Directory handling

  > Since Windows and (MacOS, Linux) handle directory in different format, it is strongly recommended to teach them to use general directory handle methods like using python function `os.path.join()` in order to make their code cross platform compatible.

- Argument Parsing

  > A lot common issue is regarding the way how to pass argument into their script. This is critical if we prefer to use auto grading script to run their scripts in batch. Recommend to include an example of how to handle argument passing in the handout.
  >
  > Recommended reference:
  >
  > 	1. https://docs.python.org/3/library/sys.html#sys.argv  (With no flags)
  >  	2. https://docs.python.org/3/library/argparse.html   (With flags)

- Results file format (if applicable)

  > If result files are expected, it is recommended to handout an example of result file sample, an example how to create result file as well as a result file format checker in order to have their submitted results well formatted. 
  >
  > An example of such format checker can be found in: 
  >
  > [checker](../Project3_FaceDetection/Json_Checker_Annotator/)
  >
  > [result creation demo](../Project3_FaceDetection/Json_example/)

- Submission Guideline

  > A submission guideline is recommended to hand out before the assignment deadline. Sample submission guidelines can be found in project 2 and project 3's grading folder.







# Academic Integrity Checking Guide

*<u>It is recommended to have those files ready to perform AI check:</u>*

- All current year's student submission 

  >  each student recommended to have just one file for ease of quantify total number of lines matched with others. If their script are in separate python files, we can concatenate them. See following section regarding how to concatenate them.

- All previous year's submissions 

  > It is recommended to concatenate all files from previous semesters into just one big file in order to eliminate too many pairs of combinations in the check.

- Popular github repository

  > One repo which was fond to be very popular is already included in the "Integrity" folder. 
  >
  > It can be accessed here [Integrity](../Integrity/) 















# API Checking



