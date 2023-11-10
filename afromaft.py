import collections
import io
import zstandard
import json

from dataclasses import dataclass

import datasets


logger = datasets.logging.get_logger(__name__)

_DESCRIPTION =  """AfroMAFT Corpus: Language Adaptation Corpus for African languages."""
_TRAIN = "{language}/train.{language}.txt"
_DEV = "{language}/eval.{language}.txt"
_URL = "https://zenodo.org/records/6990611"

def _languages():
    """Create the sorted dictionary of language codes, and language names.
    Returns:
      The sorted dictionary as an instance of `collections.OrderedDict`.
    """
    langs = {
        "Afrikaans": "af",
        "Amharic": "am",
        "Arabic": "ar",
        "English": "en",
        "French": "fr",
        "Hausa": "ha",
        "Igbo": "ig",
        "Malagasy": "mg",
        "Chichewa": "ny",
        "Oromo": "om",
        "Nigerian Pidgin": "pcm",
        "Kinyarwanda": "rw",
        "Shona": "sn",
        "Somali": "so",
        "Southern Sotho": "st",
        "Swahili": "sw",
        "Xhosa": "xh",
        "Yoruba": "yo",
        "Zulu": "zu"
    }
    langs = {v: k for k, v in langs.items()}
    return collections.OrderedDict(sorted(langs.items()))

class afromaftConfig(datasets.BuilderConfig):
    """AfroMAFT corpus."""

    def __init__(self, language: str, **kwargs):
        """BuilderConfig for afromaft.
        Args:
            language (str): It has to contain 2-letter or 3-letter coded strings. For example: "se", "hu", "eml"
            **kwargs: Keyword arguments forwarded to super.
        """
        # Validate the language.
        if language not in _languages():
            raise ValueError("Invalid language: %s " % language)

        name = f"{language}"
        description = (
            f"Original {_languages()[language]} afromaft dataset from August 2022"
        )
        super(afromaftConfig, self).__init__(
            name=name, description=description, **kwargs
        )

        # Additional attributes
        self.language = language
        
class afromaft(datasets.GeneratorBasedBuilder):
    """AfroMAFT Corpus: Language Adaptation Corpus for African languages."""

    BUILDER_CONFIGS = [
        afromaftConfig(  # pylint: disable=g-complex-comprehension
            language=language,
        )
        for language in _languages()
    ]
    BUILDER_CONFIG_CLASS = afromaftConfig

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("int64"),
                    "text": datasets.Value("string"),
                    "meta": {
                        "language": datasets.Value("string"),
                    },
                }
            ),
            supervised_keys=None,
            homepage=_URL,
        )

    def _split_generators(self, dl_manager):
        language = self.config.language
        train, eval = _TRAIN.format(language=language), _DEV.format(language=language)
        doc_files = dl_manager.download([train, eval])
        logger.info("Downloaded files: %s", doc_files)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN, gen_kwargs={"file_path": doc_files[0]}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION, gen_kwargs={"file_path": doc_files[1]}
            ),
        ]
    
    def _generate_examples(self, file_path):
        logger.info("generating examples from = %s", file_path)
        id_ = 0
        with open(file_path, "rb") as fh:
            buffered_reader = io.BufferedReader(file_path)
            text_stream = io.TextIOWrapper(buffered_reader, encoding="utf-8")
            for line in text_stream:
                example = line.strip()
                yield id_, {"id": id_, "text": example, "meta": {"language": self.config.language}}
                id_ += 1