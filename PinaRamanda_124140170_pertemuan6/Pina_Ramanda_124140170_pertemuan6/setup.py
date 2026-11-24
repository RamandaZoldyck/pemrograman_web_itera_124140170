import os

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    README = f.read()

requires = [
    'alembic',
    'plaster_pastedeploy',
    'psycopg2-binary',
    'pyramid',
    'pyramid_debugtoolbar',
    'pyramid_jinja2',
    'pyramid_retry',
    'pyramid_tm',
    # SQLAlchemy 2.1+ memakai driver psycopg (v3) untuk URL postgresql://,
    # sedangkan proyek ini memakai psycopg2.
    'SQLAlchemy<2.1',
    'setuptools<81',
    'transaction',
    'waitress',
    'zope.sqlalchemy',
]

tests_require = [
    'pytest',
    'pytest-cov',
    'WebTest',
]

setup(
    name='pyramid_mahasiswa',
    version='0.0',
    description='Aplikasi CRUD Mahasiswa dan Matakuliah dengan Pyramid',
    long_description=README,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    author='Pina Ramanda',
    keywords='web pyramid pylons',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'testing': tests_require,
    },
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = pyramid_mahasiswa:main',
        ],
        'console_scripts': [
            'initialize_pyramid_mahasiswa_db='
            'pyramid_mahasiswa.scripts.initialize_db:main',
        ],
    },
)
