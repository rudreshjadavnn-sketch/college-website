function toggleSidebar(){

    document.querySelector(".sidebar").classList.toggle("active");

    document.querySelector(".overlay").classList.toggle("show");

}

function closeSidebar(){

    document.querySelector(".sidebar").classList.remove("active");

    document.querySelector(".overlay").classList.remove("show");

}