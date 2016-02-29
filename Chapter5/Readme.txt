This folder contains the procedure used for computing reputation-based(in procedure.py), provenance-based assessments (in svm.r) and a combination of the two (in procedure.py).

NOTE:
For privacy reasons we could not share the original data.The .csv file contains the intermediate (data_testset_* and data_trainset_*) and final results (reputations_* and results_*) with different granularities.

TO COMPUTE PROVENANCE-BASED ESTIMATES:
from svm.r, run:
graph_pca(rbind(read.csv("data_testset.csv"),read.csv("data_trainset.csv"))) 

TO COMBINE BOTH REPUTATION ASSESSMENTS BASED ON COMBINATION OF REPUTATION AND PROVENANCE, run:
python procedure.py to compute reputations and reputation  