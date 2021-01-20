from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='cpf',
  version='2.1',
  description='Gera e checa CPFs de acordo com o padrão brasileiro.',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='pedrokp',
  author_email='pedrokp@protonmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='cpf', 
  packages=find_packages(),
  install_requires=[''] 
)