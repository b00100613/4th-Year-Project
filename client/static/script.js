/*
# File name: /client/static/script.js
# Student id:B00100613
# Student Name: Anthony Yalcin
# University: Technological University Dublin Blanchardstown Campus.
# Purpose: stores the XHR request needed to communicate with the API
*/

/*this function is used to send a request to the /api/challenge/{id} endpoint*/
function getchallenge(){
    document.getElementById("challenge_id").innerHTML = getchallengeId();
    //XMLHttpRequest (xhr) is used to send request to the API
    const xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        //if the response from the API is 200 ok update the title and the decription on the web page 
        if (this.readyState == 4 && this.status == 200) {
            var o=JSON.parse(xhr.responseText);
            document.getElementById("title").innerHTML += o.title;
            document.getElementById("challenge_description").innerHTML += o.description;
        }
        else if(this.readyState == 4 && this.status == 401){         
        }      
    };
    xhr.open('GET', '/api/challenge/'+getchallengeId(),true)
    xhr.send() 
}

/*this function is used to send a request to the /api/challenge/{id}/reset endpoint*/
function resetchallenge(id){
    const xhr = new XMLHttpRequest()
    xhr.open('POST', '/api/challenge/'+id+'/reset');
    //the API only accepts json content type
    xhr.setRequestHeader('Content-Type', 'application/json');
    // send request
    xhr.send(JSON.stringify({"reset":true})); // send a json request body with reset = true
}

/*this function is used to send a request to the /api/challenges endpoint*/
function getchallenges(){
    const xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        //if the response from the API is 200 ok update update the page with list of challenges.
        if (this.readyState == 4 && this.status == 200) {
            var o=JSON.parse(xhr.responseText);
            for (let i = 0; i < o.length; i++) {
                //for loop seperates the challenges by categories.
                document.getElementById("resource_body").innerHTML += "<div><li><a href=\"/challenge/"+o[i].id+"\"><strong>Challenge "+o[i].id+" - "+o[i].title+"</a></strong><a href='#' onclick='resetchallenge("+o[i].id+")'>Reset challenge</a></li><br><custom><strong>Difficulty:</strong> "+o[i].difficulty+"</custom></div>";
                if(i==2){
                    document.getElementById("resource_body").innerHTML += "<h2>Authorization Challenges</h2>";
                }
                else if(i == 5){
                    document.getElementById("resource_body").innerHTML += "<h2>Other Challenges</h2>";
                }
            } 
        }
    };
    xhr.open('GET', '/api/challenges',true)
    xhr.send()


}

/*this function is used to send a request to the /api/challenge/{id}/status endpoint*/
function check_status(){
    const xhr = new XMLHttpRequest()
    xhr.open('GET', '/api/challenge/'+getchallengeId()+'/status')
     //the API only accepts json content type
    xhr.setRequestHeader('Content-Type', 'application/json')
    xhr.send()
    //if the response from the API is 200 ok update update the status on the page
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
           // Typical action to be performed when the document is ready:
          var o=JSON.parse(xhr.responseText);
          document.getElementById("status").innerHTML = o.message;   
        }
        else if(this.readyState == 4 && this.status == 401){
          
        }
    };
};

/*this function is used to get the challenge id from the URL, which is needed throughout the web application*/
function getchallengeId(){
	var path = window.location.pathname.split("/");
	var challenge = parseInt(path[2]);
	return challenge
}

/*this function is used to send a request to the /api/challenge/{id}/submit_flag endpoint*/
function submitFlag(form){
    const xhr = new XMLHttpRequest()
    xhr.open('POST', '/api/challenge/'+getchallengeId()+'/submit_flag');
    var formData = new FormData(form);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(Object.fromEntries(formData)))
    //if the response from the API is 200 call the check_status function to update the status on the page.
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
        check_status()
        }
        else if(this.readyState == 4 && this.status == 401){
        }
    };
}

/*this function is used to send a request to the /api/challenge/{id}/login endpoint*/
function submitLogin(loginForm){
    const xhr = new XMLHttpRequest()
    xhr.open('POST', '/api/challenge/'+getchallengeId()+'/login')
    var formData = new FormData(loginForm);
    xhr.setRequestHeader('Content-Type', 'application/json')
    xhr.send(JSON.stringify(Object.fromEntries(formData))) // send the form data in json parseable format as the API only accept JSON data.
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var o=JSON.parse(xhr.responseText);
            //store the returned JWT token as an access token in the browsers session storage.
            sessionStorage.setItem("access_token", o.access_token);
            var id = getchallengeId()
            if(id == 4 || id == 5){
                //if challenge 4 or 5 store the returned user id in the browsers local storage.
                user_id=localStorage.setItem("user_id",o.user_id);
            }
            window.location = "/challenge/"+getchallengeId()+"/account"
        }
        else if(this.readyState == 4 && this.status == 401){
            //if the user is unauthenticated return an error.
            document.getElementById("resource_body").innerHTML = "not authenticated please login"
        }
    };
}

/*this function is used to send a GET request to the /api/challenge/{id}/account endpoint*/
function getProtected(id){
    if (sessionStorage.getItem("access_token") != null){
    const xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        //if the jwt token is valid the user details are returned and the page updated to reflect the account information.
        if (this.readyState == 4 && this.status == 200) {
            // Typical action to be performed when the document is ready:
            var o=JSON.parse(xhr.responseText);
            if (getchallengeId() == 7){
                //if challenge is 7 then show the update account form
                document.getElementById("hidden_name_update").hidden =false;
            }
            //if challenge is 6 then show the update account form
            else if(getchallengeId == 6){
                document.getElementById("hidden_account_update").hidden =false;       
            }
            //if there is no flag in the response only show the username, role, name
            if(o.flag == null){
                document.getElementById("resource_body").innerHTML = "you are logged in as user:"+o.username+" <br> role:"+o.role+"<br> name:"+o.name;
            }
            //if there is a flag show it on the page.
            else{
                document.getElementById("resource_body").innerHTML = "you are logged in as user:"+o.username+" <br> role:"+o.role+"<br> flag:"+o.flag+"<br> name:"+o.name;
            }
        }
        else if(this.readyState == 4 && this.status == 401){
             //if the user is unauthenticated return an error and a link to log in.
            document.getElementById("resource_body").innerHTML = "not authenticated please login <a href=\"/challenge/"+getchallengeId()+"\">here</a>";
        }
    };
    //if there is no user id then only send a request to /api/challenge/{id}/account
    if(id == null){
        xhr.open('GET', '/api/challenge/'+getchallengeId()+'/account',true);
    }
    //if there is an id append it onto the end of the endpoint
    else{
        xhr.open('GET', '/api/challenge/'+getchallengeId()+'/account/'+id,true);
    } 
    //get the access_token from session storage in the browser and submit it as a Authorization header.
    access_token = sessionStorage.getItem("access_token")
    xhr.setRequestHeader('Authorization','Bearer '+access_token)
    if (getchallengeId() == 5){
        //if challenge is 5 get the X-USER-ID value from the browsers local storage.
        user_id = localStorage.getItem("user_id")
        xhr.setRequestHeader('X-USER-ID',user_id) //send the X-USER-ID header in the request.
    }
    xhr.send()
    }
    else{
        //if the user is unauthenticated return an error and a link to log in.
        document.getElementById("resource_body").innerHTML = "not authenticated please login <a href=\"/challenge/"+getchallengeId()+"\">here</a>";
    }
}

/*this function is used to send a PUT request to the /api/challenge/{id}/account endpoint*/
function updateName(updateForm){
    const xhr = new XMLHttpRequest()
    xhr.open('PUT', '/api/challenge/'+getchallengeId()+'/account') //send request with PUT method
    var formData = new FormData(updateForm);
    xhr.setRequestHeader('Content-Type', 'application/json');
    let access_token = sessionStorage.getItem("access_token");
    xhr.setRequestHeader('Authorization','Bearer '+access_token);
    xhr.send(JSON.stringify(Object.fromEntries(formData))); //api only accepts json data
    //if jwt_token is valid the get accounts request is sent again and the page updated.
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var o=JSON.parse(xhr.responseText);
            getProtected();
        }
        //if the user is unauthenticated return an error
        else if(this.readyState == 4 && this.status == 401){
            document.getElementById("resource_body").innerHTML = "not authenticated please login"
        }
    };
}

/*this function is used to send a PUT request to the /api/challenge/1/protected endpoint*/
function basicAuthAccount(){
    const xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
    //when 
    if (this.readyState == 4 && this.status == 200) {
        var o=JSON.parse(xhr.responseText);
        if (getchallengeId() == 4){
            document.getElementById("hidden_name").hidden =false;
        }
      if(o.flag == null){
         //if there is no flag in the response only show the username, role, name
         document.getElementById("resource_body").innerHTML = "you are logged in as user:"+o.username+" <br> role:"+o.role+"<br> name:"+o.name;
      }
      else{
        //if there is a flag show it on the page.
        document.getElementById("resource_body").innerHTML = "you are logged in as user:"+o.username+" <br> role:"+o.role+"<br> flag:"+o.flag+"<br> name:"+o.name;  
      }
    }
    else if(this.readyState == 4 && this.status == 401){
        //if the user is unauthenticated return an error and a link to log in.
        document.getElementById("resource_body").innerHTML = "not authenticated please login <a href=\"/challenge/"+getchallengeId()+"\">here</a>";
    }
};
  xhr.open('GET', '/api/challenge/1/protected',true)
  xhr.withCredentials = true; // this is needed to send the basic authentication header.
  xhr.send()
}

