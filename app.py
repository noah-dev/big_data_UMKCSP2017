#Import global variables, used for values that do not change during runtime
from config import *

#conf_TEST_Query is used for testing/validation. Load small, test data.
#conf_Q = conf_TEST_Query()
conf_Q = conf_Query()
log_Print = conf_Q.log_print

#flask is used as the backend, turning requests from frontend into queries.
#After the query is complete, the result is returned to frontend.
from flask import *

#query holds the pyspark code to run the code.
from query import *

#graph holds the code to turn results in a list into a figure (pyplot)
from graph import *

#After a query is complete, it returns a pyplot object, which holds the results.
#The pyplot is then saved as a figure and is displayed on frontend
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot

#Used to time stamp results.
import datetime

import os
#Clears old figures before query run
def clearFigures():
    if log_Print: print 'Clearing old figures...'
    loc = conf_Q.bS()
    images = os.listdir(loc)
    for image in images:
        if image.endswith(conf_Q.ext):
            os.remove(os.path.join(loc,image))
    if log_Print: print 'Old figures cleared...'

#Setup flask
app = Flask(__name__)
#If at homepage, dispaly home.html template
@app.route('/')
def main():
    if log_Print: print '\nRendering home HTML page now...\n'
    return render_template('index.html')

#When a button is pressed on frontend, it redirects the browser to the result
#page. So if the first button is selected, then the browser will be told to
#go to http://localhost:5555/result/1 - which will call the result function
#with an argument of 1. e.g. result(1)
@app.route('/result/<int:q>')
def result(q):

    #If none of the valid tasks are selected, render error message (q=0)
    if q<1 or q >3:
        if log_Print: print 'ERROR - q was either less than 1 or greater than 3'
        return render_template('result.html', q = 0, figName = "")

    #Clear out previous results
    if log_Print: print ''
    clearFigures()

    #Retrive names from config file
    source = conf_Q.bI(q)
    nameSave, nameDisplay = conf_Q.bF(q)
    fig_attrib = conf_Q.bFA(q)

    #When a query is first started, retrive the date and time to time stamp it.
    if log_Print: print 'Query ' + str(q) + ' selected. Now starting...'
    now = datetime.datetime.now()
    time_stamp = str(now.replace(microsecond = 0))
    if log_Print: print 'Query started at: ' + time_stamp

    #Run from query.py
    if log_Print: print 'Executing on Spark...\nLoading input ' + source + '...'
    result = runQuery(q, source)

    if log_Print: print 'Execution finished. Generating plot...'
    makeFig(q, result, nameSave, fig_attrib, time_stamp)
    if log_Print: print 'Plot generated. Saved in project folder as: ' + nameDisplay

    if log_Print: print 'Finished at: ' +\
                        str(datetime.datetime.now().replace(microsecond = 0))

    if log_Print: print 'Rendering result HTML page now....'+'\n'
    #With figure saved, display
    return render_template('result.html', q = q, figName = nameDisplay)

#Startup server
if __name__ == '__main__':
   app.run(host="0.0.0.0",threaded=True)
