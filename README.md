## prerequisites
- python <3.13,>=3.8
- dependency manager [python-poetry](https://python-poetry.org/)
- poppler
    ```bash
    brew install poppler
    ```
    NOTE: on windows please follow [here](https://pdf2image.readthedocs.io/en/latest/installation.html#windows), especially if you want to pack with pyinstaller

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
    ('/path/to/pdftoppm/binaries/*', 'poppler/'),
    ('/path/to/pptx/templates/default.pptx', 'pptx/templates')
]
```
NOTE: you may need to modify `def get_poppler_path()` to point to your own `pdftoppm` executable. You can use pyinstaller option `--onedir` to resolve problem "Where is my file?"


```bash
pyinstaller pdf2ppt.spec
```
