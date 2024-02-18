
# DoSA: (Do)cument (S)pecific Automated Annotations

we are proposing an active learning based automated annotation system DoSA (Document Specific Automated Annotations), where initials annotations are given to train a model which can be later be improved with more number of annotations. But rather than involving user at initial stage of manual annotations, we are proposing a novel approach of automatic annotations and using the model feedback in generating new annotations. 

This repo has been created to work the paper:

[DoSA : A System to Accelerate Annotations on Business Documents with Human-in-the-Loop](https://aclanthology.org/2022.dash-1.4/) Neelesh K Shukla, Msp Raja, Raghu C Katikeri, Amit Vaid; In Proceedings of the Fourth Workshop on Data Science with Human-in-the-Loop (Language Advances), pages 23–27, Abu Dhabi, United Arab Emirates (Hybrid).


## Citing
Our work can be cited using:
```
@inproceedings{shukla-etal-2022-dosa,
    title = "{D}o{SA} : A System to Accelerate Annotations on Business Documents with Human-in-the-Loop",
    author = "Shukla, Neelesh  and
      Raja, Msp  and
      Katikeri, Raghu  and
      Vaid, Amit",
    editor = "Dragut, Eduard  and
      Li, Yunyao  and
      Popa, Lucian  and
      Vucetic, Slobodan  and
      Srivastava, Shashank",
    booktitle = "Proceedings of the Fourth Workshop on Data Science with Human-in-the-Loop (Language Advances)",
    month = dec,
    year = "2022",
    address = "Abu Dhabi, United Arab Emirates (Hybrid)",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2022.dash-1.4",
    pages = "23--27",
    abstract = "Business documents come in a variety of structures, formats and information needs which makes information extraction a challenging task. Due to these variations, having a document generic model which can work well across all types of documents for all the use cases seems far-fetched. For document-specific models, we would need customized document-specific labels. We introduce DoSA (Document Specific Automated Annotations), which helps annotators in generating initial annotations automatically using our novel bootstrap approach by leveraging document generic datasets and models. These initial annotations can further be reviewed by a human for correctness. An initial document-specific model can be trained and its inference can be used as feedback for generating more automated annotations. These automated annotations can be reviewed by humanin-the-loop for the correctness and a new improved model can be trained using the current model as pre-trained model before going for the next iteration. In this paper, our scope is limited to Form like documents due to limited availability of generic annotated datasets, but this idea can be extended to a variety of other documents as more datasets are built. An opensource ready-to-use implementation is made available on GitHub.",
}

```

## Software Dependency

DoSA uses tesseract as OCR Engine. Please install it and set the path before running this system

- On MacOS
```
brew install tesseract
```

- On Windows
Download and install [tesseract](https://sourceforge.net/projects/tesseract-ocr-alt/files/) and add to the path

- On Unix/Linux
```
sudo apt-get install tesseract
```

## python package dependncies

```
pip install -r requirements.txt
```

## Generating annotation image

```
python generate_annotations.py -i <image_file>
```


Example:

```
python generate_annotations.py -i examples/82092117.png
```
