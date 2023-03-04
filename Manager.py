import logging

logger = logging.getLogger(__name__)
FORMAT = "%(asctime)s [%(filename)s] [%(levelname)s] - %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.INFO)


import ExtractSDF 
import ReportSDF
import argparse


def main():

    """main function with arguments"""
    parser = argparse.ArgumentParser(description="Manager to extract sdfs and generate report")

    parser.add_argument("sim_mngr_path", help="Path to MOT.ppj File for Gogeta ", nargs = 1)
    parser.add_argument("sdf_input_path", help="Pass to save csv", nargs = 1)

    

    args = parser.parse_args()
    SimulationManager = args.sim_mngr_path[0]
    sdf_path          = args.sdf_input_path[0]

    logger.info("----------   Calling Extract SDF Script   ----------")
    ExtractSDF.CreateExportPath()
    ExtractSDF.read_sdfs(sdf_path, SimulationManager)
    resim_sdf_path = ExtractSDF.dst_path
    logger.info("----------   Calling REport Generation Script   ----------")
    ReportSDF.ReportGen(resim_sdf_path)




if __name__ == "__main__":
    main()