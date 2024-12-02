function togglePasswordVisibility(element) {
   const icon = element.children[0];
   const isPasswordVisible = icon.getAttribute("data-password") === "visible";

   // toggle eye icon
   icon.setAttribute("data-password", isPasswordVisible ? "hidden" : "visible");

   // toggle password input type
   const passwordInput = element.parentElement.querySelector(".password-field");
   passwordInput.type = isPasswordVisible ? "password" : "text";
}

function ShowDropdownMenu(element) {
   const menu = element.parentElement.querySelector(".dropdown-menu");

   const isHidden = menu.classList.toggle("hidden");

   !isHidden
      ? document.addEventListener("click", hideOnClickOutside)
      : document.removeEventListener("click", hideOnClickOutside);

   function hideOnClickOutside(event) {
      if (!element.contains(event.target) && !menu.contains(event.target)) {
         menu.classList.add("hidden");
         document.removeEventListener("click", hideOnClickOutside);
      }
   }
}

function ShowFilter(element) {
   const menu = document.getElementById("filter-menu");
   const isHidden = menu.classList.toggle("hidden");

   !isHidden
      ? document.addEventListener("click", hideOnClickOutside)
      : document.removeEventListener("click", hideOnClickOutside);

   function hideOnClickOutside(event) {
      if (!element.contains(event.target) && !menu.contains(event.target)) {
         menu.classList.add("hidden");
         document.removeEventListener("click", hideOnClickOutside);
      }
   }
}

function showImage(event, previewId = "#image-preview") {
   const imageInput = event.target;
   const previews = document.querySelectorAll(previewId);

   const file = imageInput.files[0];

   if (file) {
      const reader = new FileReader();
      reader.onload = function (e) {
         previews.forEach((preview) => {
            preview.src = e.target.result;
            preview.classList.remove("hidden");
         });
      };
      reader.readAsDataURL(file);
   }
}

function syncText(event, previewId, defaultText = "") {
   const preview = document.getElementById(previewId);
   preview.textContent = event.target.value || defaultText;
}

function getAreasFromZone(event) {
   const areaSelect = document.getElementById("id_area");
   const zoneId = event.target.value;
   areaSelect.innerHTML = "<option value=''>Select area</option>";

   if (zoneId) {
      fetch(`/areas?zone=${zoneId}`)
         .then((response) => response.json())
         .then((data) => {
            if (data.areas) {
               data.areas.forEach((area) => {
                  areaSelect.appendChild(new Option(area.name, area.id));
               });
            }
         })
         .catch((error) => {
            console.error("Error fetching areas:", error);
            areaSelect.innerHTML = "<option value=''>Error loading areas</option>";
         });
   }
}
