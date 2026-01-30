document.addEventListener("scroll", () => {
    const button = document.querySelector("#scroll-to-top");

    if (window.scrollY > 300) {
        button.classList.add("show");
    } else {
        button.classList.remove("show");
    }
});
