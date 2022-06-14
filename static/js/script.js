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
        console.log(res);
        // 送信成功！
        // 有毒の場合
        if([0,4,5,7].includes(res[1])){
            document.getElementById("result_img").src = "../static/img/"+res[1]+".png";
            document.getElementById("title").innerHTML = "これは<br>"+res[0]+"<br>であると判断されました。<br>有毒である可能性があります。<br>取り扱いには注意しましょう。";
            $("#result_img").css("width", "500px");
            $("#result_img").css("height", "500px");
        }
        else {
            document.getElementById("result_img").src = "../static/img/"+res[1]+".png";
            document.getElementById("title").innerHTML = "<center>これは<br>"+res[0]+"<br>であると判断されました</center>";
            $("#result_img").css("width", "500px");
            $("#result_img").css("height", "500px");
        }
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

$('#page-link a[href*="#"]').click(function () {
  var elmHash = $(this).attr('href'); //ページ内リンクのHTMLタグhrefから、リンクされているエリアidの値を取得
  var pos = $(elmHash).offset().top;  //idの上部の距離を取得
  $('body,html').animate({scrollTop: pos}, 200); //取得した位置にスクロール。500の数値が大きくなるほどゆっくりスクロール
  return false;
});