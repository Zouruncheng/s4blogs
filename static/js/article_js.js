/**
 * Created by zou on 2017/7/16.
 */





// ---------------赞---------------
$("#like").click(function(){
   var path = window.location.pathname;
   var token = $.cookie('csrftoken');

   $.ajax({
       url:"/updown/",
       type:"post",
       data:{"up":"1","article_id":path},
       headers:{"X-CSRFToken":token},
       success:function(data){
           if(data=="ok"){
               location.reload();
           }else{
               var error = $("<span></span>");
               error.text(data);
               $("#likeit").append(error)
           }
       }

   })
});

// ---------------踩---------------
$("#dislike").click(function(){
   var path = window.location.pathname;
   var token = $.cookie('csrftoken');

   $.ajax({
       url:"/updown/",
       type:"post",
       data:{"up":"0","article_id":path},
       headers:{"X-CSRFToken":token},
       success:function(data){
           if(data=="ok"){
               location.reload();
           }else{
               var error = $("<span></span>");
               error.text(data);
               $("#likeit").append(error)
           }
       }

   })
});

// ========================提交评论=================================================
$("#put").click(function() {
    var path = window.location.pathname;

    var token = $.cookie('csrftoken');
    var content = $("#content").val();
    console.log(content)

    $.ajax({
        url:"/put_comment/",
        type:"post",
        data:{"article_id":path,
              "content":content},
        headers:{"X-CSRFToken":token},
        success: function(data){
            if (data=="okay"){
                location.reload();
            }else{
                var ele = $("<span></span>");
                ele.text(data);
                $("#content").after(ele);

            }
        }
    });
});














