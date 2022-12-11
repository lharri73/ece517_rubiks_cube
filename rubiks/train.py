from rubiks.lib.utils.args import parse_args
from rubiks.lib.utils.model_utils import gen_model
from rubiks.lib.cubeset import CubeDataset
from torch.utils.data import DataLoader
import lightning as pl


def gen_dataset(args):
    train_set = CubeDataset(args.train_size)
    val_set = CubeDataset(args.val_size)
    train_loader = DataLoader(train_set,
                        batch_size=args.batch_size,
                        num_workers=args.num_workers,
                        persistent_workers=True)

    val_loader = DataLoader(val_set,
                        batch_size=1,
                        num_workers=1,
                        persistent_workers=True)
    return train_loader, val_loader

def main():
    args = parse_args()
    model = gen_model(args)
    trainer = pl.Trainer(
        accelerator="gpu" if args.gpu else "cpu",
        auto_scale_batch_size='binsearch',
        enable_checkpointing=True,
        default_root_dir="rubiks/logs",
        devices=args.gpu_devices,
        max_epochs=args.stop_epoch,
        log_every_n_steps=5,
        resume_from_checkpoint="/home/lharri73/code/ece517_rubiks_cube/rubiks/rubiks/logs/lightning_logs/version_3/checkpoints/epoch=1048-step=33568.ckpt"
    )
    train, val = gen_dataset(args)
    trainer.fit(model, train, val)


if __name__ == "__main__":
    main()
