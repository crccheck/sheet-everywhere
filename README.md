A simple Google Spreadsheet to JSON resource.

## Developing

Getting started:

```bash
pip install -r requirements.txt
```

See `Procfile` for example of how to run the webserver.

## Deploying to Heroku

Just push this to your Heroku app.

*Optional:* For a redis backed cache, install the [Redis To Go] addon:

```bash
heroku addons:add redistogo:nano
```

  [Redis To Go]: https://addons.heroku.com/redistogo
