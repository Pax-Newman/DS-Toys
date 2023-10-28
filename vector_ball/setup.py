from setuptools import setup, find_packages

setup(
    name="vector_ball",
    version="1.0.0",
    author="Pax Newman",
    author_email="pax.newman@email.com",
    description="A game of word vectors.",
    url="https://github.com/Pax-Newman/DS-Toys",
    license="MIT",
    install_requires=[
        "sentence_transformers",
        "typer",
        "questionary",
        "scipy",
    ],
    entry_points={
        "console_scripts": [
            "vectorball = vector_ball.main:app",
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
