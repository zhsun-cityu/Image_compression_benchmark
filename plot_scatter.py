import os, glob
import csv
# import plotly.plotly as py
import plotly.graph_objs as go

# import plotly.express as px

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--dataset', type=str, default='KODAK_PNG')
parser.add_argument('--ref_image_dir', type=str, default='..\\KODAK_PNG')
parser.add_argument('--metric_dir', type=str, default='.\\metric_data\\KODAK_CSV')
parser.add_argument('--metric_name', type=str, default='ssim')
parser.add_argument('--output_dir', type=str, default='.\\metric_data')
args = parser.parse_args()

psnr_index=6
ssim_index=7
if args.metric_name=='psnr':
    m_index = psnr_index
    x_range = [0, 40]
    y_range = [20, 40]

if args.metric_name=='ssim':
    m_index = ssim_index
    x_range = [0, 20]
    y_range = [0.6, 1]

dataset=args.dataset
ref_image_dir = args.ref_image_dir
metric_dir= args.metric_dir
output_dir=args.output_dir
if not os.path.isdir(output_dir):
    os.makedirs(output_dir)

metric_path_list = glob.glob(os.path.join(metric_dir, dataset+'*.csv'))
refimg_path_list = glob.glob(os.path.join(ref_image_dir, '*.*'))


for refimg_path in refimg_path_list:
    refimg_name = os.path.basename(refimg_path)
    refimg_prefix = os.path.splitext(refimg_path)

    print(refimg_name)
    # ref_dict={}
    data = []

    for metric_path in metric_path_list:
        print(metric_path)
        codec = os.path.basename(metric_path).split('_')[-1].split('.')[0]
        csv_reader=csv.reader(open(metric_path, 'r'))
        bitrate_list = []
        metric_list = []
        for row in csv_reader:
            if refimg_name in row:
                bitrate_list.append(int(row[4]))
                metric_list.append(float(row[m_index]))

        bitrate_list.sort()
        metric_list.sort()
        trace = go.Scatter(
            x=bitrate_list, 
            y=metric_list, 
            mode='lines+markers',
            name=codec
            )
        data.append(trace)

    layout=go.Layout(
        title=refimg_name, width=800, height=640, 
        xaxis = dict(
            nticks = 10,
            range=x_range, 
            title = "Bitrate(kb)"),
        yaxis = dict(
            range=y_range, 
            title = args.metric_name
        ),
        )
    fig=go.Figure(data=data, layout=layout)
    output_path = os.path.join(output_dir, refimg_name)
    # py.image.save_as(fig, filename=output_path)
    fig.write_image(output_path)
    # exit()