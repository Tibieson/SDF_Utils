import sys
import argparse
import subprocess
from subprocess import Popen
import os
import re
import shutil
import time
from pathlib import Path


SANDBOX_PREFIX = 'avenger'
dst_path       = ''

def get_runid():
    run_id = time.strftime("run_%Y_%m_%d-%H_%M_%S")
    return run_id

def get_files(path,ext):
    """get all files with extension ext in path path
    Args:
        path (str): path to search files in
        ext (str): extension of files
    Returns:
        list: list of strings of absolute paths to files
    """    
    file_lst = []
    for path, subdirs, files in os.walk(path):
        for name in files:
            if name.endswith(ext):
                file_lst.append(os.path.join(path, name))
    return file_lst



def read_sdfs(sdf_path,gpj_file):
    """reads all sdf in a path
    Args:
        sdf_path (str): path to sdfs
    """
    global dst_path
    CreateExportPath()
    
    sdf_files = get_files(sdf_path, ".sdf")
    sdfexporter_path = get_Gogeta_exporterpath(gpj_file)

    if(sdfexporter_path == -1):
        print(Path(gpj_file).stem +'.gpj Does not have exporter settings, select a valid one.')
        return -1
    
    commands = []
    for file in sdf_files:
        cmd = 'GogetaCmdline.exe -p '+ gpj_file + ' -i ' + str(file) + ' -o ' + os.path.join(os.getcwd(),dst_path[2:],file.split("\\")[-1])
        commands.append(cmd)
    
    procs = [ Popen(i) for i in commands]
    for p in procs:
        p.wait()

    #n = 4 #the number of parallel processes you want
    #for j in range(max(int(len(commands)/n), 1)):
    #    procs = [subprocess.Popen(i, shell=True) for i in commands[j*n: min((j+1)*n, len(commands))] ]
    #    for p in procs:
    #        p.wait()


def get_Gogeta_exporterpath(gpj_file):
    """reads the output path where gogeta exports the sdf files
    Args:
        gpj_file (str): path to gpj config file
    Returns:
        Str:  str path where gogeta exports the Output sdf file. 
    """
    root_sandbox    = gpj_file[:gpj_file.find(SANDBOX_PREFIX)]
    sdfexporter_path = ''
    with open(gpj_file) as f:
        lines = f.readlines()
        for row in lines:
            if row.find('filePath') != -1:
                sdfexporter_path = row.split(" ")[-1].split('"')[1] 
                #Verify if path is either absolute or relative
                if(os.path.isabs(sdfexporter_path.split(Path(sdfexporter_path).stem)[0])):
                    sdfexporter_path = sdfexporter_path.replace("/","\\")
                    return sdfexporter_path
                else:
                    remove_relativepath = re.match(r'.*(/../)',sdfexporter_path)
                    sdfexporter_path = sdfexporter_path.split(remove_relativepath[0])[-1]
                    sdfexporter_path = sdfexporter_path.replace("/","\\")
                    return os.path.join(root_sandbox,sdfexporter_path)

    if sdfexporter_path == '':
        return -1


def CreateExportPath():
    global dst_path
    run_id = get_runid()
    dataroot = os.path.join(os.curdir, "Data")
    try:
        dst_path = os.path.join(dataroot, "SDFs_" + run_id)
        #os.mkdir(os.path.join(dataroot, "SDFs_" + run_id.split("-")[0]))
        os.makedirs(os.path.join(dataroot, "SDFs_" + run_id))
        
    except:
        if(os.path.exists(dst_path)):
            print('Directory already exists')
        else:
            print("Directory couldn't be created. Check Admin Rights")
            return 


def main():
    

    sdf_path = r"C:\data\sdfs" 
    SimulationManager = r"C:\sndboxes\gogeta_debugmode\avengers-initiative-gogeta\GoGetASim\Custom\OF\Gen7_360_MOTwExp.gpj"

    """main function with arguments"""
    parser = argparse.ArgumentParser(description="Script for extracting SDF data from Gogeta Sim")

    parser.add_argument("sim_mngr_path", help="Path to MOT.ppj File for Gogeta ", nargs = 1)
    parser.add_argument("sdf_input_path", help="Pass to save csv", nargs = 1)

    args = parser.parse_args()
    SimulationManager = args.sim_mngr_path[0]
    sdf_path          = args.sdf_input_path[0]
 
    read_sdfs(sdf_path, SimulationManager)



if __name__ == "__main__":

    main()