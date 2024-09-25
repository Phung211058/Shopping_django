$(document).ready(function () {
    loadProducts();
    // ____________________________GET PRODUCT_____________________________
    // Hàm loadProducts sẽ hỗ trợ tìm kiếm và hiển thị tất cả sản phẩm
    function loadProducts(searchKey = '') {
        var ProductUrl = getProductUrl;
        if (searchKey) {
            ProductUrl += '?q=' + encodeURIComponent(searchKey); // Gắn tham số tìm kiếm nếu có
        }
        $.ajax({
            url: ProductUrl,
            type: "GET",
            success: function (res) {
                $('#productsList').empty(); // Xóa hết các sản phẩm cũ
                if (res.products.length > 0) {
                    res.products.forEach(function (product, index) {
                        var productHtml = `
                        <tr>
                            <td>${index+1}</td> 
                            <td>${product.name}</td>
                            <td>
                                <img style="width: 120px;" src="${product.image_url}" alt="">
                            </td>
                            <td>${product.category}</td>
                            <td>${product.description}</td>
                            <td>${product.price}</td>
                            <td>${product.quantity}</td>
                            <td>
                                <button type="submit" class="btn btn-warning edit_product_btn" data-bs-toggle="modal" data-bs-target="#updateProductModal" data-id="${product.id}">Edit</button>
                                <button type="button" class="btn btn-danger delete_product_btn" data-id="${product.id}">Delete</button>
                            </td>
                        </tr>
                     `;
                        $('#productsList').append(productHtml); // Thêm sản phẩm vào danh sách
                    });
                } else {
                    // Nếu không tìm thấy sản phẩm
                    $('#productsList').append('<tr><td colspan="8" class="text-center">No products found</td></tr>');
                }
            },
            error: function (xhr) {
                alert("Error fetching products");
                console.error("Error fetching products:", xhr);
            }
        })
    }
    // ____________________________SEARCH PRODUCT_____________________________
    // Gọi hàm loadProducts khi người dùng nhập từ khóa tìm kiếm
    $('.search_bar').on('keyup', function () {
        var searchKey = $(this).val(); // Lấy giá trị từ input tìm kiếm
        loadProducts(searchKey); // Gọi hàm loadProducts với từ khóa tìm kiếm
    });

    // ____________________________CREATE PRODUCT_____________________________
    $('#createProduct').submit(function (e) {
        e.preventDefault();
        var formData = new FormData(this); // Lấy tất cả dữ liệu từ form, bao gồm cả file
        $.ajax({
            url: createProductUrl,
            type: 'POST',
            data: formData,
            processData: false, // Không xử lý dữ liệu vì đang gửi FormData
            contentType: false, // Không thiết lập loại nội dung, để cho FormData xử lý
            headers: {
                'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (response) {
                // Xử lý khi tạo sản phẩm thành công
                Swal.fire({
                    position: "top",
                    icon: "success",
                    title: "Product created successfully!",
                    showConfirmButton: false,
                    timer: 2000
                });
                // Reset form sau khi thành công
                $('#createProduct')[0].reset();
                // Đóng modal sau khi thành công
                // $('#createModal').modal('hide');
                // load lại tất cả sản phẩm sau khi tạo
                loadProducts();
            },
            error: function (xhr) {
                // Hiển thị thông báo lỗi nếu có lỗi xảy ra
                var errorMsg = JSON.parse(xhr.responseText).error;
                Swal.fire({
                    icon: "error",
                    title: "Error",
                    text: errorMsg
                });
            }
        });
    });

    // ____________________________DELETE PRODUCT_____________________________

    $(document).on('click', '.delete_product_btn', function (e) {
        e.preventDefault();
        var productId = $(this).data('id'); // lấy id của sản phẩm được chọn
        var deleteProductUrl = '/manage/delete_product/' + productId + '/';
        // SEND AN ALERT TO ASK USER CONFIRM 
        Swal.fire({
            title: "Are you sure?",
            text: "You won't be able to revert this!",
            icon: "question",
            showCancelButton: true,
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
            confirmButtonText: "Yes, delete it!"
        }).then((result) => {
            // DELETE PRODUCT IF USER AGREE
            if (result.isConfirmed) {
                $.ajax({
                    type: 'DELETE',
                    url: deleteProductUrl,
                    dataType: 'json',
                    headers: {
                        'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
                    },
                    success: function (response) {
                        loadProducts();
                        Swal.fire({
                            title: "Deleted!",
                            text: "Deleted successfully",
                            icon: "success"
                        });
                    },
                    error: function (xhr, status, error) {
                        console.log("Error: " + error);
                    }
                });
            }
        });
    })

    // UPDATE PRODUCT_____________________________
    // Get Product Information
    $(document).on('shown.bs.modal', '#updateProductModal', function (e) {
        e.preventDefault();
        // Lấy nút đã kích hoạt modal
        var button = $(e.relatedTarget);
        let product_id = button.data('id');
        var getProductUrl = '/manage/update_product/' + product_id + '/'
        // $('#update_product_form').attr('action', getProductUrl);
        $.ajax({
            type: "GET",
            url: getProductUrl,
            success: function (response) {
                console.log(response);
                $('#update_product_id').val(product_id);
                $('#update_product_name').val(response.products.name);
                $('#update_product_category').val(response.products.category);
                $('#update_product_description').val(response.products.description);
                $('#update_product_price').val(response.products.price);
                $('#update_product_quantity').val(response.products.quantity);
            },
            error: function (xhr, status, error) {
                console.log("Error: " + error);
            }
        });
    });
    // Update choosen product
    $("#update_product_form").submit(function (e) {
        e.preventDefault(); // Ngăn chặn hành vi submit mặc định của form

        var product_id = $('#update_product_id').val();
        var getProductUrl = '/manage/update_product/' + product_id + '/'
        var formData = new FormData(this); // Tạo đối tượng FormData từ form
        $.ajax({
            type: "POST",
            url: getProductUrl,
            data: formData, // Gửi dữ liệu form
            processData: false, // Không xử lý dữ liệu vì đang gửi FormData
            contentType: false, // Không thiết lập loại nội dung, để cho FormData xử lý
            headers: {
                'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (response) {
                // Sau khi cập nhật thành công
                Swal.fire({
                    title: "Updated!",
                    text: "Updated successfully",
                    icon: "success"
                });
                $('#updateProductModal').modal('hide'); // Ẩn modal
                $('#update_product_form')[0].reset();
                loadProducts(); // Tải lại danh sách sản phẩm
            },
            error: function (xhr) {
                // Hiển thị thông báo lỗi nếu có lỗi xảy ra
                var errorMsg = JSON.parse(xhr.responseText).error;
                Swal.fire({
                    icon: "error",
                    title: "Error",
                    text: errorMsg
                });
            }
        })
    });
})