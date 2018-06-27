
function disable() {
  document.getElementById("upload1").onclick = null;
  document.getElementById("loading1").style.display="block";
}

function enable() {
  document.getElementById("upload1").disabled = false;
}

function disable2() {
  document.getElementById("upload2").onclick = null;
  document.getElementById("loading2").style.display="block";
}

function enable2() {
  document.getElementById("upload2").disabled = false;
}
