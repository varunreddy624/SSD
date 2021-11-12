document.getElementById("Student_Profiles").style.display="none";

function changeToStudent(){
    document.getElementById("Faculty").setAttribute("class","list-group-item list-group-item-action py-2 ripple");
    document.getElementById("Student").setAttribute("class","list-group-item list-group-item-action py-2 ripple active");
    document.getElementById("Student_Profiles").style.display="block";
    document.getElementById("Faculty_Profiles").style.display="none";
}


function changeToFaculty(){
    document.getElementById("Faculty").setAttribute("class","list-group-item list-group-item-action py-2 ripple active");
    document.getElementById("Student").setAttribute("class","list-group-item list-group-item-action py-2 ripple");
    document.getElementById("Student_Profiles").style.display="none";
    document.getElementById("Faculty_Profiles").style.display="block";
}