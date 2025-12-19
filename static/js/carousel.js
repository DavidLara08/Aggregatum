// static/js/carousel.js

document.addEventListener("DOMContentLoaded", function () {
  // 1. Obtener todos los slides del carrusel
  const slides = document.querySelectorAll(".carousel-slide");

  // Si no hay slides, salimos
  if (slides.length === 0) {
    return;
  }

  let currentSlide = 0; // Índice del slide actual (0 = primer slide)
  const intervalTime = 5000; // Tiempo en milisegundos (5 segundos) entre transiciones
  const transitionDuration = 1500; // Duración de la transición CSS (1.5 segundos)

  // 2. Función para mostrar el slide deseado
  function showSlide(index) {
    // Remover la clase 'active' de todos los slides
    slides.forEach((slide) => {
      slide.classList.remove("active");
    });

    // Asegurar que el índice esté dentro del rango
    if (index >= slides.length) {
      currentSlide = 0;
    } else if (index < 0) {
      currentSlide = slides.length - 1;
    } else {
      currentSlide = index;
    }

    // Agregar la clase 'active' al slide actual para mostrarlo
    slides[currentSlide].classList.add("active");
  }

  // 3. Función para pasar al siguiente slide
  function nextSlide() {
    showSlide(currentSlide + 1);
  }

  // 4. Iniciar el carrusel: pasar al siguiente slide cada 'intervalTime'
  setInterval(nextSlide, intervalTime);

  // Opcional: Ajustar la altura del contenedor al cargar la imagen activa
  const wrapper = document.querySelector(".hero-image-wrapper.carousel");
  if (wrapper) {
    // Esperar a que la imagen activa cargue para obtener su altura natural
    const activeImage = slides[currentSlide];

    if (activeImage.complete) {
      // Si ya cargó, ajustamos la altura
      wrapper.style.height = activeImage.offsetHeight + "px";
    } else {
      // Si no ha cargado, esperamos el evento 'load'
      activeImage.addEventListener("load", function () {
        wrapper.style.height = activeImage.offsetHeight + "px";
      });
    }
  }

  // Iniciar mostrando el primer slide (ya debería tener la clase 'active' en HTML)
  showSlide(currentSlide);
});
