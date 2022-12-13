#!/bin/bash
python train.py --gpu --stop_epoch=100000 --train_size 100000 --resume rubiks/logs/lightning_logs/version_9/checkpoints/epoch\=1104-step\=79703.ckpt --batch_size=32 --lr=0.0005