import os as _os

from distutils import core as _core
import setuptools as _setuptools


package = dict(
    repo="whatsapp-analyzer",
    name="wapp-analyzer",
    fullname="wapp.analyzer",
    depname="wapp-analyzer",
    pathname="wapp/analyzer",
    desc="Data Visulization app to visualise your Whatsapp data",
    author="Dineshkarthik Raveendran",
    email="dineshkarthik.r@gmail.com",
    classifiers=[
        "Development Status :: 2 - Beta",
        "Intended Audience :: Public",
        "Operating System :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
)

install_requires = [line for line in (line.strip() for line in """
    Flask==1.1.2
    Flask-Session==0.3.2
    numpy==1.19.0
    pandas==1.0.5
    python_dateutil==2.8.1
""".splitlines()) if line and not line.startswith('#')]


def setup():
    """ Main """

    packages = [package["fullname"]] + [
        "%s.%s" % (package["fullname"], item)
        for item in _setuptools.find_packages(package["pathname"])
    ]

    req = list(install_requires)
    if _os.path.isdir("setups"):

        def exec_(code, globs, locs):
            """ Exec helper """
            exec("exec(code, globs, locs)")

        for name in _os.listdir("setups"):
            if name.startswith(".") or not name.endswith(".py"):
                continue
            fname = _os.path.join("setups", name)
            global_vars, local_vars = {}, {}
            with open(fname) as fp:
                code = compile(fp.read(), fname, "exec")
                exec_(code, global_vars, local_vars)
            req.extend(local_vars.get("install_requires") or ())

        req = sorted(
            set(
                line
                for line in (line.strip() for line in req)
                if line and not line.startswith(package["depname"])
            )
        )

    _core.setup(
        author=package["author"],
        author_email=package["email"],
        classifiers=package["classifiers"],
        description=package["desc"],
        include_package_data=True,
        install_requires=req,
        name=package["depname"],
        packages=packages,
        url="https://github.com/dineshkarthik/%(repo)s" % package,
        version="0.2.1",
        zip_safe=False,
        entry_points={
            "console_scripts": [
                "wapp-analyzer=wapp.analyzer.cli:main"
            ]
        },
    )


if __name__ == "__main__":
    setup()
