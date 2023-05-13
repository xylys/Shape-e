#!/bin/bash

if [ "$(uname)" == "Darwin" ]; then
    curl https://repo.anaconda.com/miniconda/Miniconda3-py310_23.3.1-0-MacOSX-x86_64.sh -o Miniconda3-latest-Linux-x86_64.sh
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -o Miniconda3-latest-Linux-x86_64.sh
fi


chmod -v +x Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda

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