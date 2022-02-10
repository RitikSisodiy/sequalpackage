 function ajaxCallPromise(api_url, method, request_data, loader = true) {
        var promiseObj = new Promise(function (resolve, reject) {
            $.ajax({
                url: api_url,
                type: method,
                data: request_data,
                beforeSend: function () {
                    if (loader) {
                        $("#ajax-loader").show();
                    }
                },
                success: resolve,
                error: reject
            });
        });
        return promiseObj;
    }
    function makerequest(url, query, appendopt, responce = false) {
    return new Promise((resolve, reject) => {
            var xhttp = new XMLHttpRequest()
            xhttp.open('GET', `${url}${query}`, true)
            xhttp.send()
            xhttp.onreadystatechange = function () {
                if (xhttp.readyState == 4 && xhttp.status == 200) {
                    data = JSON.parse(xhttp.response)
                    if (responce) {
                        resolve(data)
                    } else {
                        appendopt.html('<option value="">Select</option>')
                        for (i = 0; i < data.length; i++) {
                            appendopt.append(`<option value="${data[i].id}">${data[i].name}</option>`)
                        }
                        resolve("error1")
                    }
                }
            }
        });
    }