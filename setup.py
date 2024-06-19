from setuptools import setup, find_packages

# Lisez le contenu de votre fichier README.md pour l'utiliser comme long_description
with open("README.md", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

setup(
    name="lingua_extraction",
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
        "lexicalrichness>=0.5.1",
        "more-itertools>=10.1.0",
        "nltk>=3.8.1",
        "numpy>=1.26.2",
        "openpyxl>=3.1.2",
        "pandas>=2.1.3",
        "scikit-learn>=1.3.2",  
        "sense2vec>=2.0.2",  
        "sentencepiece",
        "sentence-transformers>=2.2.2", 
        "setuptools",  
        "spacy>=3.7.2", 
        "spacy-sentence-bert>=0.1.2",  
        "statsmodels>=0.14.0",
        "torch>=2.1.1",
        "torchvision>=0.16.0",
        "transformers>=4.35.2",
        "twine>=4.0.2"
    ],
    python_requires=">=3.11.5",
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "text2variable = lingua_extraction.main:main",
        ]
    }
)
