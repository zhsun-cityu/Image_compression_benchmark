import glob
import cv2
import sys
import csv
import numpy
import re
import sys
import scipy.misc
import subprocess
import os.path
sys.path.append('utils/video-quality')
import vifp
import ssim
import psnr
# import niqe
# import reco

from tqdm import tqdm
import matplotlib.pyplot as plt

import argparse



parser = argparse.ArgumentParser()
parser.add_argument('--ref_dir', type=str, default='..\\KODAK_PNG')
parser.add_argument('--stream_dir', type=str, default='..\\tfic_result\\compressed_stream_combined') ## the directory store the compressed steram file
parser.add_argument('--reconst_dir', type=str, default='..\\tfic_result\\reconstruct_combined') # the directory store the reconstructed png file

parser.add_argument('--output_base', type=str, default='metric_data\\KODAK_CSV')

args = parser.parse_args()
ref_dir = args.ref_dir
stream_dir = args.stream_dir
reconst_dir = args.reconst_dir
output_base = args.output_base
# if args.output_path is None:
#     output_path = os.path.basename(ref_dir)+'_'+os.path.basename(stream_dir)+'.csv'
# else:
#     output_path = args.output_path


# each model have different quality settings
 # model_list = ['b2018-leaky_relu-128-', 'b2018-leaky_relu-192-', 'b2018-gdn-128-', 'b2018-gdn-192-', 'bmshj2018-factorized-mse-', 'bmshj2018-factorized-msssim-', 'bmshj2018-hyperprior-mse-', 'bmshj2018-hyperprior-msssim-', 'mbt2018-mean-mse-', 'mbt2018-mean-msssim-']
# model_list =  ['b2018-gdn-192-%d' % (i+1) for i in range(4)]
# model_list = ['b2018-leaky_relu-128-%d'%i for i in range(1, 4+1)]
# model_list.extend(['b2018-leaky_relu-192-%d'%i for i in range(1, 4+1)])
# model_list.extend(['b2018-gdn-128-%d'%i for i in range(1, 4+1)])
# model_list.extend(['b2018-gdn-192-%d'%i for i in range(1, 4+1)])

# model_list.extend(['bmshj2018-factorized-mse-%d'%i for i in range(1, 8+1)])
# model_list.extend(['bmshj2018-factorized-msssim-%d'%i for i in range(1, 8+1)])
# model_list.extend(['bmshj2018-hyperprior-mse-%d'%i for i in range(1, 8+1)])
# model_list.extend(['bmshj2018-hyperprior-msssim-%d'%i for i in range(1, 8+1)])

# model_list.extend(['mbt2018-mean-mse-%d'%i for i in range(1, 8+1)])
# model_list.extend(['mbt2018-mean-msssim-%d'%i for i in range(1, 8+1)])
# model_list.extend(['hific-lo', 'hific-mi', 'hific-hi'])

model_list = os.listdir(stream_dir)




for model in model_list:
    # reco_values = []
    output_path = os.path.join(output_base, '%s_%s.csv'%(os.path.basename(ref_dir), model))
    w_f =open(output_path, 'w', newline='')
    csv_writer = csv.writer(w_f)
    csv_writer.writerow(['reference image', 'compress image', 'ref img shape', 'ref image size', 'cps stream size', 'compress ratio', 'psnr', 'ssim'])
    ref_path_list = glob.glob(os.path.join(ref_dir, '*.*'))

    for ref_path in tqdm(ref_path_list):
        size_values = []
        # vifp_values = []
        ssim_values = []
        psnr_values = []
        path_list = []
        ref_name = os.path.splitext(os.path.basename(ref_path))[0]

        
        # ref_img = scipy.misc.imread(ref_path, flatten=False, mode='RGB').astype(numpy.float32)#[:, :, :3]
        ref_img = cv2.imread(ref_path).astype(numpy.float32)
        # print type(ref_img), ref_img.shape, 
        ori_shape = ref_img.shape
        ori_size = 1
        for dim in ori_shape:
            ori_size = ori_size * dim
        ori_size = int(ori_size/1024)
        
        reconst_path_list = glob.glob(os.path.join(reconst_dir, model, ref_name+'*.*'))
        for reconst_path in reconst_path_list:
            # cps_img = scipy.misc.imread(cps_path, flatten=False, mode='RGB').astype(numpy.float32)
            # reconst_img = scipy.misc.imread(reconst_path, flatten=False, model='RGB').astype(numpy.float32)
            # cps_path = 
            name = os.path.splitext(os.path.basename(reconst_path))[0]
            cps_path = glob.glob(os.path.join(stream_dir, model, name+'*'))[0]
            stream_file_size = os.path.getsize(cps_path)


            reconst_img = cv2.imread(reconst_path).astype(numpy.float32)


            # print cps_img.shape #exit()
            path_list.append(reconst_path)
            size_values.append( int(stream_file_size/1024) ) ## kb
            # vifp_values.append( vifp.vifp_mscale(ref_img, cps_img) )
            ssim_values.append( ssim.ssim_exact(ref_img/255, reconst_img/255) )
            psnr_values.append( psnr.psnr(ref_img, reconst_img) )
            # reco_values.append( reco.reco(ref_img/255, cps_img/255) )


        # cps_path_list = glob.glob(os.path.join(stream_dir, model, ref_name+'*'))
        # # print ref_path
        # for cps_path in cps_path_list:
        #     file_size = os.path.getsize(cps_path)

        #     # reconst_path = os.path.join(reconst_dir, model, ref_name) ## have to be same format with reference image 
            

        # print size_values;exit()
        for i in range(len(size_values)):
            # csv_writer.writerow
            output_row=[os.path.basename(ref_path), os.path.basename(path_list[i]), str(ori_shape), str(ori_size), str(size_values[i]), str(float(ori_size)/size_values[i]), str(psnr_values[i]), str(ssim_values[i])]
            csv_writer.writerow(output_row)

    w_f.close()