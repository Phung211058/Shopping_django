$(document).ready(function () {
    $('#register_form').submit(function (e) {
        e.preventDefault(); // Ngăn chặn form submit mặc định
        // Thu thập dữ liệu từ form
        var formData = new FormData(this);
        $.ajax({
            url: registerUrl, // Sử dụng biến đã truyền từ template
            type: 'POST',
            data: formData,
            processData: false, // Không xử lý dữ liệu vì sử dụng FormData
            contentType: false, // Không thiết lập loại nội dung
            headers: {
                'X-CSRFToken': '{{ csrf_token }}' // Thêm CSRF token
            },
            success: function (response) {
                Swal.fire({
                    position: "center",
                    icon: "success",
                    title: "Your account has been saved",
                    showConfirmButton: false,
                    timer: 3000,
                    onClose: () => {
                        window.location.href = '/manage/get/login';
                    }
                });
            },
            error: function (xhr) {
                alert(JSON.parse(xhr.responseText).error);
            }
        });
    });

    $('#login_form').submit(function (e) {
        e.preventDefault();
        var data = new FormData(this);
        $.ajax({
            url: loginUrl, // Sử dụng biến đã truyền từ template
            type: 'POST',
            data: data,
            processData: false, // Không xử lý dữ liệu vì sử dụng FormData
            contentType: false, // Không thiết lập loại nội dung
            headers: {
                'X-CSRFToken': '{{ csrf_token }}' // Thêm CSRF token
            },
            success: function (response) {
                Swal.fire({
                    position: "center",
                    icon: "success",
                    title: "Welcome with us!",
                    showConfirmButton: false,
                    timer: 3000,
                    onClose: () => {
                        window.location.href = '/manage';
                    }
                });
            },
            error: function (xhr) {
                Swal.fire({
                    position: "center",
                    icon: "error",
                    title: JSON.parse(xhr.responseText).error,
                    showConfirmButton: true,
                    timer: 3000,
                });
            }
        });
    })

    $('.log_out').click(function () {
        // Hiển thị thông báo xác nhận
        Swal.fire({
            title: "Are you sure?",
            text: "You want to log out?",
            icon: "question",
            showCancelButton: true,
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
            confirmButtonText: "Sign out"
        }).then((result) => {
            if (result.isConfirmed) {
                // Lấy CSRF token từ thẻ input ẩn
                const csrftoken = $('#csrf-token').val();
                $.ajax({
                    url: '/manage/logout/', // Đường dẫn tới view logout của bạn
                    type: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken // Thêm CSRF token vào header
                    },
                    success: function (response) {
                        if (response.success) {
                            window.location.href = '/manage/get/login'; // Điều hướng người dùng tới trang đăng nhập
                        }
                    },
                    error: function (xhr, status, error) {
                        // Hiển thị chi tiết lỗi
                        let errorMessage = 'Logout failed: ' + xhr.responseJSON.error; // Lấy thông tin lỗi cụ thể
                        console.log(errorMessage); // Hiển thị lỗi ra màn hình
                    }
                });
            }
        });
    });
})