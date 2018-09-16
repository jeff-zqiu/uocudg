$(document).ready(function() {
  $('*').click(function(e) {
    target = e.target;
    if (!$(target).parents().is(".content-card") &&
      !$(target).is(".content-card") &&
      $("#content-overlay").html()) {
      $('#content-overlay').html('');
    }
  });

  $(".card-body").click(function() {
    post_url = ["/forum/", $(this).attr('id'), "/"];
    $("#content-overlay").load(post_url.join(''))
  });

  $("#new-post").click(function() {
    $("#content-overlay").load("/forum/edit/")
  });

});
