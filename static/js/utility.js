const player = new Plyr('audio', {
    title: 'Hanayori music radio'
});
window.player = player;


const toggler = document.querySelector(".menu__toggler");
const menu = document.querySelector(".menu");
const profile = document.querySelector(".profile");
toggler.addEventListener("click", () => {
toggler.classList.toggle("active");
menu.classList.toggle("active");
});


function snackbar() {
  var x = document.getElementById("snackbar");
  x.className = "show";
  setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
}
function snackbar2() {
  var y = document.getElementById("snackbar2");
  y.className = "show";
  setTimeout(function(){ y.className = y.className.replace("show", ""); }, 3000);
}
function music() {
  var y = document.getElementById("mu");
  y.className = "music show";
  (function(){ y.className = y.className.replace("music", ""); });
}
function music_off() {
    var y = document.getElementById("mu");
    y.className = "music";
    (function(){ y.className = y.className.replace("music", ""); });
}

document.addEventListener('DOMContentLoaded', function () {
var checkbox = document.querySelector('input[type="checkbox"]');
var obj = {"video": {"value": "<iframe title='YouTube video player' type=\"text/html\" width='540' height='290' src='https://www.youtube.com/embed/videoseries?list=PL8eVDmjKe3tUIn0sT4yJM3guPcWe0gngP' frameborder='0' allowFullScreen></iframe>"}}
checkbox.addEventListener('change', function () {
    if (checkbox.checked) {
        snackbar()
        music_off()
        player.pause();
        document.getElementById('st').innerHTML = (obj.video.value);
    } else {
        document.getElementById('st').innerHTML = ""
        snackbar2()
        music()
    }
  });
});