# WhatsApp-Analyzer

![CircleCI](https://circleci.com/gh/Dineshkarthik/Whatsapp-analyzer.svg?style=svg&circle-token=c02cdb0e0021bb805b7810c30601d31fbc4de81d)

WhatsApp-Analyzer is a simple analytics and visualization Python app, dashboard powered by Twitter-bootstrap and D3.js.

##### All you need to do:
  - Export your WhatsApp conversation to text file
  - Upload it to analyzer
  - View your analysis on the dashboard

##### Known Issues:

> There’s no way that it will work for everyone because I’ve found that depending on your OS and version of Whatsapp, the format of text file lines varies wildly. I’m sorry if it doesn’t work for you.


### Tech

WhatsApp-Analyzer uses a number of open source projects to work properly:

* [Flask] - microframework for Python based on Werkzeug, Jinja 2
* [Pandas] - pandas is an open source, library providing high-performance, easy-to-use data structures and data analysis tools for the Python
* [Twitter Bootstrap] - great UI boilerplate for modern web apps
* [D3.js] - JavaScript library for manipulating documents based on data, helps you bring data to life using HTML, SVG, and CSS.
* [jQuery] - duh

And of course WhatsApp-Analyzer itself is open source with a [public repository][WhatsApp-Analyzer] on GitHub.

###### Live [Demo] available here.
### Installation

You need Python 3.6 and above, its dependency packages, flask and pandas installed globally:

```sh
$ git clone https://github.com/Dineshkarthik/Whatsapp-analyzer.git WhatsApp-Analyzer
$ cd WhatsApp-Analyzer
$ make install
$ make run
```

Docker image is also available:

    docker pull dineshkarthik/whatsapp-analyzer
    docker run -p 8000:5000  dineshkarthik/whatsapp-analyzer

Support for python2 is depricated but old docker image is available

    docker pull dineshkarthik/whatsapp-analyzer:python2
    docker run -p 8000:5000  dineshkarthik/whatsapp-analyzer:python2

Service will be running on port 8000 - `http://localhost:8000/`

License
----

MIT


**Free Software, Hell Yeah!**



   [D3.js]: <https://d3js.org/>
   [Flask]: <http://flask.pocoo.org/>
   [Pandas]: <http://pandas.pydata.org/>
   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [jQuery]: <http://jquery.com>
   [WhatsApp-Analyzer]: <https://github.com/Dineshkarthik/Whatsapp-analyzer>
   [Demo]: <http://whatsapp-analyzer.herokuapp.com/>
