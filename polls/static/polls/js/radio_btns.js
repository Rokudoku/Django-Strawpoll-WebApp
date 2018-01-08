// Custom radio buttons using font awesome icons.

'use strict';

$(function() {

    var checked = 'fa-check-circle';
    var unchecked = 'fa-circle';

    var $radio = $('input[type="radio"] + label');
    var $curr = null;

    $radio.each(function() {
        // if a label (the 'button' and the text) is clicked
        $(this).on('click', function() {
            // un-check the currently checked option (if there is one)
            if ($curr != null) {
                $curr.find('[data-fa-processed]')
                    .toggleClass(checked)
                    .toggleClass(unchecked);
            }
            // check the clicked option
            $(this).find('[data-fa-processed]')
                .toggleClass(checked)
                .toggleClass(unchecked);
            // update currently checked option
            $curr = $(this);
        });
    });
});