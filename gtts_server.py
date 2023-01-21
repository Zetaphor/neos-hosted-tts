from pydub import AudioSegment
import atexit
import arrow
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.background import BackgroundScheduler
from pathlib import Path
import hashlib
import os
from gtts import gTTS
from flask import Flask, request, send_file
app = Flask(__name__)


gtts_language_tlds = {
    'en-au': ['en', 'com.au'],
    'en-uk': ['en', 'co.uk'],
    'en-us': ['en', 'com'],
    'en-ca': ['en', 'ca'],
    'en-in': ['en', 'co.in'],
    'en-ie': ['en', 'ie'],
    'en-za': ['en', 'co.za'],
    'fr-ca': ['fr', 'ca'],
    'fr-fr': ['fr', 'fr'],
    'zh-cn': ['zh-CN', 'com'],
    'zh-tw': ['zh-TW', 'com'],
    'pt-br': ['pt', 'com.br'],
    'pt-pt': ['pt', 'pt'],
    'es-mx': ['es', 'com.mx'],
    'es-es': ['es', 'es'],
    'es-us': ['es', 'com'],
    # Default languages if no country locale is included
    'en': ['en', 'com'],
    'es': ['es', 'com'],
    'pt': ['pt', 'pt'],
    'zh': ['zh-CN', 'com'],
}

gtts_default_locales = {
    'en': 'en-us',
    'es': 'es-us',
    'pt': 'pt-pt',
    'fr': 'fr-fr',
    'zh': 'zh-cn',
}

# From https://stackoverflow.com/questions/12485666/python-deleting-all-files-in-a-folder-older-than-x-days
# Deletes all data files more than 4 hours old


def cleanUpFiles():
    criticalTime = arrow.now().shift(hours=-2)
    print("running cleanup")
    filesToRemove = []
    for item in Path("data").glob('*'):
        if item.is_file():
            itemTime = arrow.get(item.stat().st_mtime)
            if itemTime < criticalTime:
                filesToRemove.append(str(item))
    for fileToRemove in filesToRemove:
        print("removing: " + str(fileToRemove))
        os.remove(fileToRemove)


@app.route('/data/<path:filename>', methods=['GET', 'POST'])
def getData(filename):
    Path("data").mkdir(parents=True, exist_ok=True)
    return send_file('data/' + filename)


@app.route('/gtts', methods=['GET', 'POST'])
def get_gtts():
    text = ""
    lang = ""
    try:
        Path("data").mkdir(parents=True, exist_ok=True)
        if request.method == 'GET':
            text = request.args.get('text', "")
            lang = request.args.get('lang', "en-us").lower()
        elif request.method == 'POST':
            text = request.form.get('text', "")
            lang = request.form.get('lang', "en-us").lower()

        if lang in gtts_default_locales:
            lang = gtts_default_locales[lang]

        gtts_language = gtts_language_tlds[lang]

        filename = 'gtts_' + lang + '_' + \
            hashlib.md5(text.encode()).hexdigest()
        outfilemp3 = "data/" + filename + ".mp3"
        outfileogg = "data/" + filename + ".ogg"
        if not os.path.isfile(outfileogg):
            tts = gTTS(text=text, lang=gtts_language[0], tld=gtts_language[1])
            tts.save(outfilemp3)
            sound = AudioSegment.from_mp3(outfilemp3)
            sound.export(outfileogg, format='ogg')
        return "Success" + "\n" + str(request.host_url) + outfileogg + "\n" + text
    except Exception as e:
        # print
        return "Error" + "\n" + "\n" + text


if __name__ == '__main__':

    scheduler = BackgroundScheduler()
    scheduler.add_job(cleanUpFiles, IntervalTrigger(
        seconds=60*60*3), id="filecleanup")
    scheduler.start()

    def cleanupScheduler():
        scheduler.shutdown()

    cleanUpFiles()

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=8000, host='0.0.0.0')
