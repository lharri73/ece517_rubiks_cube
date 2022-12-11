from rubiks.lib.models.resnet_ish import ResnetModel
from rubiks.lib.consts import actionDict


def gen_model(cfg):
    model = ResnetModel(3*3*6, 1, cfg)
    return model
