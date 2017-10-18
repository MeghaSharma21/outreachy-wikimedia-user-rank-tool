$(document).ready(function(){
  
  if ($('.bar').length > 0) {

    $('.bar').each(function() {
      $(this).css('width', 0);      
    })

    $('.count').each(function() {
      $(this).text(0 + '%');
    })

    setTimeout(function start (){
      
      $('.bar').each(function(i){  
          var $bar = $(this);
          $bar.css('transition', 'width 2s, background .2s');
          setTimeout(function(){
            $bar.css('width', $bar.attr('data-percent'));      
          }, i*100);
      });

      $('.count').each(function () {
          $(this).prop('Counter',0).animate({
              Counter: $(this).parent('.bar').attr('data-percent')
          }, {
              duration: 2000,
              easing: 'swing',
              step: function (now) {
                  $(this).text(now.toFixed(2) +'%');
              }
          });
      });

    }, 500)
    
  }
})