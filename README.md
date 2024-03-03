## install poppler
[pdf2image doc](https://pdf2image.readthedocs.io/en/latest/installation.html)
```bash
brew install poppler
```
verify installation:
```bash
pdftoppm -h
```

## setup python env
```bash
poetry install
```


## packaging
prepare your own spec
```bash
pyinstaller --name=pdf2ppt --onefile main.py --noconsole
```
add additional dependencies and binaries to .spec file
```
datas=[
    ('/path/to/pdftoppm/binaries/*', 'pdftoppm'),
    ('/path/to/pptx/templates/default.pptx', 'pptx/templates')
]
```

run
```bash
pyinstaller pdf2ppt.spec
```
