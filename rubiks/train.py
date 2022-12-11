from rubiks.lib.utils.args import parse_args
from rubiks.lib.utils.model_utils import gen_model
from rubiks.lib.cubeset import CubeDataset
from torch.utils.data import DataLoader
import pytorch_lightning as pl


def gen_dataset(args):
    dataset = CubeDataset()
    loader = DataLoader(dataset,
                        batch_size=args.batch_size,
                        num_workers=args.num_workers)
    return loader

def main():
    args = parse_args()
    model = gen_model(args)
    trainer = pl.Trainer(
        accelerator="gpu" if args.gpu else "cpu",
        auto_scale_batch_size=True,
        enable_checkpointing=True,
        default_root_dir="rubiks/logs",
        devices=args.gpu_device,
        max_epochs=args.stop_epoch
    )
    dataset = gen_dataset(args)
    trainer.fit(model, dataset, dataset)


if __name__ == "__main__":
    main()
