$(document).ready(function () {
  // Handle "Add to Cart"
  $(document).on('click', '.add-to-cart-button', function () {
      const pizzaId = $(this).data('id');

      $.ajax({
          type: 'POST',
          url: `/add_to_cart/${pizzaId}/`,
          data: {
              csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
          },
          success: function (response) {
              // Replace cart items section with updated HTML
              $('#cart-content').html(response.cart_items_html);

              // Update the cart counts and price dynamically
              $('#cart-items-count').text(response.total_items);
              $('#cart-total-price').text(response.total_price);
          },
          error: function () {
              alert('Error adding to cart');
          },
      });
  });

  // Handle "Decrement" quantity
  $(document).on('click', '.decrement-btn', function () {
      const pizzaId = $(this).data('id');

      $.ajax({
          type: 'POST',
          url: `/remove_from_cart/${pizzaId}/`,
          data: {
              csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
          },
          success: function (response) {
              // Replace cart items section with updated HTML
              $('#cart-content').html(response.cart_items_html);

              // Update the cart counts and price dynamically
              $('#cart-items-count').text(response.total_items);
              $('#cart-total-price').text(response.total_price);
          },
          error: function () {
              alert('Error decrementing');
          },
      });
  });

  // Handle "Increment" quantity
  $(document).on('click', '.increment-btn', function () {
      const pizzaId = $(this).data('id');

      $.ajax({
          type: 'POST',
          url: `/add_to_cart/${pizzaId}/`,
          data: {
              csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
          },
          success: function (response) {
              // Replace cart items section with updated HTML
              $('#cart-content').html(response.cart_items_html);

              // Update the cart counts and price dynamically
              $('#cart-items-count').text(response.total_items);
              $('#cart-total-price').text(response.total_price);
          },
          error: function () {
              alert('Error incrementing');
          },
      });
  });

  // Handle "Delete Item" from cart
  $(document).on('click', '.delete-cart-item', function () {
      const pizzaId = $(this).data('id');

      $.ajax({
          type: 'POST',
          url: `/delete_from_cart/${pizzaId}/`,
          data: {
              csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
          },
          success: function (response) {
              // Replace cart items section with updated HTML
              $('#cart-content').html(response.cart_items_html);

              // Update the cart counts and price dynamically
              $('#cart-items-count').text(response.total_items);
              $('#cart-total-price').text(response.total_price);

              // Check if cart is empty
              if (response.total_items === 0) {
                  $('#cart-content').html('<div class="emt-cart"><img src="' + emptyCartImage + '" alt="emptycart"><h3>Oops, Your cart is empty!</h3><p>Looks like you haven\'t added anything to your cart yet.</p></div>');
              }
          },
          error: function () {
              alert('Error deleting item');
          },
      });
  });
});





