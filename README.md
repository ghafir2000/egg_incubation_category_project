# Egg Incubation Category Project

This project is a computer vision project which involves studying the development process of chicken eggs within the incubation process. It classifies the egg into fertile and infertile categories using a model trained on a dataset of egg images.

## Dependencies

This project uses several scripts from the PyTorch Vision repository:

- engine.py: This script provides functions for training and evaluating the model.
- utils.py: This script contains utility functions for image transformations and metric calculations.
- coco_utils.py: This script helps in loading the COCO dataset and converting annotations for the model.
- coco_eval.py: This script is used for evaluating the model on the COCO dataset.
- transforms.py: This script is used for applying transformations to the images and targets before feeding them to the model.

These scripts are used under the terms of their license.

## Original Notebook

The original code for this project is in this [notebook](https://colab.research.google.com/github/pytorch/tutorials/blob/gh-pages/_downloads/4a542c9f39bedbfe7de5061767181d36/torchvision_tutorial.ipynb)
This notebook is used under the terms of its license. The code in the notebook was heavily modified and additional functions were added for the specific needs of this project.

## Dataset

The dataset used in this project is stored in the `dataset(v2)` directory. The `dataset_masks` directory contains binary masks of the corresponding images. One JSON file is used for validation and another is used for training and testing. Roboflow augmentations were used to generate more images to balance the dataset.

## Results

This project yielded a model with a 96% Average Precision (AP) and 97% Average Recall (AR) over a restriction of 0.75 Intersection over Union (IoU). These results are exceptionally good.

## License

This project is licensed under the GPL license.

## Acknowledgments

- Thanks to the PyTorch team for their vision scripts.
- Thanks to the authors of the original PyTorch tutorial notebook.
- Thanks to Roboflow for their image augmentations.
