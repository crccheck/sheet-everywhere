# Sheet Everywhere

Miracle Google spreadsheets into JSON so you can use them everywhere.

## Try It

You can try the reference implementation hosted on Heroku at:

> http://sheet-everywhere.herokuapp.com/

Use the key of the spreadsheet (found in the url) to miracle it into a JSON
resource like:

> http://sheet-everywhere.herokuapp.com/0AvtWFMTdBQSLdFI3Y2M0RnI5OTBMa2FydXNFelBDTUE/

The spreadsheet must be publicly accessible.

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
