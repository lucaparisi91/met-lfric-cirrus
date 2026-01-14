import tqdm
import shutil
import os
import re
from typing import List
import jmespath as jp
import pandas as pd
import argparse
import json

def get_gungho_path(param: dict) -> str:
    """Get the path to the gungho executable based on the given parameters.
    """
    gungho_exe=""
    
    if param["profiler"] is not None:

        # Cray pat profile should be of the form cray_pat:<mode>

        if param["profiler"].startswith("cray_pat"):
            
            mode= param["profiler"].split(":")[1]
            gungho_exe = f"/work/z04/shared/lparisi/software-cirrus-ex/spack-cirrus-ex/test_lfric/build_lfric/lfric_apps_{param['opt']}_craypat/applications/gungho_model/bin/gungho_model+pat+{mode}"
    
    if gungho_exe == "": # Default executable fallback
        gungho_exe = f"/work/z04/shared/lparisi/software-cirrus-ex/spack-cirrus-ex/test_lfric/build_lfric/lfric_apps_{param['opt']}/applications/gungho_model/bin/gungho_model"
    
    return gungho_exe

def setup(param) -> str:
    """Generate a job folder for the given parameters.
    Args:
        param (dict): A dictionary containing the parameters for the job.
    Returns:
        Directory name of the generated job folder.
    """

    assert "template_dir" in param

    template_dir  : str =param["template_dir"]
    dirname      : str =param["working_dir"]
    

    mesh_dir = os.path.join( 
        param["mesh_dir"] ,
        f"{param['mesh']}_{int(param['nodes'])*int(param['ppn'])}"
    )
   
    # Copy the template folder to a new folder named dirname
    shutil.copytree(template_dir, dirname)

    # Check if mesh_dir exists
    if not os.path.exists(mesh_dir):
        raise FileNotFoundError(f"Mesh directory {mesh_dir} does not exist.")
    
    
    # Symlink all .nc files in `mesh_dir` in the new folder
    for file_name in os.listdir(mesh_dir):
        if file_name.endswith(".nc"):
            full_file_name = os.path.join(mesh_dir, file_name)
            if os.path.isfile(full_file_name):
                os.symlink(full_file_name, os.path.join(dirname, file_name))
    
    # Replace the prefix in configuration.nml with the correct mesh file name
    config_path = os.path.join(dirname, "configuration.nml")
    with open(config_path, "r") as file:
        config_data = file.read()
    
    mesh_prefix= param["mesh"]
    config_data = config_data.replace("unset_file_prefix", mesh_prefix)

    with open(config_path, "w") as file:
        file.write(config_data)


def get_script(param: dict) -> str:
    """Generate a script to run gungho with the given parameters.
    Args:
        param (dict): A dictionary containing the parameters for the job.
    Returns:
        The script to run in a batch session.
    """
    
    
    launcher="" # Launcher command between srun and the executable

    # Load modules and set environment variables
    script= """
module load PrgEnv-gnu
module load cray-hdf5-parallel/1.14.3.5
module load cray-netcdf-hdf5parallel/4.9.0.17

export FI_CXI_RX_MATCH_MODE=hybrid
export SRUN_CPUS_PER_TASK=$SLURM_CPUS_PER_TASK

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export OMP_PLACES=cores
"""


    # setup run with hpctoolkit
    if param["profiler"] and param["profiler"]["tool"] == "hpctoolkit":
        launcher="hpcrun -o hpctoolkit-gungho_model-measurements"
        script= script + f"""
source /work/z04/shared/lparisi/software-cirrus-ex/spack-cirrus-ex/env.sh
module load spack/1.0.2/epcc-config-0.2
spack env activate /work/z04/shared/lparisi/software-cirrus-ex/spack-cirrus-ex/test_lfric/lfric
spack env activate /work/z04/shared/lparisi/software-cirrus-ex/spack-cirrus-ex/test_lfric/environments/lfric/
spack load hpctoolkit
        """

    
    # Generate run command
    
    script  = script + f"""

GUNGHO_EXEC={get_gungho_path(param)}

srun --hint=nomultithread \
     --distribution=block:block \
     {launcher} \
     ${{GUNGHO_EXEC}} configuration.nml

"""
    return script


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Manage LFRic job runs")
    
    # Action to perform: setup or get_script
    parser.add_argument(
        "action",
        choices=["setup", "get_script"],
        help="Action to perform: setup (create job folders), get_script (generate job scripts)"
    )

    # Get number of nodes
    parser.add_argument(
        "--nodes",
        type=int,
        default=1,
        help="Number of nodes to use for the job"
    )

    # Get number of tasks per node
    parser.add_argument(
        "--ppn",
        type=int,
        default=288,
        help="Number of tasks per node to use for the job "
    )

    # Get mandatory mesh type
    parser.add_argument(
        "--mesh",
        type=str,
        default=None,
        help="Mesh type to use for the job",
        required=True
    )

    # Get mandatory mesh directory
    parser.add_argument(
        "--mesh_dir",
        type=str,
        default=None,
        help="Directory containing mesh files for the job",
        required=True
    )

    # Get optmization level
    parser.add_argument(
        "--opt",
        type=str,
        default="fast-debug",
        choices=["fast-debug","fast","debug","production"],
        help="Optimization level to use for the job",
        required=False
    )

    # Get profiler tool
    parser.add_argument(
        "--profiler",
        type=str,
        default=None,
        choices=["hpctoolkit","cray_pat:sampling","cray_pat:mpi"],
        help="Optimization level to use for the job",
        required=False
    )

    # Get a template directory to use to generate different directories
    parser.add_argument(
        "--template_dir",
        type=str,
        default=None,
        help="Path to a template directory to use to generate different job folders"
    )

    # name of a working directory
    parser.add_argument(
        "--working_dir",
        type=str,
        default=".",
        help="Path to a working directory to use to generate different job folders"
    )
    

    args = parser.parse_args()

    parameters = {
        "nodes": args.nodes,
        "ppn": args.ppn,
        "mesh": args.mesh,
        "mesh_dir": args.mesh_dir,
        "opt": args.opt,
        "template_dir": args.template_dir,
        "profiler": args.profiler,
        "working_dir": args.working_dir
    }


    # Perform the requested action
    if args.action == "setup":
        setup(parameters)
    elif args.action == "get_script":
        print(get_script(parameters))
    