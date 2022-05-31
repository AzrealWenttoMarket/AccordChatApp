//when you submit a form, leave it there and do not refresh
window.onload = function(e) {
    $("#messageForm").submit(function (e) {
        e.preventDefault();
    });

    var socket = io.connect(location.protocol + "//" + document.domain + ":" + location.port)

    //get value of what user wants to send then pass it to back-end and the send it back to front-end
    // front-end => back-end => front-end
    socket.on("connect", () => {
        var button = document.getElementById
        ("sendMessageButton");
        //after user click submit do following codes
        button.onclick = () => {
            var message = document.getElementById
            ("message").value;
            socket.emit("broadcast message", 
            //creating dictionary
            {"message": message});
        }
    });

    socket.on("show message", data => {
        console.log(data.message);
    });
}