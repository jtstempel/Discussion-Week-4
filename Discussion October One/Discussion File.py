from flask import Flask, render_template, session, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField, widgets
from wtforms.validators import Required

import json
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'
app.debug = True

class WeatherForm(FlaskForm):
	zipcode = StringField('Enter a US zipcode:', validators = [Required()])
	submit = SubmitField('Submit')

	def validate_zipcode(self, field):
		if len(str(field.data)) != 5:
			raise ValidationError('Your zipcode was not valid because it was not 5 characters')

@app.route('/zipcode', methods = ['POST', 'GET'])
def zipcode():
	form = WeatherForm()
	if form.validate_on_submit():
		zipcode = str(form.zipcode.data)
		base_url = 'http://api.openweathermap.org/data/2.5/weather?'
		params = {}
		params['zip'] = zipcode + ',us'
		params['appid'] = 'ca0b2f389b4dcef18a061b9249561441'
		response = requests.get(base_url, params = params)
		response_dict = json.loads(response.text)

		
		my_description = response_dict['weather'][0]['description']
		my_city = response_dict['name']
		my_temperature = response_dict['main']['temp']
		return render_template('results.html', city = my_city, description = my_description, temperature = my_temperature)
	
	flash(form.errors)
	return render_template('zipform.html', form=form)


if __name__ == '__main__':
	app.run(use_reloader = True, debug = True)


