from setuptools import setup, find_packages

setup(
    name='gridfinity_plate_generator',
    version='0.1.0',
    description='Gridfinity Plate Generator',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Jakob Guldberg Aaes',
    author_email='jakob1379@gmail.com',
    url='https://github.com/jakob1379/gridfinity-plate-generator',
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
    ],
    packages=find_packages(),  # Replace with your package's name
    install_requires=[
        'click>=8.1.7,<9.0',
        'typer>=0.9.0,<1.0',
        'cadquery==2.3.1',
        'streamlit>=1.26.0,<2.0',
        'numpy-stl>=3.0.1,<4.0',
        'plotly>=5.16.1,<6.0',
        'python-dotenv>=1.0.0,<2.0',
    ],
    extras_require={
        'dev': [
            'Pygments>=2.10.0',
            'black>=21.10b0',
            'coverage[toml]>=6.2',
            'darglint>=1.8.1',
            'flake8>=4.0.1',
            # Add your other dev dependencies here
        ]
    },
    entry_points={
        'console_scripts': [
            'gridfinity-generator=gridfinity_plate_generator.__main__:app',
        ],
    },
    license='MIT',
)
