from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="termichess",
    version="0.1.0",
    author="Krishna Sangeeth KS",
    author_email="kskrishnasangeeth@gmail.com",
    description="A chess game on your terminal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/whiletruelearn/termichess",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "termichess": ["assets/*"],
    },
    install_requires=[
        "textual==0.82.0",
        "pillow==10.3.0",
        "chess==1.11.0",
        "rich-pixels==3.0.1",
        "simpleaudio==1.0.4"
    ],
    entry_points={
        "console_scripts": [
            "termichess=termichess.__main__:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)