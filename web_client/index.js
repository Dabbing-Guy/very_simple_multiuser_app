let joined = false;
const url = "https://very-simple-multiuser-app-api.tk/";

let user_id = "";
let user_password = "";

function buttonFunction() {
    let menuname = document.getElementById("menuname");
    let prompt = document.getElementById("prompt");
    let user_input = document.getElementById("user_input");
    let messages = document.getElementById("messages");

    if (joined === false) {
        let name = user_input.value;
        let http = new XMLHttpRequest();
        http.open("POST", url + "/users", true);
        http.setRequestHeader("Content-Type", "application/json");
        let data = { "user_nickname": name, "message": "Has Joined the Chat!" }
        http.onreadystatechange = function () {
            if (http.readyState == 4 && http.status == 200) {
                console.log(http.responseText);
                let data = JSON.parse(http.responseText);
                // Update the display to a chat interface
                name = data.user_nickname;
                user_id = data.user_id;
                user_password = data.user_password;
                menuname.innerHTML = "Chat as " + name;
                prompt.innerHTML = "Enter your message:";
                joined = true;
            }
        }
        http.send(JSON.stringify(data));
    } else {
        let http = new XMLHttpRequest();
        let message = user_input.value;
        http.open("PATCH", url + "/message/" + user_id, true);
        http.setRequestHeader("Content-Type", "application/json");
        let data = { "user_password": user_password, "message": message }
        http.send(JSON.stringify(data));
        http.onreadystatechange = function () {
            // clear user input
            if (http.readyState == 4 && http.status == 200) {
                console.log(http.responseText);
                user_input.value = "";
            }
        }
    }
}

// Update the display with new messages
const updateMessages = () => {
    if (joined === true) {
        let http = new XMLHttpRequest();
        http.open("GET", url + "/users", true);
        http.send();
        http.onreadystatechange = function () {
            if (http.readyState == 4 && http.status == 200) {
                let messages = JSON.parse(http.responseText).users;
                console.log(messages);
                let html = "";
                for (var i = 0; i < messages.length; i++) {
                    html += messages[i].user_nickname + ": " + messages[i].message + "<br>";
                }
                document.getElementById("messages").innerHTML = html;
            }
        }
    }
}

// Update the display with new messages
setInterval(updateMessages, 800);

// Make the server delete the user when the window is closed
function leave() {
    if (joined === true) {
        let http = new XMLHttpRequest();
        http.open("DELETE", url + "/users", true);
        http.setRequestHeader("Content-Type", "application/json");
        let data = { "user_id": user_id, "user_password": user_password }
        http.send(JSON.stringify(data));
    }
    return null;
}

window.onbeforeunload = function () {
    leave();
    return "You have been disconnected from the chat, you can safely leave."
};
