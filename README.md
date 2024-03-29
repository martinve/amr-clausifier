AMR annotation pipeline is a collection of scripts that takes text as input and returns text annotated with additional information extracted from AMR.

The system consists of the following primary components:
- AMR parser.
- Propbank reader. 
- Information Extractor
- AMR aligner
- Annotator


# Installation Instructions

## Set up software

It is recommended to create a virtual environment first: `python -m venv ./env/amr` and `source ./env/amr/bin/activate`

Clone the repository `git clone git@github.com:martinve/amr-clausifier.git`

Install the requirements `cd amr-clausifier && pip install -r requirements txt`





## Setting up AMR parsing

### Installing the Model

Install the AMR parse model. It is possible to use the models from AMRLib Models project `https://github.com/bjascob/amrlib-models`. We have used `parse_t5`, `parse_xfm_bart_base` and `parse_xfm_bart_large` in our previous experiments. 

As none of the models provided by AMRLib support wikification, we have trained `bart-large` model on wikified AMR 3.0 LDC corpus (https://catalog.ldc.upenn.edu/LDC2020T02) 

The model is available from https://cs.taltech.ee/staff/martin.verrev/model_parse_xfm_bart_large_wiki-v1_0_0.tgz

```
cd amr_clausifier/amr_parser/models/model_stog`
wget https://cs.taltech.ee/staff/martin.verrev/model_parse_xfm_bart_large_wiki-v1_0_0.tgz
tar zxvf model_parse_xfm_bart_large_wiki-v1_0_0.tgz
```


## Adding propbank 3.4 support

As only Propbank 1.0 is used natively with NLTK package, we need to add 
Propbank 3.4 support manually.

First step is to find the NLTK data path (default: `~/nltk_data`)

```
python 
>> import nltk
>> print(nltk.data.path[0])
```

Clone propbank version 3.4 under NLTK data:

```
cd <nltk.data.path>/corpora
git clone git@github.com:propbank/propbank-frames.git propbank-3.4
```

**Note:** You need to remove duplicate tag `</example>` from line 5684 from 
file `AMR-UMR-91-rolesets.xml` until the pull request https://github.
com/propbank/propbank-frames/pull/17/commits
/7ea8ab156f4213a39cdb2cc2285f65868744afbf has been merged to main branch of 
https://github.com/propbank/propbank-frames repository


## Adding additional language resources

Additional language resources are needed for postprocessing text:

```
python -m spacy download en_core_web_sm

python 
>> import stanza
>> stanza.download("en")
```



# Running the pipeline 

To run the pipeline first start the AMR server.

AMR parse server must be started under `amr_parser` directory:

```a
cd amr_parser
./amrserver.py
```

### Calling the application

To call the CLI application, run `extract_info.py` with passage provided as arguments, e.g. 

`./extract_info.py Titanic sank in the Atlantic.`




