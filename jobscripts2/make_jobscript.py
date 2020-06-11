
# Makes a set of jobscripts by looping through a set of variables

import re
import os

# Execute, or just write?
execute=False


# The number of CPUs per chunk
n_jobs=20

# The number of chunks
nchunks=100



# sbatch or sh?
#execute_type='sh'
execute_type='sbatch'


jobscript_base_path='/storage/basic/nh_leverhulme/JOBS/popeye/BASE/myjob_base.sh'


#job_path='/Users/nicholashedger/Code/PRF_PLAY/JOBS'
job_path='/storage/basic/nh_leverhulme/JOBS/popeye'


# Directory to output
outputpath='/storage/basic/nh_leverhulme/JOBS/popeye/outputs'

# Directory to data
datadir='/storage/basic/nh_leverhulme/DATA/avdata'

# Directory to stim
stimdir='/home/users/yg916972/TEMP/SYNCJOB/STIM'




# Split into nchunks.
chunkstrings=[]
for i in range(nchunks):
    chunkstrings.append('{0:03}'.format(i))


hems=['l','r']



for chunk in chunkstrings:
	for hem in hems:
		#The path to the jobfile to be written
		jobscript_current_path=os.path.join(job_path,'myjob_'+chunk+hem+'.sh')


		RE_dict =  {'---n_jobs---': str(n_jobs),
		'---hem---':hem,
		'---chunk---':chunk,
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