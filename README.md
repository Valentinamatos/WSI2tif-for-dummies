# 🖼️ WSI2tif

**WSI2tif** is a user-friendly Python tool designed to effortlessly convert Whole Slide Images (WSIs) into standard `.tif` format. Ideal for researchers and image analysts working with histopathological slides.

---

## 🚀 Quick Installation Guide

Follow the steps below to get started:

### 1️⃣ Install Miniconda

First, install [Miniconda](https://docs.anaconda.com/miniconda/), a lightweight distribution of Conda.  

---

### 2️⃣ Create and Activate Your Conda Environment

Open your terminal or command prompt and run the following commands:

```bash
   conda create -n WSI2tif python=3.9.19
   conda activate WSI2tif
```

---

### 3️⃣ Install WSI2tif

Install the WSI2tif package using `pip`:

```bash
  pip install -e git+https://github.com/Valentinamatos/WSI2tif-for-dummies.git#egg=WSI2tif_for_dummies
```

🧰 **Note**: If you do not have Git installed, download it [here](https://git-scm.com/downloads/win).  
💡 *After installing Git, restart your IDE or terminal to apply the changes.*

---

## After Installing: Run the `WSI2tif.ipynb` Jupyter Notebook

### ✅ Run the Following Cells in the Notebook

1. **Import the module**

```python
from base import *
```

2. **Define Input Parameters**

```python
# Path to the folder containing the WSI files
path = 'put the location to your path here'

# Desired output resolutions
# Use this reference: 8µm = 1.25x, 4µm = 2.5x, 2µm = 5x, 1µm = 10x, 0.5µm = 20x, 0.25µm = 40x
resolutions = ['10x', '5x', '1x']

# Corresponding microns per pixel values
umpix_list = [1, 2, 8]
```

3. **Run the Conversion**

```python
WSI2tif(path, resolutions, umpix_list)
```