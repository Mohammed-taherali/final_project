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

function show_cart(id) {
    var opt = document.getElementById(id);
    if (opt.style.display == "none") {
        opt.style.display = "block";   
    }
    else {
        opt.style.display = "none";
    }
}

function deletionConfirmation(id) {
    var btn = document.getElementById(id);
    if (btn.style.display == "none") {
        btn.style.display = "block";
    } else {
        btn.style.display = "none";
    }
}

function addMed(){
    var form = document.getElementById("addmed");
    if (form.style.display == "none") {
        form.style.display = "block";
    }
    else {
        form.style.display = "none";
    }
}
// this works