var stripe = Stripe(stripe_publishable_key);

// Create an instance of Elements.
var elements = stripe.elements();

// Custom styling can be passed to options when creating an Element.
// (Note that this demo uses a wider set of styles than the guide below.)
var style = {
  base: {
    color: '#32325d',
    fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
    fontSmoothing: 'antialiased',
    fontSize: '16px',
    '::placeholder': {
      color: '#aab7c4'
    }
  },
  invalid: {
    color: '#fa755a',
    iconColor: '#fa755a'
  }
};

// Create an instance of the card Element.
var card = elements.create('card', {style: style});

// Add an instance of the card Element into the `card-element` <div>.
card.mount('#card-element');

// Handle real-time validation errors from the card Element.
card.on('change', function(event) {
  var displayError = document.getElementById('card-errors');
  if (event.error) {
    displayError.textContent = event.error.message;
  } else {
    displayError.textContent = '';
  }
});

// Handle form submission.
var form = document.getElementById('payment-form');
form.addEventListener('submit', function(event) {
  event.preventDefault();

  stripe.createToken(card).then(function(result) {
    if (result.error) {
      // Inform the user if there was an error.
      var errorElement = document.getElementById('card-errors');
      errorElement.textContent = result.error.message;
    } else {
      // Send the token to your server.
      stripeTokenHandler(result.token);
    }
  });
});

// Submit the form with the token ID.
function stripeTokenHandler(token) {
  // Insert the token ID into the form so it gets submitted to the server
  var form = document.getElementById('payment-form');
  var hiddenInput = document.createElement('input');
  hiddenInput.setAttribute('type', 'hidden');
  hiddenInput.setAttribute('name', 'stripeToken');
  hiddenInput.setAttribute('value', token.id);
  form.appendChild(hiddenInput);

  // Submit the form
  form.submit();
}

var show_form_elements = document.getElementsByClassName('card_show_add_form')

for (i = 0; i < show_form_elements.length; i++) {
  show_form_elements[i].addEventListener('click', function() {
    var card_form = document.getElementById('card_add_container')
    if (!card_form.style.display) {card_form.style.display = "none"}
    if (card_form.style.display == "none") {
      card_form.style.display = "block"
    } else {
      card_form.style.display = "none"
    }
  });
}

document.getElementById('fee_form').reset();  // to reset discount checkbox

function change_discount_fees(event) {
  var checked = event.checked
  var fee_selector = document.getElementById("fee_selector");
  var fee_selector_discount = document.getElementById("fee_selector_discount");
  if (checked) {
    fee_selector.classList.add("hidden_select");
    fee_selector_discount.classList.remove("hidden_select");
  } else {
    fee_selector.classList.remove("hidden_select");
    fee_selector_discount.classList.add("hidden_select");
  }
}