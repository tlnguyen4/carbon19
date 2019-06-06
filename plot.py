# Libraries
from io import BytesIO
from flask import Flask, render_template, send_file, make_response, request, redirect
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json
plt.style.use('ggplot')

app = Flask(__name__) 
# Make data: I have 3 groups and 7 subgroups

food = 0
trans = 0
ent = 0
bills = 0
other = 0

@app.route('/pie_chart')
def plot():
	fsum = 0
	tsum = 0
	esum = 0
	bsum = 0
	osum = 0
	with open("data.json") as json_file:
	    json_data = json.load(json_file)
	    for row in json_data:
	    	type = row['title']
	    	if type == "food":
	    		fsum += int(row['amount'])
	    	elif type == "bills":
	    		bsum += int(row['amount'])
	    	elif type == "other":
	    		osum += int(row['amount'])
	    	elif type == "trans":
	    		tsum += int(row['amount'])
	    	elif type == "ent":
	    		esum += int(row['amount'])

	group_names=['Food- $' + str(food) + '\n Rem - $' + str(food-fsum), 'Transportation- $' + str(trans), 'Entertainment- $' + str(ent), 'Bills- $' + str(bills), 'Others- $' + str(other)]
	group_size=[food, trans, ent, bills, other]
	subgroup_names=[' ', 'Rem- $' + str(food-fsum), ' ', 'Rem- $' + str(trans-tsum), ' ', 'Rem- $' + str(ent-esum), ' ', 'Rem- $' + str(bills-bsum), ' ', 'Rem- $' + str(other-osum)]
	subgroup_size=[fsum, food-fsum, tsum, trans-tsum, esum, ent-esum, bsum, bills-bsum, osum, other-osum]
	# Create colors
	a, b, c, d, e=[plt.cm.Blues, plt.cm.Reds, plt.cm.Greens, plt.cm.Oranges, plt.cm.Purples]
 
	# First Ring (outside)
	fig, ax = plt.subplots()
	ax.axis('equal')
	mypie, _ = ax.pie(group_size, radius=1.3, labels=group_names, colors=[a(0.8), b(0.8), c(0.8), d(0.8), e(0.8)] )
	plt.setp( mypie, width=0.3, edgecolor='white')
 
	# Second Ring (Inside)
	mypie2, _ = ax.pie(subgroup_size, radius=1.3-0.3, labels=subgroup_names, labeldistance=0.7, colors=[a(0.6), a(0.4), b(0.6), b(0.4), c(0.6), c(0.4), d(0.6), d(0.4), e(0.6), e(0.4)])
	plt.setp( mypie2, width=0.4, edgecolor='white')
	inner_circle = plt.Circle((0,0),0.70,fc='white')
	plt.margins(0,0)
	fig = plt.gcf()
	fig.gca().add_artist(inner_circle)
	ax.axis('equal')  
	ax.set_title("Goals\n",fontsize=24)
	plt.tight_layout()
	canvas = FigureCanvas(fig)
	img = BytesIO()
	fig.savefig(img)
	img.seek(0)
	return send_file(img, mimetype='image/png')
	 
@app.route('/')
def index():
	return render_template("index.html")

@app.route('/redirect', methods=["POST"])
def index2():
	#print "hi"
	global food
	#print request.form
	food = int(request.form['food'])
	global ent
	ent = int(request.form['ent'])
	global bills
	bills = int(request.form['bills'])
	global trans
	trans = int(request.form['trans'])
	global other
	other = int(request.form['other'])
	return render_template("plot.html")

if __name__ == '__main__':
    app.run(debug=True)

