# Stocker

## Reason

> This program is still under creation.

## Basics

- The **OS** of creation of Stocker project is _Windows 11_.
- The **Programming Language** and **Version** for data manipulation, management and ML is _Python 3.9_
- The **API** _yahoo_fin_ is being used to retrieve the **stock** data.

## Installation

```powershell
conda create -n stocker python=3.12 pip
pip install requirements.txt
```

If there are more packages installed, update the `environment.yml` file with:

```powershell
conda env export --from-history > environment.yml
```

To export the packages to a `requirements.txt` file:

```powershell
pipreqs . --force
```

If you want to build the environment from scratch, run the following:

```powershell
conda create -n stocker python=3.12 pip
pip install SQLAlchemy
pip install rich
pip install psycopg2-binary
pip install -U "ray[default]"
pip install gpustat
pip install tqdm
pip install yfinance
pip install yahooquery
pip install "modin[all]"
pip install yahoo_fin
```

## Base branches

- [x] Master
- [x] Develop

## Base contributors

1. [**Nikolas Bakalis**](https://github.com/NikosBakalis)
2. [**Andreas Karatzas**](https://github.com/AndreasKaratzas)
