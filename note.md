Notes:

Error message:
Use a production WSGI server instead.



Using Flask calling function from anchor tag in html

```
<a href= "{{ url_for= 'name_of_function' }}">Click for app.route assigned to function</a>
```

Using Flask setting varialbe in html.  
```
{% set x = "x-ray" %}
```

Set up dictionary in flask.  
When passed to html, keys call wit dot notation
```
<ul>
	<li>{{dict.key}}</li>
</ul>
```

Using flask, from html call loop
```
{% for name in list %}  
 <li>{{ name }}</li>  
{% endfor %}
```

#### Flask with Mongo.  
Use function to connect to Mongo. Call function in flask function.

```python
def find_teams():
	return list(db.teams.find())
	
@app.route("/")
def index():
	teams = find_teams()
	return render_template('index.html', teams = teams)
```
