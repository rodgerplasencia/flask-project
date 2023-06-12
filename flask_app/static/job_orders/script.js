// $(document).ready(function() {
//     $('#project_name').change(function() {
//         this.form.submit();
//     });

//     var project_budget_ids = $('.project_budget_id').map((i, e) => e.value).get();
//     var unit_of_measures = $('.unit_of_measure').map((i, e) => e.value).get();
//     var unit_costs = $('.unit_cost').map((i, e) => e.value).get();
//     var avl_supply = $('.quantity').map((i, e) => e.value).get();

//     $('#item_cost').change(function() {
//         $('#unit_of_measure').val(unit_of_measures[project_budget_ids.indexOf($(this).val())]);

//         var unit_cost = unit_costs[project_budget_ids.indexOf($(this).val())];
//         $('#unit_cost').val(Number(unit_cost).toLocaleString(undefined, {maximumFractionDigits: 2}));
//     });

//     $('#quantity').change(function() {
//         $('#total_cost').val($('#quantity').val() * $('#unit_cost').val());
//     });
// });




$(document).ready(function() {
    $('#project_name').change(function() {
        this.form.submit();
    });

    var project_budget_ids = $('.project_budget_id').map((i, e) => e.value).get();
    var unit_of_measures = $('.unit_of_measure').map((i, e) => e.value).get();
    var unit_costs = $('.unit_cost').map((i, e) => e.value).get();
    var avl_supply = $('.quantity').map((i, e) => e.value).get();

    $('#item_cost').change(function() {
        $('#unit_of_measure').val(unit_of_measures[project_budget_ids.indexOf($(this).val())]);

        var unit_cost = unit_costs[project_budget_ids.indexOf($(this).val())];
        $('#unit_cost').val(Number(unit_cost).toLocaleString(undefined, {maximumFractionDigits: 2}));

        // Update the available supply (avl_supply) based on the selected item_cost
        $('#avl_supply').val(avl_supply[project_budget_ids.indexOf($(this).val())]);
    });

    $('#quantity').change(function() {
        var quantity = parseFloat($('#quantity').val());
        var unit_cost = parseFloat($('#unit_cost').val());
        var total_cost = quantity * unit_cost;

        $('#total_cost').val(total_cost.toLocaleString(undefined, {maximumFractionDigits: 2}));
    });
});