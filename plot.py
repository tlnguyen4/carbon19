# Libraries
from io import BytesIO
from flask import Flask, render_template, send_file, make_response, request, redirect
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
matplotlib.use('TkAgg')
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

	group_names=['Food- $' + str(food) + '\nRem - $' + str(food-fsum), 'Transportation- $' + str(trans)+ '\nRem - $' + str(trans-tsum), 'Entertainment- $' + str(ent)+ '\nRem - $' + str(ent-esum), 'Bills- $' + str(bills)+ '\nRem - $' + str(bills-bsum), 'Others- $' + str(other) + '\nRem - $' + str(other-osum)]
	group_size=[food, trans, ent, bills, other]
	#subgroup_names=[' ', ' ', ' ', ' ', ' ', 'Rem- $' + str(ent-esum), ' ', 'Rem- $' + str(bills-bsum), ' ', 'Rem- $' + str(other-osum)]
	subgroup_size=[min(food, fsum), max(0, food-fsum), min(trans, tsum), max(0, trans-tsum), min(ent, esum), max(0, ent-esum), min(bills, bsum), max(0, bills-bsum), min(other, osum), max(0, other-osum)]
	# Create colors
	a, b, c, d, e, f=[plt.cm.Blues, plt.cm.Reds, plt.cm.Greens, plt.cm.Oranges, plt.cm.Purples, plt.cm.Greys]

	# First Ring (outside)
	fig, ax = plt.subplots()
	ax.axis('equal')
	mypie, _ = ax.pie(group_size, radius=1.3, labels=group_names, colors=[a(0.8), b(0.8), c(0.8), d(0.8), e(0.8)] )
	plt.setp( mypie, width=0.3, edgecolor='white')

	# Second Ring (Inside)
	mypie2, _ = ax.pie(subgroup_size, radius=1.3-0.3, colors=[f(0.4), a(0.45), f(0.4), b(0.45), f(0.4), c(0.45), f(0.4), d(0.45), f(0.4), e(0.45)])
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

@app.route('/bar_chart')
def plot_bar():
	data = [[350,50, 275,25, 200,50, 515,85, 140,10],[380,20, 240,10, 215,35, 475,25, 75,25],[310,40, 205,45, 275,25, 475,25, 95,5],[350,0, 190,10, 295,5, 530,20, 140,10],[300,0, 85,15, 235,15, 430,20, 295,5]]
	d1,d2,d3,d4,d5,d6,d7,d8,d9,d0 = [],[],[],[],[],[],[],[],[],[]
	for row in data:
		d1.append(row.pop(0))
		d2.append(row.pop(0))
		d3.append(row.pop(0))
		d4.append(row.pop(0))
		d5.append(row.pop(0))
		d6.append(row.pop(0))
		d7.append(row.pop(0))
		d8.append(row.pop(0))
		d9.append(row.pop(0))
		d0.append(row.pop(0))

	d1=np.array(d1)
	d2=np.array(d2)
	d3=np.array(d3)
	d4=np.array(d4)
	d5=np.array(d5)
	d6=np.array(d6)
	d7=np.array(d7)
	d8=np.array(d8)
	d9=np.array(d9)
	d0=np.array(d0)

	ind = np.arange(5)
	p1 = plt.barh(ind, d1, height=0.4, align = 'center', color='orange')
	p2 = plt.barh(ind, d2, height=0.4, left=d1, align = 'center', color='orange')
	p3 = plt.barh(ind, d3, height=0.4, left=d2+d1, align = 'center', color='green')
	p4 = plt.barh(ind, d4, height=0.4, left=d3+d2+d1, align = 'center', color='green')
	p5 = plt.barh(ind, d5, height=0.4, left=d4+d3+d2+d1, align = 'center', color='red')
	p6 = plt.barh(ind, d6, height=0.4, left=d5+d4+d3+d2+d1, align = 'center', color='red')
	p7 = plt.barh(ind, d7, height=0.4, left=d6+d5+d4+d3+d2+d1, align = 'center', color ='blue')
	p8 = plt.barh(ind, d8, height=0.4, left=d7+d6+d5+d4+d3+d2+d1, align = 'center', color='blue')
	p9 = plt.barh(ind, d9, height=0.4, left=d8+d7+d6+d5+d4+d3+d2+d1, align = 'center', color='purple')
	p0 = plt.barh(ind, d0, height=0.4, left=d9+d8+d7+d6+d5+d4+d3+d2+d1, align = 'center', color='purple')


	

	plt.yticks(ind, ('May', 'April', 'March', 'February', 'January'))
	plt.xticks(np.arange(0, 2000, 500))
	
	plt.title("Past Months\n",fontsize=24)
	plt.savefig('pic.png')

	
	# plt.tight_layout()
	# canvas = FigureCanvas(fig)
	# img = BytesIO()
	# fig.savefig(img)
	# img.seek(0)
	return send_file('pic.png')

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
