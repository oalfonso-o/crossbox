# Crossbox - App to handle reservations of Crossbox Palau

Some considerations:

- You need to install the python module in your environment:
```bash
pip install '.[dev]'
```


### Packaging
In order to mantain the repeatability we package the app using pip:
- Bump version in file setup.py (version='X.Y')
- Create the wheel: `pip3 wheel . --no-deps`


### Installing from a package
Make sure you use a proper user and password combination
```bash
pip install oalfonso-crossbox
```


### Pre-deployment

- Copy crossbox/settings/.env.example to crossbox/settings/.env
- Uncomment the #DJANGO_SECRET_KEY='GENERATE' line
- Generate a new **DJANGO_SECRET_KEY**
- Replace add the new key to the uncommented line above.
