import numpy as np
from numpy import random
import math
from scipy import stats
import matplotlib.pyplot as plt

import pickle
from scipy.special import comb
import pandas as pd
import os
import sys
import RC
import SFmodel_MLE
import SFmodel_Copeland
import DFlearn
import LRPR
import majority_vote3
import blade_chest_Synthetic_DFData
import BC_Accuracy
import GNNRank_Synthetic
import Generate_Score_BTL
import Data_BTL_model


#idx = sys.argv[1]

num_items = 100
dim = 10

total_pairs = int(comb(num_items,2))

m2 = int(num_items * math.log2(num_items))

l = int(math.log2(num_items))


r = int(total_pairs/m2)

m_vals = []
l_vals = []
no_of_pairs = np.zeros(r-1)
no_of_comparisons = np.zeros(6)

for i in range(1,r):
    m3 = i*m2
    m_vals.append(m3)
    #no_of_pairs[i-1] = m3

no_of_pairs = m_vals

print(m_vals)
print(no_of_pairs)

#for i in range(0,6,1):
#    l3 = (2**i)*l2
#    l_vals.append(l3)

#no_of_comparisons = l_vals

accuracy_no_of_pairs = np.zeros(((10,r-1)))
ktc_vals = np.zeros(((10,r-1)))
ktc2_vals = np.zeros(((10,r-1)))


dim2 = 50
c = 0.00009 #l2 regularization parameter
#h_val = h_1
#num_clusters = 1

'''accuracy_RC_total = []
ktc_RC_total = []

accuracy_DFlearn_total = []
ktc_DFlearn_total = []

accuracy_SF_total = []
ktc_SF_total = []'''

accuracy_RC_total = np.zeros(((10,r-1)))
accuracy_DFlearn_total = np.zeros(((10,r-1)))
accuracy_SF_total = np.zeros(((10,r-1)))
accuracy_LRPR_total = np.zeros(((10,r-1)))
accuracy_MV_total = np.zeros(((10,r-1)))
accuracy_BC_total = np.zeros(((10,r-1)))


cycles_total = np.zeros(((10,r-1)))
cycle_fraction_total = np.zeros(((10,r-1)))

ktc_RC_total = np.zeros(((10,r-1)))
ktc_DFlearn_total = np.zeros(((10,r-1)))
ktc_SF_total = np.zeros(((10,r-1)))
ktc_LRPR_total = np.zeros(((10,r-1)))
ktc_MV_total = np.zeros(((10,r-1)))
ktc_BC_total = np.zeros(((10,r-1)))

        
upset_RC_total = np.zeros(((10,r-1)))
upset_SF_total = np.zeros(((10,r-1)))
upset_DFlearn_total = np.zeros(((10,r-1)))
upset_LRPR_total = np.zeros(((10,r-1)))
upset_MV_total = np.zeros(((10,r-1)))

rmse_RC_total = np.zeros(((10,r-1)))
rmse_DFlearn_total = np.zeros(((10,r-1)))
rmse_MV_total = np.zeros(((10,r-1)))
rmse_SF_total = np.zeros(((10,r-1)))
rmse_LRPR_total = np.zeros(((10,r-1)))
rmse_BC_total = np.zeros(((10,r-1)))


dim_mv = 3
dim_BC = 10

count_iter = 0

def initialize_params_normal(num_items, dim_mv, std_deviation,t):

    np.random.seed(t)
        
    params = np.random.normal(0, scale = std_deviation, size = (dim_mv,num_items))

    params = params/np.linalg.norm(params,2,axis = 0)
       
    return params

def initialize_params_uniform(num_items, dim_mv):
    
    params = np.random.uniform(low = -1, high = 1, size = (dim_mv,num_items))

    return params



for t in range(10):
    
    print(t)
 
    embeddings = Generate_Score_BTL.generate_score(num_items)

    params = initialize_params_normal(num_items, dim_mv, 1/math.sqrt(1), t)

    np.savetxt("embeddings_BTL"+str(t)+".txt", embeddings)
          
    count_m = 0

    
    for m in m_vals:
    
        embedding_obj = Data_BTL_model.embedding(embeddings, num_items, l, m)

        accuracy_RC, ktc_RC, upset_RC, rmse_RC = RC.RankCentrality(embedding_obj, num_items, l, m)
        accuracy_SF, ktc_SF, rmse_SF = SFmodel_Copeland.SF_Copeland_DFdata(embedding_obj, num_items, l, m, dim)
        accuracy_DFlearn, ktc_DFlearn, upset_DFlearn, cycles, cycle_fraction, rmse_DFlearn = DFlearn.Ranking_BTLdata(embedding_obj, num_items, l, m, dim, dim2) #, idx)
        accuracy_LRPR, ktc_LRPR, rmse_LRPR = LRPR.LRPR(embedding_obj, num_items, l , m)
        accuracy_MV, ktc_MV, upsets_MV, rmse_MV = majority_vote3.MV_MLE_DFdata(embedding_obj, params, num_items, l, m, dim_mv, t, 'BTL')
        data_BC = blade_chest_Synthetic_DFData.create_data(embedding_obj, num_items, l, m, t, 'BTL')
        
        #score_BTL = np.copy(embedding_obj.score)
        
        #pred_accuracy,rmse, ktc = BC_Accuracy.BC_Synthetic(m, t, score_BTL, 'BTL')

        GNNRank_Synthetic.DFdata(embedding_obj, num_items, l, m, t, 'BTL') #GNN format data generation 

        
        accuracy_RC_total[count_iter][count_m] = accuracy_RC
        accuracy_SF_total[count_iter][count_m] = accuracy_SF
        accuracy_DFlearn_total[count_iter][count_m] = accuracy_DFlearn
        accuracy_LRPR_total[count_iter][count_m] = accuracy_LRPR
        accuracy_MV_total[count_iter][count_m] = accuracy_MV
        #accuracy_BC_total[count_iter][count_m] = pred_accuracy

        rmse_RC_total[count_iter][count_m] = rmse_RC
        rmse_DFlearn_total[count_iter][count_m] = rmse_DFlearn
        rmse_MV_total[count_iter][count_m] = rmse_MV
        rmse_SF_total[count_iter][count_m] = rmse_SF
        rmse_LRPR_total[count_iter][count_m] = rmse_LRPR
        #rmse_BC_total[count_iter][count_m] = rmse
        
        count_m = count_m + 1
    
    count_iter = count_iter + 1


np.savetxt("accuracy_RC_BTLData.txt", accuracy_RC_total)
np.savetxt("accuracy_SF_BTLData.txt", accuracy_SF_total)
np.savetxt("accuracy_DF_BTLData.txt", accuracy_DFlearn_total)
np.savetxt("accuracy_LRPR_BTLData.txt", accuracy_LRPR_total)
np.savetxt("accuracy_MV_BTLData.txt", accuracy_MV_total)
#np.savetxt("accuracy_BC_BTLData.txt", accuracy_BC_total)




np.savetxt("rmse_RC_BTLData.txt", rmse_RC_total)
np.savetxt("rmse_DFlearn_BTLData.txt", rmse_DFlearn_total)
np.savetxt("rmse_MV_BTLData.txt", rmse_MV_total)
np.savetxt("rmse_SF_BTLData.txt", rmse_SF_total)
np.savetxt("rmse_LRPR_BTLData.txt", rmse_LRPR_total)
#np.savetxt("rmse_BC_BTLData.txt", rmse_BC_total)

