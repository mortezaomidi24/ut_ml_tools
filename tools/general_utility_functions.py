import time
import random
import torch
import numpy as np
from prettytable import PrettyTable

"""
##TODO: when load model there is no need to build model first ,
"""


def load_saved_model(bot ,opts):
    load_path = None
    loaded_logs = None
    if opts['LOAD_MODEL'] or opts['RESUME_MODEL_TRIAN']:
        bot.send_message(text="start loading model from telegram")
        loaded_logs = bot.download_model(log_file_id= opts['load_log_file_id'])
        loaded_logs['loaded_log_orginal'] = loaded_logs
        
        if opts['RESUME_MODEL_TRIAN']:
            bot.send_message(text="RESUME_MODEL_TRIAN , loading model setting")
            history = loaded_logs['history']
            start_epoch = int(list(loaded_logs['model_files'].keys())[-1]) - 1
            # opts.update(logs['opts'])
        ##?path of downloaded model and load it
        load_path = f"./loaded_model/{opts['model_type']}.tar"
    return load_path,loaded_logs


def seed_everything(seed):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


# count number of trainable parameter in model:
def count_parameters_simple(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)

def count_parameters(model):
    table = PrettyTable(["Modules", "Parameters"])
    total_params = 0
    for name, parameter in model.named_parameters():
        if not parameter.requires_grad: 
            continue
        param = parameter.numel()
        table.add_row([name, param])
        total_params+=param
    print(table)
    print(f"Total Trainable Params: {total_params}")
    return total_params