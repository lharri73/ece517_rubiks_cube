# Source from https://github.com/forestagostinelli/DeepCubeA/blob/38b8174d6b034871b6bea8686e45dc982cc1f04a/utils/pytorch_models.py
import torch
import torch.nn as nn
import torch.nn.functional as F
import lightning as pl
import time


class ResnetModel(pl.LightningModule):
    def __init__(self, state_dim: int, out_dim: int, cfg):
        super().__init__()
        self.one_hot_depth: int = 6
        h1_dim = 5000
        resnet_dim = 1000
        num_resnet_blocks = 4
        batch_norm = True

        self.state_dim: int = state_dim
        self.blocks = nn.ModuleList()
        self.num_resnet_blocks: int = num_resnet_blocks
        self.batch_norm = batch_norm
        self.cfg = cfg

        # first two hidden layers
        self.fc1 = nn.Linear(self.state_dim * self.one_hot_depth, h1_dim)

        self.bn1 = nn.BatchNorm1d(h1_dim)

        self.fc2 = nn.Linear(h1_dim, resnet_dim)

        self.bn2 = nn.BatchNorm1d(resnet_dim)

        # resnet blocks
        for block_num in range(self.num_resnet_blocks):
            res_fc1 = nn.Linear(resnet_dim, resnet_dim)
            res_bn1 = nn.BatchNorm1d(resnet_dim)
            res_fc2 = nn.Linear(resnet_dim, resnet_dim)
            res_bn2 = nn.BatchNorm1d(resnet_dim)
            self.blocks.append(nn.ModuleList([res_fc1, res_bn1, res_fc2, res_bn2]))


        # output
        self.fc_out = nn.Linear(resnet_dim, out_dim)

        #if cfg.gpu:
        #    self.blocks.cuda(cfg.gpu_device)
        #    self.fc1.cuda(cfg.gpu_device)
        #    if self.batch_norm:
        #        self.bn1.cuda(cfg.gpu_device)
        #        self.bn2.cuda(cfg.gpu_device)
        #    self.fc2.cuda(cfg.gpu_device)
        #    self.fc_out.cuda(cfg.gpu_device)

    def forward(self, states_nnet):
        x = states_nnet

        # preprocess input
        if self.one_hot_depth > 0:
            x = F.one_hot(x.long(), self.one_hot_depth)
            x = x.float()
            x = x.view(-1, self.state_dim * self.one_hot_depth)
        else:
            x = x.float()

        # first two hidden layers
        x = self.fc1(x)

        x = self.bn1(x)

        x = F.relu(x)
        x = self.fc2(x)
        x = self.bn2(x)

        x = F.relu(x)

        # resnet blocks
        for block_num in range(self.num_resnet_blocks):
            res_inp = x
            x = self.blocks[block_num][0](x)
            x = self.blocks[block_num][1](x)
            x = F.relu(x)
            x = self.blocks[block_num][2](x)
            x = self.blocks[block_num][3](x)

            x = F.relu(x + res_inp)

        # output
        x = self.fc_out(x)
        return x

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=self.cfg.lr)
        return optimizer

    def training_step(self, batch, batch_idx):
        x, y = batch
        y = y.reshape((-1, 1))
        tic=time.perf_counter()
        y_hat = self(x)
        toc = time.perf_counter()
        loss = F.mse_loss(y_hat, y)
        self.log('train_loss', loss)
        self.log('eval_time', toc-tic)
        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        y = y.reshape((-1,1))
        y_hat = self(x)
        loss = F.mse_loss(y_hat, y)
        self.log('val_loss', loss)
        return loss
