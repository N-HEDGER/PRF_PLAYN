#!/bin/bash

#SBATCH --ntasks=20
#SBATCH -N 1-1
#SBATCH -p limited
#SBATCH --mail-type=ALL
#SBATCH --mail-user=nhedger1@gmail.com
#SBATCH --error=/home/users/yg916972/TEMP/SYNCJOB/DUMP/JOBS/myjob.err


module load python3/anaconda/5.1.0
source activate myenv


python /Users/nicholashedger/Code/PRF_PLAY/model_fit.py ---n_jobs--- ---hem--- ---ROI--- ---atlaspath--- ---outputpath--- ---stimdir--- ---datadir---




