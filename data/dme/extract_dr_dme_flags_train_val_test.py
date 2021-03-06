import os
import pandas as pd
import numpy as np
import argparse
from glob import glob

from sklearn.cross_validation import train_test_split

def parse_args():
    parser = argparse.ArgumentParser(description='extract dr&dme flags')
    parser.add_argument('--root', required=True)
    parser.add_argument('--csvtrain', default='train_multi.csv')
    parser.add_argument('--csvval', default='val_multi.csv')
    parser.add_argument('--csvtest', default='test_multi.csv')
    parser.add_argument('--valratio', type=float, default=0.1)
    parser.add_argument('--testratio', type=float, default=0.2)

    return parser.parse_args()

args = parse_args()

print('====> args:')
print(args)

dme_path = os.path.join(args.root, 'dme')
assert os.path.isdir(dme_path)

# csv_file = os.path.join(args.root, args.csvfile)
csv_train = os.path.join(args.root, args.csvtrain)
csv_val = os.path.join(args.root, args.csvval)
csv_test = os.path.join(args.root, args.csvtest)

images_list = glob(os.path.join(dme_path, '*.jpg'))

images_list = [os.path.basename(img) for img in images_list]

# dr_level_list = [int(index.split('.')[0].split('_')[2]) for index in images_list]
# dme_level_list = [int(index.split('.')[0].split('_')[4]) for index in images_list]

print('raw images count is: {}'.format(len(images_list)))

images_list_filtered = []
dr_list_filtered = []
dme_list_filtered = []

for img in images_list:
    index = img.split('.')[0]
    dr_level = int(index.split('_')[2])
    dme_level = int(index.split('_')[4])
    if dr_level <= 1  and dme_level > 0:
        continue
    images_list_filtered.append(index)
    dr_list_filtered.append(dr_level)
    dme_list_filtered.append(dme_level)

referable_list = []

for i in range(len(images_list_filtered)):
    dr = dr_list_filtered[i]
    dme = dme_list_filtered[i]
    if dr >=2 and dme > 0:
        referable_list.append(1)
    else:
        referable_list.append(0)

assert len(images_list_filtered) == len(dr_list_filtered) == len(dme_list_filtered) == len(referable_list)

print('filtered images count is: {}'.format(len(images_list_filtered)))

data = np.column_stack((images_list_filtered, dr_list_filtered, dme_list_filtered, referable_list))

train_data, test_data = train_test_split(data, test_size=args.testratio)

train_data, val_data = train_test_split(train_data, test_size=args.valratio)

df = pd.DataFrame(data, columns=['image', 'dr_level', 'dme_level', 'totreat'])

train_df = pd.DataFrame(train_data, columns=['image', 'dr_level', 'dme_level', 'totreat'])
val_df = pd.DataFrame(val_data, columns=['image', 'dr_level', 'dme_level', 'totreat'])
test_df = pd.DataFrame(test_data, columns=['image', 'dr_level', 'dme_level', 'totreat'])

# df.to_csv(csv_file)
train_df.to_csv(csv_train)
val_df.to_csv(csv_val)
test_df.to_csv(csv_test)