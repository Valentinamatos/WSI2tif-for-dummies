from setuptools import setup, find_packages

setup(
    name='WSI2tif_for_dummies',
    version='0.1.0',
    description='Easy to use WSI2tif for all those coding-elite wannabes.',
    author='Valentina Matos',
    url='https://github.com/Valentinamatos/WSI2tif-for-dummies',
    packages=find_packages(),
    # Update setup.py to avoid building from source
    install_requires=[
        'numpy>=1.23.5',
        'pillow==10.4.0',
        'setuptools==75.8.2',
        'openslide-python==1.3.1',
        'jupyter==1.1.1',
        'matplotlib==3.7.2',
        'openslide-bin'
    ],
    package_data={
        '': ['*.ipynb', '*.qss'],
    },
    classifiers=[
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.9',
)