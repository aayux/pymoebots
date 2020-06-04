from setuptools import setup, find_packages
PACKAGES = find_packages()

opts = dict(name="pymoebots",
            maintainer="Aayush Yadav",
            description="Stochastic Algorithms simulator for the Amoebot Model",
            url="http://github.com/aayux/pymoebots",
            download_url="http://github.com/aayux/pymoebots",
            license=None,
            packages=PACKAGES)


if __name__ == '__main__':
    setup(**opts)
