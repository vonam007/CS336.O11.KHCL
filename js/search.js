// Chèn jQuery từ CDN
var script = document.createElement('script');
script.src = 'https://code.jquery.com/jquery-3.6.4.min.js';
script.type = 'text/javascript';
document.getElementsByTagName('head')[0].appendChild(script);

sampledata = {
    "rank": [1, 2, 3],
    "score": [0.5, 0.4, 0.3],
    "docs": ['Yes. Just like us, cats vary in size and shape and weight. And like us, some of that is diet',
        'Thank you for your question. You have a few different issues within your one question, but lets start wi',
        'ge their food preferences without anything bei']

}
// Chờ jQuery được tải xong trước khi thực thi mã
script.onload = function () {
    $(document).ready(function () {
        const searchInput = $("#searchBar");
        const suggestionsList = $("#suggestions");
        const searchButton = $("#searchBtn");
        // Đường dẫn đến file CSV
        const csvFilePath = "../src/data/qry_filtered.tsv";

        // Đọc dữ liệu từ file CSV
        $.ajax({
            type: "GET",
            url: csvFilePath,
            dataType: "text",
            success: function (data) {
                // Chuyển đổi dữ liệu CSV thành mảng
                const dataArray = CSVToArray(data);

                // Mảng chứa dữ liệu từ cột 'title'
                const titlesArray = dataArray.map(row => row[0]);

                // Xử lý sự kiện khi người dùng nhập vào ô tìm kiếm
                searchInput.on("input", function () {
                    const userInput = searchInput.val().toLowerCase();
                    const filteredTitles = titlesArray
                        .filter(title => title && title.toLowerCase().includes(userInput))
                        .slice(0, 5); // Lấy 10 kết quả đầu tiên

                    // Hiển thị gợi ý
                    displaySuggestions(filteredTitles);
                });
                // Kiểm tra nếu phím "Enter" được nhấn (keyCode 13)
                searchInput.on("keydown", function (event) {
                    if (event.keyCode == 13) {
                        searchButton.click();
                    }
                });

                // Xử lý sự kiện khi người dùng bấm nút search
                searchButton.on("click", function () {
                    console.log("searching...");
                    if (searchInput.val().length == 0) {
                        alert("Vui lòng nhập từ khóa tìm kiếm");
                        return;
                    }
                    const userInput = searchInput.val().toLowerCase();

                    sendDataToAPI({ "query": userInput });
                    //printResult(sampledata)

                });
            }
        });

        // Hiển thị gợi ý
        function displaySuggestions(suggestions) {
            suggestionsList.empty();

            if (suggestions.length > 0) {
                suggestions.forEach(suggestion => {
                    const li = $("<li>").text(suggestion);

                    // Xử lý sự kiện khi người dùng chọn gợi ý
                    li.on("click", function () {
                        searchInput.val(suggestion);
                        suggestionsList.hide();
                    });

                    suggestionsList.append(li);
                });

                suggestionsList.show();
            } else {
                suggestionsList.hide();
            }
        }

        // Ẩn gợi ý khi nhấp ra ngoài ô tìm kiếm
        $(document).on("click", function (event) {
            if (!$(event.target).is("#searchInput")) {
                suggestionsList.hide();
            }
        });

        // Hàm chuyển đổi dữ liệu CSV thành mảng
        function CSVToArray(csvString, delimiter = ",") {
            const rows = csvString.split("\n");
            return rows.map(row => row.split(delimiter));
        }

        // Gửi dữ liệu tìm kiếm đến API
        function sendDataToAPI(Data) {
            const BASE = "https://343a-34-87-153-0.ngrok-free.app"; // Replace with your Flask API URL

            const apiUrl = BASE + "/search"; // Replace with your Flask API endpoint



            function isJSON(str) {
                try {
                    JSON.parse(str);
                    return true;
                } catch (e) {
                    return false;
                }
            }

            // Sử dụng hàm isJSON để kiểm tra

            const xhr = new XMLHttpRequest();
            xhr.open("POST", apiUrl, true);
            xhr.setRequestHeader("Content-Type", "application/json");

            xhr.onreadystatechange = function () {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    const response = JSON.parse(xhr.responseText);

                    if (isJSON(response)) {
                        console.log("Response is a valid JSON.");
                        const jsonResponse = JSON.parse(response);
                        console.log(jsonResponse);
                        // Do something with jsonResponse here
                        printResult(jsonResponse);
                    } else {
                        console.log("Response is not a valid JSON.");
                        console.log(response);
                    }

                }
            };

            let jsonData = JSON.stringify(Data);
            xhr.send(jsonData);
        }


        function printResult(jsonResponse) {
            const result = $("#result");
            result.empty();

            const rank = jsonResponse["rank"];
            const score = jsonResponse["score"];
            const docs = jsonResponse["docs"];

            var table = $("<table id='resultTable'>");
            table.addClass("hidden")
            var titleTr = $("<tr>");
            titleTr.append($("<th>").append($("<p>").text("No.")));
            titleTr.append($("<th>").append($("<p>").text("Related Scores")));
            titleTr.append($("<th>").append($("<p>").text("Passages")));
            table.append(titleTr);

            for (let i = 0; i < jsonResponse.rank.length; i++) {
                var row = $("<tr>");
                row.append($("<td>").append(($("<p>").text(rank[i]))));
                row.append($("<td>").append(($("<p>").text(score[i]))));
                row.append($("<td>").append(($("<p>").text(docs[i]))));
                table.append(row);
            }

            result.append(table);
            console.log(jsonResponse);


            setTimeout(function () {
                showElement("resultTable");
            }, 250);

            function showElement(elementId) {
                var element = document.getElementById(elementId);
                if (element) {
                    // Hiển thị phần tử
                    table.removeClass("hidden");
                    table.addClass("visible");
                }
            }
        }
    });
}