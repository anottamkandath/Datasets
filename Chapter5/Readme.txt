This folder contains the procedure used for computing reputation- (in procedure.py), provenance-based assessments (In svm.r) and a combination of the two (in procedure.py).

NOTE:

For privacy reasons we could not share the original data. The .csv file contain intermediate (data_testset_* and data_trainset_*) and final results (reputations_* and results_*) with different granularities.


TO COMPUTE PROVENANCE-BASED ASSESSMENTS:
from svm.r, run:
graph_pca(rbind(read.csv("data_testset.csv"),read.csv("data_trainset.csv"))) 



TO COMPUTE BOTH REPUTATIONS AND ASSESSMENTS BASED ON COMBINATION OF REPUTATION AND PROVENANCE:
run:
python procedure.py to compute reputations and reputation 