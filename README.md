<a id="top"></a>

<!-- Banner -->
<p align="center">
  <a href="https://www.uit.edu.vn/" title="Trường Đại học Công nghệ Thông tin" style="border: none;">
    <img src="https://i.imgur.com/WmMnSRt.png" alt="Trường Đại học Công nghệ Thông tin | University of Information Technology">
  </a>
</p>

<h1 align="center"><b>TRUY VẤN THÔNG TIN ĐA PHƯƠNG TIỆN<br>(MULTIMEDIA INFORMATION RETRIEVAL)</b></h>


## [BẢNG MỤC LỤC](#top)
* [Giới thiệu môn học](#giới-thiệu-môn-học)
* [Thông tin các thành viên](#thông-tin-về-các-thành-viên-nhóm)
* [Thông tin đồ án](#thông-tin-đồ-án)
* [Các bước cần thiết](#các-bước-cần-thiết)
* [Chuẩn bị dataset](#chuẩn-bị-dataset)
* [Indexing và Evaluating](#indexing-và-evaluating)
* [Chạy hệ thống trên web](#chạy-hệ-thống-trên-web)

## [GIỚI THIỆU MÔN HỌC](#top)
* **Tên môn học:** Truy vấn thông tin đa phương tiện - Multimedia Information Retrieval
* **Mã môn học:** CS336
* **Mã lớp:** CS336.O11.KHCL
* **Năm học:** HK1 (2023 - 2024)
* **Giảng viên:** TS. Ngô Đức Thành

## [THÔNG TIN VỀ CÁC THÀNH VIÊN NHÓM](#top)

| STT    | MSSV          | Họ và Tên                |Vai trò    | Github                                          | Email                   |
| :----: |:-------------:| :-----------------------:|:---------:|:-----------------------------------------------:|:-------------------------:
| 1      | 20520645      | Võ Nguyễn Hoài Nam          |Trưởng nhóm|[vonam007](https://github.com/vonam007)              |20520645@gm.uit.edu.vn   |
| 2      | 20520767      | Trương Thị Thanh Thanh      |Thành viên |[TTTThanh2812](https://github.com/TTTThanh2812)          |20520767@gm.uit.edu.vn   |
| 3      | 21521695      | Lê Thị Kim Yến   |Thành viên |[yenle73](https://github.com/yenle73)          |21521695@gm.uit.edu.vn   |
| 4      | 21520587      | Phạm Trâm Anh               |Thành viên |[tramanhpham](https://github.com/tramanhpham)          |21520587@gm.uit.edu.vn   |
| 5      | 20521641      | Nguyễn Thị Ngọc Nga               |Thành viên |[unknown](https://github.com/unknown)          |20521641@gm.uit.edu.vn   |

## [THÔNG TIN ĐỒ ÁN](#top)
* **Tên đồ án:** Hệ thống truy vấn thông tin bằng hình ảnh - Content-Based Information Retrieval System
* **Ngôn ngữ lập trình:** Python, HTML, CSS, JavaScript
* **Input:** Một bức ảnh
* **Output:** Một tập những bức ảnh được xem là liên quan đến bức ảnh đầu vào

## [CÁC BƯỚC CẦN THIẾT](#top)
Sử dụng Git Bash để có thể khởi chạy project.

### 1. Clone project
Clone project repository bằng câu lệnh dưới đây.

```bash
git clone https://github.com/vonam007/CS336.O11.KHCL.git
```

### Setting up the environment

#### Di chuyển vào thư mục 
```bash
cd DEMO_APP
```
#### Create a virtual environment

```bash
python -m venv venv
```

#### Activate the virtual environment

```bash
# Windows
venv\Scripts\activate

# Linux
source venv/bin/activate
```

#### Install dependencies

```bash
pip install -r requirements.txt
```


## [CHUẨN BỊ DATASET](#top)
* Ở đây, chúng ta có thể sử dụng 2 bộ dataset là Oxford Buildings và Paris Buildings để thực hiện truy vấn.
* Đường dẫn tải dataset và groundtruth sẽ được gắn ở phần chi tiết bên dưới.

### 1. Oxford Buildings
* Ta tải các ảnh trong dataset Oxford Buildings tại [đây](https://thor.robots.ox.ac.uk/datasets/oxford-buildings/oxbuild_images-v1.tgz).
* Sau đó, giải nén và đặt nó vào trong thư mục ```static/datasets/oxbuild/images```
* Cấu trúc như sau:
  ```
  DEMO_APP
      └───static
            └───datasets
                    └───oxbuild
                          └───images
                                │all_souls_000000.jpg
                                │all_souls_000001.jpg
                                │all_souls_000002.jpg
                                |all_souls_000003.jpg
                                |...
  ```

* Ta cũng cần phải tải các file groundtruth tại [đây](https://www.robots.ox.ac.uk/~vgg/data/oxbuildings/gt_files_170407.tgz).
* Giải nén và đặt nó trong thư mục ```static/datasets/oxbuild/groundtruth```
* Cấu trúc như sau:
  ```
  DEMO_APP
      └───static
            └───datasets
                    └───oxbuild
                          └───groundtruth
                                    │all_souls_1_good.txt
                                    │all_souls_1_junk.txt
                                    │all_souls_1_ok.txt
                                    │all_souls_1_query.txt
                                    |...
  ```

### 2. Paris Buildings
* Đối với bộ dataset này, nó được chia ra làm 2 phần. Ta có thể tải tại đây:
   * [paris_part1](https://thor.robots.ox.ac.uk/datasets/paris-buildings/paris_1-v1.tgz)
   * [paris_part2](https://thor.robots.ox.ac.uk/datasets/paris-buildings/paris_2-v1.tgz)
* Sau đó, giải nén cả 2 và đặt chúng cùng vào trong thư mục ```static/datasets/paris/images```
* Cấu trúc như sau:
  ```
  DEMO_APP
      └───static
            └───datasets
                    └───paris
                          └───images
                                │paris_defense_000000.jpg
                                │paris_defense_000002.jpg
                                │paris_defense_000004.jpg
                                |paris_defense_000005.jpg
                                |...
  ```

* Ta cũng cần phải tải các file groundtruth tại [đây](https://www.robots.ox.ac.uk/~vgg/data/parisbuildings/paris_120310.tgz).
* Giải nén và đặt nó trong thư mục ```static/datasets/paris/groundtruth```
* Cấu trúc như sau:
  ```
  DEMO_APP
      └───static
            └───datasets
                    └───paris
                          └───groundtruth
                                  │defense_1_good.txt
                                  │defense_1_junk.txt
                                  │defense_1_ok.txt
                                  │defense_1_query.txt
                                  |...
  ```

## [INDEXING VÀ EVALUATING](#top)
* Trong project này, chúng tôi đã cài đặt 6 feature extractors để thử nghiệm. Chúng lần lượt là:
  * VGG16
  * Xception
  * ResNet50
  * MobileNetV2
  * EfficientNetV2
  * InceptionResNetV2
* Chúng tôi đã **indexing** sẵn 2 feature extractors là **ResNet50** và **MobileNetV2** cho 2 bộ dataset đã nêu ở trên.
* Chúng ta có thể **indexing** và **evaluating** cho 2 bộ dataset đã nêu trên cho 6 phương pháp này.
* Các dòng lệnh ví dụ dưới đây sẽ được sử dụng dựa trên phương pháp **ResNet50**.

### 1. Indexing
* Lập chỉ mục cho bộ dataset Oxford Buildings với câu lệnh dưới đây.
  ```bash
  python retrieval_system/retrieve_and_evaluate.py --d 'oxbuild' --m 'ResNet50' --mode 'Indexing'
  ```

* Lập chỉ mục cho bộ dataset Paris Buildings với câu lệnh dưới đây.
  ```bash
  python retrieval_system/retrieve_and_evaluate.py --d 'paris' --m 'ResNet50' --mode 'Indexing'
  ```

### 2. Evaluating
#### 2.1. Oxford Buildings Evaluation
* Đánh giá cho bộ dataset Oxford Buildings với câu lệnh dưới đây.
  ```bash
  python retrieval_system/retrieve_and_evaluate.py --d 'oxbuild' --m 'ResNet50' --mode 'Evaluate'
  ```
* Kết quả đánh giá sẽ được lưu tại đường dẫn ```static/datasets/oxbuild/results``` với định dạng file là ```oxbuild_ResNet50_evaluation.txt```.
* Tương tự với 5 phương pháp còn lại, ta được các file trong cấu trúc như sau:
  ```
  DEMO_APP
      └───static
            └───datasets
                    └───oxbuild
                          └───results
                                  │oxbuild_EfficientNetV2L_evaluation.txt
                                  │oxbuild_InceptionResNetV2_evaluation.txt
                                  │oxbuild_InceptionV3_evaluation.txt
                                  │oxbuild_ResNet152V2_evaluation.txt
                                  │oxbuild_VGG16_evaluation.txt
                                  │oxbuild_Xception_evaluation.txt
  ```

#### 2.2. Paris Buildings Evaluation
* Đánh giá cho bộ dataset Paris Buildings với câu lệnh dưới đây.
  ```bash
  python retrieval_system/retrieve_and_evaluate.py --d 'paris' --m 'ResNet50' --mode 'Evaluate'
  ```
* Kết quả đánh giá sẽ được lưu tại đường dẫn ```static/datasets/paris/results``` với định dạng file là ```paris_ResNet50_evaluation.txt```.
* Tương tự với 5 phương pháp còn lại, ta được các file trong cấu trúc như sau:
  ```
  DEMO_APP
      └───static
            └───datasets
                    └───paris
                          └───results
                                │paris_EfficientNetV2L_evaluation.txt
                                │paris_InceptionResNetV2_evaluation.txt
                                │paris_InceptionV3_evaluation.txt
                                │paris_ResNet152V2_evaluation.txt
                                │paris_VGG16_evaluation.txt
                                │paris_Xception_evaluation.txt
  ```


## [CHẠY HỆ THỐNG TRÊN WEB](#top)
* Web được xây dựng bằng **Flask**
* Chạy dòng lệnh dưới đây để bắt đầu khởi chạy hệ thống.
```bash
flask run
```
