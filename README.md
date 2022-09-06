
# DoSA: (Do)cument (S)pecific Automated Annotations

we are proposing an active learning based automated annotation system DoSA (Document Specific Automated Annotations), where initials annotations are given to train a model which can be later be improved with more number of annotations. But rather than involving user at initial stage of manual annotations, we are proposing a novel approach of automatic annotations and using the model feedback in generating new annotations. 

## Usage

DoSA uses tesseract as OCR Engine. Please install it and set the path before running this system

- On MacOS
```
brew install tesseract
```


```
1.pip install -r requirements.txt
2.python generate_annotations.py -i {image_file}
```
