function changeTheme(event){
    document.body.classList.toggle("dark-theme");
    // const label = document.getElementById("theme-label");
    const icon = document.querySelector(".changeTheme-icon");
    icon.classList.toggle("fa-circle-half-stroke");
    icon.classList.toggle("fa-sun");
}
