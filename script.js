document.addEventListener("DOMContentLoaded", function () {
    const placeholders = document.querySelectorAll(".location-input, .search-input");

    placeholders.forEach(input => {
        let placeholderText = input.getAttribute("placeholder");
        input.setAttribute("placeholder", "");

        let i = 0;
        function typePlaceholder() {
            if (i < placeholderText.length) {
                input.setAttribute("placeholder", placeholderText.slice(0, i + 1));
                i++;
                setTimeout(typePlaceholder, 100);
            }
        }

        input.addEventListener("focus", function () {
            input.setAttribute("placeholder", placeholderText);
        });

        input.addEventListener("blur", function () {
            i = 0;
            input.setAttribute("placeholder", "");
            typePlaceholder();
        });

        typePlaceholder();
    });
});
