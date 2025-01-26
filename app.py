from flask import Flask, jsonify, request, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Example URLs for different subjects (Update with actual URLs)
URLs = {
    "English 2nd Language": [
        "https://kseebsolutions.guru/kseeb-solutions-for-class-5-english-prose-chapter-1/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-5-english-prose-chapter-2/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-5-english-prose-chapter-3/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-5-english-prose-chapter-4/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-5-english-prose-chapter-5/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-5-english-prose-chapter-6/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-5-english-prose-chapter-7/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-5-english-prose-chapter-8/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-5-english-poem-chapter-1/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-5-english-poem-chapter-2/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-5-english-poem-chapter-3/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-5-english-poem-chapter-4/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-5-english-poem-chapter-5/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-5-english-poem-chapter-6/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-5-english-poem-chapter-7/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-5-english-poem-chapter-8/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-english-prose-chapter-1/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-english-prose-chapter-2/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-english-prose-chapter-3/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-english-prose-chapter-4/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-english-prose-chapter-5/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-english-prose-chapter-6/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-english-prose-chapter-7/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-english-prose-chapter-8/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-english-poem-chapter-1/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-english-poem-chapter-2/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-english-poem-chapter-3/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-english-poem-chapter-4/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-english-poem-chapter-5/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-english-poem-chapter-6/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-english-poem-chapter-7/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-english-poem-chapter-8/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-7-english-prose-chapter-1/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-7-english-prose-chapter-2/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-7-english-prose-chapter-3/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-7-english-prose-chapter-4/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-7-english-prose-chapter-5/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-7-english-prose-chapter-6/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-7-english-prose-chapter-7/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-7-english-prose-chapter-8/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-7-english-poem-chapter-1/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-7-english-poem-chapter-2/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-7-english-poem-chapter-3/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-7-english-poem-chapter-4/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-7-english-poem-chapter-5/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-7-english-poem-chapter-6/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-7-english-poem-chapter-7/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-7-english-poem-chapter-8/",
    "https://kseebsolutions.guru/kseeb-solutions-class-8-english-chapter-1/",
    "https://kseebsolutions.guru/kseeb-solutions-class-8-english-chapter-2/",
    "https://kseebsolutions.guru/kseeb-solutions-class-8-english-chapter-3/",
    "https://kseebsolutions.guru/kseeb-solutions-class-8-english-chapter-4/",
    "https://kseebsolutions.guru/kseeb-solutions-class-8-english-chapter-5/",
    "https://kseebsolutions.guru/kseeb-solutions-class-8-english-chapter-6/",
    "https://kseebsolutions.guru/kseeb-solutions-class-8-english-chapter-7/",
    "https://kseebsolutions.guru/kseeb-solutions-class-8-english-chapter-8/",
    "https://kseebsolutions.guru/kseeb-solutions-class-8-english-poem-chapter-1/",
    "https://kseebsolutions.guru/kseeb-solutions-class-8-english-poem-chapter-2/",
    "https://kseebsolutions.guru/kseeb-solutions-class-8-english-poem-chapter-3/",
    "https://kseebsolutions.guru/kseeb-solutions-class-8-english-poem-chapter-4/",
    "https://kseebsolutions.guru/kseeb-solutions-class-8-english-poem-chapter-5/",
    "https://kseebsolutions.guru/kseeb-solutions-class-8-english-poem-chapter-6/",
    "https://kseebsolutions.guru/kseeb-solutions-class-8-english-poem-chapter-7/",
    "https://kseebsolutions.guru/kseeb-solutions-class-8-english-poem-chapter-8/"
    ],
    "EVS": [
        "https://kseebsolutions.guru/kseeb-solutions-for-class-5-evs-chapter-1/",
        "https://kseebsolutions.guru/kseeb-solutions-for-class-5-evs-chapter-2/",
        "https://kseebsolutions.guru/kseeb-solutions-for-class-5-evs-chapter-3/",
        "https://kseebsolutions.guru/kseeb-solutions-for-class-5-evs-chapter-4/",
        "https://kseebsolutions.guru/kseeb-solutions-for-class-5-evs-chapter-5/",
        "https://kseebsolutions.guru/kseeb-solutions-for-class-5-evs-chapter-6/",
        "https://kseebsolutions.guru/kseeb-solutions-for-class-5-evs-chapter-7/",
        "https://kseebsolutions.guru/kseeb-solutions-for-class-5-evs-chapter-8/",
        "https://kseebsolutions.guru/kseeb-solutions-for-class-5-evs-chapter-9/",
        "https://kseebsolutions.guru/kseeb-solutions-for-class-5-evs-chapter-10/",
        "https://kseebsolutions.guru/kseeb-solutions-for-class-5-evs-chapter-11/",
        "https://kseebsolutions.guru/kseeb-solutions-for-class-5-evs-chapter-12/",
        "https://kseebsolutions.guru/kseeb-solutions-for-class-5-evs-chapter-13/",
        "https://kseebsolutions.guru/kseeb-solutions-for-class-5-evs-chapter-14/",
        "https://kseebsolutions.guru/kseeb-solutions-for-class-5-evs-chapter-15/",
        "https://kseebsolutions.guru/kseeb-solutions-for-class-5-evs-chapter-16/"
    ],
    "Maths": [
        "https://kseebsolutions.guru/kseeb-solutions-for-class-5-maths-chapter-1-part-1/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-5-maths-chapter-2-part-1/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-5-maths-chapter-3-part-1/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-5-maths-chapter-4-part-1/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-5-maths-chapter-5-part-1/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-5-maths-chapter-6-part-1/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-5-maths-chapter-7-part-1/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-5-maths-chapter-8-part-1/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-5-maths-chapter-9-part-1/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-5-maths-chapter-10-part-1/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-5-maths-chapter-1-part-2/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-5-maths-chapter-2-part-2/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-5-maths-chapter-3-part-2/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-5-maths-chapter-4-part-2/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-5-maths-chapter-5-part-2/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-5-maths-chapter-6-part-2/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-5-maths-chapter-7-part-2/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-5-maths-chapter-8-part-2/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-5-maths-chapter-9-part-2/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-5-maths-chapter-10-part-2/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-1-ex-1-1/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-1-ex-1-2/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-1-ex-1-3/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-2-ex-2-1/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-2-ex-2-2/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-2-ex-2-3/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-3-ex-3-1/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-3-ex-3-2/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-3-ex-3-3/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-3-ex-3-4/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-3-ex-3-5/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-3-ex-3-6/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-3-ex-3-7/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-4-ex-4-1/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-4-ex-4-2/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-4-ex-4-3/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-4-ex-4-5/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-4-ex-4-6/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-5-ex-5-1/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-5-ex-5-2/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-5-ex-5-3/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-5-ex-5-4/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-5-ex-5-5/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-5-ex-5-6/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-5-ex-5-7/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-6-ex-6-1/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-6-ex-6-2/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-6-ex-6-3/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-7-ex-7-1/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-7-ex-7-2/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-7-ex-7-3/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-7-ex-7-4/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-7-ex-7-5/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-7-ex-7-6/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-8-ex-8-1/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-8-ex-8-2/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-8-ex-8-3/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-8-ex-8-4/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-8-ex-8-5/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-8-ex-8-6/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-9-ex-9-1/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-9-ex-9-2/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-9-ex-9-3/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-9-ex-9-4/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-10-ex-10-1/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-10-ex-10-2/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-10-ex-10-3/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-11-ex-11-1/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-11-ex-11-2/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-11-ex-11-3/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-11-ex-11-4/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-11-ex-11-5/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-12-ex-12-1/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-12-ex-12-2/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-12-ex-12-3/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-13-ex-13-1/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-13-ex-13-2/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-13-ex-13-3/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-14-ex-14-1/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-14-ex-14-2/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-14-ex-14-3/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-14-ex-14-4/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-14-ex-14-5/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-maths-chapter-14-ex-14-6/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-1-ex-1-1/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-1-ex-1-2/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-1-ex-1-3/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-1-ex-1-4/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-2-ex-2-1/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-2-ex-2-2/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-2-ex-2-3/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-2-ex-2-4/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-2-ex-2-5/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-2-ex-2-6/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-2-ex-2-7/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-3-ex-3-1/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-3-ex-3-2/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-3-ex-3-3/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-3-ex-3-4/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-4-ex-4-1/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-4-ex-4-2/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-4-ex-4-3/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-4-ex-4-4/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-5-ex-5-1/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-5-ex-5-2/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-6-ex-6-1/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-6-ex-6-2/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-6-ex-6-3/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-6-ex-6-4/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-6-ex-6-5/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-7-ex-7-1/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-7-ex-7-2/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-8-ex-8-1/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-8-ex-8-2/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-8-ex-8-3/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-9-ex-9-1/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-9-ex-9-2/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-10-ex-10-1/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-10-ex-10-2/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-10-ex-10-3/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-10-ex-10-4/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-10-ex-10-5/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-11-ex-11-1/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-11-ex-11-2/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-11-ex-11-3/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-11-ex-11-4/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-12-ex-12-1/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-12-ex-12-2/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-12-ex-12-3/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-12-ex-12-4/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-13-ex-13-1/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-13-ex-13-2/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-13-ex-13-3/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-14-ex-14-1/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-14-ex-14-2/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-14-ex-14-3/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-15-ex-15-1/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-15-ex-15-2/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-15-ex-15-3/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-maths-chapter-15-ex-15-4/",
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-1-ex-1-1/",
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-1-ex-1-2/",
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-1-intext-questions/",
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-2-ex-2-1/",
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-2-ex-2-2/",
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-2-ex-2-3/",
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-2-ex-2-4/",
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-2-ex-2-5/",
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-2-ex-2-6/",
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-3-ex-3-1/",
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-3-ex-3-2/",
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-3-ex-3-3/",
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-3-ex-3-4/",
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-3-intext-questions/",
    "https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-4-ex-4-1/",  
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-4-ex-4-2/"  ,
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-4-ex-4-3/"  ,
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-4-ex-4-4/"  ,
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-4-ex-4-5/"  ,
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-4-intext-questions/",  
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-5-ex-5-1/"  ,
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-5-ex-5-2/"  ,
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-5-ex-5-3/"  ,
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-5-intext-questions/",  
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-6-ex-6-1/"  ,
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-6-ex-6-2/"  ,
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-6-ex-6-3/"  ,
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-6-ex-6-4/"  ,
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-6-intext-questions/",  
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-7-ex-7-1/"  ,
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-7-ex-7-2/"  ,
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-7-intext-questions/",  
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-8-ex-8-1/"  ,
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-8-ex-8-2/"  ,
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-8-ex-8-3/"  ,
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-8-intext-questions/"  ,
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-9-ex-9-1/"  ,
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-9-ex-9-2/"  ,
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-9-ex-9-3/"  ,
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-9-ex-9-4/"  ,
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-9-ex-9-5/"  ,
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-9-intext-questions/",  
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-10-ex-10-1/"  ,
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-10-ex-10-2/"  ,
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-10-ex-10-3/"  ,
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-11-ex-11-1/"  ,
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-11-ex-11-2/"  ,
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-11-ex-11-3/"  ,
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-11-ex-11-4/"  ,
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-11-intext-questions/",  
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-12-ex-12-1/"  ,
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-12-ex-12-2/"  ,
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-12-intext-questions/",  
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-13-ex-13-1/"  ,
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-13-ex-13-2/"  ,
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-13-intext-questions/",  
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-14-ex-14-1/"  ,
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-14-ex-14-2/"  ,
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-14-ex-14-3/"  ,
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-14-ex-14-4/"  ,
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-14-intext-questions/",  
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-15-ex-15-1/"  ,
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-15-ex-15-2/"  ,
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-15-ex-15-3/"  ,
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-15-intext-questions/"  ,
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-16-ex-16-1/"  ,
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-16-ex-16-2/"  ,
"https://ktbssolutions.com/kseeb-solutions-for-class-8-maths-chapter-16-intext-questions/"
    ],
    "Social Science": [
        "https://kseebsolutions.guru/kseeb-solutions-for-class-6-social-science-chapter-1-part-1/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-social-science-chapter-2-part-1/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-social-science-chapter-3-part-1/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-social-science-chapter-4-part-1/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-social-science-chapter-5-part-1/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-social-science-chapter-6-part-1/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-social-science-chapter-7-part-1/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-social-science-chapter-8-part-1/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-social-science-chapter-9-part-1/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-social-science-chapter-10-part-1/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-social-science-chapter-1-part-2/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-social-science-chapter-2-part-2/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-social-science-chapter-3-part-2/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-social-science-chapter-4-part-2/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-social-science-chapter-5-part-2/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-social-science-chapter-6-part-2/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-social-science-chapter-7-part-2/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-social-science-chapter-8-part-2/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-social-science-chapter-9-part-2/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-social-science-chapter-10-part-2/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-7-social-science-chapter-1/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-7-social-science-chapter-2/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-7-social-science-chapter-3/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-7-social-science-chapter-4/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-7-social-science-chapter-5/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-7-social-science-chapter-6/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-7-social-science-chapter-7/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-7-social-science-chapter-8/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-7-social-science-chapter-9/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-7-social-science-chapter-10/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-7-social-science-chapter-11/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-7-social-science-chapter-12/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-7-social-science-chapter-13/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-7-social-science-chapter-14/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-7-social-science-chapter-15/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-7-social-science-chapter-16/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-7-social-science-chapter-17/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-7-social-science-chapter-18/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-7-social-science-chapter-19/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-7-social-science-chapter-20/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-7-social-science-chapter-21/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-7-social-science-chapter-22/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-7-social-science-chapter-23/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-7-social-science-chapter-24/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-7-social-science-chapter-25/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-7-social-science-chapter-26/"],

   "History":[ "https://kseebsolutions.guru/kseeb-solutions-class-8-history-chapter-1/",  
"https://kseebsolutions.guru/kseeb-solutions-class-8-history-chapter-2/",  
"https://kseebsolutions.guru/kseeb-solutions-class-8-history-chapter-3/",  
"https://kseebsolutions.guru/kseeb-solutions-class-8-history-chapter-4/",  
"https://kseebsolutions.guru/kseeb-solutions-class-8-history-chapter-5/",  
"https://kseebsolutions.guru/kseeb-solutions-class-8-history-chapter-6/",  
"https://kseebsolutions.guru/kseeb-solutions-class-8-history-chapter-7/",  
"https://kseebsolutions.guru/kseeb-solutions-class-8-history-chapter-8/",  
"https://kseebsolutions.guru/kseeb-solutions-class-8-history-chapter-9/",  
"https://kseebsolutions.guru/kseeb-solutions-class-8-history-chapter-10/",  
"https://kseebsolutions.guru/kseeb-solutions-class-8-history-chapter-11/",  
"https://kseebsolutions.guru/kseeb-solutions-class-8-history-chapter-12/"],
  "Political science":["https://kseebsolutions.guru/kseeb-solutions-class-8-political-science-chapter-1/",  
"https://kseebsolutions.guru/kseeb-solutions-class-8-political-science-chapter-2/",  
"https://kseebsolutions.guru/kseeb-solutions-class-8-political-science-chapter-3/",  
"https://kseebsolutions.guru/kseeb-solutions-class-8-political-science-chapter-4/"],
"Sociology":[
"https://kseebsolutions.guru/kseeb-solutions-class-8-sociology-chapter-1/",  
"https://kseebsolutions.guru/kseeb-solutions-class-8-sociology-chapter-2/",  
"https://kseebsolutions.guru/kseeb-solutions-class-8-sociology-chapter-3/",  
"https://kseebsolutions.guru/kseeb-solutions-class-8-sociology-chapter-4/"],
"Geography":[
"https://kseebsolutions.guru/kseeb-solutions-class-8-geography-chapter-1/",  
"https://kseebsolutions.guru/kseeb-solutions-class-8-geography-chapter-2/",  
"https://kseebsolutions.guru/kseeb-solutions-class-8-geography-chapter-3/",  
"https://kseebsolutions.guru/kseeb-solutions-class-8-geography-chapter-4/",  
"https://kseebsolutions.guru/kseeb-solutions-class-8-geography-chapter-5/"],  
"Economics":[
"https://kseebsolutions.guru/kseeb-solutions-class-8-economics-chapter-1/",  
"https://kseebsolutions.guru/kseeb-solutions-class-8-economics-chapter-2/",  
"https://kseebsolutions.guru/kseeb-solutions-class-8-economics-chapter-3/",  
"https://kseebsolutions.guru/kseeb-solutions-class-8-economics-chapter-4/",  
"https://kseebsolutions.guru/kseeb-solutions-class-8-economics-chapter-5/"],  
"Business studies":[
"https://kseebsolutions.guru/kseeb-solutions-class-8-business-studies-chapter-1/",  
"https://kseebsolutions.guru/kseeb-solutions-class-8-business-studies-chapter-2/",  
"https://kseebsolutions.guru/kseeb-solutions-class-8-business-studies-chapter-3/"
    ],
    "Science": [
        "https://kseebsolutions.guru/kseeb-solutions-for-class-6-science-chapter-1/",  
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-science-chapter-2/",  
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-science-chapter-3/",  
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-science-chapter-4/",  
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-science-chapter-5/",  
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-science-chapter-6/",  
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-science-chapter-7/",  
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-science-chapter-8/",  
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-science-chapter-9/",  
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-science-chapter-10/",  
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-science-chapter-11/",  
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-science-chapter-12/",  
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-science-chapter-13/",  
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-science-chapter-14/",  
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-science-chapter-15/",  
    "https://kseebsolutions.guru/kseeb-solutions-for-class-6-science-chapter-16/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-7-science-chapter-1/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-science-chapter-2/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-science-chapter-3/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-science-chapter-4/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-science-chapter-5/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-science-chapter-6/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-science-chapter-7/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-science-chapter-8/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-science-chapter-9/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-science-chapter-10/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-science-chapter-11/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-science-chapter-12/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-science-chapter-13/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-science-chapter-14/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-science-chapter-15/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-science-chapter-16/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-science-chapter-17/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-7-science-chapter-18/",
    "https://ktbssolutions.com/kseeb-solutions-for-class-8-science-chapter-1/",  
"https://ktbssolutions.com/kseeb-solutions-for-class-8-science-chapter-2/",  
"https://ktbssolutions.com/kseeb-solutions-for-class-8-science-chapter-3/",  
"https://ktbssolutions.com/kseeb-solutions-for-class-8-science-chapter-4/",  
"https://ktbssolutions.com/kseeb-solutions-for-class-8-science-chapter-5/",  
"https://ktbssolutions.com/kseeb-solutions-for-class-8-science-chapter-6/",  
"https://ktbssolutions.com/kseeb-solutions-for-class-8-science-chapter-7/",  
"https://ktbssolutions.com/kseeb-solutions-for-class-8-science-chapter-8/",  
"https://ktbssolutions.com/kseeb-solutions-for-class-8-science-chapter-9/",  
"https://ktbssolutions.com/kseeb-solutions-for-class-8-science-chapter-10/",  
"https://ktbssolutions.com/kseeb-solutions-for-class-8-science-chapter-11/",  
"https://ktbssolutions.com/kseeb-solutions-for-class-8-science-chapter-12/",  
"https://ktbssolutions.com/kseeb-solutions-for-class-8-science-chapter-13/",  
"https://ktbssolutions.com/kseeb-solutions-for-class-8-science-chapter-14/",  
"https://ktbssolutions.com/kseeb-solutions-for-class-8-science-chapter-15/",  
"https://ktbssolutions.com/kseeb-solutions-for-class-8-science-chapter-16/",  
"https://ktbssolutions.com/kseeb-solutions-for-class-8-science-chapter-17/",  
"https://ktbssolutions.com/kseeb-solutions-for-class-8-science-chapter-18/"
    ],
    "English 1st Language": [
        "https://kseebsolutions.guru/kseeb-solutions-class-5-english-prose-chapter-1/",  
"https://kseebsolutions.guru/kseeb-solutions-class-5-english-prose-chapter-2/",  
"https://kseebsolutions.guru/kseeb-solutions-class-5-english-prose-chapter-3/",  
"https://kseebsolutions.guru/kseeb-solutions-class-5-english-prose-chapter-4/",  
"https://kseebsolutions.guru/kseeb-solutions-class-5-english-prose-chapter-5/",  
"https://kseebsolutions.guru/kseeb-solutions-class-5-english-prose-chapter-6/",  
"https://kseebsolutions.guru/kseeb-solutions-class-5-english-prose-chapter-7/",  
"https://kseebsolutions.guru/kseeb-solutions-class-5-english-prose-chapter-8/",  
"https://kseebsolutions.guru/kseeb-solutions-class-5-english-prose-chapter-9/",  
"https://kseebsolutions.guru/kseeb-solutions-class-5-english-prose-chapter-10/",
     "https://kseebsolutions.guru/kseeb-solutions-class-5-english-poem-chapter-1/",  
"https://kseebsolutions.guru/kseeb-solutions-class-5-english-poem-chapter-2/",  
"https://kseebsolutions.guru/kseeb-solutions-class-5-english-poem-chapter-3/",  
"https://kseebsolutions.guru/kseeb-solutions-class-5-english-poem-chapter-4/",  
"https://kseebsolutions.guru/kseeb-solutions-class-5-english-poem-chapter-5/",  
"https://kseebsolutions.guru/kseeb-solutions-class-5-english-poem-chapter-6/",  
"https://kseebsolutions.guru/kseeb-solutions-class-5-english-poem-chapter-7/",  
"https://kseebsolutions.guru/kseeb-solutions-class-5-english-poem-chapter-8/",  
"https://kseebsolutions.guru/kseeb-solutions-class-5-english-poem-chapter-9/",  
"https://kseebsolutions.guru/kseeb-solutions-class-5-english-poem-chapter-10/",
     "https://kseebsolutions.guru/kseeb-solutions-class-6-english-prose-chapter-1/",  
"https://kseebsolutions.guru/kseeb-solutions-class-6-english-prose-chapter-2/",  
"https://kseebsolutions.guru/kseeb-solutions-class-6-english-prose-chapter-3/",  
"https://kseebsolutions.guru/kseeb-solutions-class-6-english-prose-chapter-4/",  
"https://kseebsolutions.guru/kseeb-solutions-class-6-english-prose-chapter-5/",  
"https://kseebsolutions.guru/kseeb-solutions-class-6-english-prose-chapter-6/",  
"https://kseebsolutions.guru/kseeb-solutions-class-6-english-prose-chapter-7/",  
"https://kseebsolutions.guru/kseeb-solutions-class-6-english-prose-chapter-8/",  
"https://kseebsolutions.guru/kseeb-solutions-class-6-english-prose-chapter-9/",  
"https://kseebsolutions.guru/kseeb-solutions-class-6-english-prose-chapter-10/",
     "https://kseebsolutions.guru/kseeb-solutions-class-6-english-poem-chapter-1/",  
"https://kseebsolutions.guru/kseeb-solutions-class-6-english-poem-chapter-2/",  
"https://kseebsolutions.guru/kseeb-solutions-class-6-english-poem-chapter-3/",  
"https://kseebsolutions.guru/kseeb-solutions-class-6-english-poem-chapter-4/",  
"https://kseebsolutions.guru/kseeb-solutions-class-6-english-poem-chapter-5/",  
"https://kseebsolutions.guru/kseeb-solutions-class-6-english-poem-chapter-6/",  
"https://kseebsolutions.guru/kseeb-solutions-class-6-english-poem-chapter-7/",  
"https://kseebsolutions.guru/kseeb-solutions-class-6-english-poem-chapter-8/",  
"https://kseebsolutions.guru/kseeb-solutions-class-6-english-poem-chapter-9/",  
"https://kseebsolutions.guru/kseeb-solutions-class-6-english-poem-chapter-10/",
     "https://kseebsolutions.guru/kseeb-solutions-class-7-english-prose-chapter-1/",  
"https://kseebsolutions.guru/kseeb-solutions-class-7-english-prose-chapter-2/",  
"https://kseebsolutions.guru/kseeb-solutions-class-7-english-prose-chapter-3/",  
"https://kseebsolutions.guru/kseeb-solutions-class-7-english-prose-chapter-4/",  
"https://kseebsolutions.guru/kseeb-solutions-class-7-english-prose-chapter-5/",  
"https://kseebsolutions.guru/kseeb-solutions-class-7-english-prose-chapter-6/",  
"https://kseebsolutions.guru/kseeb-solutions-class-7-english-prose-chapter-7/",  
"https://kseebsolutions.guru/kseeb-solutions-class-7-english-prose-chapter-8/",
     "https://kseebsolutions.guru/kseeb-solutions-class-7-english-poem-chapter-1/",  
"https://kseebsolutions.guru/kseeb-solutions-class-7-english-poem-chapter-2/",  
"https://kseebsolutions.guru/kseeb-solutions-class-7-english-poem-chapter-3/",  
"https://kseebsolutions.guru/kseeb-solutions-class-7-english-poem-chapter-4/",  
"https://kseebsolutions.guru/kseeb-solutions-class-7-english-poem-chapter-5/",  
"https://kseebsolutions.guru/kseeb-solutions-class-7-english-poem-chapter-6/",  
"https://kseebsolutions.guru/kseeb-solutions-class-7-english-poem-chapter-7/",  
"https://kseebsolutions.guru/kseeb-solutions-class-7-english-poem-chapter-8/",
"https://kseebsolutions.guru/kseeb-solutions-for-class-8-english-prose-chapter-1/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-8-english-prose-chapter-2/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-8-english-prose-chapter-3/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-8-english-prose-chapter-4/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-8-english-prose-chapter-5/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-8-english-prose-chapter-6/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-8-english-prose-chapter-7/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-8-english-prose-chapter-8/",
    "https://kseebsolutions.guru/kseeb-solutions-for-class-8-english-poem-chapter-9/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-8-english-poem-chapter-10/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-8-english-poem-chapter-11/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-8-english-poem-chapter-12/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-8-english-poem-chapter-13/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-8-english-poem-chapter-14/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-8-english-poem-chapter-15/",  
"https://kseebsolutions.guru/kseeb-solutions-for-class-8-english-poem-chapter-16/"
    ],
}

UNWANTED_IMAGE_URLS = [
    "https://kseebsolutions.guru/wp-content/uploads/2019/11/KSEEB-Solutions-300x28.png",
    "https://ktbssolutions.com/wp-content/uploads/2021/05/KTBS-Solutions.png",
    "https://kseebsolutions.guru/wp-content/uploads/2019/11/KSEEB-Solutions.png",
]

def scrape_chapter_content(url):
    """Scrape the content of a chapter."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise error for bad responses
        soup = BeautifulSoup(response.content, 'html5lib')
        content_div = soup.find('div', {'class': 'entry-content'})

        if not content_div:
            return []

        content = []
        for child in content_div.descendants:
            if child.name == 'p':
                text = child.get_text()
                if text:
                    content.append({'type': 'text', 'data': text.strip()})
            elif child.name == 'img':
                img_url = child.get('src')
                if img_url and img_url not in UNWANTED_IMAGE_URLS:
                    content.append({'type': 'image', 'data': img_url})
            elif child.name == 'table':
                table_data = [[cell.get_text(strip=True) for cell in row.find_all(['td', 'th'])] for row in child.find_all('tr')]
                content.append({'type': 'table', 'data': table_data})

        return content
    except requests.exceptions.RequestException as e:
        print(f"Error while scraping {url}: {e}")
        return []

def get_matching_url(subject, class_number, content_type, chapter, part, exercise):
    """Find the matching URL based on subject and criteria."""
    def normalize_part(part):
        roman_to_int = {
            "I": "1", "II": "2", "III": "3", "IV": "4", "V": "5",
            "VI": "6", "VII": "7", "VIII": "8", "IX": "9", "X": "10"
        }
        return roman_to_int.get(part.upper(), part)

    normalized_part = normalize_part(part) if part else None
    urls = URLs.get(subject, [])

    # Iterate over the URLs to find the matching one
    for u in urls:
        if f"class-{class_number}" in u:
            if content_type and content_type.lower() not in u:
                continue
            if chapter and f"chapter-{chapter}" in u:
                if normalized_part and f"part-{normalized_part}" in u:
                    return u
                if exercise and f"ex-{exercise.replace('.', '-').lower()}" in u:
                    return u
                if not part and not exercise:
                    return u
    return None


@app.before_request
def log_request_info():
    app.logger.debug(f"Request: {request.method} {request.url}")

@app.route('/')
def index():
    """Serve the frontend."""
    return render_template('Edu.html')
@app.route('/courses')
def courses():
    return render_template('courses.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/class-5')
def class5():
    return render_template('class5.html')
@app.route('/class-6')
def class6():
    return render_template('class6.html')
@app.route('/class-7')
def class7():
    return render_template('class7.html')
@app.route('/class-8')
def class8():
    return render_template('class8.html')
@app.route('/contact')
def contact():
    return render_template('contact.html')
@app.route('/class-5/English 1st Language')
def engc51():
    return render_template('engc51.html')
@app.route('/class-5/English 2nd Language')
def engc52():
    return render_template('engc52.html')
@app.route('/class-5/Maths')
def mathc5():
    return render_template('mathc5.html')
@app.route('/class-5/EVS')
def evs():
    return render_template('evs.html')
@app.route('/class-5/English 1st Language/Poem')
def Poem():
    return render_template('poem.html')
@app.route('/class-5/English 1st Language/Prose')
def Prose():
    return render_template('prose.html')
@app.route('/class-5/English 2nd Language/Poem')
def Poem1():
    return render_template('poem.html')
@app.route('/class-5/English 2nd Language/Prose')
def Prose1():
    return render_template('prose.html')
@app.route('/class-5/Maths/PartI')
def part1():
    return render_template('part1.html')
@app.route('/class-5/Maths/PartII')
def part2():
    return render_template('part2.html')

@app.route('/class-6/English 1st Language')
def englishc61():
    return render_template('englishc61.html')
@app.route('/class-6/English 2nd Language')
def englishc62():
    return render_template('englishc62.html')
@app.route('/class-6/English 1st Language/Poem')
def poem2():
    return render_template('poem1.html')
@app.route('/class-6/English 1st Language/Prose')
def prose2():
    return render_template('prose1.html')
@app.route('/class-6/English 2nd Language/Prose')
def poem3():
    return render_template('poem1.html')
@app.route('/class-6/English 2nd Language/Prose')
def prose3():
    return render_template('prose1.html')
@app.route('/class-6/Maths')
def mathsc6():
    return render_template('mathsc6.html')
@app.route('/class-6/Science')
def sciencec6():
    return render_template('sciencec6.html')
@app.route('/class-6/Social Science')
def socialc6():
    return render_template('socialc6.html')
@app.route('/class-6/Social Science/Part I')
def part11():
    return render_template('part11.html')
@app.route('/class-6/Social Science/Part II')
def part22():
    return render_template('part22.html')

@app.route('/class-7/English 1st Language')
def englishc71():
    return render_template('englishc71.html')
@app.route('/class-7/English 2nd Language')
def englishc72():
    return render_template('englishc72.html')
@app.route('/class-7/Maths')
def mathc7():
    return render_template('mathc7.html')
@app.route('/class-7/Science')
def sciencec7():
    return render_template('sciencec7.html')
@app.route('/class-7/Social Science')
def socialc7():
    return render_template('socialc7.html')
@app.route('/class-7/English 1st Language/Poem')
def poem4():
    return render_template('poem2.html')
@app.route('/class-7/English 1st Language/Prose')
def prose4():
    return render_template('prose2.html')
@app.route('/class-7/English 1st Language/Poem')
def poem5():
    return render_template('poem2.html')
@app.route('/class-7/English 1st Language/Prose')
def prose5():
    return render_template('prose2.html')

@app.route('/class-8/English 1st Language')
def englishc81():
    return render_template('englishc81.html')
@app.route('/class-8/English 2nd Language')
def englishc82():
    return render_template('englishc82.html')
@app.route('/class-8/Maths')
def mathc8():
    return render_template('mathc8.html')
@app.route('/class-8/Science')
def sciencec8():
    return render_template('sciencec8.html')
@app.route('/class-8/History')
def hisc8():
    return render_template('hisc8.html')
@app.route('/class-8/Political science')
def polc8():
    return render_template('polc8.html')
@app.route('/class-8/Sociology')
def sociologyc8():
    return render_template('sociologyc8.html')
@app.route('/class-8/Geography')
def geoc8():
    return render_template('geoc8.html')
@app.route('/class-8/Economics')
def ecoc8():
    return render_template('ecoc8.html')
@app.route('/class-8/Business studies')
def buic8():
    return render_template('buic8.html')
@app.route('/class-8/English 1st Language/Poem')
def poem6():
    return render_template('poem.html')
@app.route('/class-8/English 1st Language/Prose')
def prose6():
    return render_template('prose.html')
@app.route('/class-8/English 2nd Language/Poem')
def poem7():
    return render_template('poem.html')
@app.route('/class-8/English 2nd Language/Prose')
def prose7():
    return render_template('prose.html')


@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.json
    app.logger.debug(f"Received data: {data}")
    class_number = data.get('class')
    subject = data.get('subject')
    content_type = data.get('content_type')
    chapter = data.get('chapter')
    part = data.get('part')
    exercise = data.get('exercise')

    # Get the matching URL
    url = get_matching_url(subject, class_number, content_type, chapter, part, exercise)

    if not url:
        return jsonify({"error": "No matching URL found"}), 404

    # Scrape the content
    content = scrape_chapter_content(url)
    if not content:
        return jsonify({"error": "No content found or error during scraping"}), 500

    return jsonify(content)

if __name__ == '__main__':
    app.run(debug=True)

       
