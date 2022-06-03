//アップロード画像のプレビュー表示
$(function(){
    $("[name='upload_image']").on('change', function (e) {
      
      var reader = new FileReader();
      
      reader.onload = function (e) {
          $("#preview").attr('src', e.target.result);
      }
  
      reader.readAsDataURL(e.target.files[0]);   
  
    });
  });
//アップロードの非同期処理
$(function(){
  $("#uploadform").submit(evt => {
    evt.preventDefault();
    
    
    // formdataの取得
    const formData = new FormData($("#uploadform")[0]);

    // 判定中アイコンを表示する
    document.getElementById("result_img").src = "../static/img/loading.gif";
    document.getElementById("title").innerText = "判定中...";
    
     // Ajaxで送信
     $.ajax({
      url: "/result",
      method: "POST",
      data: formData,
      processData: false,
      contentType: false
    })
      .done(res => {
        // 送信成功！
          console.log(res)
          document.getElementById("result_img").src = "../static/img/"+res+".png";
          document.getElementById("title").innerHTML = "これは<br>"+res+"<br>であると判断されました";
          $("#result_img").css("width", "200px");
        })
      .fail(() => {
        document.getElementById("result_unit").src = "../static/img/error.png";
        $("#result_img").css("width", "200px");
        document.getElementById("title").innerHTML =
          "通信に失敗しました。<br>しばらく経ってから再度ご利用ください!";
      });


    return false;
  });
});