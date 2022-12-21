# ECE517 Rubik's Cube Solver

The project report is in [report.pdf](report.pdf).

## Setup Instructions

1. Clone Repository

```bash
git clone git@github.com:lharri73/ece517_rubiks_cube.git
cd ece517_rubiks_cube
```

2. Setup Repository

```bash
pip install -e .
```

3. Download the checkpoint from [here](https://drive.google.com/file/d/1rg5s-dZmf1IuQAvfhk1-kJ9uzz3QBOpW/view?usp=share_link)

4. Download the pre-computed twophase tables from [here](https://drive.google.com/file/d/1eS9JVfxasUEZx7evKnnozKCm4dzDJiUx/view?usp=share_link) and extract to the `data/twophase` directory

6. Run the solver to evaluate efficiency of Greedy solver vs A* solver

```bash
python rubiks/eval.py --gpu --checkpoint <path_to_checkpoint>
```
