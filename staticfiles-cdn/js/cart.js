var updateBtns = document.getElementsByClassName('update-cart')

for (let i = 0; i < updateBtns.length; i++) {
  updateBtns[i].addEventListener('click', function() {
    const foodId = this.dataset.food;
    const action = this.dataset.action;

    console.log('Food Id: ', foodId)
    console.log('Action: ', action)
    console.log('User: ', user)

    var url = '/update-item/'
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
      },
      body: JSON.stringify({'foodId':foodId, 'action':action})
    })
      .then((response) => {
            return response.json()
    })
      .then(data => {
        console.log(data)
        // Update the quantity value on the page
        var quantityElem = document.getElementById(`quantity_${foodId}`);
        if (quantityElem) {
          quantityElem.textContent = data.quantity;
        }

        var priceElem = document.getElementById(`price_${foodId}`);
        if (priceElem) {
          priceElem.textContent = data.price;
        }
      })
    })
}


const dropdownMenu = document.querySelector(".dropdown-menu");
const dropdownButton = document.querySelector(".dropdown-button");

if (dropdownButton) {
  dropdownButton.addEventListener("mouseover", () => {
    dropdownMenu.style.display = "block";
  });

  dropdownButton.addEventListener("mouseout", () => {
    dropdownMenu.style.display = "none";
  });

  dropdownMenu.addEventListener("mouseover", function () {
  dropdownMenu.style.display = "block";
  });

  dropdownMenu.addEventListener("mouseout", function () {
    dropdownMenu.style.display = "none";
  });
}

