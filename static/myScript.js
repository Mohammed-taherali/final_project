function myFunc() {
    document.getElementById("demo").innerHTML = "Part 2";
}

function alertFunc() {
    alert("Alert Box!");
}

function test() {
    document.getElementById("demo").style.visibility = "hidden";
    console.log("Test func called!")
}

function hide_element() {
    setTimeout(function() {
        let flash_message = document.getElementById("info_mess");
        flash_message.style.display = "none"  
    }, 1000)
};

function show_password() {
    var pass = document.getElementById("password");
    if (pass.type === "password") {
        pass.type = "text";
    }
    else {
        pass.type = "password";
    }
}

// this works