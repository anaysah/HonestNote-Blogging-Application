document.addEventListener("DOMContentLoaded", function () {
    const cookies = document.cookie.split("; ");
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].split("=");
        if (cookie[0] === "theme") {
            const themeValue = cookie[1];
            if (themeValue==="dark"){
                changeTheme();
            }
        }
    }
});


function changeTheme() {
	document.body.classList.toggle("dark-theme");
	// const label = document.getElementById("theme-label");
	const icon = document.querySelector(".changeTheme-icon");
	icon.classList.toggle("fa-circle-half-stroke");
	icon.classList.toggle("fa-sun");
	if (document.body.classList.contains("dark-theme")) {
		document.cookie = "theme=dark; path=/";
	} else {
		document.cookie = "theme=light; path=/";
	}
}


var swiper = new Swiper(".mySwiper", {
	spaceBetween: 30,
	centeredSlides: true,
	autoplay: {
		delay: 2000,
		disableOnInteraction: false,
	},
	pagination: {
		el: ".swiper-pagination",
		clickable: true,
	},
	navigation: {
		nextEl: ".swiper-button-next",
		prevEl: ".swiper-button-prev",
	},
});


function toggleSideMenu(){
	document.getElementById("mySidenav").classList.toggle("show-side-menu");
}