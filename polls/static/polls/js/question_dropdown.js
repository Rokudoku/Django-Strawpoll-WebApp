$(function() {
    'use strict';
    var icon_closed = 'fa-caret-square-down';
    var icon_open = 'fa-caret-square-up';

    var $dropdown_icon = $('.question-dropdown-icon');

    $dropdown_icon.click(function() {
        // find the dropdown associated with this icon
        var dropdown = $('#' + $(this).attr('dropdown-id'));
        // toggle the icon
        $(this).find('[data-fa-processed]')
            .toggleClass(icon_open)
            .toggleClass(icon_closed);
        // slide up/down the dropdown
        dropdown.slideToggle();
    });
});