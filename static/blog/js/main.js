function changeTheme(event){
    document.body.classList.toggle("dark-theme");
    // const label = document.getElementById("theme-label");
    const icon = document.querySelector(".changeTheme-icon");
    icon.classList.toggle("fa-circle-half-stroke");
    icon.classList.toggle("fa-sun");
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