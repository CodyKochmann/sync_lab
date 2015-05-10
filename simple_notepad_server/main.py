import base64
import cherrypy
import json
import csv

def script_path(include_name=False):
    # returns the full path of the script containing this snippet
    # by: Cody Kochmann
    from os import path
    full_path = path.realpath(__file__)
    if include_name:
        return(full_path)
    else:
        full_path = "/".join( full_path.split("/")[0:-1] ) + "/"
        return(full_path)

def write_to_csv(input_array):
  with open( script_path() + '/note_database.csv', 'a') as csvfile:
      spamwriter = csv.writer(csvfile, delimiter='|')
      # Uncomment this if you need verbose logging to debug anything
      # print "appending %s to clipboard_watcher.csv" % (input_array)
      spamwriter.writerow(input_array)

class Root(object):

    @cherrypy.expose
    def update(self):
        cl = cherrypy.request.headers['Content-Length']
        b64_body = cherrypy.request.body.read(int(cl))
        message=json.loads(base64.b64decode(b64_body))
        message["content"]=base64.b64encode(message["content"])
        write_to_csv([message["id"],message["content"]])
        # do_something_with(body)
        return "Content Recieved"

    @cherrypy.expose
    def index(self):
        return """
<html><head>
<meta name="viewport" content="width=device-width, initial-scale=1, height=device-height, user-scalable=no">
<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
<script type='text/javascript'>
function b64_e( str ) {
  return window.btoa(unescape(encodeURIComponent( str )));
}

function b64_d( str ) {
  return decodeURIComponent(escape(window.atob( str )));
}
function Update() {
    $.ajax({
      type: 'POST',
      url: "update",
      contentType: "application/json",
      processData: false,
      data: b64_e(JSON.stringify({"id":$('#namebox').val().replace(' ','_').toLowerCase(),"content":$('#updatebox').val()})),
      success: function(data) {alert(data);},
      dataType: "text"
    });
}
setInterval(function(){window.scrollTo(0,0);},100);
</script>
<style>

    body{
      background:darkgrey;
      width:100%;
      height:100%;
      max-width:100%;
      max-height:100%;
      min-width:100%;
      min-height:100%;
      margin:0;
    }
    #namebox, #updatebox, #submit_button{
      font-size:20px;
      font-family:'Avenir Next';
    position:fixed;
    margin:0;
    border-radius:0;
    border:none;
    }
    #namebox{
    top:0;
    height:0.75in;
    text-align:center;
    background:rgba(0,0,0,0.85);
    color:rgba(250,250,250,0.95);
    width:80%;
    }
    #updatebox{
    height:90%;
    width:100%;
    top:0.75in;
    background:rgba(0,0,0,0.9);
    color:rgba(250,250,250,0.95);
    left:0;
    }
    #submit_button{
    height:0.525in;
    padding:0.225in 0 0 0;
    font-size:18px;
    background:rgba(0,0,0,0.8);
    color:rgba(250,250,250,0.95);
    text-align:center;
    width:20%;
    position:fixed;
    top:0;
    right:0;
    }
</style>
</head>
<body>
<input type='text' id='namebox' value='file name' size='50' />
<textarea id="updatebox" name="updatebox" spellcheck="false" rows="10" cols="50"></textarea>
<p id='submit_button' type='submit' onClick='Update(); return false'>Update</p>
</body>
</html>
"""
cherrypy.config.update({'server.socket_host': '0.0.0.0',
                        'server.socket_port': 8080,
                       })
cherrypy.quickstart(Root())
