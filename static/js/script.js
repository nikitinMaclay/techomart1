let openFormButton = document.querySelector('.contacts-button');
let loginPopup = document.querySelector('.modal-write-us');
let closeFormButton = loginPopup.querySelector('.modal-closing-button');
let formForm = loginPopup.querySelector('.contact-form');
let nameInput = loginPopup.querySelector('.name-input');
let emailInput = loginPopup.querySelector('.email-input');
let openMapButton = document.querySelector('.contacts-img');
let mapPopup = document.querySelector('.modal-map');
let closeMapButton = mapPopup.querySelector('.modal-closing-button');
let isStorageSupport = true;
let storage = "";
let emailStorage = "";
try {
  storage = localStorage.getItem("name");
  emailStorage = localStorage.getItem("email");
} catch (err) {
  isStorageSupport = false;
}

openFormButton.addEventListener("click", function (evt) {
  evt.preventDefault();
  loginPopup.classList.add("modal--show");

  nameInput.focus();

  if (storage) {
    nameInput.value = storage;
    emailInput.focus();
  }
  else if(emailStorage){
    emailInput.value = emailStorage;
    nameInput.focus();
   }

});

closeFormButton.addEventListener("click", function (evt) {
  evt.preventDefault();
  loginPopup.classList.remove("modal--show");
});

formForm.addEventListener("submit", function(evt){
  if (!nameInput.value || !emailInput.value) {
    evt.preventDefault();
    loginPopup.classList.remove("modal-error");
    loginPopup.offsetWidth = loginPopup.offsetWidth;
    loginPopup.classList.add("modal-error");
  }
  else {
    if (isStorageSupport) {
      localStorage.setItem("name", nameInput.value);
      localStorage.setItem("email", emailInput.value);
    }
  }
});

openMapButton.addEventListener("click", function (evt) {
  evt.preventDefault();
  mapPopup.classList.add("modal--show");
});
closeMapButton.addEventListener("click", function (evt) {
  evt.preventDefault();
  mapPopup.classList.remove("modal--show");
  loginPopup.classList.remove("modal-error");
});

window.addEventListener("keydown", function (evt) {
  if (evt.keyCode === 27) {
    if (loginPopup.classList.contains("modal--show")) {
      evt.preventDefault();
      loginPopup.classList.remove("modal--show");
      loginPopup.classList.remove("modal-error");
    }
  }
});

let goodMessagePopup = document.querySelector('.modal-good-message');
let goodsList = document.querySelector('.popular-goods-list');
let goodCloseButton = goodMessagePopup.querySelector('.modal-closing-button');
let goodContinueButton = goodMessagePopup.querySelector('.good-continue-button');
let cart = document.querySelector('.cart')
goodsList.onclick = function(event) {
  let indexBuyButton = event.target.closest('.buying-button');
  event.preventDefault();
  if (!indexBuyButton) return;

  if (!goodsList.contains(indexBuyButton)) return;

  goodMessagePopup.classList.add('modal--show');

  cart.classList.add('buying-active');
};

goodCloseButton.onclick = function (evt) {
  evt.preventDefault();
  goodMessagePopup.classList.remove('modal--show');

};

goodContinueButton.onclick = function (event) {
  event.preventDefault();
  goodMessagePopup.classList.remove('modal--show');
};

let firstSlide = document.querySelector('.slide-1-wrapper');
let secondSlide = document.querySelector('.slide-2-wrapper');
let firstBackButton = firstSlide.querySelector('.slider-back');
let secondNextButton = secondSlide.querySelector('.slider-next')
firstBackButton.addEventListener("click", function () {
  secondSlide.classList.add('is-showing');
  firstSlide.classList.remove('is-showing');
});

secondNextButton.addEventListener("click", function () {
  secondSlide.classList.remove('is-showing');
  firstSlide.classList.add('is-showing');
});
