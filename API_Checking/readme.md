The API_checker can generate a table with all possible key words matched code listed. 

Below is how the result looks like:

| file_name        | line_number | matched_key_word | original code                                                |
| ---------------- | ----------- | ---------------- | ------------------------------------------------------------ |
| xx_project2.py   | 36          | bfmatcher        | def bfmatcher(img1,img2,kp1,des1,kp2,des2,threshold=65, silent=true): |
| xxs2_project2.py | 198         | bfmatcher        | kp_matches,kp_hammdist = bfmatcher(img1,img2,kp_des_pair1[0],kp_des_pair1[1],kp_des_pair2[0],kp_des_pair2[1], threshold=threshold[1]) |
| cs1_project2.py  | 18          | bfmatcher        | matcher = cv2.bfmatcher(cv2.norm_l2, true)                   |
| g21_project2.py  | 13          | findhomography   | def findhomography(matchingpoints):                          |