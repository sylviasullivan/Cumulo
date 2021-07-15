#!/bin/sh
##
#SBATCH --account=bb1131
#SBATCH --partition=prepost
#SBATCH --job-name=evap
#SBATCH -c 1
#SBATCH --time=01:00:00
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=sylvia.sullivan@kit.edu

source activate ncplot
python ERA5_EvapRetrieve_EPBig

