# TramshedTech Client Project Y1S1 GP16
_We have fully switched to sqlite3 so now all those setup steps are mostly not necessarry_

## To setup the project
Before running any of the steps below please ensure you have **`Node`** installed
I also recommend having **`pipenv`** installed although it is not necessary

- Firstly install tailwindcss by running `npm install` at the root of the project
- Install all the python dependencies by running `pipenv install` if you have pipenv installed else run `pip install -r requirements.txt` at the root of the project
- Create an empty folder at the root of the project called `instance`
- To setup the database for the first time or at any time where the schema changes run `python3 run seed.py --init`
_This will create the tables and add the data from the `seed-data.json` file into the database_

## To run the project
- First start the tailwindcss compiler by running `npm run tailwind` at the root of the project
- In another terminal Start the flask server by either running `pipenv run python app.py` if you have pipenv installed else run `python3 app.py` at the root of the project


If you wish to write your own styles you can do so by just writing them in the `app.css` file at the root of the project. Just ensure that tailwindcss is running as it will compile the css and add it to the app

## Helpful resources
- want to learn more about tailwind check this [TailwindCSS Tutorial](https://www.codeinwp.com/blog/tailwind-css-tutorial/) out.
- [TailwindCSS Docs](https://tailwindcss.com/docs/utility-first)
- [Installing pipenv](https://pipenv.pypa.io/en/latest/install/)
- [What is node?](https://www.codecademy.com/article/what-is-node)
- [What is npm?](https://nodejs.org/en/knowledge/getting-started/npm/what-is-npm/)
