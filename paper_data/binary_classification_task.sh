CUDA_VISIBLE_DEVICES=0,1 python binary_classification.py --root ../data/tmp/512 --traincsv ../data/tmp/train_bin.csv --valcsv ../data/tmp/val_bin.csv --testcsv ../data/tmp/test_bin.csv --workers 4 --batch 32