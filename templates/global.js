{% if mobile %}
window.mobile = true;
{% else %}
window.mobile = false;
{% endif %}
Array.prototype.remove = function(from, to) {
  var rest = this.slice((to || from) + 1 || this.length);
  this.length = from < 0 ? this.length + from : from;
  return this.push.apply(this, rest);
};
Array.prototype.contains = function(a) {
    for (var i = 0; i < this.length; i++) {
        if (this[i] == a) {
            return true;
        }
    }
    return false;
};
function readCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}
function createCookie(name,value,days) {
    if (days) {
        var date = new Date();
        date.setTime(date.getTime()+(days*24*60*60*1000));
        var expires = "; expires="+date.toGMTString();
    }
    else var expires = "; expires=Thu, 01-Jan-1970 00:00:01 GMT";
    document.cookie = name+"="+value+expires+"; path=/";
}
function adOptOut(showAlert) {
    createCookie('ad-opt-out', '1', 3650); // 3650 days is 10 years, which isn't forever, but is close enough
    var gad = document.getElementById('gad');
    var lgad = document.getElementById('lgad');
    if (showAlert) {
        alert("You won't see any ads again. If you regret it, head over to the donation page, where you can opt-in.");
    }
}
function switchTheme() {
    if (readCookie('dark_theme'))
        createCookie('dark_theme', '', -1);
    else
        createCookie('dark_theme', '1', 3650);
    window.location.href = window.location.href;
}
window.addEventListener('load', function() {
    var feedback = document.getElementById('feedback').querySelector('div');
    var feedbackToggle = document.getElementById('toggle-feedback');
    if (feedbackToggle) {
        feedbackToggle.addEventListener('click', function(e) {
            e.preventDefault();
            if (feedbackToggle.parentElement.className.indexOf('active') == -1) {
                feedbackToggle.parentElement.classList.add('active');
                feedback.querySelector('textarea').focus();
            } else {
                feedbackToggle.parentElement.classList.remove('active');
            }
        }, false);
    }
    var feedbackSend = document.getElementById('send-feedback');
    if (feedbackSend) {
        feedbackSend.addEventListener('click', function(e) {
            e.preventDefault();

            var feedbackText = document.getElementById("feedback-text");
            var xhr = new XMLHttpRequest();
            var formData = new FormData();

            xhr.open('POST', '/api/feedback');
            formData.append("feedback", feedbackText.value);
            xhr.onload = function() {
                if (this.status == 200)
                    result = "Thanks! We read every one of these. Keep in mind, though, this feedback is anonymous. <a href='mailto:media@nerdz.eu'>Email us</a> if you want a response.";
                else if (this.status == 420)
                    result = "Sorry, you can't send more feedback today. Try again in 24 hours!";
                else if (this.status == 413)
                    result = "Sorry, that feedback is too large.";
                else
                    result = "Sorry, something unexpected happened!";

                feedback.innerHTML = "<p>" + result + "</p>";
            };

            xhr.send(formData);
        }, false);
    }
    var dialogYes = document.querySelector('.dialog .yes');
    var dialogNo = document.querySelector('.dialog .no');
    dialogYes.addEventListener('click', function(e) {
        e.preventDefault();
        if (confirmCallback) confirmCallback(true);
        document.querySelector('.dialog').classList.add('hidden');
    }, false);
    dialogNo.addEventListener('click', function(e) {
        e.preventDefault();
        if (confirmCallback) confirmCallback(false);
        document.querySelector('.dialog').classList.add('hidden');
    }, false);
}, false);
var confirmCallback;
function confirm(callback) {
    confirmCallback = callback;
    document.querySelector('.dialog').classList.remove('hidden');
}
