// document.addEventListener("DOMContentLoaded", function () {
//     document.getElementById("loading").style.display = "block";

//   });

//   // Verstecke das Loading-Symbol, sobald die Seite geladen ist
//   window.addEventListener("load", function () {

//     document.getElementById("loading").style.display = "none";
//   });

/* <div id="loading" class="text-center" style="display: none;">
            <div class="loader loader--style5" title="4">
                <svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
                   width="24px" height="30px" viewBox="0 0 24 30" style="enable-background:new 0 0 50 50;" xml:space="preserve">
                  <rect x="0" y="0" width="4" height="10" fill="#333">
                    <animateTransform attributeType="xml"
                      attributeName="transform" type="translate"
                      values="0 0; 0 20; 0 0"
                      begin="0" dur="0.6s" repeatCount="indefinite" />
                  </rect>
                  <rect x="10" y="0" width="4" height="10" fill="#333">
                    <animateTransform attributeType="xml"
                      attributeName="transform" type="translate"
                      values="0 0; 0 20; 0 0"
                      begin="0.2s" dur="0.6s" repeatCount="indefinite" />
                  </rect>
                  <rect x="20" y="0" width="4" height="10" fill="#333">
                    <animateTransform attributeType="xml"
                      attributeName="transform" type="translate"
                      values="0 0; 0 20; 0 0"
                      begin="0.4s" dur="0.6s" repeatCount="indefinite" />
                  </rect>
                </svg>
              </div>
          </div> */

document.addEventListener("DOMContentLoaded", function () {
  const dropdownOptions = document.querySelectorAll(".dropdown-item");
  const selectedImage = document.getElementById("selected-image");
  
  dropdownOptions.forEach((option) => {
    option.addEventListener("click", () => {
      const imagePath = option.getAttribute("data-src");
      selectedImage.src = imagePath;
    });
  });

});

