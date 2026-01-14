import tqdm
import shutil
import os
import re
from typing import List
import jmespath as jp
import pandas as pd
import argparse

def get_gungho_path(param: dict) -> str:
    """Get the path to the gungho executable based on the given parameters.
    """
    gungho_exe=""
    
    if param["profiler"]:
        profiler=param["profiler"]

        if profiler["tool"] == "cray_pat":
            gungho_exe = f"/work/z04/shared/lparisi/software-cirrus-ex/spack-cirrus-ex/test_lfric/build_lfric/lfric_apps_{param['opt']}_craypat/applications/gungho_model/bin/gungho_model+pat+{profiler['mode']}"
    
    
    if gungho_exe == "": # Default executable fallback
        gungho_exe = f"/work/z04/shared/lparisi/software-cirrus-ex/spack-cirrus-ex/test_lfric/build_lfric/lfric_apps_{param['opt']}/applications/gungho_model/bin/gungho_model"
    
    return gungho_exe


def get_dirname(param) -> str:
    """Generate a directory name based on the given parameters. Also used to index different job runs.
    Args:
        param (dict): A dictionary containing the parameters for the job.
    Returns:
        Directory name as a string.
    """
    dirname="nodes{0}_ppn{1}_mesh{2}".format(
        param["nodes"],
        param["ppn"],
        param["mesh"]
    )

    if "profiler" in param and param["profiler"]:
        profiler=param["profiler"]
        dirname += f"_{profiler['tool']}"
        if "mode" in profiler:
            dirname += f"_{profiler['mode']}"
    return dirname


def run_job(dirname) -> None:
    """Run the job in the given directory.
    Args:
        dirname (str): The directory name where the job is located.
    """
    
    current_dir = os.getcwd()
    os.chdir(dirname)
    os.system(f"sbatch -J {dirname} lfric_job.slurm")
    os.chdir(current_dir)


def generate_anal_script(param: dict ) -> str:
    """Generate a script to analyze hpctoolkit data.
    
    Saves a slurm sbatch script named lfric_anal.slurm in the job folder.
    Args:
        param (dict): A dictionary containing the parameters for the job.
    Returns:
        The name of the generated analysis script file.
    """

    if param["profiler"] and param["profiler"]["tool"] == "hpctoolkit":
        script = """#!/bin/bash
#SBATCH --nodes=1
#SBATCH --time=02:00:00
#SBATCH --ntasks-per-node=288
#SBATCH --partition=standard
#SBATCH --qos=standard
#SBATCH --export=all
#SBATCH --distribution=block:block
#SBATCH --cpus-per-task=1

LFRIC_EX_DIR=/work/z04/shared/lparisi/software-cirrus-ex/spack-cirrus-ex/test_lfric 
source $LFRIC_EX_DIR/../env.sh
module load spack/1.0.2/epcc-config-0.2
module load PrgEnv-gnu
module load cray-hdf5-parallel/1.14.3.5
module load cray-netcdf-hdf5parallel/4.9.0.17
module load spack/1.0.2/epcc-config-0.2

spack env activate $LFRIC_EX_DIR/environments/lfric
spack load hpctoolkit
EXPERIMENT=hpctoolkit-gungho_model-measurements/ 
hpcstruct $EXPERIMENT
hpcprof $EXPERIMENT
        """

        dirname=get_dirname(param)
        file_name= os.path.join(dirname,"lfric_anal.slurm")
        with open( file_name, "w") as f:
            f.write(script)
        return file_name
    else:
        return None


def generate_job_folder(param) -> str:
    """Generate a job folder for the given parameters.
    Args:
        param (dict): A dictionary containing the parameters for the job.
    Returns:
        Directory name of the generated job folder.
    """
    
    dirname=get_dirname(param)

    # If dirname exists, abort
    if os.path.exists(dirname):
        print(f"Warning: Skipping directory {dirname} , as the directory already exists.")
        return None

    max_tasks_per_node : int = 288
    template_dir  : str = "template_dir"


    mesh_dir = os.path.join( 
        "/work/z04/shared/lparisi/software-cirrus-ex/spack-cirrus-ex/test_lfric/build_lfric/mesh_scripts",
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

    launcher="" # Launcher command between srun and the executable
    pre_script="" # Script to execute before the body

    # If profiling with hpctoolkit
    if param["profiler"] and param["profiler"]["tool"] == "hpctoolkit":
        launcher="hpcrun -o hpctoolkit-gungho_model-measurements"
        pre_script="""
source /work/z04/shared/lparisi/software-cirrus-ex/spack-cirrus-ex/env.sh
module load spack/1.0.2/epcc-config-0.2
spack env activate /work/z04/shared/lparisi/software-cirrus-ex/spack-cirrus-ex/test_lfric/lfric
spack env activate /work/z04/shared/lparisi/software-cirrus-ex/spack-cirrus-ex/test_lfric/environments/lfric/
spack load hpctoolkit
        """
    
    
    # Generate the new batch script with correct number of nodes and tasks per node
    
    lfric_job_body = f"""

module load PrgEnv-gnu
module load cray-hdf5-parallel/1.14.3.5
module load cray-netcdf-hdf5parallel/4.9.0.17

export FI_CXI_RX_MATCH_MODE=hybrid
export SRUN_CPUS_PER_TASK=$SLURM_CPUS_PER_TASK

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export OMP_PLACES=cores


GUNGHO_EXEC={get_gungho_path(param)}

srun --hint=nomultithread \
     --distribution=block:block \
     {launcher} \
     ${{GUNGHO_EXEC}} configuration.nml

"""

    lfric_job_header = f"""#!/bin/bash
#SBATCH --nodes={param['nodes']}
#SBATCH --exclusive
#SBATCH --time=02:00:00
#SBATCH --ntasks-per-node={param['ppn']}
#SBATCH --partition=standard
#SBATCH --qos=largescale
#SBATCH --export=all
#SBATCH --distribution=block:block
#SBATCH --cpus-per-task={max_tasks_per_node//int(param['ppn'])}

"""

    # Write the new batch script to the new folder
    with open( os.path.join(dirname,"lfric_job.slurm"), "w") as f:
        f.write(lfric_job_header)
        f.write(pre_script)
        f.write(lfric_job_body)
    
    
    # Replace the prefix in configuration.nml with the correct mesh file name
    config_path = os.path.join(dirname, "configuration.nml")
    with open(config_path, "r") as file:
        config_data = file.read()
    
    mesh_prefix= param["mesh"]
    config_data = config_data.replace("unset_file_prefix", mesh_prefix)

    with open(config_path, "w") as file:
        file.write(config_data)

    return dirname


def expand(settings: dict) -> list:
    
    """Expand the settings dictionary into a list of parameter combinations.
    Args:
        settings (dict): A dictionary containing lists of parameter values.
    Returns:
        A list of dictionaries, each containing a unique combination of parameters.
    """
    from itertools import product

    keys = settings.keys()
    values = (settings[key] for key in keys)
    combinations = [dict(zip(keys, combination)) for combination in product(*values)]
    return combinations


def collect_job_results(dirname):
    """Collect results from the given directory.
    Args:
        dirname (str): The directory name where the job results are located.
    """

    labels = [ "min_time" , "mean_time" , "max_time"] 

    # Compute a regex pattern to match timings for each label
    pattern=r"\|\|\W+([a-z_A-Z]+)\|\|"
    for labels in labels:
        pattern += r"\W+(\d+(?:\.\d+)?)\|\|"
    
    # Fetch timing results by matching each line with the pattern above

    results = {}
    with open( os.path.join(dirname,"timer.txt"), "r") as f:
        for line in f.readlines():
            
            match = re.match(pattern, line)
            if match:
                key = match.group(1)
                value = float(match.group(2))
                results[key] = value
    return results

def collect_results(parameters) -> List[dict]:
    """Collect results from multiple parameters.
    Args:
        parameters (list): A list of parameter dictionaries.
    Returns:
        A list of dictionaries containing parameters and their corresponding results.
    """

    results = []
    for param in tqdm.tqdm(parameters):

        try:
            job_folder = get_dirname(param)
        
            results.append(
                {
                    **param,
                    "timers":collect_job_results(job_folder)
                }
                )
        except Exception as e:
            print(f"Error collecting results for parameters {param}: {e}")
        
    return {"results":results}


def setup_runs(parameters) -> None:

    """Setup runs for multiple parameters.
    Args:
        parameters (list): A list of parameter dictionaries.
    """

    for param in tqdm.tqdm(parameters):
        job_folder = generate_job_folder(param)
        print(f"Generated job folder: {job_folder}")
        anal_script = generate_anal_script(param)
        if anal_script:
            print(f"Generated analysis script: {anal_script}")
        

def start_runs(parameters) -> None:

    """Start runs for multiple parameters.
    Args:
        parameters (list): A list of parameter dictionaries.
    """
    
    for param in tqdm.tqdm(parameters):
            try:
                job_folder = get_dirname(param)
                run_job(job_folder)
                print(f"Submitted job: {job_folder}")
            except Exception as e:
                print(f"Error submitting job for parameters {param}: {e}")


def get_table(results, x: str , y: str, x_label : str=None,y_label : str=None) -> pd.DataFrame:

    x=jp.compile(x).search(results)
    y=jp.compile(y).search(results)

    return pd.DataFrame({
        x_label if x_label else "x": x,
        y_label if y_label else "y": y
    })


        
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Manage LFRic job runs")
    parser.add_argument(
        "action",
        choices=["setup", "run", "collect"],
        help="Action to perform: setup (create job folders), run (submit jobs), or collect (gather results)"
    )
    args = parser.parse_args()

    parameters = expand( {
        "nodes" : [192],
        #"ppn" : [12,24,72,288,8],
        "ppn" : [12,24],
        "mesh" : ["C1536"],
        #"profiler" : [{"tool":"cray_pat","mode":"sampling"},{"tool":"cray_pat","mode":"mpi"}],
        "profiler" : [{"tool":"hpctoolkit"}],
        # mode: `sampling` or `tracing_parallelism` or False for Craypat 
        # tool: hpctoolkit or cray_pat
        "opt": ["fast-debug"]
    } )

    # Perform the requested action
    if args.action == "setup":
        setup_runs(parameters)
    elif args.action == "run":
        start_runs(parameters)
    elif args.action == "collect":
        results = collect_results(parameters)
        timer="semi_implicit_timestep_alg"
        data=get_table(results, x="results[].ppn", y=f"results[].timers.{timer}", x_label="ppn", y_label=timer)
        data_per_thread=pd.DataFrame({ "threads_per_rank" : 288/data["ppn"], "time" : data[timer]/100 }).reset_index(drop=True).sort_values(by="threads_per_rank")
        print(data_per_thread)
    

    