let catalogPopup = document.querySelector('.modal-good-message');
let catalogGoodsList = document.querySelector('.catalog-goods-list');
let catalogCloseButton = catalogPopup.querySelector('.modal-closing-button');
let continueButton = catalogPopup.querySelector('.good-continue-button');
catalogGoodsList.onclick = function(event) {
  let buyButton = event.target.closest('.buying-button');
  event.preventDefault();
  if (!buyButton) return;

  if (!catalogGoodsList.contains(buyButton)) return;

  catalogPopup.classList.add('modal--show');

};

catalogCloseButton.onclick = function (evt) {
  evt.preventDefault();
  catalogPopup.classList.remove('modal--show');

};

continueButton.onclick = function () {
  catalogPopup.classList.remove('modal--show');
};
