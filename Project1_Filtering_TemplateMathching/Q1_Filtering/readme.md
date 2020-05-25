Explanation of scripts: 

- csvwriter.py

  > All utility functions reside here

- Q1_Extraction_Run_All.py

  > extract each zip file, and run it, will output a log csv file to record whether each submission has been successfully executed or not

- Q1_Extraction_Run_Grading.py

  > In addition to above, this one will also compute the NCC with groundtruth to measure the performance. The NCC will also be logged into the output csv file.

- Q1_SingleRun.py

  > just extract and run a specified file, this is handy for spot check.