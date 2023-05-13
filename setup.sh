#!/bin/bash

curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -o Miniconda3-latest-Linux-x86_64.sh
chmod -v +x Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh

rm Miniconda3-latest-Linux-x86_64.sh

conda remove --name shape-e --all
conda env create -f ./env/environment.yml

git clone https://github.com/openai/shap-e
cd shap-e
pip install -e .

echo "setup done"
echo "run conda activate shape-e to activate the environment"
echo "then run python start.py to start the application"
echo "greetings - Lukas"