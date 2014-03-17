
from django.http import HttpResponse, HttpResponseNotFound
from django.template.loader import get_template
from django.template import Context
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import render
from django import forms

import models
import MySQLdb



class ProjectForm(forms.Form):

	db = forms.CharField()
	host = forms.CharField()
	user = forms.CharField()
	password = forms.CharField()
	
	


def consultas(query):

	bd= MySQLdb.connect("localhost","root","root","geditdb")
	cursor = bd.cursor()
	cursor.execute(query)
	data = cursor.fetchall()	

	return data





def principal(request):
	
	flag = True
	project = ProjectForm()

	if(request.method == "GET"):
		comment = ""
	elif(request.method == "POST"):
		project = ProjectForm(request.POST)
		if project.is_valid():
			flag = False
			print "Is valid"
			db = project.cleaned_data['db']
			host = project.cleaned_data['host']
			user = project.cleaned_data['user']
			password = project.cleaned_data['password']
			datos = [host, user, password, db]
			return render_to_response('principal.html',
						{'flag':flag,'name_proj':db},
						context_instance=RequestContext(request))
		else:
			comment= "Debe rellenar todos los campos"			

	return render_to_response('principal.html',
						{'flag':flag,'project':project,'comment':comment},
						context_instance=RequestContext(request))






def people(request):

	if(request.method == "GET"):
		lista = ""
		personas = consultas("SELECT * FROM people")
		for registro in personas:
			ident = registro[0]
			nombre = registro[1]
			email = registro[2]
			lista+= '<p><a href="http://localhost:1234/'+nombre+'/'+str(ident)+'/">'+nombre+'</a><br>'
			pers = '<h4><a href="http://localhost:1234/'+nombre+'/'+str(ident)+'/">'+nombre+'</a>'+'&nbsp;&nbsp;'+email+'</h4>'
			lista += email+'</p>'+'<br>'

		lista = lista.decode('ascii','ignore')
		return render_to_response('people.html',
						{'info':lista},
						context_instance=RequestContext(request))
	


def person(request,nombre, ident):

	if(request.method == "GET"):
		info = ""
		numcommits = 0
		ident = ident.split("/")[0]
		data = consultas("SELECT date, message FROM scmlog WHERE author_id=" + str(ident))
		info += '<thead><tr><th>Date</th><th>Message</th></tr></thead><tbody>'
		for registro in data:
			numcommits += 1
			date = registro[0]
			x = date.strftime('%m/%d/%Y')
			if (numcommits%2 == 0):	
				info += '<tr><td>'+x+'</td><td>'+registro[1]+'</td></tr>'
			else:
				info += '<tr class="alt"><td>'+ x+'</td><td>'+registro[1]+'</td></tr>'
		info += '<tr><th>Commits:</th><td>'+str(numcommits)+'</td></tr></tbody>'


		return render_to_response('person.html',
						{'info':info,'nombre':nombre},
						context_instance=RequestContext(request))




