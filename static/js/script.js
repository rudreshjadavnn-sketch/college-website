function openImage(src){

    const modal = document.getElementById("imageModal");
    const img = document.getElementById("modalImage");

    img.src = src;

    modal.style.display = "flex";
}

function closeImage(){

    document.getElementById("imageModal").style.display = "none";
}

document.getElementById("modalImage")?.addEventListener("click", function(event){
    event.stopPropagation();
});

function toggleMenu(){

    document.getElementById("navbar").classList.toggle("active");

}