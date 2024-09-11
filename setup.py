from setuptools import setup, find_packages

setup(
    name='WSI2tif for dummies',
    version='0.1.0',
    description='Easy to use WSI2tif for all those coding-elite wannabes.',
    author='Valentina Matos',
    url='https://github.com/Valentinamatos/CODA_python',
    packages=find_packages(),
    install_requires=[
        'numpy==1.23.5',
        'pillow==10.4.0',
        'setuptools==72.1.0',
        'openslide-python==1.3.1',
        'jupyter==1.1.1'
    ],
    package_data={
        '': ['*.ipynb', '*.qss'],
    },
    classifiers=[
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.9',
)