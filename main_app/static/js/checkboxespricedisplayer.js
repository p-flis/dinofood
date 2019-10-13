$(document).ready(function(){
  var checkboxes_cost = 0;  //cost in gr, not in zl
  var app_costs = $("#approximate_costs_id")[0].value;
  app_costs = JSON.parse(app_costs);
  $("#id_ingredients li label input:not(:checked)").each(function( index ) {
  checkboxes_cost+=app_costs[$(this).val()];
});
$("#approximate_cost_id").html("<p id=approximate_cost_id>Jeszcze około "+ checkboxes_cost/100 +" zł</p>")
$("#id_ingredients li label input").change(function () {
  if($(this).is(':checked')){
    checkboxes_cost-=app_costs[$(this).val()];
  }
  else {
    checkboxes_cost+=app_costs[$(this).val()];
  }
  $("#approximate_cost_id").html("<p id=approximate_cost_id>Jeszcze około "+ checkboxes_cost/100 +" zł</p>")
  });
})
