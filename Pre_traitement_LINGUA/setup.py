from setuptools import setup, find_packages

# Lisez le contenu de votre fichier README.md pour l'utiliser comme long_description
with open("README.md", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

setup(
    name="lingua_pre_processing",
    version="0.0.1",
    author="Pierre-Briac METAYER",
    author_email="pierre-briac.metayer--mariotti@umontreal.ca",
    url="",
    description="Bibliothèque pour préparer le texte pour les analyses",
    long_description=long_description,  # Utilisation de la description du fichier README.md
    long_description_content_type="text/markdown",  # Indication que le format est Markdown
    packages=find_packages(),
    install_requires=[
        "docx2txt>=0.8",
        "setuptools",
        "spacy>=3.7.1",
        "twine>=4.0.2"
    ],
    python_requires=">=3.11.5",
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
