#!/bin/bash

#SBATCH --ntasks=20
#SBATCH -N 1-1
#SBATCH -p limited
#SBATCH --mail-type=ALL
#SBATCH --mail-user=nhedger1@gmail.com
#SBATCH --error=/storage/basic/nh_leverhulme/JOBS/popeye/myjob.err


module load python3/anaconda/5.1.0
source activate myenv


python /storage/basic/nh_leverhulme/JOBS/popeye/BASE/model_fit.py ---n_jobs--- ---hem--- ---chunk--- ---outputpath--- ---stimdir--- ---datadir---




