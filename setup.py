from setuptools import find_packages, setup

install_requires = [
    "flask >= 1.1.2",
    "flask-cors >= 3.0.9",
    "requests >= 2.24.0",
    "pymongo >= 3.11.0",
]

extras_require = {"lint": ["black >= 20.8b1", "mypy >= 0.790", "pylint >= 2.6.0"]}

setup(
    name="runeterra-roulette-backend",
    author="Jay Stringer",
    version="0.0.1",
    maintainer="JayStringer",
    description="Backend for Runeterra Roulette Web Application",
    packages=find_packages(),
    platforms=["any"],
    install_requires=install_requires,
    extras_require=extras_require,
)
