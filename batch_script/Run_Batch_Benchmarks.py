# This script is to run all the experiments in one program

import os
import subprocess
import time
import signal

# SeqNameList = ['MH_05_difficult', 'V1_03_difficult', \
# 'dataset-room3_512_16_small_chunks', 'dataset-magistrale6_512_16_small_chunks', 'dataset-outdoors4_512_16_small_chunks', \
# 'Seq00_left', 'Seq04_left', '2019-01-25-17-30', \
# 'left_cam', 'freiburg2_desk_with_person'
# ];
# CalibList 	= ['EuRoC', 'EuRoC', 'TUM_VI', 'TUM_VI', 'TUM_VI', \
# 'Kitti_00_02', 'Kitti_04_12', 'Hololens', 'NewCollege', 'TUM_freiburg2'];
# CamTopicList = ['/cam0/image_raw', '/cam0/image_raw', \
# '/cam0/image_raw', '/cam0/image_raw', '/cam0/image_raw', \
# '/camera/image_raw', '/camera/image_raw', '/left_cam/image_raw', \
# '/cam0/image_raw', '/camera/image_raw'
# ]
# SeqDirList = ['/mnt/DATA/Datasets/EuRoC_dataset/BagFiles/', '/mnt/DATA/Datasets/EuRoC_dataset/BagFiles/', \
# '/mnt/DATA/Datasets/TUM_VI/BagFiles/', '/mnt/DATA/Datasets/TUM_VI/BagFiles/', '/mnt/DATA/Datasets/TUM_VI/BagFiles/', \
# '/mnt/DATA/Datasets/Kitti_Dataset/BagFiles/', '/mnt/DATA/Datasets/Kitti_Dataset/BagFiles/', '/mnt/DATA/Datasets/Hololens/BagFiles/', \
# '/mnt/DATA/Datasets/New_College/BagFiles/', '/mnt/DATA/Datasets/TUM_RGBD/BagFiles/'
# ];
SeqNameList = ['freiburg2_desk_with_person'];
CalibList   = ['TUM_freiburg2'];
CamTopicList = ['/camera/image_raw']
SeqDirList = ['/mnt/DATA/Datasets/TUM_RGBD/BagFiles/'];

Result_root = '/mnt/DATA/tmp/DSO_Mono_Baseline_Slomo/'

Number_GF_List =  [800] # [200, 300, 400, 600, 800, 1000, 1500, 2000];

Num_Repeating = 1 # 10 # 20 # 3 # 
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

            File_Calib = Path_DSO_Calib + '/' + CalibList[sn] + '_Mono_calib.txt'
            File_Gamma = ' '
            File_Vignette = ' '
            Misc_Config = ' mode=1 nolog=1 quiet=1 nogui=1'

            File_rosbag  = SeqDirList[sn] + SeqName + '.bag'
            File_traj = Experiment_dir + '/' + SeqName

            cmd_slam   = str('rosrun dso_ros dso_live image:=' + CamTopicList[sn] + ' calib=' + File_Calib + ' gamma=' + File_Gamma + \
                ' vignette=' + File_Vignette + ' preset='  + str(int(num_gf)) + ' realtime=' + File_traj + Misc_Config)
            cmd_rosbag = 'rosbag play ' + File_rosbag + ' -r 0.2' # + ' -u 20' 

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
