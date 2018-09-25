$(document).ready(function() {
  // console.log(($('.page-container').width())/3-18);
  var $grid = $('.grid').masonry({
    itemSelector: '.grid-item',
    columnWidth: ($('.page-container').width())/3,
  });

  $(window).on("load", function() {
    console.log("entire window is loaded!");
    $('.page-container').masonry('reloadItem');
  });


  $(window).scroll(function() {
    if ($(window).scrollTop() + $(window).height() == $(document).height()) {
      var current_page = $('.page-container').attr('id');
      var response;
      $.ajax({ type: "GET",
         url: ["/page/", parseInt(current_page)+1, "/"].join(''),
         async: false,
         success : function(text) {
           response= text;
           // console.log("ajax success!");
         }
       });
       if (response.length>60) {
         var $response = $(response);
         $('.page-container').append($grid.append($response).masonry( 'appended', $response ));
         $('.page-container').attr('id', parseInt(current_page)+1);
       } else {
         $('.loading-text').html("No more pages left!");
       }
    }
  });

  $('*').click(function(e) {
    target = e.target;
    if (!$(target).parents().is(".content-card") &&
      !$(target).is(".content-card") &&
      $("#content-overlay").html()) {
      $('#content-overlay').html('');
    }
  });

  $(".card-body-ajax").click(function() {
    post_url = ["/", $(this).attr('id'), "/"];
    $("#content-overlay").load(post_url.join(''));
  });

  $(".new-post-ajax").click(function() {
    $("#content-overlay").load("/edit/");
  });

  $(".about-ajax").click(function() {
    $("#content-overlay").load("/about/");
  });

  $(".clickup-button-ajax").click(function(e) {
    e.preventDefault();
    post_id = $(this).attr('id');
    click_url = ["/", post_id, "/clickup/"].join('');
    selector = ['#', post_id, '.clickup-button-ajax'].join('');
    $.ajax({
      url: click_url,
      success: function(data) {
        string = ['Upvote ', data['clicks']].join('');
        $(selector).html(string);
        if (data['clicked']) {
          $(selector).css('color', 'red');
        } else {
          $(selector).css('color', '#007bff');
        }
      },
      error: function(xhr, ajaxOptions, thrownError) {
        alert(xhr.status);
        alert(thrownError);
      },
    })
  });

  $(".comment-ajax").click(function() {
    post_url = ["/", $(this).attr('id'), "/"];
    $("#content-overlay").load(post_url.join(''), function() {
      $("#contentTextArea").focus();
    });
  });

});
