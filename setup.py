from setuptools import setup

__version__ = (0, 1, 0)

setup(
    name="pydap_extras",
    version=".".join(str(d) for d in __version__),
    description="PCIC Pydap handlers and Responses for Python 3",
    install_requires=["pydap", "requests", "SQLAlchemy", "PyYAML"],
    packages=["pydap_extras"],
    zip_safe=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
    ],
    entry_points="""[pydap_extras.handlers]
                sql = pydap_extras.handlers.sql:SQLHandler
                csv = pydap_extras.handlers.csv:CSVHandler
                rsql = pydap_extras.handlers.pcic:RawPcicSqlHandler
                csql = pydap.handlers.pcic:ClimoPcicSqlHandler
                """,
)
