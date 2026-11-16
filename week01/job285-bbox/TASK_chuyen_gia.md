code thuật toán lọc các vaasnd dề trước khi annotation, lọc ra sample có khả năng bị lỗi nhất sau đó mình lọc ra bằng tay, thì từ đó mới tối thiểu hóa các dữ liệu bị lỗi nhất dưới 1% để bắt đầu annotation
camera có những vấn đề như mờ rung, chiếu chói sáng, đi trong hầm, hay do thiết bị có vấn đề thi rất đa dạng thì vd như tự động cân chỉnh lại bên kĩ thuật quên căn chỉnh tự động độ sáng, nếu nó k làm tốt thì thà cho chúng ta cố định ảnh 1 cái cường độ ánh sáng cố định thì nó sẽ làm đồng bộ hơn về ddataa về context ánh sáng => dẫn đến dữ liệu đa dạng và k có track được, nhưng nếu phát hiện vấn đề đấy raise lên team AI thì
trao đổi team AI để biết dữ liệu nào đủ tốt để dùng dữ liệu nào nên xóa đi, dữ liệu bị lỗi như mất frame sai timeframe thì 2 bên đồng thuận thì nên ưu tiên xóa nó sớm
vkhi mà camera gắn trên robot thì nó có khả năng chưa biết xử lý ntn
nma nó chắc chắn có trong dữ liệu thực tế để chạy thật

bài tập là data ban đầu lọc ra cái video k bị trùng lặp

thêm vào vài thông tin kĩ thuật để làm thế nào k bị rò rỉ thông tin
thiết kế tránh reverser enginneer để k lộ lọt dữ liệu
chỉ những người có quyền truy cập thi fmowis có quyền convert đểphục vụ công việc là train dữ liệu  AI chứ k bị lộ ra ngoài
