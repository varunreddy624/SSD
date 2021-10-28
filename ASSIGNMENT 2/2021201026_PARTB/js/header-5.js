let navToggle = document.querySelector(".nav__toggle");
let navWrapper = document.querySelector(".nav__wrapper");
let edit = document.getElementById("edit");
let main = document.getElementById("main");
let changesform = document.getElementById("changesform");
edit.style.display="none";
changesform.style.display="none";

let presentPage = "home";
document.getElementById(presentPage).setAttribute("class","nav__item active");

navToggle.addEventListener("click", function () {
  if (navWrapper.classList.contains("active")) {
    this.setAttribute("aria-expanded", "false");
    this.setAttribute("aria-label", "menu");
    navWrapper.classList.remove("active");
  } else {
    navWrapper.classList.add("active");
    this.setAttribute("aria-label", "close menu");
    this.setAttribute("aria-expanded", "true");
    searchForm.classList.remove("active");
    searchToggle.classList.remove("active");
  }
});

function adminModeSwitch(x){
  if(x.getAttribute("value") == "ADMIN MODE"){
    x.setAttribute("value","NORMAL MODE");
    edit.style.display="block";
  }
  else{
    x.setAttribute("value","ADMIN MODE");
    changesform.style.display="none";
    main.style.display="block";
    edit.style.display="none";
  }
}

function hideMainContent(){
  main.style.display="none";
  document.getElementsByClassName("twitter-timeline")[0].style.display="none";
  changesform.style.display="block";
  document.getElementById("editTextBox").value = document.getElementById("paragraph").innerHTML;
}

function handleSaveChanges(){
  document.getElementById("paragraph").innerHTML= document.getElementById("editTextBox").value;
  changesform.style.display="none";
  main.style.display="block";
  document.getElementsByClassName("twitter-timeline")[0].style.display="block";
}
