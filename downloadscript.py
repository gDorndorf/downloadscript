import urllib2
import re
import os
import io
import sys
import subprocess
from pyPdf import PdfFileWriter, PdfFileReader

# Get DS Website
# If you for some reason should decide to delete a pdf in /DS
# it'll be appended to the end of your pdf with the next run
# so be carefull with deleting random pdfs

def fetchHTML(URL):
    response = urllib2.urlopen(URL)
    html = response.read()

    return html;


def detectScriptsDS(html):
    # The detected scripts
    s=re.findall("<a href=\"materials\/\d+_\w+.pdf", html)
    return s;

def updatePDFs(s, ls):
    changed = False
    pdfunite = ""
    for i in range(0, len(s)):
        s[i] = re.sub("<a href=\"materials\/", "", s[i])
        if not s[i] in ls:
            #os.system("wget -q -P DS/ https://www2.math.rwth-aachen.de/DS16/materials/" + s[i])
            source = urllib2.urlopen("https://www2.math.rwth-aachen.de/DS16/materials/" + s[i]).read()
            file = open("DS/" + s[i], "wb")
            file.write(source)
            file.close()
            
            print("fetched: " + s[i])
            if "Thomas_DS.pdf" in ls:
                print ("uniting: " +  s[i])
                #os.system("cp DS/Thomas_DS.pdf DS/ThomaT.pdf")
                #os.system("pdfunite " + " DS/" +s[i] + " DS/ThomaT.pdf" + " DS/Thomas_DS.pdf")
                append_pdf("DS/Thomas_DS.pdf", "DS/"+s[i], "DS/Thomas_DS.pdf")
                
                changed = True
    return changed;

def initialize(s):
    changed = False
    pdfunite = ""
    # If the script is run for the first time this is normally the case
    if not "Thomas_DS.pdf" in ls:
        file = open("DS/Thomas_DS.pdf", "wb")
        file.close()
        print("Creating Thomas_DS \xF0\x9F\x98\x8F")
        for i in range(0,len(s)):
            #pdfunite = pdfunite + " DS/" + s[i]
            #os.system("pdfunite " + pdfunite + " DS/Thomas_DS.pdf")
            append_pdf("DS/Thomas_DS.pdf", "DS/" + s[i], "DS/Thomas_DS.pdf")
        changed = True
    return changed;

def append_pdf(pdfIn, pdfIn2, pdfOut):
    # Creating an object where pdf pages are appended to
    output = PdfFileWriter()
    # Appending two pdf-pages from two different files
    inp = open(pdfIn,"r+")
    input = PdfFileReader(open(pdfIn))
    append_pdf(PdfFileReader(open(pdfIn2,"r+")),output)
    # Writing all the collected pages to a file
    output.write(open(pdfOut,"wb"))
    [output.addPage(input.getPage(page_num)) for page_num in range(input.numPages)]
    
html = fetchHTML('https://www2.math.rwth-aachen.de/DS16/lecture_notes.html')
scripts = detectScriptsDS(html)

# To check wether there are already any pdfs on the machine 
#ls = subprocess.check_output('ls DS/', shell=True)
ls = ""
try:
    ls = os.listdir("DS/")
except (WindowsError):
    print("DS/  doesn't exist");
# To keep track and inform the user
changed = updatePDFs(scripts, ls)

if not changed:
    changed = initialize(scripts)
    if not changed:
        print("You were all up to date nothing happened.")
        
