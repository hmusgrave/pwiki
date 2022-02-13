import setuptools

def long_description():
    with open('README.md', 'r') as file:
        return file.read()

setuptools.setup(
    name='pwiki',
    version='0.0.1',
    author='Hans Musgrave',
    author_email='Hans.Musgrave@gmail.com',
    description='An OSRS price wiki client',
    long_description=long_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/hmusgrave/pwiki',
    packages = ['pwiki'],
    install_requires=[
        'aiolimit @ git+https://github.com/hmusgrave/aiolimit.git#egg=aiolimit',
        'httpx',
    ],
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)'
        'Operating System :: OS Independent',
        'Framework :: AsyncIO',
    ],
)
