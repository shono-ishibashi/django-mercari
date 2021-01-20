$(function () {
    console.log('loaded!!!!')
    $('#depth_2_category').change(function () {
        fetchDepth3Category();
    });

    $('#depth_1_category').change(function () {
        fetchDepth2Category();
    });
});

function fetchDepth3Category() {
    var depth_2_category = $('#depth_2_category').val()
    if (depth_2_category) {
        $.ajax({
            url: `http://127.0.0.1:8000/api/get_parent_categroy/${depth_2_category}?format=json`,
            type: 'GET',
        }).done(function (data, textStatus, jqXHR) {
            depth_3_category = $('#depth_3_category')
            depth_3_category.empty()
            depth_3_category.append(
                '<option value="">==========</option>'
            )
            for (var category of data) {
                depth_3_category.append(
                    `<option value="${category.category_id}">${category.name}</option>`
                )
            }
        });
    } else {
        depth_3_category = $('#depth_3_category')
        depth_3_category.empty()
        depth_3_category.append(
            '<option value="">==========</option>'
        )
    }
}

function fetchDepth2Category() {
    var depth_1_category = $('#depth_1_category').val()
    $.ajax({
        url: `http://127.0.0.1:8000/api/get_parent_categroy/${depth_1_category}?format=json`,
        type: 'GET',
    }).done(function (data, textStatus, jqXHR) {
        depth_2_category = $('#depth_2_category')
        depth_2_category.empty()
        depth_2_category.append(
            '<option value="">==========</option>'
        )
        for (var category of data) {
            depth_2_category.append(
                `<option value="${category.category_id}">${category.name}</option>`
            )
        }
        var depth_3_category = $('#depth_3_category')
        depth_3_category.empty()
        depth_3_category.append(
            '<option value="">==========</option>'
        )
        fetchDepth3Category()
    });
}