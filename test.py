import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_dangerously_set_inner_html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_table

import base64
import datetime
import io

import os

import pandas as pd
import numpy as np
import json

import flask
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename


app = dash.Dash(__name__, url_base_pathname='/vbc-demo/launch/')

#app.config['UPLOAD_FOLDER'] = '/uploads'

server = app.server

def create_layout(app):
	return html.Div([
			html.H6('choose file to upload'),
			dash_dangerously_set_inner_html.DangerouslySetInnerHTML('''
			<form action="/uploader" method="POST" enctype="multipart/form-data">

				<div class="form-group">
				  <label>Select File</label>
				  <div class="custom-file">
					<input type="file" name="file" >
				  </div>
				</div>

				<button type="submit" class="btn btn-primary">Submit</button>

			</form>
			'''),
			dcc.Upload(
				id = 'upload-test',
				children = html.Div([
					'Select Related Files to Upload'
					],style={"font-family":"NotoSans-Regular","font-size":"0.8rem","text-decoration":"underline","color":"#1357DD"}),
				style={
					'height': '40px',
					'lineHeight': '40px',
					'borderWidth': '1px',
					'borderStyle': 'dashed',
					'borderRadius': '5px',
					'textAlign': 'center'
					}
				),
			html.Div(id = 'output-test-upload', style={"text-align":"center","padding":"0.5rem","font-family":"NotoSans-Regular","font-size":"0.6rem"}),
		])


app.layout = create_layout(app)


# @app.server.route('/upload')
# def upload_file():
#    return render_template('upload.html')

def trans_upload_to_download(contents, filename, date):
	content_type, content_string = contents.split(',')
	decoded = base64.b64decode(content_string)

#	df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

	path = str('uploads/') + filename
#	df.to_csv(path)
	with open(path, "wb") as file:
		file.write(decoded)

	return html.Div([
				html.A(filename, 
#					href='http://0.0.0.0:8052/' + path,
					href='http://139.224.186.182:8098/' + path,
					target = "_blank")
				])

@app.callback(
	Output('output-test-upload', 'children'),
	[Input('upload-test', 'contents')],
	[State('upload-test', 'filename'),
	State('upload-test','last_modified')]
	)
def upload_output(list_of_contents, list_of_names, list_of_dates):
	if list_of_contents is not None:
		children = [
			trans_upload_to_download(list_of_contents, list_of_names, list_of_dates) 
		]
		return children

@app.server.route('/<filename>', methods = ['GET'])
def serve_static(filename):

#    filename = 'downloads/' + filename
    return flask.send_file(filename, as_attachment=True)
	
# @app.server.route('/uploader', methods = ['GET', 'POST'])
# def upload_file():
# 	if request.method == 'POST':
# 		f = request.files['file']
# 		filename = secure_filename(f.filename)
		
# 		f.save('C:\\Users\\wangsunyechu\\Documents\\VBP-report-demo-test-REALTIME\\uploads\\'+filename)
# 		print(request.url)
# 		return redirect(flask.url_for('/vbc-demo/launch/'))


if __name__ == "__main__":
	app.run_server(host="127.0.0.1", debug = True, port = 8052)