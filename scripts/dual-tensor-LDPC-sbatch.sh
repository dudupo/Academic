#!/bin/bash
#SBATCH --mem=10gb
#SBATCH --time=10:0:0
#SBATCH --error=error_log.txt
#SBATCH --output=log.txt
#SBATCH --job-name=sampling-dual-tensors-codes
#SBATCH --killable
sage ./dual-tensor-LDPC.sage
