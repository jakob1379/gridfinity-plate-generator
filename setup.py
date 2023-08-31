from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()
requirements = [r for r in requirements if not r.startswith('#')]

setup(
    name='gridfinity_plate_generator',
    version='0.1.0',
    description='Gridfinity Plate Generator',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Jakob Guldberg Aaes',
    author_email='jakob1379@gmail.com',
    package_dir={'': 'src'},
    url='https://github.com/jakob1379/gridfinity-plate-generator',
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
    ],
    packages=find_packages(),  # Replace with your package's name
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'gridfinity-generator=gridfinity_plate_generator.__main__:app',
        ],
    },
    license='MIT',
)
