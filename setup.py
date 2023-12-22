from setuptools import setup

setup(name='lipgart-adas-editor',
      version='0.1.0',
      description='',
      url='https://github.com/Lipgart/adas-editor',
      author='Maxim Gomozov',
      author_email='maximgomozoff@gmail.com',
      packages=[
            'adas',
            'adas.editor'
      ],
      namespace_packages=['adas'],
      scripts=[
            'bin/adas-editor'
      ],
      install_requires=[
            'lipgart-adas-service',
            'pyside6'
      ],
      package_data={},
      zip_safe=False)
