# flask-wtforms-template

# Quickstart
## Install Dependencies

```
pip install -r requirements.txt
cd src
python app.py
```

## HOW-TO: Add or Update Translations
### Extract text strings from our HTML templates and .py files

```
pybabel extract -F babel.cfg -o messages.pot .
```
It creates a messages.pot file

### Then initialise language translation files, it will create a .po file, here for French (fr)

```
pybabel init -i messages.pot -d translations -l fr
```

Note: if you want to later update the .po file after creating a new messages.pot file

```
pybabel update -d translations -i messages.pot -l fr

```

### Translate the strings

Then manually translate all the **msgid** entries in the .po file as **msgstr**

### Compile the .po file to a .mo file 

```
pybabel compile -d translations
```