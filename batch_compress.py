from tfci import *
import glob
import os
from tqdm import tqdm
import time


img_dir = 'images'
oriimg_path_list = glob.glob(os.path.join(img_dir, '*.*'))
output_file_base = 'output'
reconstruct_file_base = 'reconstruct'

'''
model_list = ['b2018-leaky_relu-128-%d'%i for i in range(1, 4+1)]
model_list.extend(['b2018-leaky_relu-192-%d'%i for i in range(1, 4+1)])
model_list.extend(['b2018-gdn-128-%d'%i for i in range(1, 4+1)])
model_list.extend(['b2018-gdn-192-%d'%i for i in range(1, 4+1)])

model_list.extend(['bmshj2018-factorized-mse-%d'%i for i in range(1, 8+1)])
model_list.extend(['bmshj2018-factorized-msssim-%d'%i for i in range(1, 8+1)])
model_list.extend(['bmshj2018-hyperprior-mse-%d'%i for i in range(1, 8+1)])
model_list.extend(['bmshj2018-hyperprior-msssim-%d'%i for i in range(1, 8+1)])

model_list.extend(['mbt2018-mean-mse-%d'%i for i in range(1, 8+1)])
model_list.extend(['mbt2018-mean-msssim-%d'%i for i in range(1, 8+1)])
'''
model_list = ['hific-lo', 'hific-mi', 'hific-hi']
w_f = open('compress_time_log.txt', 'a')

for model in model_list:
    print("processing %s"%model)

    output_dir = os.path.join(output_file_base, model)
    reconst_dir = os.path.join(reconstruct_file_base, model)
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    if not os.path.isdir(reconst_dir):
        os.makedirs(reconst_dir)

    # compress
    compress_time = 0
    decompress_time = 0

    s_t = time.time()

    print("compressing...")
    for oriimg_path in tqdm(oriimg_path_list):
        name = os.path.basename(oriimg_path).split('.')[0]

        output_path = os.path.join(output_dir, name+'.tfci')

        compress(model, oriimg_path, output_path)
        
        #reconstruct_path = os.path.join(reconst_dir, os.path.basename(oriimg_path))

        #decompress(output_path, reconstruct_path)

    compression_duration = time.time() - s_t


    stream_path_list = glob.glob(os.path.join(output_dir, '*.*'))
    print(stream_path_list)
    s_t = time.time()

    print("decompressing...")
    for stream_path in tqdm(stream_path_list):
        reconstruct_path = os.path.join(reconst_dir, os.path.basename(stream_path).split('.')[0]+'.png')
        print(stream_path, reconstruct_path)
        decompress(stream_path, reconstruct_path)

    decompression_duration = time.time() - s_t

    w_f.write('%s: average compress_time:%.4f, average decompress_time:%.4f\n'%(model, compression_duration/len(oriimg_path_list), decompression_duration/len(oriimg_path_list)))



