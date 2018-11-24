from setuptools import setup

import collectdgcs

setup(
    name = 'collectdgcs',
    version = collectdgcs.__version__,
    author = 'jeremy',
    author_email = 'jrmsayag@gmail.com',
    maintainer = 'jeremy',
    maintainer_email = 'jrmsayag@gmail.com',
    packages = [
        'collectdgcs'
    ],
    python_requires='>=3',
    install_requires = [
        'google-cloud-storage'
    ],
    entry_points = {
        'console_scripts': ['collectdgcs=collectdgcs.collectdgcs:main'],
    },
    description = 'CollectD plugin to fetch Google Cloud Storage statistics.',
    platforms = 'ALL',
)
