# Stocker

## Reason

> This program is still under creation.

## Basics

- The **OS** of creation of Stocker project is _Windows 11_.
- The **Programming Language** and **Version** for data manipulation, management and ML is _Python 3.8_
- The **API** _yahoo_fin_ is being used to retrieve the **stock** data.

## Installation

```powershell
conda env create --file environment.yml
conda activate stocker
```

If there are more packages installed, update the `environment.yml` file with:

```powershell
conda env export --from-history > environment.yml
```

To export the packages to a `requirements.txt` file:

```powershell
pipreqs . --force
```

## Base branches

- [x] Master
- [x] Develop

## Base contributors

1. [**Nikolas Bakalis**](https://github.com/NikosBakalis)
2. [**Andreas Karatzas**](https://github.com/AndreasKaratzas)
