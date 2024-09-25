$(document).ready(function() {
    $(".add_to_cart").click(function() {
        var productId = $(this).data('product-id');
        // Lấy CSRF token từ thẻ meta
        const csrftoken = $('meta[name="csrf-token"]').attr('content');
        $.ajax({
            url: cartUrl,  // Thay bằng URL của hàm add_to_cart
            type: 'POST',
            data: {
                'product_id': productId  // Gửi productId dưới dạng một đối tượng
            },
            headers: {
                'X-CSRFToken': csrftoken  // Truyền CSRF token từ thẻ meta
            },
            success: function(response) {
                alert(response.success);
            },
            error: function(xhr, status, error) {
                alert('Error: ' + error);
            }
        });
    });
})