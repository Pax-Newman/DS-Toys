from setuptools import setup, find_packages

setup(
    name="topic_clustering",
    version="1.0.0",
    author="Pax Newman",
    author_email="pax.newman@email.com",
    description="A cli tool and api for clustering documents by topic.",
    url="https://github.com/Pax-Newman/DS-Toys",
    license="MIT",
    install_requires=[
        "sentence_transformers",
        "numpy",
        "pyyaml",
        "typer",
        "pandas",
    ],
    entry_points={
        "console_scripts": [
            "topic_cluster = topic_clustering.main:app",
        ],
    },
    include_package_data=True,
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
