document.addEventListener("DOMContentLoaded", () => {
    const clothes = document.querySelectorAll(".clothes");                                  // Clothes class selection
    const upButton = document.querySelector(".result__filter-btns button:first-child");     // Up button selection
    const downButton = document.querySelector(".result__filter-btns button:last-child");    // Down button selection
    let currentIndex = 0;                                                                   // Index for clothing option icons
    let selectedCategory = 'Men';                                                           // Selected search category

    // Function changes the class of the clothing icons to only display one at a time
    function showClothing(index) {
        clothes.forEach((item, idx) => {
            if (idx === index) {
                item.classList.remove("hidden");
                item.classList.add("active");
            }
            else
            {
                item.classList.add("hidden");
                item.classList.remove("active");
            }
        });
    }

    // Handles the clicking of the up button
    function upClick() {
        currentIndex = (currentIndex - 1 + clothes.length) % clothes.length;    // Sets index to update based off where it is in the "icons list"
        showClothing(currentIndex);
    }

    // Handles the clicking of the down button
    function downClick() {
        currentIndex = (currentIndex + 1) % clothes.length; // Sets index to update based off where it is in the "icons list"
        showClothing(currentIndex);
    }

    // Checks if the buttons are clicked and calls their respective functions if they are
    upButton.addEventListener("click", upClick);
    downButton.addEventListener("click", downClick);
    showClothing(currentIndex);

    // Sets the selected category to Men when selected by the user
    document.getElementById("categoryMen").addEventListener("click", () => {
        selectedCategory = "Men";
        updateCategoryTitle(selectedCategory);
    });

    // Sets the selected category to Women when selected by the user
    document.getElementById("categoryWomen").addEventListener("click", () => {
        selectedCategory = "Women";
        updateCategoryTitle(selectedCategory);
    });

    // Checks for the active clothing filter
    function checkFilter() {

        let categoryFilter = document.querySelector(".active").id;  // Gets the active clothing filter

        // Checks whether the main category is men or qomen and sets a filter based off which one is set
        if (selectedCategory === "Men") {
            switch (categoryFilter) {
                case "pants": categoryFilter = "pantsMen";  // Sets filter to men's pants
                break;
                case "shoes": categoryFilter = "shoesMen";  // Sets filter to men's shoes
                break;
                default : categoryFilter = "Men";           // Default filter to men's shirts
            }
        } else {
            switch (categoryFilter) {
                case "pants": categoryFilter = "pantsWomen";    // Sets filter to women's pants
                break;
                case "shoes": categoryFilter = "shoesWomen";    // Sets filter to women's shoes
                break;
                default : categoryFilter = "Women";             // Default filter to women's shirts
            }
        }

        return (categoryFilter);
    }

    // Sets the keyword when the scan button is clicked and calls the functions that display the products
    document.querySelector(".result__scan").addEventListener("click", () => {
        const keyword = "streetwear";
        displayResult(keyword);
        fetchProducts(keyword, checkFilter());
    });

    // Displays the result (keyword)
    function displayResult(keyword) {
        document.querySelector(".result__desc h1").textContent = keyword;
        document.querySelector(".result__desc h5").textContent = "RESULT";
    }

    // Updates the category title in the dropdown menu
    function updateCategoryTitle(category) {
        const categoryButton = document.querySelector(".header__section-dropdown button");
        categoryButton.textContent = `${category} `;
        categoryButton.appendChild(document.createElement("i")).className = "fa-solid fa-caret-down";
    }

    // Main function that calls the eBay API from the proxy server
    const fetchProducts = async (keyword, category) => {   
        try {
            const response = await fetch(`https://pinsift-server.onrender.com/api/products?keyword=${keyword}&category=${category}`); // Calls eBay API through proxy server
            const data = await response.json(); // Data returned by the eBay API
            displayProducts(data);
        }
        catch (error)
        {
            console.error("Error fetching products:", error);   // Returns if there is an error returning the products
        }
    };

    // Function dynamically displays products
    const displayProducts = (data) => {
        const productsContainer = document.querySelector(".products__container");   // Selects the product container
        productsContainer.innerHTML = "";   // Makes sure that the html in the product container is empty

        const items = data.findItemsAdvancedResponse[0]?.searchResult[0]?.item || [];   // Sets the items returned from the eBay APi to specific list of items

        // Iterates through each item and creates a product div to display
        items.forEach(item => {
            const productElement = document.createElement("div");       // Creates the product element
            productElement.className = "products__container-product";   // Sets the class name of the product element

            let imageUrl = item.prictureURLSuperSize || item.pictureURLLarge || item.galleryURL[0] || "images/placeholder.png"; // Retrives the best quality product image available from the options the eBay API gives

            // If no better images are found, it replaces with higher quality images if available
            if (imageUrl === item.galleryURL[0]) {
                imageUrl = imageUrl.replace("s-l140", "s-l500");
            }
            
            const title = item.title[0] || "No Title Available";                                        // Sets the product title
            const price = item.sellingStatus[0]?.currentPrice[0]?.__value__ || "No Price Available";    // Sets the product price
            const condition = item.condition?.[0]?.conditionDisplayName[0] || "No Condition Available"; // Sets the product condition
            const itemUrl = item.viewItemURL?.[0] || "#";                                               // Sets the product url
           
            // Populates the product element with the relevant product information
            productElement.innerHTML = `
                <img src="${imageUrl}" alt="${title}">
                <div class="products__container-product--desc">
                    <h3>$${price}</h3>
                    <a href="${itemUrl}" target="_blank"><i class="fa-solid fa-arrow-up-right-from-square"></i></a>
                </div>
                <h5>${condition}</h5>
            `;

            productsContainer.appendChild(productElement);  // Dynamically adds products to the product container
        });
    };
});