# CLIC code.

> CLIC: http://www.compression.cc/challenge/

linux

### CODEC table

| Classic/Commercial codec |        |                                                              |                                          |
| ------------------------ | ------ | ------------------------------------------------------------ | ---------------------------------------- |
| Codec                    | status | Implement method                                             | Note                                     |
| JPEG                     | Done   | Python opencv lib                                            |                                          |
| JPEG2000                 | Done   | ImageMagick(convert)                                         |                                          |
| WebP                     | Done   | Python opencv lib                                            |                                          |
| HEVC                     | Done   | [HM-16.9](https://hevc.hhi.fraunhofer.de/svn/svn_HEVCSoftware/tags/HM-16.9/) |                                          |
| HEVC-JEM                 | Done   | HM-16.6-JEM-7.1                                              |                                          |
| BGP                      | -      | -                                                            |                                          |
| Learning based codec     |        |                                                              |                                          |
| Codec                    | status | Implement method                                             | Note                                     |
| TF-RNN                   | Done   | [Tensorflow example](https://github.com/tensorflow/models/tree/master/research/compression) |                                          |
| CWIC                     | -      | 1703.10553 [Github code](https://github.com/limuhit/ImageCompression) | Miss caffe specific layer implementation |
| SPIC                     | -      | 1612.08712 [Github code](https://github.com/iamaaditya/image-compression-cnn) | Content based, not recommend             |

## Quick start (setup benchmark for KODAK dataset)

### Compress Images

- Prepare dataset,(e.g. KODAK), put it under the ***./dataset\*** directory

- run `bash jpeg_compression.sh KODAK`, `bash jpeg2000_compression.sh KODAK`, `bash webp_compression.sh KODAK`, to compress KODAK dataset with ***jpeg\***, ***jpeg2000\*** and ***webp\*** codec seprately.

- Before we use

   

  *hevc*

   

  and

   

  *hevc-jem*

   

  codec, we have to transefer original image file into YUV file.

  - `cd ./utils/yuvtools`

  - ```
    matlab -nodesktop -nodisplay
    ```

    - MATLAB command:
    - `rgb_dir='../../dataset/KODAK';yuv_dir='../../datast/KODAK_YUV';ext='png'`
    - run `scrirgb2yuv`, all *png* file in *rgbdir* will be save into *yuvdir* as .yuv file

- `cd ../..`, run `bash hevc_compress.sh ./dataset/KODAK_YUV ./compressed_set/KODAK/hevc ./compressed_set/KODAK/hevc_result` ***and\*** `bash hevc-jem_compress.sh ./dataset/KODAK_YUV ./compressed_set/KODAK/jem-hevc ./compressed_set/KODAK/jem-hevc_result`, to get ***hevc\*** and ***hevc-jem\*** compressed stream and results.

- With previous steps, we get jpeg, jpeg2000, webp, hevc and hevc-jem compressed streams/results

- For

   

  tfrnn codec

  , change directory into ./

  Train/tfnn

  compression/image_encoder, then run

   

  ```
  python compress.py --ori_dir=(path to your image dataset directory) --cps_dir=(path to save the reconstructed images)
  ```

  - since the stream size compressed by tfrnn codec is revelant to the iteration, so we dont have to save the compressed stream to calculate the stream size.

### Metric Evaluation

- run `python image_metric.py --ref_dir='./dataset/KODAK' --cps_dir='./compressed_set/KODAK/webp`, metric will be saved into ***KODAK_webp.csv\*** in the current folder.
- after you get all the KODAK_(codec).csv, move all the csv files into
  - `python plot_scatter.py --dataset='KODAK' --ref_image_dir='./dataset/KODAK' --metric_dir='./' --metric_name='Y-psnr' --metric_index=8 --output_dir='./metric_data/KODAK-YPSNR' --debug=True`, metric plot will be save into ./metric_data/KODAK-YPSNR
- To calculate BDBR and BDPSNR, run `python calc_bdbr_bdpsnr.py --dataset=KODAK --ref_image_dir='./dataset/KODAK' --metric_dir='./' --ref_codec='jpeg'`, make sure KODAK_(codec).csv is under **./** directory. Codec Jpeg is default reference codec to compare with.

## Scripts Instructions

#### compress_image.py

- --input_dir

  - original images directory.

- --codec

  :

  - support jpeg, jpeg2000, webp

- --output_dir

  :

  - All compresed streams will save to this directory.

- --quality

  - between 1 and 100 (worst and best quality)

- DEMO: `python compress_image.py --input_dir='/data/sunnycia/image_compression_challenge/dataset/KODAK' --output_dir='/data/sunnycia/image_compression_challenge/compressed_set/KODAK/webp' --quality=50 --codec='webp'`

#### hevc_compress.py

- --yuv_dir

  :

  - original yuv image file directory

- --hm_dir

  :

  - default `'_Train/HM-16.9'`

- --cfg_path

  :

  - default `'cfg/encoder_lowdelay_main_rext.cfg'`

- --qp

  :

  - 0~50, best to worst

- --yuvformat

  :

  - input yuv file format, 420 or 444.

- DEMO: `python hevc_compress.py --yuv_dir='/data/sunnycia/image_compression_challenge/dataset/KODAK_YUV' --result_dir='/data/sunnycia/image_compression_challenge/compressed_set/KODAK_YUV' --qp=50`

#### image_metric.py

- --ref_dir

  :

  - directory of original images

- --cps_dir

  - directory of compressed images(support jpeg, webp, jp2 stream file)
  - if use for hevc metric extraction, just leave this arg with space '_'

- --color_space

  - default 'YUV'
  - calculate BGR metric or YVU metric

- --output_path

  - Default None, the program will generate the path by itself
  - metric output path

- DEMO: `python image_metric.py --ref_dir='/data/sunnycia/image_compression_challenge/dataset/KODAK_PNG' --cps_dir='/data/sunnycia/image_compression_challenge/compressed_set/KODAK/jpeg2000'`

#### plot_scatter.py

- --dataset
  - dataset name in the ./dataset directory, e.g. KODAK
- --ref*image*dir
  - original image directory
- --metric_dir
  - default ./
  - directory for the csv metric files, e.g
- --metric_name
  - default 'psnr'
  - metric name in plot yaxis.
- --metric_index
  - default 8
  - the col index in the csv file
  - 8-> y-psnr, 9->u-psnr, 10->v-psnr, 11->yuv-psnr
- --output_dir
  - default 'metric_data'
  - output directory of plot
- --debug
  - default False
  - Since the plot lib ***plotly\*** only permit saving 100 figs per day, so set debug=True in case you get a bad plot result.
- DEMO: `python plot_scatter.py --dataset='KODAK' --ref_image_dir='/data/sunnycia/image_compression_challenge/dataset/KODAK' --metric_dir='./metric_data' --metric_name='Y-psnr' --metric_index=8 --output_dir='./metric_data/KODAK-YPSNR' --debug=True`

#### calc*bdbr*bdpsnr.py

- --dataset

  :

  - Dataset name

- --ref*image*dir

  :

  - original image directory

- --metric_dir

  :

  - default 'jpeg'
  - directory of csv metric file

- --output_dir

  :

  - default './metric_data'
  - bdbr and bdpsnr output file

- --ref_codec

  :

  - default 'jpeg'
  - which codec for reference to calculate bdbr & bdpsnr

- --metric_index

  :

  - default 8
  - psnr metric index

- DEMO:`python calc_bdbr_bdpsnr.py --dataset=KODAK --ref_image_dir='/data/sunnycia/image_compression_challenge/dataset/KODAK'`