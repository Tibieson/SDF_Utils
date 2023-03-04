import pandas as pd
import numpy as np
from sdf import SdfReader
from pathlib import Path
import os
import logging

logger = logging.getLogger(__name__)
FORMAT = "%(asctime)s [%(filename)s] [%(levelname)s] - %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)


TARGET_COLLECTION_HEADER          = 's_SDC_OutputSignals_s_SDC_RadarTargetCollection_as_RadarTargetHeaders'
TARGET_COLLECTION_RADARTARGETS    = 's_SDC_OutputSignals_s_SDC_RadarTargetCollection_as_RadarTargets'
TARGET_COLLECTION_HEADER_IDX      = 'uw_StartIndex'
TARGET_COLLECTION_HEADER_NTARGETS = 'uw_NumberOfTargets'


BLIS_COLLECTION                   = 's_BLIS_OutputSignals'
PROCESS_RADARTARGET_AMBIGUOUS     = 'as_AmbiguousAttributes'

TRACK_COLLECTION_RADAR            = 's_SDC_OutputSignals_s_SDC_RadarTrackCollection_as_RadarTracks'
TRACK_ID                          = 'ul_ID'
start_idx = [0,255,510,765,1020]



def Sdf2DictConverter(root):
    sdf_struct = {}

    logger.info("The SDF has the following content: ")
    for rootstruct in root.dtype.names:
        logger.info("** {}".format(rootstruct))

    logger.info("SDF to Dict Parsing in Progress. ")
    for rootstruct in root.dtype.names:
        subroot = root[:][1][rootstruct]
        data = ExtractStructs(subroot)
        sdf_struct[rootstruct] = data
    
    logger.info("SDF to Dict Parsing Finished.")
    return sdf_struct

def ExtractStructs(root):

    df = {}

    for rootstruct in root.dtype.names:
	
        subroot = root[rootstruct]
        
        if subroot.dtype.names is not None:
            data = ExtractStructs(subroot)
            df[rootstruct] = data
        elif(len(root.dtype.names) > 1): #end of subtree however we cant exit the loop, there are still more fields to traverse
            df[rootstruct] = subroot
        else:
            return subroot
    
    return df

def Dict2Df(data):
    '''
        The function receives a dictionary that contains the full data for a given struct. The scope of this function is
        to collect all the elements for a given struct and convert it into a DataFrame, which it will contain the full info for all frames.

    ''' 
    Targets_done = False
    Tracks_done  = False

    if TARGET_COLLECTION_HEADER in data:
        logger.info("-- Start Conversion from Dictionary to DF for  {}".format(TARGET_COLLECTION_RADARTARGETS))
        
        start_idx = data[TARGET_COLLECTION_HEADER][TARGET_COLLECTION_HEADER_IDX]
        Ntargets  = data[TARGET_COLLECTION_HEADER][TARGET_COLLECTION_HEADER_NTARGETS]

        TotalFrames = start_idx.shape[0]

        df_targets = Auxiliar_for_Dict2DF(data[TARGET_COLLECTION_RADARTARGETS],Ntargets)
        Targets_done =True
        logger.info("-- Finished Conversion for {} DataFrame".format(TARGET_COLLECTION_RADARTARGETS))
        

    if TRACK_COLLECTION_RADAR in data:
        logger.info("-- Start Conversion from Dictionary to DF for  {}".format(TRACK_COLLECTION_RADAR))
        ID_tracks = data[TRACK_COLLECTION_RADAR][TRACK_ID]
        df_tracks = AuxiliarFunc_forRadarTracks(data[TRACK_COLLECTION_RADAR],ID_tracks)
        logger.info("-- Finished Conversion for {} DataFrame".format(TRACK_COLLECTION_RADAR))
        Tracks_done = True
    
    if(Targets_done and Tracks_done):
        return(df_targets,df_tracks)
    elif(Targets_done):
        return df_targets
    elif(Tracks_done):
        return df_tracks

    
def AuxiliarFunc_forRadarTracks(data,TrackId):
    df = pd.DataFrame()
    
    for key in data.keys():
        if key == TRACK_ID:   #we dont want to process track_ID content
            continue

        df_allframes = pd.DataFrame()
        if(isinstance(data[key],dict)):
            df_temp = AuxiliarFunc_forRadarTracks(data[key],TrackId)
            df_temp = df_temp.drop('Frame', axis = 1)
            df_temp.columns = key + '_' + df_temp.columns
            if df.empty:
                df = df_temp
            else:
                df = pd.concat([df,df_temp],axis = 1)

        else:
            temp = data[key]
            
            for frame in range(temp.shape[0]):
                df_temp = pd.DataFrame()
                Timeslice = temp[frame]
                Ids = TrackId[frame]

                if(np.where(Ids == 0)[0][0] == 0): #If first zero is first element then we have to go up to the second zero
                    selection = Timeslice[:np.where(Ids == 0)[0][1]]
                else:
                    selection = Timeslice[:np.where(Ids == 0)[0][0]]
                
                df_temp[key]      = selection
                df_temp['Frame']  = [frame] * len(selection)

                df_allframes = pd.concat([df_allframes, df_temp])
            df[key] = df_allframes[key]
            df['Frame'] = df_allframes['Frame']    #

    return df

def AuxiliarFunc_forAmbiguousCase(data,Ntargets):
    
    df = pd.DataFrame()
    for key in data.keys():
        df_allframes = pd.DataFrame()
        if(isinstance(data[key],dict)):
            df_temp = AuxiliarFunc_forAmbiguousCase(data[key],Ntargets)
            df_temp = df_temp.drop(['Sensor', 'Frame','Ambiguous_Target'], axis = 1)
            df_temp.columns = key + '_' + df_temp.columns
            if df.empty:
                df = df_temp
            else:
                df = pd.concat([df,df_temp],axis = 1)

        else:
            temp = data[key]
        
            for frame in range(temp.shape[0]):
                Timeslice = temp[frame]
                Targets = Ntargets[frame]
                
                idx = 0
                selection = np.array([])
                sensornum = np.array([])
                ambiguosity = np.array([])
                df_temp = pd.DataFrame()
                for target in Targets:

                    if(target > 0):
                        temp_timeslice = Timeslice[start_idx[idx]:start_idx[idx] + target]
                        selection_flat     = temp_timeslice.reshape(1,temp_timeslice.shape[0] * temp_timeslice.shape[1])
                        selection          = np.append(selection,selection_flat)

                        ambiguousity_order = [ii%temp_timeslice.shape[1] for ii in range(temp_timeslice.shape[0] * temp_timeslice.shape[1]) ]
                        ambiguosity        = np.append(ambiguosity,ambiguousity_order)  


                        sensornum = np.append(sensornum,[idx] * len(ambiguousity_order))

                    idx = idx + 1
                df_temp[key]      = selection
                
                
                df_temp['Sensor'] = sensornum
                df_temp['Frame']  = [frame] * len(selection)
                df_temp['Ambiguous_Target'] = ambiguosity
                df_allframes = pd.concat([df_allframes, df_temp])
            df[key] = df_allframes[key]
           

    df['Sensor'] = df_allframes['Sensor']
    df['Frame'] = df_allframes['Frame']
    df['Ambiguous_Target'] = df_temp['Ambiguous_Target']

    return df




def Auxiliar_for_Dict2DF(data,Ntargets):
    df           = pd.DataFrame()
    df_allframes = pd.DataFrame()
    df_temp      = pd.DataFrame()
    ambiguous_flag = False

    for key in data.keys():

        df_allframes = pd.DataFrame()
        if(isinstance(data[key],dict)):
            if(key == PROCESS_RADARTARGET_AMBIGUOUS):
                df_ambiguous = AuxiliarFunc_forAmbiguousCase(data[key],Ntargets)
                ambiguous_flag = True
            else:    
                df_temp = Auxiliar_for_Dict2DF(data[key],Ntargets)
                df_temp = df_temp.drop(['Sensor', 'Frame'], axis = 1)
                df_temp.columns = key + '_' + df_temp.columns
                if df.empty:
                    df = df_temp
                else:
                    df = pd.concat([df,df_temp],axis = 1)
        else:

            temp = data[key]
            for frame in range(temp.shape[0]):
                Timeslice = temp[frame]
                Targets = Ntargets[frame]
                
                idx = 0
                selection = np.array([])
                sensornum = np.array([])
                df_temp = pd.DataFrame()
                for target in Targets:

                    if(target > 0):
                        
                        selection = np.append(selection,(Timeslice[start_idx[idx]:start_idx[idx] + target]))
                        sensornum = np.append(sensornum,[idx] * len(Timeslice[start_idx[idx]:start_idx[idx] + target]))

                    idx = idx + 1
                df_temp[key]      = selection
                
                
                df_temp['Sensor'] = sensornum
                df_temp['Frame']  = [frame] * len(selection)
                df_allframes = pd.concat([df_allframes, df_temp])
            df[key] = df_allframes[key]
            df['Sensor'] = df_allframes['Sensor']  #it is copied each time, couldnt find a better way specially when ambiguous target struct is being processed...
            df['Frame'] = df_allframes['Frame']    #
           

    if(ambiguous_flag):
        return (df,df_ambiguous)
    else:
        
        return df
            
def Auxiliar_for_BLIS(data):
    df           = pd.DataFrame()
    df_allframes = pd.DataFrame()
    df_temp      = pd.DataFrame()
    ambiguous_flag = False

    for key in data.keys():
        
        

        df_allframes = pd.DataFrame()
        if(isinstance(data[key],dict)):   
            df_temp = Auxiliar_for_BLIS(data[key])
            df_temp = df_temp.drop(['Frame'], axis = 1)
            df_temp.columns = key + '_' + df_temp.columns
            if df.empty:
                df = df_temp
            else:
                df = pd.concat([df,df_temp],axis = 1)
        else:
            if len(data[key].shape) > 2:
                continue

            temp = data[key]
            temp2 = temp.reshape(1,temp.shape[0] * temp.shape[1])  #creates a list of array
            df[key] = temp2[0]
           
    frames = np.array([[i]*temp.shape[1] for i in range(temp.shape[0])])
    frames = frames.reshape(1, frames.shape[0] * frames.shape[1])
    df['Frame'] = frames[0]


    return df
            

        
def get_data(file):
    
    sdf = SdfReader(file)
    lib = sdf['/Resimulation/libWeGetASim']
    data = Sdf2DictConverter(lib)
    df_radarTargets = Dict2Df(data)
    
    id = lib[:][1]['s_SDC_OutputSignals_s_SDC_RadarTrackCollection_as_RadarTracks']['ul_ID']
    x  = lib[:][1]['s_SDC_OutputSignals_s_SDC_RadarTrackCollection_as_RadarTracks']['s_ObjectCenter_m']['r4_X']
    y  = lib[:][1]['s_SDC_OutputSignals_s_SDC_RadarTrackCollection_as_RadarTracks']['s_ObjectCenter_m']['r4_Y']
    vx = lib[:][1]['s_SDC_OutputSignals_s_SDC_RadarTrackCollection_as_RadarTracks']['s_Velocity_mps']['r4_X']
    vy = lib[:][1]['s_SDC_OutputSignals_s_SDC_RadarTrackCollection_as_RadarTracks']['s_Velocity_mps']['r4_Y']
    rx = lib[:][1]['s_SDC_OutputSignals_s_SDC_RadarTrackCollection_as_RadarTracks']['s_RefPoint_m']['r4_X']
    ry = lib[:][1]['s_SDC_OutputSignals_s_SDC_RadarTrackCollection_as_RadarTracks']['s_RefPoint_m']['r4_Y']
    h  = lib[:][1]['s_SDC_OutputSignals_s_SDC_RadarTrackCollection_as_RadarTracks']['r4_Heading_rad']
    sx = lib[:][1]['s_SDC_OutputSignals_s_SDC_RadarTrackCollection_as_RadarTracks']['s_Size_m']['r4_X'] 
    sy = lib[:][1]['s_SDC_OutputSignals_s_SDC_RadarTrackCollection_as_RadarTracks']['s_Size_m']['r4_Y']
    tr = lib[:][1]['s_SDC_OutputSignals_s_SDC_RadarTrackCollection_as_RadarTracks']['b_ValidTrack']
    atr= lib[:][1]['s_SDC_OutputSignals_s_SDC_RadarTrackCollection_as_RadarTracks']['b_Accepted']
    acc= lib[:][1]['s_SDC_OutputSignals_s_SDC_RadarTrackCollection_as_RadarTracks']['s_Accel_mps2']['r4_Y']
    
    
    time_d = lib[:][0]
    
    veh_v       = lib[:][1]['s_SDC_OutputSignals_s_SDC_EgoVehicleDynamics']['r4_Velocity_mps']
    veh_Yawrate = lib[:][1]['s_SDC_OutputSignals_s_SDC_EgoVehicleDynamics']['r4_YawRate_Cond_radps']
    
    time_d = np.repeat(time_d,len(x[0]))

    veh_v       = np.repeat(veh_v,len(vx[0]))
    veh_Yawrate = np.repeat(veh_Yawrate,len(vx[0]))
    
    
    df = pd.DataFrame({'Id':id.flatten(),'X':x.flatten(), 'Y':y.flatten(), 'TimeOrg':time_d,
                      'Vx':vx.flatten(), 'Vy':vy.flatten(), 'Heading':h.flatten(), 'Rx':rx.flatten(), 'Ry':ry.flatten()
                       ,'Sx':sx.flatten() , 'Sy':sy.flatten(), 'Tr':tr.flatten(), 'A_Tr': atr.flatten()
                       , 'VehicleVelocity': veh_v.flatten(), 'VehicleYawRate': veh_Yawrate.flatten()
                       , 'Acceleration_X': acc.flatten()
                      })


    df['Time']               = time_converter(df)
    df['Abstargetvelocity']  = velocity_over_ground(df)
    df['AbsVelocity']        = relative_velocity_values(df)
    df['VectDirection']      = travelling_direction_vector(df)
    
    df = df[(df["X"]!=0) & (df["Y"]!=0) & (df["Id"]!=0) & (df["Vx"]!=0)  & (df["Vy"]!=0) 
                & (df["Heading"]!=0) & (df["Rx"]!=0) & (df["Ry"]!=0) & (df["Sx"]!=0)& (df["Sy"]!=0) 
           ]  #&(df["Tr"]!=0) &(df["A_Tr"]!=0)   

         
    df_grps = df.groupby(['Id'])
    
    return df_grps, df

def get_files(path,ext):
    """get all files with extension ext in path 
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

def read_data(sdf_path):
    
    list_plots = []
    list_sdf_notracksfound = []

    #out_path = CreateFilePath(sdf_path)
    sdf_files = get_files(sdf_path, ".sdf")
    df_full_trackinfo = pd.DataFrame()

    for file in sdf_files:
        logger.info("Processing SDF: {}".format(Path(file).stem))
        #df_grps, df, Ids_list= get_trk_IDs(file)
        df = get_data(file)
    
#def Single_SDF_Process_RadarTargets(file):
#
#    sdf = SdfReader(file)
#    lib = sdf['/Resimulation/libWeGetASim']
#    data = Sdf2DictConverter(lib)
#    df_radarTargets = Dict2Df(data)
#
#    return df_radarTargets  


class SDF_RadarContent():


    def __Init__(self):
        self.sdf_path = ''
        self.sdf_DictionaryContent = {}
        self.sdf_DF = None
    
    def SDF2DF_Radar_Process(self,file):
        sdf = SdfReader(file)
        lib = sdf['/Resimulation/libWeGetASim']
        self.sdf_DictionaryContent = Sdf2DictConverter(lib)
        DF = self.Radar_TargetsDict2Df(self.sdf_DictionaryContent)
        #
        if(len(DF) == 2):
            self.RadarTargetsDF = DF[0]
            self.RadarAmbiguousTargets = DF[1]
        
        df_tracks = self.Radar_TracksDict2Df(self.sdf_DictionaryContent)
        self.RadarTracksDF = df_tracks

        self.BLISDF = self.Radar_BlisDict2Df(self.sdf_DictionaryContent)
        print('debug')
        
    
    def Radar_TargetsDict2Df(self,data):
        '''
            The function receives a dictionary that contains the full data for a given struct. The scope of this function is
            to collect all the elements for a given struct and convert it into a DataFrame, which it will contain the full info for all frames.

        ''' 
        if TARGET_COLLECTION_HEADER in data:
            logger.info("-- Start Conversion from Dictionary to DF for  {}".format(TARGET_COLLECTION_RADARTARGETS))
        
            start_idx = data[TARGET_COLLECTION_HEADER][TARGET_COLLECTION_HEADER_IDX]
            Ntargets  = data[TARGET_COLLECTION_HEADER][TARGET_COLLECTION_HEADER_NTARGETS]

            TotalFrames = start_idx.shape[0]

            df = Auxiliar_for_Dict2DF(data[TARGET_COLLECTION_RADARTARGETS],Ntargets)
            logger.info("-- Finished Conversion for {} DataFrame".format(TARGET_COLLECTION_RADARTARGETS))
            return df
        else:
            logger.warn(" Current SDF doesn't contain the following struct {}".format(TARGET_COLLECTION_HEADER))
            #logger.warn(" Current SDF doesn't contain the following struct {}".format(TARGET_COLLECTION_HEADER))
    
    def Radar_TracksDict2Df(self,data):
        '''
            The function receives a dictionary that contains the full data for a given struct. The scope of this function is
            to collect all the elements for a given struct and convert it into a DataFrame, which it will contain the full info for all frames.

        ''' 
        if TRACK_COLLECTION_RADAR in data:
            logger.info("-- Start Conversion from Dictionary to DF for  {}".format(TRACK_COLLECTION_RADAR))
            ID_tracks = data[TRACK_COLLECTION_RADAR][TRACK_ID]
            df_tracks = AuxiliarFunc_forRadarTracks(data[TRACK_COLLECTION_RADAR],ID_tracks)
            logger.info("-- Finished Conversion for {} DataFrame".format(TRACK_COLLECTION_RADAR))
            
            return df_tracks
        
        else:
            logger.warn(" Current SDF doesn't contain the following struct {}".format(TRACK_COLLECTION_RADAR))
    
    def Radar_BlisDict2Df(self,data):

            BLIS_COLLECTION
            logger.info("-- Start Conversion from Dictionary to DF for  {}".format(BLIS_COLLECTION))
            #ID_tracks = data[TRACK_COLLECTION_RADAR][TRACK_ID]
            df_blis = Auxiliar_for_BLIS(data[BLIS_COLLECTION]['as_BLIS_WarningStatus'])
            logger.info("-- Finished Conversion for {} DataFrame".format(BLIS_COLLECTION))
            return df_blis

    

            

def main():
    #sdf_path = r'.\\Data\\SDFs_run_2022_11_10-13_03_50\\'
    #read_data(sdf_path)

    sdfobj = SDF_RadarContent()
    #sdfobj.SDF2DF_Radar_Process(r'.\\Data\\TC_29\\TC_Gen7_029_0001_2022_08_15_132713_001.sdf')
    sdfobj.SDF2DF_Radar_Process(r'.\\Data\\SDFs_run_2023_01_27-14_24_11\\TC_Gen7_044_0001_2022_08_16_145450_001.sdf')






if __name__ == "__main__":
    main()

