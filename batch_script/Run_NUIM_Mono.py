# This script is to run all the experiments in one program

import os
import subprocess
import time
import signal

SeqNameList = ['living_room_traj0', 'living_room_traj1', 'living_room_traj2', 'living_room_traj3', 'office_room_traj0', 'office_room_traj1', 'office_room_traj2', 'office_room_traj3', 'not_exist'];

Result_root = '/mnt/DATA/tmp/NUIM/DSO_Baseline/'

Number_GF_List =  [200, 300, 400, 600, 800, 1000, 1500, 2000];

Num_Repeating = 10 # 20 # 1 # 
SleepTime = 3 # 10 # 25

Path_DSO_Calib = '/home/yipuzhao/Codes/VSLAM/DSO/calib'

#----------------------------------------------------------------------------------------------------------------------
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    ALERT = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

for ri, num_gf in enumerate(Number_GF_List):
    
    Experiment_prefix = 'ObsNumber_' + str(int(num_gf))

    for iteration in range(0, Num_Repeating):

        Experiment_dir = Result_root + Experiment_prefix + '_Round' + str(iteration + 1)
        cmd_mkdir = 'mkdir -p ' + Experiment_dir
        subprocess.call(cmd_mkdir, shell=True)

        for sn, sname in enumerate(SeqNameList):
            
            print bcolors.ALERT + "====================================================================" + bcolors.ENDC

            SeqName = SeqNameList[sn]
            print bcolors.ALERT + "Round: " + str(iteration + 1) + "; Seq: " + SeqName

            File_Calib = Path_DSO_Calib + '/NUIM_Mono_calib.txt'
            File_Gamma = ' '
            File_Vignette = ' '
            Misc_Config = ' mode=1 nolog=1 quiet=1 nogui=1'

            File_rosbag  = '/mnt/DATA/Datasets/ICL-NUIM_dataset/BagFiles/' + SeqName + 'n.bag'
            File_traj = Experiment_dir + '/' + SeqName

            cmd_slam   = str('rosrun dso_ros dso_live image:=' + '/camera/image_raw' + ' calib=' + File_Calib + ' gamma=' + File_Gamma + \
                ' vignette=' + File_Vignette + ' preset='  + str(int(num_gf)) + ' realtime=' + File_traj + Misc_Config)
            cmd_rosbag = 'rosbag play ' + File_rosbag # + ' -r 0.3' # + ' -u 20' 

            print bcolors.WARNING + "cmd_slam: \n"   + cmd_slam   + bcolors.ENDC
            print bcolors.WARNING + "cmd_rosbag: \n" + cmd_rosbag + bcolors.ENDC

            print bcolors.OKGREEN + "Launching SLAM" + bcolors.ENDC
            proc_slam = subprocess.Popen(cmd_slam, shell=True)
            # proc_slam = subprocess.call(cmd_slam, shell=True)
            time.sleep(SleepTime)

            print bcolors.OKGREEN + "Launching rosbag" + bcolors.ENDC
            proc_bag = subprocess.call(cmd_rosbag, shell=True)

            print bcolors.OKGREEN + "Wait for exporting results" + bcolors.ENDC
            time.sleep(SleepTime)

            print bcolors.OKGREEN + "Finished rosbag playback, kill the process" + bcolors.ENDC
            subprocess.call('rosnode kill dso_live', shell=True)
            time.sleep(SleepTime)
            subprocess.call('pkill dso_live', shell=True)
