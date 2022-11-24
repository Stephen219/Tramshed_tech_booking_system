# TramshedTech Client Project Y1S1 GP16

## To setup the project
Before running any of the steps below please ensure you have **`Node`** installed
I also recommend having **`pipenv`** installed

- Firstly install tailwindcss by running `npm install` at the root of the project
- Install all the python dependencies by running `pipenv install` at the root of the project

### Database
I propose we use sqlalchemy due to its superiority over sqlite3.
- First go into `app.py` and comment all the imports above `if __name__ == "__main__":` e.g `import user`
- Then from the root of the project run `flask db init` to create the database
- Then run `flask db upgrade` to apply the latest migration to the database
- Finally uncomment the commented lines you commented above

_If you do not comment out the imports you will receive an ImportError_

_A migration is basically the schema of the database outlining the columns_

_If you do not have pipenv installed or are unable to install it just manually install the dependencies in the `requirements.txt` file. This can be done by running `pip install -r requirements.txt`_

## To run the project
- First start the tailwindcss compiler by running `npm run tailwind` at the root of the project
- In another terminal Start the flask server by either running `pipenv run python app.py` if you have pipenv installed or `python3 app.py` if you do not have it installed from the root of the project

The database's tables are generated from the classes in `db.py`
After adding any new models to the database in `db.py` and making sure they are correct you may do the following:
- Comment out all the imports above `if __name__ == "__main__":` e.g `import user`
- Run `flask db migrate -m "<A comment stating what you have changed>"` to create the migration
- Run `flask db upgrade` to apply the migration
- Finally uncomment the commented lines you commented above

If you wish to write your own styles you can do so by just writing them in the `app.css` file at the root of the project. Just ensure that tailwindcss is running as it will compile the css and add it to the app

## Helpful resources
- want to learn more about tailwind check this [TailwindCSS Tutorial](https://www.codeinwp.com/blog/tailwind-css-tutorial/) out.
- [TailwindCSS Docs](https://tailwindcss.com/docs/utility-first)
- [Installing pipenv](https://pipenv.pypa.io/en/latest/install/)
- [What is node?](https://www.codecademy.com/article/what-is-node)
- [What is npm?](https://nodejs.org/en/knowledge/getting-started/npm/what-is-npm/)
