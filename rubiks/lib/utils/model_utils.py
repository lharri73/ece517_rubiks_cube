from rubiks.lib.models.resnet_ish import ResnetModel
from rubiks.lib.ctg import calc_cost_to_go
from rubiks.lib.consts import actionDict

import torch


def gen_model(cfg):
    model = ResnetModel(3*3*6, 1, cfg)
    return model

def load_model(cfg):
    assert cfg.checkpoint is not None, "must provide path to checkpoint to load from. Refusing to run with random model. (use --checkpoint)"
    model = ResnetModel.load_from_checkpoint(cfg.checkpoint, cfg=cfg, state_dim=3*3*6, out_dim=1)
    return model

def get_next_action_model(model, env):
    actions = {action: 2048 for action in actionDict.keys()}
    for action in actionDict.keys():
        with env.inverse_protect(action):
            state = torch.tensor(env.state).flatten()
        result = model(state).cpu().detach().numpy()
        actions[action] = result
    return min(actions, key=actions.get)

def get_next_action_ctg(env):
    actions = {action: 2048 for action in actionDict.keys()}
    for action in actionDict.keys():
        with env.inverse_protect(action):
            result = calc_cost_to_go(env)
        actions[action] = result
    return min(actions, key=actions.get)