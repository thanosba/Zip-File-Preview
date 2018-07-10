$(function () {
    $('.tree li').hide();
    $('.tree li:first').show();
    $('.tree li:has(ul)').addClass('parent_li').find(' > span').attr('title', 'Expand folder');

    $('.tree li.parent_li > span').on('click', function (e) {
        var children = $(this).parent('li.parent_li').find(' > ul > li');
        if (children.is(":visible")) {
            children.hide('fast');
            $(this).attr('title', 'Expand folder').find('span > i').addClass('glyphicon-folder-close').removeClass('glyphicon-folder-open');
        } else {
            children.show('fast');
            $(this).attr('title', 'Close folder').find(' span > i').addClass('glyphicon-folder-open').removeClass('glyphicon-folder-close');
        }
        e.stopPropagation();
    });
});