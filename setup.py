from setuptools import setup, find_packages

setup(
    name='SSI',
    version='1.0',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask', 'bokeh', 'pandas', 'numpy',
                      'Flask-SQLAlchemy', 'psycopg2', 'uwsgi']
)
