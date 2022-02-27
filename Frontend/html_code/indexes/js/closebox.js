$(document).ready(function() {
    $('.exam').on('mouseout', function() {
 
      $("#dialog").dialog("open");
      // loop time
      $('.time').text('10');
      (function myLoop(i) {
 
        setTimeout(function() {
 
          // To check whether OK button on dialog was clicked
          $('.ui-dialog-buttonset').click(function() {
 
            $(this).data('clicked', true);
          });
 
          // To check whether 'X' button on dialog was clicked
          $('.ui-dialog-titlebar-close').click(function() {
 
            $(this).data('clicked', true);
          });
 
          // storing button click status
          var clckd = $('.ui-dialog-buttonset').data('clicked');
          var xclckd = $('.ui-dialog-titlebar-close').data('clicked');
          console.log(clckd);
 
          // exiting the loop if 'OK' or 'X' button is clicked
          if (clckd || xclckd) {
            $('.ui-dialog-buttonset').data('clicked', false); // resetting 'OK' button status
            $('.ui-dialog-titlebar-close').data('clicked', false); // resetting 'X' button status
            return;
 
          }
          if (--i) myLoop(i);
          $('.time').text(i); //  decrement i and call myLoop again if i > 0
 
          // If user has not come back
          if (i == 0) {
            alert('Sorry exam closed'); //code for ending exam
          }
 
        }, 1000)
 
      })(10);
 
      // End loop time
 
 
 
    });
 
 
 
    $('.exam').on('mouseenter', function() {
 
      $("#dialog").dialog("close");
      $('.time').text('10');
    });
 
    $(function() {
      $("#dialog").dialog({
        autoOpen: false,
        show: {
          effect: "blind",
          duration: 1000
        },
        hide: {
          effect: "explode",
          duration: 1000
        },
        modal: true,
        buttons: {
          Ok: function() {
            $(this).dialog("close");
          }
        }
      }); // dialog.dialog
    }); // function dialog
  }); // Document ready