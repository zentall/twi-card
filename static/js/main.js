function toggle(btn) {
    btn.disabled = !btn.disabled
}

function get_meta_info(target_id) {
    var url = document.getElementById(target_id).value
    var btn = document.getElementById("auto_get_button")
    toggle(btn)

    // パラメータの作成
    var param = new FormData();
    param.append("url", url);

    var data = {
        body: param,
        method: "POST"
    }

    // リクエスト送信
    fetch("/meta", data).then(resp => {
        console.log(resp)
        if (!resp.ok) throw Error(response.statusText);
        else return resp.json()
    })
    // リクエストが成功した場合
    // 結果をフォームに入力
    .then(data => {
        var url_input = document.getElementById("target_url")
        var title_input = document.getElementById("title")
        var desc_input = document.getElementById("description")
        url_input.value = url
        title_input.value = data["title"]
        desc_input.value = data["description"]
        
        toggle(btn)
    })
    .catch(err => {
        toggle(btn)
    })
}



function set_preview(files) {

    var reader = new FileReader();
    reader.onload = function (e) {
        var preview = document.getElementById("preview")
        preview.src = e.target.result;
    }
    reader.readAsDataURL(files[0]);
}