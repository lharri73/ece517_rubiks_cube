from argparse import ArgumentParser
import multiprocessing

def get_cpu_count():
    cpu_count = multiprocessing.cpu_count()
    if cpu_count < 2:
        cpu_count = 2
    return int(cpu_count-1)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--batch_size', type=int, default=32)
    parser.add_argument('--num_workers', type=int, default=get_cpu_count())
    parser.add_argument('--gpu', action='store_true', default=False)
    parser.add_argument('--gpu_devices', type=str, default="0")
    parser.add_argument('--lr', type=float, default=0.001)
    parser.add_argument('--stop_epoch', type=int, default=1000)
    parser.add_argument('--train_size', type=int, default=1000)
    parser.add_argument('--val_size', type=int, default=256)

    args = parser.parse_args()

    if not args.gpu and args.gpu_devices != "0":
        raise ValueError("changed gpu_device, but gpu training not enabled...did you want to train with GPUs?")

    args.gpu_devices = [int(x) for x in args.gpu_devices.split(",")]

    return args
