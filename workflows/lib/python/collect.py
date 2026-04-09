from vernier import collect_vernier_data
import pandas as pd
import os
import sys

def collect(shared_folder: str, vernier=True) -> pd.DataFrame:
    """Collects vernier data from a given folder and returns it as a pandas DataFrame

    ::param shared_folder: The path to the root folder containing the working directoris of lfric_atm jobs
    ::param vernier: A boolean indicating whether to collect vernier data
    ::returns: A pandas DataFrame containing the collected vernier data, annotated with the parameters
    extracted from its subdirectories.

    """
    data_list=[]
    for folder in os.listdir(shared_folder):
        
        if folder.startswith("lfric_atm_"): # Only look for lfric_atm job folders
            
            if vernier:
                data=collect_vernier_data(f"{shared_folder}/{folder}")
                data_list.append(data)
    if len(data_list)==0:
        return pd.DataFrame({})
    else:
        return pd.concat(data_list)

if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(description='Collect data from a shared lfric_apps folder')
    parser.add_argument('root_folder', type=str, help='The path to the root folder containing the working directoris of lfric_apps jobs')
    parser.add_argument('--vernier', action='store_true', help='Whether to collect vernier data')
    args = parser.parse_args()
    
    data=collect(args.root_folder, vernier=args.vernier)
    data.to_csv(sys.stdout, sep=' ')