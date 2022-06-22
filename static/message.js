//when you submit a form, leave it there and do not refresh
window.onload = function(e) {
    
    fetch('http://127.0.0.1:5000/api', {
        method: 'GET', // or 'PUT'
        headers: {
          'Content-Type': 'application/json',
        },
      })
      .then(response => response.json())
      .then(data => {
            console.log(data)
            for(let i=0; i<data["users"].length; i++) {
                console.log(data["users"][i])
                try {
                    document.getElementById(data["users"][i]).innerHTML = "online";
                    document.getElementById(data["users"][i]).setAttribute("style", "color: green;")
                } catch(err) {
                    var span = document.createElement("SPAN");
                    span.innerHTML = `<span id=${data["users"][i]} style="color: green;">online</span>`
                    document.getElementById("users").appendChild(span);
                }
            }
      })

    $("#messageForm").submit(function (e) {
        e.preventDefault();
    });

    var socket = io.connect(location.protocol + "//" + document.domain + ":" + location.port)

    //get value of what user wants to send then pass it to back-end and the send it back to front-end
    // front-end => back-end => front-end
    socket.on("connect", () => {
        var button = document.getElementById("sendMessageButton");
        button.onclick = () => {
            var message = document.getElementById("message").value;
            document.getElementById("message").value = " ";
            var room_id = location.pathname.split("/")[location.pathname.split("/").length-1];
            console.log(room_id)
            socket.emit("broadcast message", {"message": message, "room_id": room_id});
        }
        // socket.emit("connect")
    });

    socket.on("show message", data => {
        if (data["room_id"] == location.pathname.split("/")[location.pathname.split("/").length-1]) {
            $("#messages").append(`<small>${data.timestamp}</small><h4>${data.name}:</h4><p>${data.message}</p>`);
            window.scrollTo(0, document.getElementById("messages").scrollHeight);
        }
    });

    socket.on("update status", data => {
        console.log("status updated")
        if (data["status"] == "online") {
            try {
                document.getElementById(data["user"]).setAttribute("style", "color: green;");
            } catch (err) {
                var SPAN = document.createElement("SPAN");
                // SPAN.setAttribute("id", data["user"]);
                SPAN.innerHTML = `${data["user"]} <span id="${data['user']}" style="color: green;">online</span>`
                document.getElementById("users").appendChild(SPAN);
            }
        } else {
            document.getElementById(data["user"]).setAttribute("style", "color: gray;")
        }
        document.getElementById(data["user"]).innerHTML = data["status"];
    });

    socket.on("new people joined", data => {
        console.log("hi")
        var room_id = location.pathname.split("/")[location.pathname.split("/").length-1];
        console.log(room_id)
        if (room_id === data["room_id"]) {
            $(".container").append(`<small>${data.timestamp}</small><h4>${data.name}:</h4><p>${data.message}</p>`);
            window.scrollTo(0, document.getElementById("messages").scrollHeight);
            window.location.reload(true);
        }
    })

}