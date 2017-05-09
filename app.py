from flask import Flask, request, render_template, flash, redirect
from flask.ext.runner import Runner
from forms import InputForm
import parse_sent
import AMRICA.disagree
import hashlib
import time
import os
import base64
import logging
from logging.handlers import RotatingFileHandler
import json
from flask_jsonpify import jsonify

hash = hashlib.sha1()

app = Flask(__name__)
app.config.from_object('config')

runner = Runner(app)

@app.route('/amreager', methods=['GET', 'POST'])
def main():
    form = InputForm()
    sent = request.args.get('sent')
    lang = request.args.get('lang')
    graph = None
    if form.validate_on_submit():
        try:
            graph = parse_sent.run(form.input_sent.data, form.input_sent.lang)
        except:
            graph = parse_sent.run(form.input_sent.data)
        # sent = form.input_sent.data
    elif sent is not None:
	if lang is None:
	    lang = 'en'
        graph = parse_sent.run(sent, lang)
        if graph is not None:
            app.logger.info('Input: ' + sent)
            hash.update(str(time.time()))
            hash.update(sent)
            last = hash.hexdigest()
            AMRICA.disagree.run("# ::id 1\n" + graph, "tmp" + last + ".png")
            binpng = open("tmp" + last + ".png", "rb").read()
            os.remove("tmp" + last + ".png")
            link = "http://bollin.inf.ed.ac.uk:9010/amreager?lang=" + lang + "&sent=" + "+".join([t for t in sent.split()])
            return jsonify({'graph': graph.replace("\n","<br/>").replace(" ","&nbsp;"), 'png': base64.b64encode(binpng), 'link': link}, sort_keys=True, indent=4, separators=(',', ': '))
    
    return render_template('sentence.html',form=form)

@app.route('/', methods=['GET', 'POST'])
def main2():
    form = InputForm()
    sent = request.args.get('sent')
    lang = request.args.get('lang')
    graph = None
    if form.validate_on_submit():
        try:
            graph = parse_sent.run(form.input_sent.data, form.input_sent.lang)
        except:
            graph = parse_sent.run(form.input_sent.data)
        sent = form.input_sent.data
    elif sent is not None:
	if lang is None:
            lang = 'en'
        graph = parse_sent.run(sent, lang)
        if graph is not None:
            app.logger.info('Input: ' + sent)
            hash.update(str(time.time()))
            hash.update(sent)
            last = hash.hexdigest()
            AMRICA.disagree.run("# ::id 1\n" + graph, "tmp" + last + ".png")
            binpng = open("tmp" + last + ".png", "rb").read()
            os.remove("tmp" + last + ".png")
            link = "<span id ='link' style='height:150;width:162;background-color:pink'> http://bollin.inf.ed.ac.uk:9010?lang" + lang + "&sent=" + "+".join([t for t in sent.split()]) + "</span>"
            return render_template('sentence.html', form=form, graph=graph.replace("\n","<br/>").replace(" ","&nbsp;"),png="<img src=\"data:image/png;base64," + base64.b64encode(binpng) + "\">", link="<b>Link:</b> " + link + " <button onClick=\"ClipBoard();\">Copy to Clipboard</button>")
        
    return render_template('sentence.html',form=form)


if __name__ == '__main__':
    handler = RotatingFileHandler('sentences.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(message)s")
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)
    runner.run()
