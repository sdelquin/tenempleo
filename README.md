# tenempleo

Job offers notifications pulled from [tenempleo.com](https://tenempleo.com).

## Justification

Website [tenempleo.com](https://tenempleo.com) displays very good job offers for Canary Islands, but you cannot filter them in order to certain search criteria. This project allows to set target terms and desired locations, thus users will receive an email if any job offers satisfies their needs.

## Installation

Create a Python3 virtualenv and install the requirements inside:

```console
$ pip install -r requirements.txt
```

## Usage

Define, at least, the following settings in an `.env` file:

- `TENEMPLEO_GCP_URL`: url where data is stored.
- `SENDGRID_APIKEY`: check [sendgrify](https://github.com/sdelquin/sendgrify) package.
- `NOTIFICATION_FROM_ADDR`: check [sendgrify](https://github.com/sdelquin/sendgrify) package.
- `NOTIFICATION_FROM_NAME`: check [sendgrify](https://github.com/sdelquin/sendgrify) package.

Create a `config.yml` where you will define the users and their job looking terms:

```yaml
users:
  - name: Franz
    email: franz@example.com
    locations: # desired locations
      - Tenerife
      - Gran Canaria
    targets: # desired terms as they appear in job descriptions
      - técnico, mantenimiento # AND between words
      - auxiliar, supermercado # OR between lines
```

Launch the notifier with:

```console
$ python main.py
```

> `--verbose` is allowed as parameter on CLI.
