#-----------------------------------MODULE CHECKS------------------------------

# Check for modules, try to exit gracefully if not found
import sys
import imp
try:
    imp.find_module('numpy')
    foundnp = True
except ImportError:
    foundnp = False
try:
    imp.find_module('matplotlib')
    foundplot = True
except ImportError:
    foundplot = False
try:
    imp.find_module('pandas')
    foundpd = True
except ImportError:
    foundplot = False
if not foundnp:
    print("Numpy is required. Exiting")
    sys.exit()
if not foundplot:
    print("Matplotlib is required. Exiting")
    sys.exit()
if not foundpd:
    print("Pandas is required. Exiting")
    sys.exit()

#-------------------------------------------------------------------------------

import os
import glob

#Stop message from appearing
import warnings
warnings.filterwarnings("ignore",".*GUI is implemented.*")
warnings.filterwarnings("ignore",".*No labelled objects found.*")

#Find relevant CSVs in folder
path = os.getcwd()
extension = 'csv'
os.chdir(path)
csvresult = [i for i in glob.glob('*.{}'.format(extension))]
print("Plotting the following:")
print(csvresult)

import numpy as np
import matplotlib.pyplot as plt
#import matplotlib.patches as patches
import pandas as pd
import math

#Make x-axis
t = np.linspace(325, 1100, 776)
#define color for graph lines
#color_code=['b','k','r','g','c','m', 'y', 'g', 'crimson', 'teal', 'aqua']
#define determinant calculation
def det(a, b):
    return a[0] * b[1] - a[1] * b[0]

#set initial values (for later use)
k=0
totalexport=[]
#iterate through CSVs
while k < len(csvresult):
    horiz=.04
    exportlist=[]
    path = os.getcwd()
    path = path + "/" + csvresult[k]
    cv=pd.read_csv(path, delimiter=",", error_bad_lines=False)

    #Extract Data from Current Column
    currentwhole=cv.values[:,1]
    ind=np.where(currentwhole == ' Current/A')
    startdata=ind[0][0]
    startdata=startdata + 1
    currentdatastr=cv.values[startdata:,1]

    #Extract Data from Potential Column
    potentialdatastr=cv.values[startdata:,0] 
    
    #Convert all elements from strings to floats so they can be math. manipulated
    currentdataOG = [ float(x) for x in currentdatastr ]
    potentialdata = [ float(x) for x in potentialdatastr ]
    #Multiply current data to fit axis properly
    currentdata = [ i * (100000) for i in currentdataOG ]
    #assign attributes to plot
    colour = 'b'
    plotlabel = csvresult[k]
    plotlabel = plotlabel[:-4]
    totalexport.append(plotlabel)
    #plot graph
    plt.plot(potentialdata, currentdata, colour, label= plotlabel)
    plt.draw()
    
    count=1
    while count <= 2:
        xline1=[] #x values of line 1 to fill in as code proceeds
        yline1=[]
        xline2=[]
        yline2=[]
        #Point Clicks and Intersections
        if count==1:
            print('>> Please choose two points for first line (onset of oxidation)')
            line1 = plt.ginput(2) # it will wait for two clicks
            line1=np.array(line1)
            x1=line1[0,0]
            xline1.append(x1)
            y1=line1[0,1]
            yline1.append(y1)
            print('>> Please choose two points for first line (onset of oxidation)')
            line2 = plt.ginput(2)
            line2=np.array(line2)
            x2=line2[0,0]
            xline2.append(x2)
            y2=line2[0,1]
            yline2.append(y2)
        if count==2:
            print('>> Please choose two points for first line (onset of reduction)')
            line1 = plt.ginput(2) # it will wait for two clicks
            line1=np.array(line1)
            x1=line1[0,0]
            xline1.append(x1)
            y1=line1[0,1]
            yline1.append(y1)
            print('>> Please choose two points for first line (onset of reduction)')
            line2 = plt.ginput(2)
            line2=np.array(line2)
            x2=line2[0,0]
            xline2.append(x2)
            y2=line2[0,1]
            yline2.append(y2)
        #Find intersection
        xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
        ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])
        div = det(xdiff, ydiff)
            #if div == 0:
               #raise Exception('lines do not intersect')
        d = (det(*line1), det(*line2))
        
        #calculate onset
        x = det(d, xdiff) / div
        xline1.append(x)
        xline2.append(x)
        #make point of intersection
        y = det(d, ydiff) / div
        yline1.append(y)
        yline2.append(y)
        
        plt.plot(xline1,yline1,'r')
        plt.plot(xline2,yline2,'r')
        plt.draw()

        exportlist.append(x)
        #calculate homo/lumo
        holu = x - 4.8
        exportlist.append(holu)
        #round these values
        x = round(x,2)
        holu = round(holu,2)
        #make these strings instead of integers
        x = str(x)
        holu = str(holu)
        #print message on command prompt
        if count==1:
            print('------------')
            print("Oxidation onset:")
            print(x + " V")
            print('------------')
        if count==2:
            print('------------')
            print("Reduction onset:")
            print(x + " V")
            print('------------')
        count=count+1
        
    totalexport.append(exportlist)
    #write texts to put on chart
    ox=exportlist[0]
    ox=round(ox,3)
    ox=str(ox)
    homo=exportlist[1]
    homo=round(homo,3)
    homo=str(homo)
    red=exportlist[2]
    red=round(red,3)
    red=str(red)
    lumo=exportlist[3]
    lumo=round(lumo,3)
    lumo=str(lumo)
    oxtxt = 'OX' '$_{onset}$' + ' = ' + ox + "V"
    redtxt = 'RED' '$_{onset}$' + ' = ' + red + "V"
    homotxt = 'HOMO = ' + homo + "eV"
    lumotxt = 'LUMO = ' + lumo + "eV"
    #change initial value and make first text label
    plt.gca().set_position((.1, .28, .8, .65)) # to make a bit of room for extra text
    vert = 0.14
    plt.figtext(horiz,vert,plotlabel,style='italic')
    #plt.figure().add_subplot(111).plot(range(10), range(10))
    txtlist = [oxtxt,redtxt,homotxt, lumotxt]
    i=0
    #iterate through text list to make text boxes of values
    while i < len(txtlist):
        if i == 2:
            horiz=horiz+0.25
            vert=vert+0.1
        vert=vert-0.05
        curr=txtlist[i]
        plt.figtext(horiz,vert,curr)
        i=i+1
        continue
    #----------------------------------EXCEL EXPORT---------------------------------

    # Create a Pandas dataframe title for data.
    df0 = pd.DataFrame({'Data': ['Onset of Oxidation (V)','HOMO (eV)','Onset of Reduction (V)','LUMO (eV)']})

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    folder = 'Processed CV Data'
    if not os.path.exists(folder):
        os.makedirs(folder)

    calcname=csvresult[k]
    calcname=calcname + '-calcs.xlsx'
    writer = pd.ExcelWriter(os.path.join(folder,calcname), engine='xlsxwriter')

    #Loop through data from total export list
    j=0
    index=1
    while j < len(totalexport):
        plotlabel=totalexport[j]
        data=totalexport[j+1]
        df = pd.DataFrame({plotlabel: data})
        df.to_excel(writer, sheet_name='Sheet1', startcol=index, index=False)
        j=j+2
        index=index+1
        continue

    # Convert the dataframe to an XlsxWriter Excel object.
    df0.to_excel(writer, sheet_name='Sheet1', startrow=1, header = False, index=False)

    # Get the xlsxwriter workbook and worksheet objects.
    workbook  = writer.book
    worksheet = writer.sheets['Sheet1']

    # Set the column width and format.
    worksheet.set_column('A:A', 20)
    worksheet.set_column('B:B', 15)
    worksheet.set_column('C:C', 15)
    worksheet.set_column('D:D', 15)

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()
    msg= csvresult[k][:-4] + ' CV Calculations exported --------->'
    print(msg)

    #---------> DATA TO CREATE GRAPH IN EXCEL

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    dataname=csvresult[k]
    dataname=dataname + '-dataset.xlsx'
    writer = pd.ExcelWriter(os.path.join(folder,dataname), engine='xlsxwriter')

    #Create wavelength column
    potentialdatastr=[float(x) for x in potentialdatastr]
    df = pd.DataFrame({'Potential/ V': potentialdatastr})
    df.to_excel(writer, sheet_name='Sheet1', startcol=0, startrow=0, index=False)
    df1 = pd.DataFrame({'Current/ A': currentdatastr})
    df1.to_excel(writer, sheet_name='Sheet1', startcol=1, startrow=0, index=False)
    i=0
    currentdatastr=[float(x) for x in currentdatastr]
    microcurrentdatastr=[x*1000000 for x in currentdatastr]
    df2 = pd.DataFrame({'Current/ microA': microcurrentdatastr})
    df2.to_excel(writer, sheet_name='Sheet1', startcol=2, startrow=0, index=False)

    # Get the xlsxwriter workbook and worksheet objects.
    workbook  = writer.book
    worksheet = writer.sheets['Sheet1']

    # Set the column width and format.
    worksheet.set_column('A:A', 11)
    worksheet.set_column('B:B', 11)
    worksheet.set_column('C:C', 11)

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()
    msg= csvresult[k][:-4] + ' CV Dataset exported --------->'
    print(msg)

    #-------------------------------------------------------------------------------

    #Bold axis numbers and change font sizes
    ax=plt.gca()
    for tick in ax.xaxis.get_major_ticks():
        tick.label1.set_fontsize(9)
        tick.label1.set_fontweight('bold')
    for tick in ax.yaxis.get_major_ticks():
        tick.label1.set_fontsize(9)
        tick.label1.set_fontweight('bold')
    #Axis Ranges
##    xmin=min(potentialdata)
##    if xmin < 0:
##        xmin=float(str(math.floor(xmin*10)/10)[:-1] + str(int(str(math.floor(xmin*10)/10)[-1:])-1))
##    else:
##        xmin=float(str(math.floor(xmin*10)/10)[:-1] + str(int(str(math.floor(xmin*10)/10)[-1:])+1))
##    xmax=max(potentialdata)
##    xmax=float(str(math.ceil(xmax*10)/10)[:-1] + str(int(str(math.ceil(xmax*10)/10)[-1:])+1))
##    plt.xlim([xmin,xmax])
##    ymin=min(currentdata)
##    if ymin <0:
##        ymin=float(str(math.floor(ymin*10)/10)[:-1] + str(int(str(math.floor(ymin*10)/10)[-1:])-1))
##    else:
##        ymin=float(str(math.floor(ymin*10)/10)[:-1] + str(int(str(math.floor(ymin*10)/10)[-1:])+1))
##    ymax=max(currentdata)
##    ymax=float(str(math.ceil(ymax*10)/10)[:-1] + str(int(str(math.ceil(ymax*10)/10)[-1:])+1))
##    plt.ylim([ymin, ymax])
    #Labels
    plt.xlabel('Potential (V) / V',weight='bold')
    plt.ylabel('Current (I) / x10$^{-1}$${\mu}A$',weight='bold')
    plt.draw()
    #Graph Finished Message
    sep=" "
    name = os.getlogin()
    name = name.split(sep, 1)[0]
    msg = 'Hey ' + name + ', ' + csvresult[k][:-4] + "'s graph has finished processing."
    picname= csvresult[k][:-4] + '.png'
    print(msg)
    plt.savefig(os.path.join(folder,picname), bbox_inches='tight')
    k=k+1
    #horiz = horiz + 0.25
    #case where if you reach your last CSV, then break the loop
    plt.show()
    if k == len(csvresult):
        plt.title('Cyclic Voltammetry',weight='bold')
        plt.legend(loc='best')
        break
    continue
