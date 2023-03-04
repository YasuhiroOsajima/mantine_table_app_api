from setuptools import setup, find_packages


def _requires_from_file(filename):
    return open(filename).read().splitlines()


setup(
    name='mantine_table_app_api',
    version='0.1',
    license="MIT",
    description='API server for practice project for mantine table with next 13 app dir',  # noqa: E501
    url='https://github.com/YasuhiroOsajima/mantine_table_app_api.git',
    author='Yasuhiro Osajima',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=_requires_from_file('requirements.txt'),
    include_package_data=True,
)
