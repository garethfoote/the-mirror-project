## The Mirror Project - Collector + Poem Parsing

Python application for traversing specified hard drive directories on *nix (Linux, OSx, Unix, ...) systems, reading specified file types (docx, txt, pdf, etc), parsing the text and categorising into word classes using a Natural Language Processing library. Saves output as JSON file.

### Dependencies 

* Python >= 2.7
* C compiler (gcc or similar) - OSx without Xcode is missing this. Download from: https://github.com/kennethreitz/osx-gcc-installer/downloads

## Install me

* `git clone git@github.com:garethfoote/the-mirror-project.git`
* `cd the-mirror-project`
* `chmod +x run.sh`
* `./setup.sh`

## Run me - Collector application.

* Edit config - `config.cfg`. DO NOT EDIT `setup.cfg`.
  * **dirs** - [REQUIRED] Array of absolute directory paths that application will scan for file types:  
`   
  dirs: [ "/Users/gareth/Projects/the-mirror-project/traverse-test" ]
`
  * **output** - [REQUIRED] Output directory for JSON file containing categorised words:
`
  output: "/Users/gareth/Projects/the-mirror-project/data/"
`
  * **acceptedFiles** - Accepted file types defined as array of mime types:  
`      acceptedFiles:  
         [   
             "text/html",
             "text/plain",
             "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
             "application/rtf",
             "application/vnd.oasis.opendocument.text",
             "application/pdf"
         ]  
`
  * **htmltags** - For type 'text/html', an array of HTML tags to parse:  
`
     htmltags:
         [   
             "p",
             "h1",
             "h2"
         ]
`
* `chmod +x run.sh`
* `./run.sh`
