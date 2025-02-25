import re
from flask import Flask, jsonify, request, render_template
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import markdown
import os
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

def clean_text(text):
    """Clean and normalize text content."""
    # Remove extra whitespace and normalize spaces
    text = ' '.join(text.split())
    # Remove common unwanted patterns
    text = re.sub(r'\[click\s+here.*?\]', '', text, flags=re.IGNORECASE)
    text = re.sub(r'download\s+pdf.*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'advertisement', '', text, flags=re.IGNORECASE)
    return text.strip()

def is_question(text):
    """Determine if text is a question."""
    text_lower = text.lower().strip()
    # Check for question mark or question starters
    question_starters = [
        'what', 'why', 'how', 'when', 'where', 'which', 'who',
        'explain', 'describe', 'discuss', 'evaluate', 'compare',
        'analyze', 'define', 'identify', 'list', 'state', 'write',
        'fill in', 'choose', 'match', 'solve', 'calculate'
    ]
    
    # Check if text starts with a number followed by a dot or parenthesis
    starts_with_number = bool(re.match(r'^\d+[\.\)]', text))
    
    return (
        text.strip().endswith('?') or
        any(text_lower.startswith(q) for q in question_starters) or
        starts_with_number
    )

def is_answer(text):
    """Determine if text is an answer."""
    text_lower = text.lower().strip()
    answer_starters = [
        'answer:', 'ans:', 'solution:', 'sol:',
        'a)', 'b)', 'c)', 'd)', 
        'a.', 'b.', 'c.', 'd.'
    ]
    
    # Check if it starts with "Answer" or similar
    starts_with_answer = any(text_lower.startswith(starter.lower()) for starter in answer_starters)
    
    # Check if it's a numbered/lettered response pattern
    is_option = bool(re.match(r'^[(]?[a-d][).]\s', text_lower))
    
    return starts_with_answer or is_option

def scrape_chapter_content(url):
    """Scrape the content of a chapter with improved table and Q&A handling."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html5lib')
        content_div = soup.find('div', {'class': 'entry-content'})

        if not content_div:
            return []

        content = []
        seen_text = set()
        seen_images = set()

        # Remove unwanted elements
        for script in content_div.find_all(['script', 'ins']):
            script.decompose()

        def process_table(table):
            """Process a table element and return structured data"""
            table_data = {'header': [], 'rows': []}
            
            # Process header
            header_row = table.find('thead')
            if header_row:
                header_cells = header_row.find_all(['th', 'td'])
                table_data['header'] = [clean_text(cell.get_text()) for cell in header_cells]
            
            # If no thead, use first row as header
            if not table_data['header'] and table.find('tr'):
                first_row = table.find('tr')
                header_cells = first_row.find_all(['th', 'td'])
                table_data['header'] = [clean_text(cell.get_text()) for cell in header_cells]
                rows = table.find_all('tr')[1:]  # Skip first row as it's header
            else:
                rows = table.find_all('tr')
            
            # Process rows
            for row in rows:
                cells = row.find_all(['td', 'th'])
                row_data = [clean_text(cell.get_text()) for cell in cells]
                if any(row_data):  # Only add row if it contains data
                    table_data['rows'].append(row_data)
            
            return table_data

        def process_element(element):
            if isinstance(element, str):
                text = clean_text(element)
                if text and text not in seen_text and not 'adpushup' in text:
                    seen_text.add(text)
                    if text.startswith('Question'):
                        content.append({'type': 'text', 'format': 'question', 'data': text})
                    elif text.startswith('Answer'):
                        content.append({'type': 'text', 'format': 'answer', 'data': text})
                    else:
                        content.append({'type': 'text', 'format': 'normal', 'data': text})
                return

            if not hasattr(element, 'name'):
                return

            # Handle tables
            if element.name == 'table':
                table_data = process_table(element)
                if table_data['rows']:  # Only add if table has data
                    content.append({'type': 'table', 'data': table_data})
                return

            if element.name == 'img':
                img_url = element.get('data-lazy-src') or element.get('data-src') or element.get('src', '')
                if img_url:
                    img_url = img_url.strip()
                    if (img_url and 
                        img_url not in UNWANTED_IMAGE_URLS and 
                        img_url not in seen_images and 
                        not img_url.endswith(('.gif', '.svg')) and
                        'logo' not in img_url.lower()):
                        seen_images.add(img_url)
                        content.append({'type': 'image', 'data': img_url})

            elif element.name in ['p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                # First process any tables within this element
                for table in element.find_all('table', recursive=False):
                    process_element(table)
                
                text = clean_text(element.get_text())
                if text and text not in seen_text and not 'adpushup' in text:
                    seen_text.add(text)
                    if text.startswith('Question'):
                        content.append({'type': 'text', 'format': 'question', 'data': text})
                    elif text.startswith('Answer'):
                        content.append({'type': 'text', 'format': 'answer', 'data': text})
                    else:
                        content.append({'type': 'text', 'format': 'normal', 'data': text})
                
                # Process images within this element
                for img in element.find_all('img', recursive=False):
                    process_element(img)

            elif element.name in ['ol', 'ul']:
                list_items = []
                for li in element.find_all('li', recursive=False):
                    text = clean_text(li.get_text())
                    if text and text not in seen_text and not 'adpushup' in text:
                        seen_text.add(text)
                        list_items.append(text)
                if list_items:
                    content.append({'type': 'list', 'data': list_items})

        # Process all elements in order
        for element in content_div.children:
            process_element(element)

        return content

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return []

def is_question(text):
    """Determine if text is a question."""
    text_lower = text.lower().strip()
    # Check for question mark or question starters
    question_starters = [
        'Question', 'what', 'why', 'how', 'when', 'where', 'which', 'who',
        'explain', 'describe', 'discuss', 'evaluate', 'compare',
        'analyze', 'define', 'identify', 'list', 'state', 'write',
        'fill in', 'choose', 'match', 'solve', 'calculate'
    ]
    
    # Check if text starts with a number followed by a dot or parenthesis
    starts_with_number = bool(re.match(r'^\d+[\.\)]', text))
    starts_with_question = text_lower.startswith('question')
    
    return (
        text.strip().endswith('?') or
        starts_with_question or
        starts_with_number or
        any(text_lower.startswith(q) for q in question_starters)
    )

def is_answer(text):
    """Determine if text is an answer."""
    text_lower = text.lower().strip()
    answer_starters = [
        'Answer:', 'answer:', 'ans:', 'solution:', 'sol:',
        'a)', 'b)', 'c)', 'd)', 
        'a.', 'b.', 'c.', 'd.'
    ]
    
    return any(text_lower.startswith(starter.lower()) for starter in answer_starters)


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
            # Handle content_type for English subjects
            if subject.lower() in ["english 1st language", "english 2nd language"]:
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
# Configure Gemini
# Load API key from environment variables
API_KEY = os.getenv("API_KEY")  

if not API_KEY:
    raise ValueError("API_KEY is not set. Make sure it's stored in the environment variables.")

# Configure Generative AI with the key
genai.configure(api_key=API_KEY)

# Create the model instance
model = genai.GenerativeModel('gemini-pro',
                              generation_config={
                                  'temperature': 0.7,
                                  'max_output_tokens': 2048,
                              })

# Start chat session
chat = model.start_chat(history=[])

@app.before_request
def log_request_info():
    app.logger.debug(f"Request: {request.method} {request.url}")

@app.route('/')
def index():
    """Serve the frontend."""
    return render_template('Edu.html')
@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        user_message = request.json['message']
        response = chat.send_message(user_message)
        # Convert markdown to HTML for better formatting
        formatted_response = markdown.markdown(response.text)
        return jsonify({'response': formatted_response})
    except Exception as e:
        return jsonify({'response': f"Error: {str(e)}"})
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
    return render_template('poem21.html')
@app.route('/class-5/English 2nd Language/Prose')
def Prose1():
    return render_template('prose21.html')
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
    return render_template('poem2.html')
@app.route('/class-6/English 1st Language/Prose')
def prose2():
    return render_template('prose2.html')
@app.route('/class-6/English 2nd Language/Prose')
def poem3():
    return render_template('poem2.html')
@app.route('/class-6/English 2nd Language/Prose')
def prose3():
    return render_template('prose2.html')
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
def poem22():
    return render_template('poem22.html')
@app.route('/class-7/English 1st Language/Prose')
def prose22():
    return render_template('prose22.html')
@app.route('/class-7/English 2nd Language/Poem')
def poem5():
    return render_template('poem22.html')
@app.route('/class-7/English 2nd Language/Prose')
def prose5():
    return render_template('prose22.html')

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
    return render_template('poem6.html')
@app.route('/class-8/English 1st Language/Prose')
def prose6():
    return render_template('prose6.html')
@app.route('/class-8/English 2nd Language/Poem')
def poem7():
    return render_template('poem6.html')
BASE_URL = "https://kseebsolutions.guru/kseeb-solutions-class-8-english-chapter-"

@app.route('/class-8/English 2nd Language/Prose', methods=['GET', 'POST'])
def prose223():
    if request.method == 'POST':
        # Check if the request is JSON
        if request.is_json:
            data = request.get_json()
            chapter = data.get('chapter')
        else:
            chapter = request.form.get('chapter')
        
        if not chapter:
            return jsonify({"error": "Chapter number is required."}), 400

        # Construct the full URL
        url = f"{BASE_URL}{chapter}/"
        
        # Fetch the content from the external URL
        response = requests.get(url)
        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch content from the external site."}), 500

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract the relevant content (e.g., the main article)
        content = soup.find('div', class_='entry-content')  # Adjust the selector as needed
        if not content:
            return jsonify({"error": "Content not found on the external site."}), 404

        # Format the content for display
        scraped_data = []
        for element in content.find_all(['p', 'img', 'table', 'ul', 'ol']):
            if element.name == 'p':
                scraped_data.append({"type": "text", "data": element.get_text(strip=True)})
            elif element.name == 'img':
                scraped_data.append({"type": "image", "data": element['src']})
            elif element.name == 'table':
                headers = [th.get_text(strip=True) for th in element.find_all('th')]
                rows = []
                for row in element.find_all('tr'):
                    cells = [td.get_text(strip=True) for td in row.find_all('td')]
                    if cells:
                        rows.append(cells)
                scraped_data.append({"type": "table", "data": {"header": headers, "rows": rows}})
            elif element.name in ['ul', 'ol']:
                items = [li.get_text(strip=True) for li in element.find_all('li')]
                scraped_data.append({"type": "list", "data": items})

        return jsonify(scraped_data)
    return render_template('prose223.html')


@app.route('/scrape', methods=['POST'])
def scrape():
    try:
        data = request.json
        app.logger.debug(f"Received data: {data}")
        class_number = data.get('class')
        subject = data.get('subject')
        chapter = data.get('chapter')
        part = data.get('part')  # Extract the part value
        content_type = data.get('content_type')  # Extract the content_type value

        if not all([class_number, subject, chapter]):
            return jsonify({"error": "Missing required fields"}), 400

        # Get the matching URL
        url = get_matching_url(subject, class_number, content_type, chapter, part, None)

        if not url:
            return jsonify({"error": "No matching URL found"}), 404

        # Scrape the content
        content = scrape_chapter_content(url)
        if not content:
            return jsonify({"error": "No content found"}), 404

        return jsonify(content)

    except Exception as e:
        app.logger.error(f"Error in scrape route: {str(e)}")
        return jsonify({"error": "An internal server error occurred"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)