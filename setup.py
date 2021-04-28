from setuptools import setup, find_packages

__version__ = (0, 1, 1)

reqs = [line.strip() for line in open("requirements.txt")]

setup(
    name="pydap_extras",
    version=".".join(str(d) for d in __version__),
    description="PCIC Pydap handlers and Responses for Python 3",
    install_requires=reqs,
    packages=find_packages(),
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
    entry_points="""[pydap.handler]
    sql = pydap_extras.handlers.sql:SQLHandler
    csv = pydap_extras.handlers.csv:CSVHandler
    rsql = pydap_extras.handlers.pcic:RawPcicSqlHandler
    csql = pydap.handlers.pcic:ClimoPcicSqlHandler
[pydap.response]
    nc = pydap_extras.responses.netcdf:NCResponse
    xlsx = pydap_extras.responses.xlsx:XLSXResponse
""",
)
