$(function(){
    $('#org_properties_table').DataTable({
        paging:true,
        select: true,
        info: false,
        //language: {
        //    "decimal": ",",
        //    "thousands": "."
        //},
        order: [[ 8, "desc" ]],
        stateSave: false,
    });
});
