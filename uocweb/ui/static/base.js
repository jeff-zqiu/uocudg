$(document).ready(function() {
  console.log('base.js loaded');
  // console.log(($('.page-container').width())/3-18);
  var $grid = $('.grid').masonry({
    itemSelector: '.grid-item',
    columnWidth: ($('.page-container').width())/3,
  });


  // eventBinder: used to prevent duplicated event binding
  // after ajax load more pages
  function eventBinder(jqElem, eventStr, handler) {
    jqElem.off(eventStr);
    jqElem.on(eventStr, handler);
  }

  $(window).scroll(function() {
    if ($(window).scrollTop() + $(window).height() == $(document).height()) {
      var current_page = $('.page-container').attr('id');
      var response;
      $.ajax({ type: "GET",
         url: ["/",$('title').attr('id'),"/", parseInt(current_page)+1, "/"].join(''),
         async: false,
         success : function(text) {
           response= text;
           // console.log("ajax success!");
         }
       });
       if (response.length>300) {
         // console.log('response length: ' + response.length + ', is valid');
         var $response = $(response);
         $('.page-container').append($grid.append($response).masonry( 'appended', $response ));
         $('.page-container').attr('id', parseInt(current_page)+1);
       } else {
         // console.log('response length: ' + response.length + ', is invalid')
         $('.loading-text').html("No more pages left!");
       }
    }
  });

  eventBinder($('*'),'click.close-content-overlay',function(e) {
    target = e.target;
    if (!$(target).parents().is(".content-card") &&
      !$(target).is(".content-card") &&
      $("#content-overlay").html()) {
      $('#content-overlay').html('');
    }
  });

  eventBinder($(".card-body-ajax"),'click.show-content-overlay', function() {
      post_url = ["/", $(this).attr('id'), "/"];
      $("#content-overlay").load(post_url.join(''));
  });

  eventBinder($(".new-post-ajax"),'click.new-post',function() {
    $("#content-overlay").load("/edit/");
  });


  eventBinder($(".about-ajax"), 'click.about', function() {
    $("#content-overlay").load("/about/");
  });

  eventBinder($('.clickup-button-ajax'), 'click.clckup', function(e){
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
  })

  eventBinder($(".comment-ajax"),'click.comment',function() {
    post_url = ["/", $(this).attr('id'), "/"];
    $("#content-overlay").load(post_url.join(''), function() {
      $("#contentTextArea").focus();
    });
  });

});
