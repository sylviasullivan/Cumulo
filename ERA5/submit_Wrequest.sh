#!/bin/sh
##
#SBATCH --account=bb1131
#SBATCH --partition=prepost
#SBATCH --job-name=w5
#SBATCH -c 1
#SBATCH --time=01:00:00
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=sylvia.sullivan@kit.edu

source activate ncplot
python ERA5_WRetrieve_EPBig

