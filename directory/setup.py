import setuptools

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(name='directory',
version='0.1',
description='Testing installation of Package',
url='#',
author='Andreas Timoudas',
author_email='andreas.timoudas@gmail.com',
license='MIT',
packages=['directory'],
install_requires=requirements,
zip_safe=False)