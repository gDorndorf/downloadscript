import urllib.request as urllib
import re
import os
import io
import sys
import subprocess
from PyPDF2 import PdfFileWriter, PdfFileReader
# Get DS Website
# If you for some reason should decide to delete a pdf in /DS
# it'll be appended to the end of your pdf with the next run
# so be carefull with deleting random pdfs

REG_FINDSTRING  = b"<a href=\"materials\/\d+_\w+.pdf"
REG_SUBSTRING   = b"<a href=\"materials\/"
URL_MATERIALS   = r"https://www2.math.rwth-aachen.de/DS16/materials/"
URL_LECTURENOTES= r"https://www2.math.rwth-aachen.de/DS16/lecture_notes.html"
OUT_DIR     = r"DS/"
OUT_FILE    = r"DS_Thomas"
OUT_PDF     = OUT_DIR + OUT_FILE + ".pdf"

def fetchHTML(URL):
    response = urllib.urlopen(URL)
    html = response.read()

    return html;


def detectScripts(html):
    # The detected scripts
    s=re.findall(REG_FINDSTRING, html)
    return s;

def updatePDFs(s, ls):
    changed = False
    pdfunite = ""
    for i in range(0, len(s)):
        s[i] = re.sub(REG_SUBSTRING, b"", s[i]).decode('utf8')
        if not s[i] in ls:
            #os.system("wget -q -P DS/ https://www2.math.rwth-aachen.de/DS16/materials/" + s[i])
            with urllib.urlopen(URL_MATERIALS + s[i]) as response:
                source = response.read()
            file = open(OUT_DIR + s[i], "wb")
            file.write(source)
            file.close()
            
            print("fetched: " + s[i])
            if OUT_FILE+".pdf" in ls:
                print ("uniting: " +  s[i])
                #os.system("cp DS/Thomas_DS.pdf DS/ThomaT.pdf")
                #os.system("pdfunite " + " DS/" +s[i] + " DS/ThomaT.pdf" + " DS/Thomas_DS.pdf")
                append_pdf(OUT_PDF, OUT_DIR+s[i], OUT_PDF)
                
                changed = True
    return changed;

def initialize(s):
    changed = False
    pdfunite = ""
    # If the script is run for the first time this is normally the case
    if not OUT_FILE + ".pdf" in ls:
        file = open(OUT_PDF, "wb")
        file.close()
        print("Creating "+OUT_FILE+" ")#\xF0\x9F\x98\x8F
        for i in range(0,len(s)):
            #Not so beutiful work-around, "Windows-Code" generates an Error 22 under Ubuntu 16.10
            if (os.name == "posix"):
                pdfunite = pdfunite + " " + OUT_DIR + s[i]
                os.system("pdfunite " + pdfunite + " " + OUT_PDF)
            else:
                append_pdf(OUT_PDF, OUT_DIR + s[i], OUT_PDF)
        changed = True
    return changed;

def append_pdf(pdfIn, pdfIn2, pdfOut):
    # Creating an object where pdf pages are appended to
    output = PdfFileWriter()
    # Appending two pdf-pages from two different files
    #inp = open(pdfIn,"w+b")
    input = PdfFileReader(open(pdfIn,"w+b"))
    append_pdf(PdfFileReader(open(pdfIn2,"w+b")),output)
    # Writing all the collected pages to a file
    output.write(open(pdfOut,"wb"))
    [output.addPage(input.getPage(page_num)) for page_num in range(input.numPages)]
    
html = fetchHTML(URL_LECTURENOTES)
scripts = detectScripts(html)

# To check wether there are already any pdfs on the machine 
#ls = subprocess.check_output('ls DS/', shell=True)
ls = ""
try:
    ls = os.listdir(OUT_DIR)
except (Exception):
    print(OUT_DIR+" doesn't exist, now creating");
    os.mkdir(r"./"+OUT_DIR)      
# To keep track and inform the user
changed = updatePDFs(scripts, ls)

if not changed:
    changed = initialize(scripts)
    if not changed:
        print("You were all up to date nothing happened.")
