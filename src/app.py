from flask import Flask,render_template, request, url_for, redirect, session,jsonify
import mysql.connector
import datetime
from dateutil.relativedelta import relativedelta
import json
import base64
from PIL import Image
import io
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('agg')

mydb = mysql.connector.connect(host="localhost", user="root",password="",database="feedback_system")
mycursor = mydb.cursor()

app = Flask(__name__)

faculty_subjects = {}

def convert_dict(val):
    year = {}
    for a in val:
        b = a[1].replace('[', '').replace(']', '').replace("\"",'').split(',')
        year[a[0]]=b 
    return year

@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/index_ajax",methods=['POST','GET'])
def index_ajax():
    value = request.form['value']
    if value == 'admin':
        return render_template('admin.html')
    if value == 'dc':
        return render_template('dc.html')
    if value == 'feedback':
        mydb = mysql.connector.connect(host="localhost", user="root",password="",database="feedback_system")
        mycursor = mydb.cursor()
        mycursor.execute('SELECT * from subjects')
        subjects = mycursor.fetchall()
        elective = []
        for a in subjects:
            faculty_subjects[a[0].split('_',1)[0]] = a[1]
            mycursor.execute("SELECT `elective/not` FROM `subject_faculties` WHERE sub_code='"+a[0].split('_',1)[0]+"'")
            elective.append(mycursor.fetchone()[0])
        mycursor.close()
        mydb.close()
        return render_template('feedback.html',data = list(faculty_subjects.keys()),cond=elective)

@app.route("/validate_dc",methods=['POST','GET'])
def validate_dc():
    username = request.form['email']
    password = request.form['pass']

    mydb = mysql.connector.connect(host="localhost", user="root",password="",database="feedback_system")
    mycursor = mydb.cursor()

    mycursor.execute('Select * from dc where username=%s and password=%s',(username,password))
    account = mycursor.fetchall()

    mycursor.close()
    mydb.close()

    if account:
        return render_template('add_faculty.html')
    else:
        return render_template('index.html',msg=2)

@app.route("/validate_admin",methods=['GET','POST'])
def validate_admin():
    username = request.form['email']
    password = request.form['pass']

    mydb = mysql.connector.connect(host="localhost", user="root",password="",database="feedback_system")
    mycursor = mydb.cursor()

    mycursor.execute('Select * from admin where username=%s and password=%s',(username,password))
    account = mycursor.fetchall()

    mycursor.close()
    mydb.close()

    if account:
        return render_template('add_subject.html')
    else:
        return render_template('index.html',msg=1)

@app.route("/validate_subject",methods=['POST','GET'])
def validate_subject():
    sub_code = request.form['sub_code']
    sub_name = request.form['sub_name']
    staff_code = request.form['staff_code']
    staff_name = request.form['staff_name']
    year = request.form['year']

    mydb = mysql.connector.connect(host="localhost", user="root",password="",database=""+staff_code)
    mycursor = mydb.cursor()
    mycursor.execute('CREATE TABLE IF NOT EXISTS `'+sub_code+'_'+year+'`(`Teacher is punctual, arrives on time and leaves on time` int(1),`Teacher is good at explaining the subject matter` int(1),`Teacher\'s presentation was clear, loud ad easy to understand` int(1),`Teacher is good at using innovative teaching methods/ways` int(1),`Teacher has completed the whole course as per course outline` int(1))')
    mydb.commit()
    mycursor.close()
    mydb.close()

    mydb = mysql.connector.connect(host="localhost", user="root",password="",database="feedback_system")
    mycursor = mydb.cursor()
    mycursor.execute('INSERT into subjects values(%s, %s)',(sub_code+'_'+year,staff_code))
    mydb.commit()
    mycursor.close()
    mydb.close()

    return render_template('add_subject.html',msg='Successfully Created')

@app.route("/validate_faculty",methods=['POST','GET'])
def validate_faculty():
    fac_code = request.form['fac_code']
    fac_name = request.form['fac_name']
    abbr = request.form['abb']

    mydb = mysql.connector.connect(host="localhost", user="root",password="")
    mycursor = mydb.cursor()
    mycursor.execute('CREATE DATABASE IF NOT EXISTS '+fac_code)
    mydb.commit()
    mycursor.close()
    mydb.close()

    return render_template('add_faculty.html',msg='Successfully Created')

@app.route("/validate_feedback",methods=['POST','GET'])
def validate_feedback():
    if request.method == 'POST':
        year = str((datetime.datetime.now() - relativedelta(years=1)).year)+'-'+str(datetime.date.today().year)
        values = request.get_json()
        for key,value in values.items():
            mydb = mysql.connector.connect(host="localhost", user="root",password="",database=""+faculty_subjects[key])
            mycursor = mydb.cursor()
            mycursor.execute('INSERT INTO `'+key+'_'+year+'` VALUES (%s,%s,%s,%s,%s)',(int(value[0]),int(value[1]),int(value[2]),int(value[3]),int(value[4])))
            mydb.commit()
            mycursor.close()
            mydb.close()

        return render_template('Thanks.html')

@app.route("/New",methods=['POST','GET'])
def New():
    mydb = mysql.connector.connect(host="localhost", user="root",password="",database="feedback_system")
    mycursor = mydb.cursor()
    mycursor.execute('Delete from subjects')
    mydb.commit()
    mycursor.close()
    mydb.close()

    return render_template('add_subject.html',msg='')

@app.route("/analysis",methods=['POST','GET'])
def analysis():
    mydb = mysql.connector.connect(host="localhost", user="root",password="",database="feedback_system")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT sub_code,json_extract(fac_code,'$') FROM `subject_faculties` WHERE year='1'")
    val = mycursor.fetchall()
    print(val)
    year1 = convert_dict(val)

    mycursor.execute("SELECT sub_code,json_extract(fac_code,'$') FROM `subject_faculties` WHERE year='2'")
    val = mycursor.fetchall()
    year2 = convert_dict(val) 
    
    mycursor.execute("SELECT sub_code,json_extract(fac_code,'$') FROM `subject_faculties` WHERE year='3'")
    val = mycursor.fetchall()
    year3 = convert_dict(val)
    
    mycursor.execute("SELECT sub_code,json_extract(fac_code,'$') FROM `subject_faculties` WHERE year='4'")
    val = mycursor.fetchall()
    year4 = convert_dict(val)
    
    mycursor.close()
    mydb.close()

    return render_template('analysis.html',data1=year1,data2=year2,data3=year3,data4=year4)

@app.route('/comparison/<fac>/<sub>')
def comparison(fac,sub): 
    year = str((datetime.datetime.now() - relativedelta(years=1)).year)+'-'+str(datetime.date.today().year)
    mydb = mysql.connector.connect(host="localhost", user="root",password="",database=""+fac)
    mycursor = mydb.cursor()
    mycursor.execute('Select * from `'+sub+'_'+year+'`')
    v = len(mycursor.fetchall())
    mycursor.execute('Select * from `'+sub+'_'+year+'` where `Teacher is punctual, arrives on time and leaves on time` BETWEEN 3 and 5')
    v1 = len(mycursor.fetchall())
    mycursor.execute('Select * from `'+sub+'_'+year+'` where `Teacher is good at explaining the subject matter` BETWEEN 3 and 5')
    v2 = len(mycursor.fetchall())
    mycursor.execute('Select * from `'+sub+'_'+year+'` where `Teacher\'s presentation was clear, loud ad easy to understand` BETWEEN 3 and 5')
    v3 = len(mycursor.fetchall()) 
    mycursor.execute('Select * from `'+sub+'_'+year+'` where `Teacher is good at using innovative teaching methods/ways` BETWEEN 3 and 5')
    v4 = len(mycursor.fetchall())   
    mycursor.execute('Select * from `'+sub+'_'+year+'` where `Teacher has completed the whole course as per course outline` BETWEEN 3 and 5')
    v5 = len(mycursor.fetchall()) 

    img = io.BytesIO()
    y = [v1,v2,v3,v4,v5]
    print(y)
    plt.pie(y, labels=['1','2','3','4','5'],explode=[0,0,0,0,0],autopct=lambda p: '{:.0f}%'.format(p * sum(y) / v), shadow=False, startangle=90,wedgeprops = { 'linewidth' : 3, 'edgecolor' : 'white' })
    plt.title('Analysis')
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    mycursor.close()
    mydb.close()

    return render_template('display.html',plot_url=plot_url,data=[fac,sub,year])

@app.route('/Prev_comparison/<fac>/<sub>',methods=['POST','GET'])
def Prev_comparison(fac,sub): 
    year = request.form['year']
    mydb = mysql.connector.connect(host="localhost", user="root",password="",database=""+fac)
    mycursor = mydb.cursor()
    mycursor.execute('Select * from `'+sub+'_'+year+'`')
    v = len(mycursor.fetchall())
    mycursor.execute('Select * from `'+sub+'_'+year+'` where `Teacher is punctual, arrives on time and leaves on time` BETWEEN 3 and 5')
    v1 = len(mycursor.fetchall())
    mycursor.execute('Select * from `'+sub+'_'+year+'` where `Teacher is good at explaining the subject matter` BETWEEN 3 and 5')
    v2 = len(mycursor.fetchall())
    mycursor.execute('Select * from `'+sub+'_'+year+'` where `Teacher\'s presentation was clear, loud ad easy to understand` BETWEEN 3 and 5')
    v3 = len(mycursor.fetchall()) 
    mycursor.execute('Select * from `'+sub+'_'+year+'` where `Teacher is good at using innovative teaching methods/ways` BETWEEN 3 and 5')
    v4 = len(mycursor.fetchall())   
    mycursor.execute('Select * from `'+sub+'_'+year+'` where `Teacher has completed the whole course as per course outline` BETWEEN 3 and 5')
    v5 = len(mycursor.fetchall()) 

    img = io.BytesIO()
    y = [v1,v2,v3,v4,v5]
    plt.pie(y, labels=['1','2','3','4','5'],explode=[0,0,0,0,0],autopct=lambda p: '{:.0f}%'.format(p * sum(y) / v), shadow=False, startangle=90,wedgeprops = { 'linewidth' : 3, 'edgecolor' : 'white' })
    plt.title('Analysis')
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    mycursor.close()
    mydb.close()

    return render_template('display.html',plot_url=plot_url,data=[fac,sub,year])

@app.route('/overall',methods=['POST','GET'])
def overall():
    mydb = mysql.connector.connect(host="localhost", user="root",password="",database=""+request.form['fac'])
    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM `'+request.form['sub']+'_'+request.form['year']+'` WHERE (`Teacher is punctual, arrives on time and leaves on time`+ `Teacher is good at explaining the subject matter`+`Teacher\'s presentation was clear, loud ad easy to understand`+`Teacher is good at using innovative teaching methods/ways`+`Teacher has completed the whole course as per course outline`)/5 >= 4')
    E = len(mycursor.fetchall())
    mycursor.execute('SELECT * FROM `'+request.form['sub']+'_'+request.form['year']+'` WHERE (`Teacher is punctual, arrives on time and leaves on time`+ `Teacher is good at explaining the subject matter`+`Teacher\'s presentation was clear, loud ad easy to understand`+`Teacher is good at using innovative teaching methods/ways`+`Teacher has completed the whole course as per course outline`)/5 between 3 and 3.9')
    A = len(mycursor.fetchall())
    mycursor.execute('SELECT * FROM `'+request.form['sub']+'_'+request.form['year']+'` WHERE (`Teacher is punctual, arrives on time and leaves on time`+ `Teacher is good at explaining the subject matter`+`Teacher\'s presentation was clear, loud ad easy to understand`+`Teacher is good at using innovative teaching methods/ways`+`Teacher has completed the whole course as per course outline`)/5 < 3')
    W = len(mycursor.fetchall())
    x=[E,A,W]
    img1 = io.BytesIO()
    plt.pie(x, labels=['Excellent','Average','Worst'], autopct='%1.1f%%',shadow=False, startangle=90,wedgeprops = { 'linewidth' : 3, 'edgecolor' : 'white' })
    plt.title('Overall')
    plt.savefig(img1, format='png')
    plt.close()
    img1.seek(0)
    overall_plot = base64.b64encode(img1.getvalue()).decode('utf8')

    mycursor.close()
    mydb.close()

    return render_template('overall.html',overall_plot=overall_plot)

@app.route('/compare/<sub>')
def compare(sub):
    mydb = mysql.connector.connect(host="localhost", user="root",password="",database="feedback_system")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT json_extract(fac_code,'$') FROM `subject_faculties` WHERE sub_code='cs19101'")
    val = mycursor.fetchone()
    faculties = val[0].replace('[', '').replace(']', '').replace("\"",'').replace(' ','').split(',')
    plots = []    
    year = str((datetime.datetime.now() - relativedelta(years=1)).year)+'-'+str(datetime.date.today().year)
    sub='cs19101'
    for i in range(len(faculties)):
        mycursor.execute('use '+faculties[i])
        mycursor.execute('SELECT * FROM `'+sub+'_'+year+'` WHERE (`Teacher is punctual, arrives on time and leaves on time`+ `Teacher is good at explaining the subject matter`+`Teacher\'s presentation was clear, loud ad easy to understand`+`Teacher is good at using innovative teaching methods/ways`+`Teacher has completed the whole course as per course outline`)/5 >= 4')
        E = len(mycursor.fetchall())
        mycursor.execute('SELECT * FROM `'+sub+'_'+year+'` WHERE (`Teacher is punctual, arrives on time and leaves on time`+ `Teacher is good at explaining the subject matter`+`Teacher\'s presentation was clear, loud ad easy to understand`+`Teacher is good at using innovative teaching methods/ways`+`Teacher has completed the whole course as per course outline`)/5 between 3 and 3.9')
        A = len(mycursor.fetchall())
        mycursor.execute('SELECT * FROM `'+sub+'_'+year+'` WHERE (`Teacher is punctual, arrives on time and leaves on time`+ `Teacher is good at explaining the subject matter`+`Teacher\'s presentation was clear, loud ad easy to understand`+`Teacher is good at using innovative teaching methods/ways`+`Teacher has completed the whole course as per course outline`)/5 < 3')
        W = len(mycursor.fetchall())
        x=[E,A,W]
        img = io.BytesIO()
        plt.pie(x, labels=['Excellent','Average','Worst'], autopct='%1.1f%%',shadow=False, startangle=90,wedgeprops = { 'linewidth' : 3, 'edgecolor' : 'white' })
        plt.title(faculties[i])
        plt.savefig(img, format='png')
        plt.close()
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode('utf8')
        plots.append(plot_url)
    
    mycursor.close()
    mydb.close()
    
    return render_template('collegues.html',plots=plots)
    

if __name__=="_main_":
    app.run(debug=True)