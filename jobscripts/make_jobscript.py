
# Makes a set of jobscripts by looping through a set of variables

import re
import os

# Execute, or just write?
execute=False

# sbatch or sh?
#execute_type='sh'
execute_type='sbatch'

# The jobscript template.
#jobscript_base_path='/Users/nicholashedger/Code/PRF_PLAY/myjob_base.sh'

jobscript_base_path='/home/users/yg916972/TEMP/SYNCJOB/DUMP/BASE/myjob_base.sh'


#job_path='/Users/nicholashedger/Code/PRF_PLAY/JOBS'
job_path='/home/users/yg916972/TEMP/SYNCJOB/DUMP/JOBS'

# Directory to atlases
#atlaspath='/Volumes/BAHAMUT/ATLAS'
atlaspath='/home/users/yg916972/TEMP/SYNCJOB/DUMP/ATLAS/ATLAS'


# Directory to output
outputpath='/home/users/yg916972/TEMP/SYNCJOB/DUMP/OUTPUT'

# Directory to data
datadir='/home/users/yg916972/TEMP/SYNCJOB/DUMP'

# Directory to stim
stimdir='/home/users/yg916972/TEMP/SYNCJOB/STIM'




# The number of CPUs.
n_jobs=20



# ROIs wherein models are fit.
ROInames=["V1v", "V1d" ,"V2v" ,"V2d" ,"V3v" ,"V3d" ,"hV4" ,"VO1" ,"VO2",
    "TO2" ,"TO1" ,"LO2", "LO1" ,"V3B","V3A"]

# Hemispheres
#hems=['l','r']


hems=['l']



for ROI in ROInames:
	for hem in hems:
		#The path to the jobfile to be written
		jobscript_current_path=os.path.join(job_path,'myjob_'+ROI+hem+'.sh')


		RE_dict =  {'---n_jobs---': str(n_jobs),
		'---hem---':hem,
		'---ROI---':ROI,
		'---atlaspath---':atlaspath,
		'---outputpath---':outputpath,
		'---stimdir---':stimdir,
		'---datadir---':datadir,
		}

		jobscript = open(jobscript_base_path)
		working_string = jobscript.read()
		jobscript.close()



		for e in RE_dict:
			rS = re.compile(e)
			working_string = re.sub(rS, RE_dict[e], working_string)
		of = open(jobscript_current_path,'w')
		of.write(working_string)
		of.close()


		if execute:
			os.system(execute_type + ' ' + jobscript_current_path)