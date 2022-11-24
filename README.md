# Neos Hosted TTS

This is a hosted python script that provides TTS functionality in Neos. This repo is to serve as an alternative to [the neos-local-tts project](https://github.com/Zetaphor/neos-local-tts).

The python codebase and in-world object is a heavily modified version of the [original ttswrapper by TessaCoil](https://github.com/Phylliida/ttswrapper).


## Installation

This was developed using Python 3.10.8 and pip 21.3.1 on Fedora 37.

```
pip3 install -r requirements.txt
python3 app.py
```

## Usage

The server starts at localhost:5000. Requests can be sent via get or POST. The following arguments are supported:

* text: The actual message text
* lang: The language/accent region

```
http://localhost:5000/gtts?text=wow%20hi%20there&lang=en-us
```

It outputs as `Success\nfilePath.ogg\ninput text` or `Error\n\ninput text`

### Accent Regions

The script will default to US English if no option is provided. It supports all of the currently available regional accents provided by GoogleTTS:

Accent Code | Accent Language
---|---
en-au | English (Australia)
en-uk | English (United Kingdom)
en-us | English (United States)
en-ca | English (Canada)
en-in | English (India)
en-ie | English (Ireland)
en-za | English (South Africa)
fr-ca | French (Canada)
fr-fr | French (France)
zh-cz | Mandarin (China Mainland)
zh-tw | Mandarin (Taiwan)
pt-br | Portuguese (Brazil)
pt-pt | Portuguese (Portugal)
es-mx | Spanish (Mexico)
es-es | Spanish (Spain)
es-us | Spanish (United States)




