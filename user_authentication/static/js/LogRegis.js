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
                // if(response.status == 400){
                //     showerr(response.errors);
                // }
                Swal.fire({
                    position: "top-end",
                    icon: "success",
                    title: "Your account has been saved",
                    showConfirmButton: false,
                    timer: 3000,
                    onClose: () => {
                        window.location.href = '/user/get/login';
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
                        window.location.href = '/home/';
                    }
                });
            },
            error: function (xhr) {
                alert(JSON.parse(xhr.responseText).error);
            }
        });
    })

    function showerr(errors) {
        $.each(errors, function (key, value) {
            $('.' + key + '_err').text(value);
        })
    };
});