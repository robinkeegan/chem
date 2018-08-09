from setuptools import setup
import setuptools
setup(name='chem',
      version='0.1',
      description='Groundwater chemistry analysis',
      author='Robin Keegan-Treloar',
      author_email='robin_kt@outlook.com',
      url='https://github.com/robinkeegan/chem',
      license='MIT',
      packages=setuptools.find_packages(),
      zip_safe=False,
      install_requires=[
          "pandas >= 0.23.1",
          "numpy >= 1.14.5",
          "matplotlib >= 2.2.2",
          "scipy >= 1.1.0"
      ])
